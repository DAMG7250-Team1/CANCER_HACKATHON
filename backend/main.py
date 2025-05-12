
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import sys
import logging
import traceback
import uvicorn
from typing import Union

# Set environment to allow failed OCSP checks
os.environ["SF_OCSP_FAIL_OPEN"] = "true"


load_dotenv()

# FastAPI app
app = FastAPI(
    title="Cancer Research Backend",
    description="Multi-Agent Research Report Generator using MCP",
    version="1.0",
    debug=True
)

# Add backend folder to path if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp.mcp import CancerResearchMCP  # Must be after sys.path append

# Initialize MCP
mcp = CancerResearchMCP()

# Request and Response models
class ResearchRequest(BaseModel):
    query: str

class ResearchResponse(BaseModel):
    snowflake_data: dict
    rag_data: dict
    # web_data: dict
    web_data: Union[str, dict]

@app.post("/generate_report", response_model=ResearchResponse)
async def generate_report(request: ResearchRequest):
    """
    Generate a comprehensive cancer research report by coordinating multiple agents.
    """
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    try:
        logging.info(f"Received query: {request.query}")
        report = await mcp.run(request.query)
        return {"snowflake_data": report['snowflake_data'], "rag_data": report['rag_data'], "web_data": report['web_data']}
    except Exception as e:
        logging.error("Exception occurred during report generation")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

# Local dev entry point
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

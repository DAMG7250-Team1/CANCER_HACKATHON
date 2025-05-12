
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import sys
import logging
import traceback
import uvicorn

load_dotenv()

app = FastAPI(title="Cancer Research Backend", debug=True)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp.mcp import CancerResearchMCP

mcp = CancerResearchMCP()

class ResearchRequest(BaseModel):
    query: str

class ResearchResponse(BaseModel):
    report: str

@app.post("/generate_report", response_model=ResearchResponse)
async def generate_report(request: ResearchRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    try:
        logging.info(f"Received query: {request.query}")
        report = await mcp.run(request.query)
        return {"report": report["report"]}
    except Exception as e:
        logging.error("Exception occurred during report generation")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


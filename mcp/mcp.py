
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agents.snowflake_agent import SnowflakeAgent
from backend.agents.rag_agent import get_rag_response
from backend.agents.web_agent import WebAgent
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class CancerResearchMCP:
    def __init__(self):
        self.snowflake_agent = SnowflakeAgent()
        self.web_agent = WebAgent()
       

    async def run(self, query: str) -> Dict[str, Any]:
        """
        Orchestrates the multi-agent research based on the query.
        """
        try:
            # 1. Fetch structured data (Cancer statistics) from Snowflake
            snowflake_data = self.snowflake_agent.get_cancer_statistics()
            by_site_data = snowflake_data.get("by_site", [])
            logger.info(f"[MCP] ✅ Received {len(by_site_data)} rows from Snowflake for 'by_site'")
            if len(by_site_data) > 0:
                logger.info(f"[MCP] 🔍 First row sample: {by_site_data[0]}")
            else:
                logger.warning("[MCP] ⚠️ No data returned for 'by_site'")


            # 2. Fetch research papers or findings from RAG system (S3 backend)
            rag_summary = await get_rag_response(query)
            # logger.info(f"RAG summary: {rag_summary}")
            # 3. Fetch relevant web search results (clinical trials)
            web_results = self.web_agent.get_clinical_trials(query)
            web_results_str = "\n\n".join([
                f"**{item.get('title', 'No Title')}**  \n"
                f"- Description: {item.get('description', 'N/A')}  \n"
                f"- Phase: {item.get('phase', 'Unknown')}  \n"
                f"- Status: {item.get('status', 'Unknown')}  \n"
                f"- [View Study]({item.get('source_url', '#')})"
                for item in web_results
            ]) or "No clinical trial results found."

            return {
                "snowflake_data": snowflake_data,
                "rag_data": {"summary": rag_summary},
                "web_data": web_results_str
            }
            # web_results = self.web_agent.get_all_web_data(query)
            # # logger.info(f"Web summary: {web_results}")

            # return {
            #     "snowflake_data": snowflake_data,
            #     "rag_data": {"summary": rag_summary},
            #     "web_data": {"results": web_results},
            # }
        except Exception as e:
            return {
                "snowflake_data": {},
                "rag_data": {"summary": f"Error during RAG: {str(e)}"},
                "web_data": {"results": []},
            }

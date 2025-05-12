
import sys
import os
import json
import logging
from typing import Dict, Any
from openai import OpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agents.snowflake_agent import SnowflakeAgent
from backend.agents.rag_agent import get_rag_response
from backend.agents.web_agent import WebAgent

logger = logging.getLogger(__name__)

class CancerResearchMCP:
    def __init__(self):
        self.snowflake_agent = SnowflakeAgent()
        self.web_agent = WebAgent()

    async def run(self, query: str) -> Dict[str, Any]:
        try:
            snowflake_data = self.snowflake_agent.get_cancer_statistics()
            rag_summary = await get_rag_response(query)
            web_results = self.web_agent.get_clinical_trials(query)

            web_results_str = "\n\n".join([
                f"Title: {item.get('title')}\n"
                f"Description: {item.get('description')}\n"
                f"Phase: {item.get('phase')}\n"
                f"Status: {item.get('status')}\n"
                f"Link: {item.get('source_url')}"
                for item in web_results
            ])

            snowflake_text = json.dumps(snowflake_data, indent=2)

            full_context = f"""
            === SNOWFLAKE STRUCTURED DATA ===
            {snowflake_text}

            === RESEARCH SUMMARY FROM RAG ===
            {rag_summary}

            === WEB SEARCH RESULTS ===
            {web_results_str}
            """

            prompt = f"""
            You are a cancer research assistant.
            Generate a comprehensive research report based on the user query below using the provided structured data, research documents, and web search results.

            User Query:
            {query}

            Data:
            {full_context}
            """

            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1200
            )

            full_report = response.choices[0].message.content
            return {"report": full_report}

        except Exception as e:
            logger.exception("Error during full report generation")
            return {"report": f"Error generating report: {str(e)}"}

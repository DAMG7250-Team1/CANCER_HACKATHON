

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

            import datetime

            prompt = f"""
                    You are an AI-powered Cancer Research Assistant writing for a peer-reviewed oncology journal.
                    Write in formal academic English, using “we” when describing our analyses.
                    Target each main section at ~200–300 words, and include a 1–2 sentence bullet summary at its end.

                    ---
                    TITLE PAGE
                    - Title: Auto-generate a concise yet descriptive title based on the user’s query.
                    - Running head: 50 characters max.
                    - Author: AI Cancer Research Assistant.
                    - Affiliation: Cancer Research Platform.
                    - Date: {datetime.date.today().isoformat()}.
                    - Keywords: list 3–5, comma-separated.
                    - Table of Contents: list each section with page number placeholders.

                    ABSTRACT (150–200 words)
                    - Background
                    - Objectives
                    - Methods
                    - Key Results (with numeric highlights)
                    - Conclusions

                    INTRODUCTION
                    - Contextualize the cancer topic; reference 2–3 key studies in APA style.
                    - State specific research questions or hypotheses.
                    - End with a 2-sentence bullet summary.

                    METHODS
                    - Data Sources:
                    1. Snowflake epidemiological dataset (years, populations, event types).
                    2. RAG summaries of peer-reviewed PDFs (inclusion/exclusion criteria).
                    3. Real-time web data from Tavily.
                    - Analysis Plan:
                    - Show formulas for:
                        - Incidence rate per 100 000: `(CASECOUNT/POPULATION)×100000`.
                        - Year-over-year % change: `((Rate_t – Rate_{{t–1}})/Rate_{{t–1}})×100`.
                    - List software used (e.g. Python 3.11, pandas 2.0.1, OpenAI gpt-4o-mini).
                    - End with a 2-sentence bullet summary.

                    RESULTS
                    5.1 Incidence Trends  
                    - **Table 1: Incidence Rates & Year-over-Year Changes**  
                    | YEAR | CASECOUNT | POPULATION | RATE_PER_100K | %_CHANGE |  
                    |------|-----------|------------|---------------|----------|  
                    | …    | …         | …          | …             | …        |  
                    - Narrative: “Incidence rose from X in 20YY to Y in 20ZZ (Z % increase; average annual growth A %). The largest jump (B %) occurred in YEAR.”  
                    - **Figure 1: Incidence Trend Over Time**  
                    `![Figure 1: Incidence trend over time (line chart placeholder)](#)`  
                    - Bullet summary (2 sentences).

                    5.2 RAG Literature Insights  
                    - Summarize 3–5 key findings from S3 PDFs, with in-text citations (e.g. [@Smith2023]).  
                    - Bullet summary.

                    5.3 Web-sourced Commentary  
                    - Highlight top 2–3 clinical trial trends or cost insights from Tavily.  
                    - Provide URLs in APA format.  
                    - Bullet summary.

                    FIGURES & TABLES (at end)
                    - **Table 1:** see above  
                    - **Figure 1:** see above  

                    DISCUSSION  
                    - Compare your incidence findings to at least two landmark studies (cite DOIs).  
                    - Discuss potential biological or demographic mechanisms.  
                    - Detail data limitations (e.g., Snowflake YEAR stored as VARCHAR, missing p-values).  
                    - Suggest how future RCTs or registries could address gaps.  
                    - Bullet summary.

                    CONCLUSION  
                    - Restate main takeaways.  
                    - Implications for policy or clinical practice.  
                    - Future research directions.  
                    - Bullet summary.

                    REFERENCES (APA)
                    - List every cited paper or URL with full APA details and DOIs.

                    **User Query:**
                    {query}

                    **All Available Data (for context):**
                    {full_context}
                    """




            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=3000
            )

            full_report = response.choices[0].message.content
            return {"report": full_report}

        except Exception as e:
            logger.exception("Error during full report generation")
            return {"report": f"Error generating report: {str(e)}"}

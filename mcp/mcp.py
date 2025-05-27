
# import sys
# import os
# import json
# import logging
# from typing import Dict, Any
# from openai import OpenAI
# # from google import genai
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



# from backend.agents.snowflake_agent import SnowflakeAgent
# from backend.agents.rag_agent import get_rag_response
# from backend.agents.web_agent import WebAgent

# logger = logging.getLogger(__name__)

# class CancerResearchMCP:
#     def __init__(self):
#         self.snowflake_agent = SnowflakeAgent()
#         self.web_agent = WebAgent()

#     async def run(self, query: str) -> Dict[str, Any]:
#         try:
#             # Fetch data from each agent
#             snowflake_data = self.snowflake_agent.get_cancer_statistics()
#             rag_summary = await get_rag_response(query)
#             clinical_trials = self.web_agent.get_clinical_trials(query)
#             funding = self.web_agent.get_funding_opportunities(query)
#             hospitals = self.web_agent.get_hospitals_by_location(query)

#             # Format web results
#             clinical_str = "\n\n".join([
#                 f"Title: {item.get('title')}\n"
#                 f"Description: {item.get('description')}\n"
#                 f"Phase: {item.get('phase')}\n"
#                 f"Status: {item.get('status')}\n"
#                 f"Link: {item.get('source_url')}"
#                 for item in clinical_trials
#             ])

#             funding_str = "\n\n".join([
#                 f"Title: {f.get('title')}\n"
#                 f"Description: {f.get('description')}\n"
#                 f"Link: {f.get('source_url')}"
#                 for f in funding
#             ])

#             hospital_str = "\n\n".join([
#                 f"Name: {h.get('name')}\n"
#                 f"Address: {h.get('address')}\n"
#                 f"Rating: {h.get('rating')}\n"
#                 f"Link: {h.get('source_url')}"
#                 for h in hospitals
#             ])

#             # Combine all context
#             snowflake_text = json.dumps(snowflake_data, indent=2)
#             full_context = f"""
#                 === SNOWFLAKE STRUCTURED DATA ===
#                 {snowflake_text}

#                 === RAG RESEARCH SUMMARY ===
#                 {rag_summary}

#                 === CLINICAL TRIALS ===
#                 {clinical_str}

#                 === FUNDING OPPORTUNITIES ===
#                 {funding_str}

#                 === TREATMENT CENTERS ===
#                 {hospital_str}
#                 """

#             # Generate today's date
#             import datetime
#             today = datetime.date.today().isoformat()

#             # Comprehensive prompt
#             prompt = f"""
#                 You are an AI-powered Cancer Research Assistant tasked with producing an exceptionally comprehensive, peer-reviewed style oncology report. Use formal academic English, adopt “we” to describe analyses, and target each main section at 300–500 words. Include numbered lists, detailed figures, and exhaustive bullet summaries.

#                 EXECUTIVE SUMMARY:
#                 - Provide a succinct overview (2–3 paragraphs) of the study’s purpose, key findings, and implications.

#                 TITLE PAGE:
#                 1. Title: Auto-generate a precise, descriptive title reflecting the query.
#                 2. Running head: ≤50 characters.
#                 3. Author: AI Cancer Research Assistant.
#                 4. Affiliation: Cancer Research Platform.
#                 5. Date: {today}.
#                 6. Keywords: List 5–7, comma-separated.
#                 7. Table of Contents: Enumerate sections with page numbers.

#                 ABSTRACT (200–250 words):
#                 - Background, Objectives, Methods, Key Results (with numeric highlights), Conclusions.

#                 INTRODUCTION:
#                 - Contextualize the cancer topic against current literature, cite 3–5 key studies in APA style.
#                 - State research questions or hypotheses.
#                 - Conclude with a concise bullet summary.

#                 METHODS:
#                 1. Data Sources:
#                 a. Snowflake epidemiological dataset (years, populations, event types).
#                 b. RAG-derived literature summaries (inclusion/exclusion criteria).
#                 c. Real-time web data (Tavily clinical trials, funding, hospitals).
#                 2. Data Cleaning & Preprocessing:
#                 - Describe handling of missing values, data type conversions, and stratification by demographics.
#                 3. Statistical Analysis:
#                 - Formulas:
#                     • Incidence rate per 100,000: `(CASECOUNT/POPULATION)×100000`.
#                     • Year-over-year % change: `((Rate_t – Rate_{{t–1}})/Rate_{{t–1}})×100`.
#                 - Mention statistical tests (e.g., chi-square, t-tests) where relevant.
#                 4. Visualization Plan:
#                 - Line charts, bar graphs, geospatial maps, and allocation pie charts.
#                 5. Software & Libraries:
#                 - E.g., Python 3.11, pandas 2.0.1, matplotlib, geopandas, OpenAI gpt-4o-mini.
#                 - End with a detailed 3-bullet summary.

#                 RESULTS:
#                 5.1 Incidence Trends:
#                 - Table 1: Incidence Rates & YOY Changes.
#                 - Figure 1: Trend line chart.
#                 - Narrative analysis with % growth and statistical significance.
#                 - Bullet summary.

#                 5.2 Literature Insights:
#                 - Summarize 3–5 key findings from RAG with in-text citations.
#                 - Bullet summary.

#                 5.3 Clinical Trials Analysis:
#                 - Trends in phases, status, enrollment numbers.
#                 - URLs in APA format.
#                 - Bullet summary.

#                 5.4 Funding Opportunities:
#                 - Detailed list of grants, amounts, eligibility.
#                 - Pie chart breakdown.
#                 - Bullet summary.

#                 5.5 Treatment Centers by Region:
#                 - Top 5 centers with names, addresses, ratings.
#                 - Geospatial map description.
#                 - Bullet summary.

#                 5.6 Treatment Modalities & Medication Overview:
#                 - List standard-of-care regimens by line of therapy.
#                 - Describe mechanism of action, dosing schedules, and key toxicities.
#                 - Bullet summary.

#                 TABLES:
#                 - Table 1   placeholders with captions.

#                 DISCUSSION:
#                 - Compare findings to ≥2 landmark studies (include DOIs).
#                 - Discuss biological/demographic mechanisms.
#                 - Address data limitations (e.g., VARCHAR year fields, missing metrics).
#                 - Propose future RCTs or registry enhancements.
#                 - Bullet summary.

#                 CONCLUSION:
#                 - Synthesize main takeaways.
#                 - Implications for policy/clinical practice.
#                 - Future research directions.
#                 - Bullet summary.

#                 REFERENCES (APA):
#                 - Full APA citations for all sources, with DOIs.

#                 APPENDICES:
#                 - Raw data tables.
#                 - Sample code snippets for analyses.

#                 **User Query:**
#                 {query}

#                 **All Available Data:**
#                 {full_context}
#                 """

         
            
#             from google import genai
#             import os

#             # initialize the client (Gemini Developer API)
#             client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

#             # start a stateful chat session
#             chat = client.chats.create(model="gemini-2.0-flash-001")

#             # send your prompt
#             resp = chat.send_message(prompt)

            
#             # full_report = response.choices[0].message.content
#             full_report = resp.text
#             return {"report": full_report}

#         except Exception as e:
#             logger.exception("Error during full report generation")
#             return {"report": f"Error generating report: {str(e)}"}























import sys
import os
import json
import logging
import time
from typing import Dict, Any, List, Tuple
from datetime import date

# make sure project packages are on the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agents.snowflake_agent import SnowflakeAgent
from backend.agents.rag_agent import get_rag_response
from backend.agents.web_agent import WebAgent

from google import genai
from google.genai import errors

# ── Logging ─────────────────────────────────────────
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ── Configuration ───────────────────────────────────
MODEL_NAME          = "gemini-2.0-flash-001"
COMPRESSION_BUDGET  = 400
SECTIONS: List[Tuple[str,int]] = [
    ("EXECUTIVE SUMMARY",  800),
    ("TITLE & ABSTRACT",   600),
    ("INTRODUCTION",       800),
    ("METHODS",            600),
    ("RESULTS",           1200),
    ("DISCUSSION",         800),
    ("CONCLUSION",         400),
]

# ── Helpers ─────────────────────────────────────────
def with_backoff(fn, retries: int = 3, base_delay: float = 2.0):
    """Retry on 429 errors with exponential backoff."""
    for i in range(retries):
        try:
            return fn()
        except errors.ClientError as e:
            if e.status_code == 429:
                delay = base_delay * (2 ** i)
                logger.warning(f"Rate limit hit, retrying in {delay:.1f}s…")
                time.sleep(delay)
            else:
                raise
    # final attempt
    return fn()

def compress_segment(client: genai.Client, label: str, text: str, max_tokens: int = COMPRESSION_BUDGET) -> str:
    """Ask Gemini to summarize a chunk into ≤ max_tokens."""
    chat = client.chats.create(model=MODEL_NAME)
    prompt = f"Summarize this {label} into no more than {max_tokens} tokens:\n\n{text}"
    resp = with_backoff(lambda: chat.send_message(prompt))
    return resp.last.content.strip()

def generate_section(client: genai.Client, context: str, name: str, max_tokens: int) -> str:
    """Generate one section of the report given the lean context."""
    chat = client.chats.create(model=MODEL_NAME, temperature=0.7)
    prompt = (
        "You are an AI-powered Cancer Research Assistant writing for a peer-reviewed oncology journal. "
        "Use formal academic English and adopt “we” when describing analyses.\n\n"
        f"Based on the context below, draft the **{name}** section (~{max_tokens} tokens):\n\n"
        f"---\n{context}\n---\n"
        f"## {name}:\n"
    )
    resp = with_backoff(lambda: chat.send_message(prompt))
    return resp.last.content.strip()

# ── Main Class ───────────────────────────────────────
class CancerResearchMCP:
    def __init__(self):
        self.snowflake_agent = SnowflakeAgent()
        self.web_agent       = WebAgent()
        self.client          = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    async def run(self, query: str) -> Dict[str, Any]:
        try:
            # 1) Fetch raw data
            snowflake_data   = self.snowflake_agent.get_cancer_statistics()
            rag_summary      = await get_rag_response(query)
            clinical_trials  = self.web_agent.get_clinical_trials(query)
            funding_opps     = self.web_agent.get_funding_opportunities(query)
            hospitals        = self.web_agent.get_hospitals_by_location(query)

            # 2) Render each to text
            snowflake_text = json.dumps(snowflake_data, indent=2)
            rag_text       = rag_summary
            trials_text    = "\n\n".join(f"{t['title']}: {t['description']}" for t in clinical_trials)
            funding_text   = "\n\n".join(f"{f['title']}: {f['description']}" for f in funding_opps)
            hosp_text      = "\n\n".join(f"{h['name']}, {h['address']}" for h in hospitals)

            # 3) Compress each chunk into ~400 tokens
            sf_sum   = compress_segment(self.client, "Snowflake data",        snowflake_text)
            rag_sum  = compress_segment(self.client, "RAG literature",        rag_text)
            ct_sum   = compress_segment(self.client, "Clinical trials",       trials_text)
            fd_sum   = compress_segment(self.client, "Funding opportunities", funding_text)
            hs_sum   = compress_segment(self.client, "Hospital information",  hosp_text)

            # 4) Build lean context
            lean_context = "\n\n".join([sf_sum, rag_sum, ct_sum, fd_sum, hs_sum])

            # 5) Generate each section separately
            report_parts: List[str] = []
            for name, budget in SECTIONS:
                section_text = generate_section(self.client, lean_context, name, budget)
                report_parts.append(f"### {name}\n\n{section_text}")

            # 6) Combine
            full_report = "\n\n".join(report_parts)
            return {"report": full_report}

        except Exception as e:
            logger.exception("Error during full report generation")
            return {"report": f"Error generating report: {str(e)}"}

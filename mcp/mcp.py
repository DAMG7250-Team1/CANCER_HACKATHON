

# import sys
# import os
# import json
# import logging
# from typing import Dict, Any
# from openai import OpenAI

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
#             snowflake_data = self.snowflake_agent.get_cancer_statistics()
#             rag_summary = await get_rag_response(query)
#             web_results = self.web_agent.get_clinical_trials(query)

#             web_results_str = "\n\n".join([
#                 f"Title: {item.get('title')}\n"
#                 f"Description: {item.get('description')}\n"
#                 f"Phase: {item.get('phase')}\n"
#                 f"Status: {item.get('status')}\n"
#                 f"Link: {item.get('source_url')}"
#                 for item in web_results
#             ])

#             snowflake_text = json.dumps(snowflake_data, indent=2)

#             full_context = f"""
#             === SNOWFLAKE STRUCTURED DATA ===
#             {snowflake_text}

#             === RESEARCH SUMMARY FROM RAG ===
#             {rag_summary}

#             === WEB SEARCH RESULTS ===
#             {web_results_str}
#             """

#             import datetime

#             prompt = f"""
#                     You are an AI-powered Cancer Research Assistant writing for a peer-reviewed oncology journal.
#                     Write in formal academic English, using “we” when describing our analyses.
#                     Target each main section at ~200–300 words, and include a 1–2 sentence bullet summary at its end.

#                     ---
#                     TITLE PAGE
#                     - Title: Auto-generate a concise yet descriptive title based on the user’s query.
#                     - Running head: 50 characters max.
#                     - Author: AI Cancer Research Assistant.
#                     - Affiliation: Cancer Research Platform.
#                     - Date: {datetime.date.today().isoformat()}.
#                     - Keywords: list 3–5, comma-separated.
#                     - Table of Contents: list each section with page number placeholders.

#                     ABSTRACT (150–200 words)
#                     - Background
#                     - Objectives
#                     - Methods
#                     - Key Results (with numeric highlights)
#                     - Conclusions

#                     INTRODUCTION
#                     - Contextualize the cancer topic; reference 2–3 key studies in APA style.
#                     - State specific research questions or hypotheses.
#                     - End with a 2-sentence bullet summary.

#                     METHODS
#                     - Data Sources:
#                     1. Snowflake epidemiological dataset (years, populations, event types).
#                     2. RAG summaries of peer-reviewed PDFs (inclusion/exclusion criteria).
#                     3. Real-time web data from Tavily.
#                     - Analysis Plan:
#                     - Show formulas for:
#                         - Incidence rate per 100 000: `(CASECOUNT/POPULATION)×100000`.
#                         - Year-over-year % change: `((Rate_t – Rate_{{t–1}})/Rate_{{t–1}})×100`.
#                     - List software used (e.g. Python 3.11, pandas 2.0.1, OpenAI gpt-4o-mini).
#                     - End with a 2-sentence bullet summary.

#                     RESULTS
#                     5.1 Incidence Trends  
#                     - **Table 1: Incidence Rates & Year-over-Year Changes**  
#                     | YEAR | CASECOUNT | POPULATION | RATE_PER_100K | %_CHANGE |  
#                     |------|-----------|------------|---------------|----------|  
#                     | …    | …         | …          | …             | …        |  
#                     - Narrative: “Incidence rose from X in 20YY to Y in 20ZZ (Z % increase; average annual growth A %). The largest jump (B %) occurred in YEAR.”  
#                     - **Figure 1: Incidence Trend Over Time**  
#                     `![Figure 1: Incidence trend over time (line chart placeholder)](#)`  
#                     - Bullet summary (2 sentences).

#                     5.2 RAG Literature Insights  
#                     - Summarize 3–5 key findings from S3 PDFs, with in-text citations (e.g. [@Smith2023]).  
#                     - Bullet summary.

#                     5.3 Web-sourced Commentary  
#                     - Highlight top 2–3 clinical trial trends or cost insights from Tavily.  
#                     - Provide URLs in APA format.  
#                     - Bullet summary.

#                     FIGURES & TABLES (at end)
#                     - **Table 1:** see above  
#                     - **Figure 1:** see above  

#                     DISCUSSION  
#                     - Compare your incidence findings to at least two landmark studies (cite DOIs).  
#                     - Discuss potential biological or demographic mechanisms.  
#                     - Detail data limitations (e.g., Snowflake YEAR stored as VARCHAR, missing p-values).  
#                     - Suggest how future RCTs or registries could address gaps.  
#                     - Bullet summary.

#                     CONCLUSION  
#                     - Restate main takeaways.  
#                     - Implications for policy or clinical practice.  
#                     - Future research directions.  
#                     - Bullet summary.

#                     REFERENCES (APA)
#                     - List every cited paper or URL with full APA details and DOIs.

#                     **User Query:**
#                     {query}

#                     **All Available Data (for context):**
#                     {full_context}
#                     """




#             client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#             response = client.chat.completions.create(
#                 model="gpt-4o-mini",
#                 messages=[{"role": "user", "content": prompt}],
#                 temperature=0.7,
#                 max_tokens=3000
#             )

#             full_report = response.choices[0].message.content
#             return {"report": full_report}

#         except Exception as e:
#             logger.exception("Error during full report generation")
#             return {"report": f"Error generating report: {str(e)}"}















# import sys
# import os
# import json
# import logging
# from typing import Dict, Any
# from openai import OpenAI

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
#             snowflake_data = self.snowflake_agent.get_cancer_statistics()
#             rag_summary = await get_rag_response(query)
#             clinical_trials = self.web_agent.get_clinical_trials(query)
#             funding = self.web_agent.get_funding_opportunities(query)
#             hospitals = self.web_agent.get_hospitals_by_location(query)

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

#             import datetime
#             today = datetime.date.today().isoformat()

#             prompt = f"""
#                     You are an AI-powered Cancer Research Assistant writing for a peer-reviewed oncology journal.
#                     Write in formal academic English, using “we” when describing our analyses.
#                     Target each main section at ~200–300 words, and include a 1–2 sentence bullet summary at its end.

#                     ---
#                     TITLE PAGE
#                     - Title: Auto-generate a concise yet descriptive title based on the user’s query.
#                     - Running head: 50 characters max.
#                     - Author: AI Cancer Research Assistant.
#                     - Affiliation: Cancer Research Platform.
#                     - Date: {today}.
#                     - Keywords: list 3–5, comma-separated.
#                     - Table of Contents: list each section with page number placeholders.

#                     ABSTRACT (150–200 words)
#                     - Background
#                     - Objectives
#                     - Methods
#                     - Key Results (with numeric highlights)
#                     - Conclusions

#                     INTRODUCTION
#                     - Contextualize the cancer topic; reference 2–3 key studies in APA style.
#                     - State specific research questions or hypotheses.
#                     - End with a 2-sentence bullet summary.

#                     METHODS
#                     - Data Sources:
#                     1. Snowflake epidemiological dataset (years, populations, event types).
#                     2. RAG summaries of peer-reviewed PDFs (inclusion/exclusion criteria).
#                     3. Real-time web data from Tavily.
#                     - Analysis Plan:
#                     - Show formulas for:
#                     - Incidence rate per 100 000: `(CASECOUNT/POPULATION)×100000`.
#                     - Year-over-year % change: `((Rate_t – Rate_{{t–1}})/Rate_{{t–1}})×100`.
#                     - List software used (e.g. Python 3.11, pandas 2.0.1, OpenAI gpt-4o-mini).
#                     - End with a 2-sentence bullet summary.

#                     RESULTS
#                     5.1 Incidence Trends
#                     - **Table 1: Incidence Rates & Year-over-Year Changes**
#                     | YEAR | CASECOUNT | POPULATION | RATE_PER_100K | %_CHANGE |
#                     |------|-----------|------------|---------------|----------|
#                     | …    | …         | …          | …             | …        |
#                     - Narrative: “Incidence rose from X in 20YY to Y in 20ZZ (Z % increase; average annual growth A %). The largest jump (B %) occurred in YEAR.”
#                     - **Figure 1:** Incidence trend over time (line chart).
#                     - Bullet summary (2 sentences).

#                     5.2 RAG Literature Insights
#                     - Summarize 3–5 key findings from S3 PDFs, with in-text citations (e.g. [@Smith2023]).
#                     - Bullet summary.

#                     5.3 Web-sourced Commentary
#                     - Highlight top 2–3 clinical trial trends or cost insights from Tavily (list URLs in APA format).
#                     - Bullet summary.

#                     5.4 Funding Opportunities
#                     - List key grants/funding sources identified, with award amounts if available.
#                     - Provide source URLs in APA format.
#                     - Bullet summary.

#                     5.5 Treatment Centers by Region
#                     - Detail top 3–5 cancer treatment centers based on location data.
#                     - Include name, address, and rating.
#                     - Bullet summary.

#                     FIGURES & TABLES (at end)
#                     - **Table 1:** see above
#                     - **Figure 1:** see above

#                     DISCUSSION
#                     - Compare your incidence findings to at least two landmark studies (cite DOIs).
#                     - Discuss potential biological or demographic mechanisms.
#                     - Detail data limitations (e.g., Snowflake YEAR stored as VARCHAR, missing p-values).
#                     - Suggest how future RCTs or registries could address gaps.
#                     - Bullet summary.

#                     CONCLUSION
#                     - Restate main takeaways.
#                     - Implications for policy or clinical practice.
#                     - Future research directions.
#                     - Bullet summary.

#                     REFERENCES (APA)
#                     - List every cited paper or URL with full APA details and DOIs.

#                     **User Query:**
#                     {query}

#                     **All Available Data (for context):**
#                     {full_context}
#                     """

#             client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#             response = client.chat.completions.create(
#                 model="gpt-4o-mini",
#                 messages=[{"role": "user", "content": prompt}],
#                 temperature=0.7,
#                 max_tokens=4000
#             )

#             full_report = response.choices[0].message.content

#             return {"report": full_report}

#         except Exception as e:
#             logger.exception("Error during full report generation")
#             return {"report": f"Error generating report: {str(e)}"}











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
            # Fetch data from each agent
            snowflake_data = self.snowflake_agent.get_cancer_statistics()
            rag_summary = await get_rag_response(query)
            clinical_trials = self.web_agent.get_clinical_trials(query)
            funding = self.web_agent.get_funding_opportunities(query)
            hospitals = self.web_agent.get_hospitals_by_location(query)

            # Format web results
            clinical_str = "\n\n".join([
                f"Title: {item.get('title')}\n"
                f"Description: {item.get('description')}\n"
                f"Phase: {item.get('phase')}\n"
                f"Status: {item.get('status')}\n"
                f"Link: {item.get('source_url')}"
                for item in clinical_trials
            ])

            funding_str = "\n\n".join([
                f"Title: {f.get('title')}\n"
                f"Description: {f.get('description')}\n"
                f"Link: {f.get('source_url')}"
                for f in funding
            ])

            hospital_str = "\n\n".join([
                f"Name: {h.get('name')}\n"
                f"Address: {h.get('address')}\n"
                f"Rating: {h.get('rating')}\n"
                f"Link: {h.get('source_url')}"
                for h in hospitals
            ])

            # Combine all context
            snowflake_text = json.dumps(snowflake_data, indent=2)
            full_context = f"""
                === SNOWFLAKE STRUCTURED DATA ===
                {snowflake_text}

                === RAG RESEARCH SUMMARY ===
                {rag_summary}

                === CLINICAL TRIALS ===
                {clinical_str}

                === FUNDING OPPORTUNITIES ===
                {funding_str}

                === TREATMENT CENTERS ===
                {hospital_str}
                """

            # Generate today's date
            import datetime
            today = datetime.date.today().isoformat()

            # Comprehensive prompt
            prompt = f"""
                You are an AI-powered Cancer Research Assistant tasked with producing an exceptionally comprehensive, peer-reviewed style oncology report. Use formal academic English, adopt “we” to describe analyses, and target each main section at 300–500 words. Include numbered lists, detailed figures, and exhaustive bullet summaries.

                EXECUTIVE SUMMARY:
                - Provide a succinct overview (2–3 paragraphs) of the study’s purpose, key findings, and implications.

                TITLE PAGE:
                1. Title: Auto-generate a precise, descriptive title reflecting the query.
                2. Running head: ≤50 characters.
                3. Author: AI Cancer Research Assistant.
                4. Affiliation: Cancer Research Platform.
                5. Date: {today}.
                6. Keywords: List 5–7, comma-separated.
                7. Table of Contents: Enumerate sections with page numbers.

                ABSTRACT (200–250 words):
                - Background, Objectives, Methods, Key Results (with numeric highlights), Conclusions.

                INTRODUCTION:
                - Contextualize the cancer topic against current literature, cite 3–5 key studies in APA style.
                - State research questions or hypotheses.
                - Conclude with a concise bullet summary.

                METHODS:
                1. Data Sources:
                a. Snowflake epidemiological dataset (years, populations, event types).
                b. RAG-derived literature summaries (inclusion/exclusion criteria).
                c. Real-time web data (Tavily clinical trials, funding, hospitals).
                2. Data Cleaning & Preprocessing:
                - Describe handling of missing values, data type conversions, and stratification by demographics.
                3. Statistical Analysis:
                - Formulas:
                    • Incidence rate per 100,000: `(CASECOUNT/POPULATION)×100000`.
                    • Year-over-year % change: `((Rate_t – Rate_{{t–1}})/Rate_{{t–1}})×100`.
                - Mention statistical tests (e.g., chi-square, t-tests) where relevant.
                4. Visualization Plan:
                - Line charts, bar graphs, geospatial maps, and allocation pie charts.
                5. Software & Libraries:
                - E.g., Python 3.11, pandas 2.0.1, matplotlib, geopandas, OpenAI gpt-4o-mini.
                - End with a detailed 3-bullet summary.

                RESULTS:
                5.1 Incidence Trends:
                - Table 1: Incidence Rates & YOY Changes.
                - Figure 1: Trend line chart.
                - Narrative analysis with % growth and statistical significance.
                - Bullet summary.

                5.2 Literature Insights:
                - Summarize 3–5 key findings from RAG with in-text citations.
                - Bullet summary.

                5.3 Clinical Trials Analysis:
                - Trends in phases, status, enrollment numbers.
                - URLs in APA format.
                - Bullet summary.

                5.4 Funding Opportunities:
                - Detailed list of grants, amounts, eligibility.
                - Pie chart breakdown.
                - Bullet summary.

                5.5 Treatment Centers by Region:
                - Top 5 centers with names, addresses, ratings.
                - Geospatial map description.
                - Bullet summary.

                FIGURES & TABLES:
                - Table 1–5 and Figures 1–4 placeholders with captions.

                DISCUSSION:
                - Compare findings to ≥2 landmark studies (include DOIs).
                - Discuss biological/demographic mechanisms.
                - Address data limitations (e.g., VARCHAR year fields, missing metrics).
                - Propose future RCTs or registry enhancements.
                - Bullet summary.

                CONCLUSION:
                - Synthesize main takeaways.
                - Implications for policy/clinical practice.
                - Future research directions.
                - Bullet summary.

                REFERENCES (APA):
                - Full APA citations for all sources, with DOIs.

                APPENDICES:
                - Raw data tables.
                - Sample code snippets for analyses.

                **User Query:**
                {query}

                **All Available Data:**
                {full_context}
                """

            # Call OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=6000
            )

            full_report = response.choices[0].message.content
            return {"report": full_report}

        except Exception as e:
            logger.exception("Error during full report generation")
            return {"report": f"Error generating report: {str(e)}"}

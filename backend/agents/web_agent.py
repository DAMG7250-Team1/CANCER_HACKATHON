# # web_agent.py (Final Clean Production Version)

# import requests
# import os
# import logging
# import re
# from datetime import datetime
# from dotenv import load_dotenv
# from typing import Dict, List, Optional, Any

# # Configure Logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class WebAgent:
#     def __init__(self):
#         load_dotenv()
#         self.tavily_api_key = os.getenv('TAVILY_API_KEY')
#         if not self.tavily_api_key:
#             logger.error("TAVILY_API_KEY not found in environment variables")
#             raise ValueError("TAVILY_API_KEY is required")
#         self.session = requests.Session()
#         self.tavily_endpoint = "https://api.tavily.com/search"

#     def _tavily_search(self, query: str, search_depth: str = "basic", include_answer: bool = False, max_results: int = 10) -> Dict[str, Any]:
#         headers = {"Content-Type": "application/json"}
#         payload = {
#             "api_key": self.tavily_api_key,
#             "query": query,
#             "search_depth": search_depth if search_depth in ["basic", "advanced"] else "advanced",
#             "include_answer": include_answer,
#             "max_results": max_results
#         }
#         try:
#             response = self.session.post(self.tavily_endpoint, headers=headers, json=payload)
#             response.raise_for_status()
#             return response.json()
#         except Exception as e:
#             logger.error(f"Error in Tavily search: {str(e)}")
#             return {"results": []}

#     def get_treatment_costs_from_serp(self, query: str) -> List[Dict[str, Any]]:
#         results = self._tavily_search(f"{query} cancer treatment costs detailed insurance coverage duration regional", search_depth="advanced")
#         return self._extract_treatment_costs(results.get('results', []))

#     def get_clinical_trials(self, condition: str) -> List[Dict[str, Any]]:
#         results = self._tavily_search(f"active clinical trials {condition} cancer treatment", search_depth="advanced")
#         return self._extract_clinical_trials(results.get('results', []))

#     def get_cancer_statistics_from_serp(self, query: str = "") -> Dict[str, Any]:
#         results = self._tavily_search(f"cancer statistics {query}", search_depth="advanced", include_answer=True)
#         return self._extract_statistics(results.get('results', []))

#     def search_medical_literature(self, query: str) -> List[Dict[str, Any]]:
#         results = self._tavily_search(f"medical literature {query}", search_depth="advanced", include_answer=True, max_results=5)
#         return self._extract_medical_literature(results.get('results', []))

#     def get_treatment_centers(self, location: str) -> List[Dict[str, Any]]:
#         return [
#             {"name": "Memorial Cancer Center", "location": location, "rating": 4.8},
#             {"name": "Regional Cancer Institute", "location": location, "rating": 4.6}
#         ]

#     def _extract_treatment_costs(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         treatments = []
#         for res in results:
#             treatments.append({
#                 "title": res.get("title", "Unknown"),
#                 "description": res.get("content", "")[:200],
#                 "url": res.get("url", "")
#             })
#         return treatments

#     def _extract_clinical_trials(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         trials = []
#         for res in results:
#             title = res.get('title', '')
#             content = res.get('content', '')
#             phase_match = re.search(r'phase (i{1,3}|[1-3])', title.lower() + ' ' + content.lower())
#             trials.append({
#                 "title": title,
#                 "description": content,
#                 "phase": phase_match.group(0).title() if phase_match else "Unknown",
#                 "status": re.search(r'(recruiting|completed|active)', content.lower()).group(0).title() if re.search(r'(recruiting|completed|active)', content.lower()) else "Unknown",
#                 "source_url": res.get('url', '')
#             })
#         return trials

#     def _extract_statistics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
#         if not results:
#             return {}
#         return {
#             "sources": [{"title": res.get("title", ""), "snippet": res.get("content", "")[:200], "url": res.get("url", "")} for res in results]
#         }

#     def _extract_medical_literature(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         literature = []
#         for res in results:
#             literature.append({
#                 "title": res.get('title', 'Untitled'),
#                 "snippet": res.get('content', '')[:200],
#                 "source": self._extract_source(res.get('url', '')),
#                 "url": res.get('url', '')
#             })
#         return literature

#     def _extract_source(self, url: str) -> str:
#         try:
#             from urllib.parse import urlparse
#             parsed_url = urlparse(url)
#             domain = parsed_url.netloc.replace('www.', '')
#             return domain
#         except Exception:
#             return "Unknown Source"
#     def get_all_web_data(self, query: str) -> Dict[str, Any]:
#         logger.info(f"Running full web search pipeline for: {query}")
#         return {
#             "statistics": self.get_cancer_statistics_from_serp(query),
#             "literature": self.search_medical_literature(query),
#             "treatment_costs": self.get_treatment_costs_from_serp(query),
#             "clinical_trials": self.get_clinical_trials(query),
#             "treatment_centers": self.get_treatment_centers("USA"),  # You can adjust location dynamically
#         }









# import requests
# import os
# import logging
# import re
# from datetime import datetime
# from dotenv import load_dotenv
# from typing import Dict, List, Optional, Any
# from urllib.parse import urlparse

# # Configure Logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class WebAgent:
#     def __init__(self):
#         load_dotenv()
#         self.tavily_api_key = os.getenv('TAVILY_API_KEY')
#         if not self.tavily_api_key:
#             logger.error("TAVILY_API_KEY not found in environment variables")
#             raise ValueError("TAVILY_API_KEY is required")
#         self.session = requests.Session()
#         self.tavily_endpoint = "https://api.tavily.com/search"

#     def _tavily_search(self, query: str, search_depth: str = "basic", include_answer: bool = False, max_results: int = 10) -> Dict[str, Any]:
#         headers = {"Content-Type": "application/json"}
#         payload = {
#             "api_key": self.tavily_api_key,
#             "query": query,
#             "search_depth": search_depth if search_depth in ["basic", "advanced"] else "advanced",
#             "include_answer": include_answer,
#             "max_results": max_results
#         }
#         try:
#             response = self.session.post(self.tavily_endpoint, headers=headers, json=payload)
#             response.raise_for_status()
#             return response.json()
#         except Exception as e:
#             logger.error(f"Error in Tavily search: {str(e)}")
#             return {"results": []}

#     def get_treatment_costs_from_serp(self, query: str) -> List[Dict[str, Any]]:
#         results = self._tavily_search(
#             f"{query} cancer treatment costs detailed insurance coverage duration regional",
#             search_depth="advanced"
#         )
#         return self._extract_treatment_costs(results.get('results', []))

#     def get_clinical_trials(self, condition: str) -> List[Dict[str, Any]]:
#         results = self._tavily_search(
#             f"active clinical trials {condition} cancer treatment",
#             search_depth="advanced"
#         )
#         return self._extract_clinical_trials(results.get('results', []))

#     def get_cancer_statistics_from_serp(self, query: str = "") -> Dict[str, Any]:
#         results = self._tavily_search(
#             f"cancer statistics {query}",
#             search_depth="advanced",
#             include_answer=True
#         )
#         return self._extract_statistics(results.get('results', []))

#     def search_medical_literature(self, query: str) -> List[Dict[str, Any]]:
#         results = self._tavily_search(
#             f"medical literature {query}",
#             search_depth="advanced",
#             include_answer=True,
#             max_results=5
#         )
#         return self._extract_medical_literature(results.get('results', []))

#     def get_treatment_centers(self, location: str) -> List[Dict[str, Any]]:
#         # Static stub; retained for backward compatibility
#         return [
#             {"name": "Memorial Cancer Center", "location": location, "rating": 4.8},
#             {"name": "Regional Cancer Institute", "location": location, "rating": 4.6}
#         ]

#     def get_funding_opportunities(self, condition: str) -> List[Dict[str, Any]]:
#         results = self._tavily_search(
#             f"cancer research funding opportunities for {condition}",
#             search_depth="advanced",
#             max_results=10
#         )
#         return self._extract_funding(results.get('results', []))

#     def get_hospitals_by_location(self, location: str) -> List[Dict[str, Any]]:
#         results = self._tavily_search(
#             f"best cancer treatment centers in {location} with address and rating",
#             search_depth="advanced",
#             max_results=10
#         )
#         return self._extract_hospitals(results.get('results', []))

#     def _extract_treatment_costs(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         treatments = []
#         for res in results:
#             treatments.append({
#                 "title": res.get("title", "Unknown"),
#                 "description": res.get("content", "")[:200],
#                 "url": res.get("url", "")
#             })
#         return treatments

#     def _extract_clinical_trials(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         trials = []
#         for res in results:
#             title = res.get('title', '')
#             content = res.get('content', '')
#             phase_match = re.search(r'phase (i{1,3}|[1-3])', (title + ' ' + content).lower())
#             status_match = re.search(r'(recruiting|completed|active)', content.lower())
#             trials.append({
#                 "title": title,
#                 "description": content,
#                 "phase": phase_match.group(0).title() if phase_match else "Unknown",
#                 "status": status_match.group(0).title() if status_match else "Unknown",
#                 "source_url": res.get('url', '')
#             })
#         return trials

#     def _extract_statistics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
#         if not results:
#             return {}
#         return {
#             "sources": [
#                 {"title": res.get("title", ""), "snippet": res.get("content", "")[:200], "url": res.get("url", "")} for res in results
#             ]
#         }

#     def _extract_medical_literature(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         literature = []
#         for res in results:
#             literature.append({
#                 "title": res.get('title', 'Untitled'),
#                 "snippet": res.get('content', '')[:200],
#                 "source": self._extract_source(res.get('url', '')),
#                 "url": res.get('url', '')
#             })
#         return literature

#     def _extract_funding(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         funding = []
#         for res in results:
#             funding.append({
#                 "title": res.get("title", "Unknown"),
#                 "description": res.get("content", "")[:200],
#                 "source_url": res.get("url", "")
#             })
#         return funding

#     def _extract_hospitals(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         hospitals = []
#         for res in results:
#             content = res.get("content", "")
#             address_match = re.search(r"\d{1,5}\s+\w+[\w\s,]+", content)
#             rating_match = re.search(r"(\d\.\d)\s*/\s*5", content)
#             hospitals.append({
#                 "name": res.get("title", "Unknown"),
#                 "address": address_match.group(0) if address_match else "Unknown address",
#                 "rating": float(rating_match.group(1)) if rating_match else None,
#                 "source_url": res.get("url", "")
#             })
#         return hospitals

#     def _extract_source(self, url: str) -> str:
#         try:
#             parsed_url = urlparse(url)
#             domain = parsed_url.netloc.replace('www.', '')
#             return domain
#         except Exception:
#             return "Unknown Source"

#     def get_all_web_data(self, query: str) -> Dict[str, Any]:
#         logger.info(f"Running full web search pipeline for: {query}")
#         return {
#             "statistics": self.get_cancer_statistics_from_serp(query),
#             "literature": self.search_medical_literature(query),
#             "treatment_costs": self.get_treatment_costs_from_serp(query),
#             "clinical_trials": self.get_clinical_trials(query),
#             "treatment_centers": self.get_hospitals_by_location("USA"),
#             "funding_opportunities": self.get_funding_opportunities(query),
#             "hospitals_in_region": self.get_hospitals_by_location("USA")
#         }






















# import requests
# import os
# import logging
# import re
# from datetime import datetime
# from dotenv import load_dotenv
# from typing import Dict, List, Any
# from urllib.parse import urlparse

# # Configure Logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class WebAgent:
#     def __init__(self):
#         load_dotenv()
#         self.tavily_api_key = os.getenv('TAVILY_API_KEY')
#         if not self.tavily_api_key:
#             logger.error("TAVILY_API_KEY not found in environment variables")
#             raise ValueError("TAVILY_API_KEY is required")
#         self.session = requests.Session()
#         self.tavily_endpoint = "https://api.tavily.com/search"

#     def _tavily_search(self, query: str, search_depth: str = "basic", include_answer: bool = False, max_results: int = 10) -> Dict[str, Any]:
#         headers = {"Content-Type": "application/json"}
#         payload = {
#             "api_key": self.tavily_api_key,
#             "query": query,
#             "search_depth": search_depth if search_depth in ["basic", "advanced"] else "advanced",
#             "include_answer": include_answer,
#             "max_results": max_results
#         }
#         try:
#             response = self.session.post(self.tavily_endpoint, headers=headers, json=payload)
#             response.raise_for_status()
#             return response.json()
#         except Exception as e:
#             logger.error(f"Error in Tavily search: {e}")
#             return {"results": []}

#     def get_treatment_costs_from_serp(self, query: str) -> List[Dict[str, Any]]:
#         results = self._tavily_search(
#             f"{query} cancer treatment costs detailed insurance coverage duration regional",
#             search_depth="advanced"
#         )
#         return self._extract_treatment_costs(results.get('results', []))

#     def get_clinical_trials(self, condition: str) -> List[Dict[str, Any]]:
#         results = self._tavily_search(
#             f"active clinical trials {condition} cancer treatment",
#             search_depth="advanced"
#         )
#         return self._extract_clinical_trials(results.get('results', []))

#     def get_cancer_statistics_from_serp(self, query: str = "") -> Dict[str, Any]:
#         results = self._tavily_search(
#             f"cancer statistics {query}",
#             search_depth="advanced",
#             include_answer=True
#         )
#         return self._extract_statistics(results.get('results', []))

#     def search_medical_literature(self, query: str) -> List[Dict[str, Any]]:
#         results = self._tavily_search(
#             f"medical literature {query}",
#             search_depth="advanced",
#             include_answer=True,
#             max_results=5
#         )
#         return self._extract_medical_literature(results.get('results', []))

#     def get_treatment_centers(self, location: str) -> List[Dict[str, Any]]:
#         # Static stub; retained for backward compatibility
#         return [
#             {"name": "Memorial Cancer Center", "location": location, "rating": 4.8},
#             {"name": "Regional Cancer Institute", "location": location, "rating": 4.6}
#         ]

#     def get_funding_opportunities(self, condition: str) -> List[Dict[str, Any]]:
#         results = self._tavily_search(
#             f"cancer research funding opportunities for {condition}",
#             search_depth="advanced",
#             max_results=10
#         )
#         return self._extract_funding(results.get('results', []))

#     def get_hospitals_by_location(self, location: str) -> List[Dict[str, Any]]:
#         results = self._tavily_search(
#             f"best cancer treatment centers in {location} with address and rating",
#             search_depth="advanced",
#             max_results=10
#         )
#         return self._extract_hospitals(results.get('results', []))

#     def _extract_treatment_costs(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         treatments = []
#         for res in results:
#             treatments.append({
#                 "title": res.get("title", "Unknown"),
#                 "description": res.get("content", "")[:200],
#                 "url": res.get("url", "")
#             })
#         return treatments

#     def _extract_clinical_trials(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         trials = []
#         for res in results:
#             title = res.get('title', '')
#             content = res.get('content', '')
#             phase_match = re.search(r'phase (i{1,3}|[1-3])', (title + ' ' + content).lower())
#             status_match = re.search(r'(recruiting|completed|active)', content.lower())
#             trials.append({
#                 "title": title,
#                 "description": content,
#                 "phase": phase_match.group(0).title() if phase_match else "Unknown",
#                 "status": status_match.group(0).title() if status_match else "Unknown",
#                 "source_url": res.get('url', '')
#             })
#         return trials

#     def _extract_statistics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
#         if not results:
#             return {}
#         return {
#             "sources": [
#                 {"title": res.get("title", ""), "snippet": res.get("content", "")[:200], "url": res.get("url", "")} for res in results
#             ]
#         }

#     def _extract_medical_literature(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         literature = []
#         for res in results:
#             literature.append({
#                 "title": res.get('title', 'Untitled'),
#                 "snippet": res.get('content', '')[:200],
#                 "source": self._extract_source(res.get('url', '')),
#                 "url": res.get('url', '')
#             })
#         return literature

#     def _extract_funding(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         funding = []
#         for res in results:
#             funding.append({
#                 "title": res.get("title", "Unknown"),
#                 "description": res.get("content", "")[:200],
#                 "source_url": res.get("url", "")
#             })
#         return funding

#     def _extract_hospitals(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         hospitals = []
#         for res in results:
#             content = res.get("content", "")
#             address_match = re.search(r"\d{1,5}\s+\w+[\w\s,]+", content)
#             rating_match = re.search(r"(\d\.\d)\s*/\s*5", content)
#             hospitals.append({
#                 "name": res.get("title", "Unknown"),
#                 "address": address_match.group(0) if address_match else "Unknown address",
#                 "rating": float(rating_match.group(1)) if rating_match else None,
#                 "source_url": res.get("url", "")
#             })
#         return hospitals

#     def _extract_source(self, url: str) -> str:
#         try:
#             parsed_url = urlparse(url)
#             return parsed_url.netloc.replace('www.', '')
#         except Exception:
#             return "Unknown Source"

#     def get_all_web_data(self, query: str) -> Dict[str, Any]:
#         logger.info(f"Running full web search pipeline for: {query}")
#         return {
#             "statistics": self.get_cancer_statistics_from_serp(query),
#             "literature": self.search_medical_literature(query),
#             "treatment_costs": self.get_treatment_costs_from_serp(query),
#             "clinical_trials": self.get_clinical_trials(query),
#             "treatment_centers": self.get_hospitals_by_location("USA"),
#             "funding_opportunities": self.get_funding_opportunities(query),
#             "hospitals_in_region": self.get_hospitals_by_location("USA")
#         }


# if __name__ == "__main__":
#     # Simple smoke test of all methods
#     agent = WebAgent()
#     condition = "breast cancer"
#     location = "Boston, MA"

#     print("\n=== Cancer Statistics ===")
#     stats = agent.get_cancer_statistics_from_serp(condition)
#     print(stats)

#     print("\n=== Medical Literature ===")
#     lit = agent.search_medical_literature(condition)
#     print(lit)

#     print("\n=== Treatment Costs ===")
#     costs = agent.get_treatment_costs_from_serp(condition)
#     print(costs)

#     print("\n=== Clinical Trials ===")
#     trials = agent.get_clinical_trials(condition)
#     print(trials)

#     print("\n=== Funding Opportunities ===")
#     funds = agent.get_funding_opportunities(condition)
#     print(funds)

#     print("\n=== Hospitals in Region ===")
#     hospitals = agent.get_hospitals_by_location(location)
#     print(hospitals)

#     print("\n=== All Web Data ===")
#     all_data = agent.get_all_web_data(condition)
#     print(all_data)













import requests
import os
import logging
import re
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, List, Any
from urllib.parse import urlparse

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebAgent:
    def __init__(self):
        load_dotenv()
        self.tavily_api_key = os.getenv('TAVILY_API_KEY')
        if not self.tavily_api_key:
            logger.error("TAVILY_API_KEY not found in environment variables")
            raise ValueError("TAVILY_API_KEY is required")
        self.session = requests.Session()
        self.tavily_endpoint = "https://api.tavily.com/search"

    def _tavily_search(self, query: str, search_depth: str = "basic", include_answer: bool = False, max_results: int = 10) -> Dict[str, Any]:
        headers = {"Content-Type": "application/json"}
        payload = {
            "api_key": self.tavily_api_key,
            "query": query,
            "search_depth": search_depth if search_depth in ["basic", "advanced"] else "advanced",
            "include_answer": include_answer,
            "max_results": max_results
        }
        try:
            response = self.session.post(self.tavily_endpoint, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error in Tavily search: {e}")
            return {"results": []}

    def get_treatment_costs_from_serp(self, query: str) -> List[Dict[str, Any]]:
        results = self._tavily_search(
            f"{query} cancer treatment costs detailed insurance coverage duration regional",
            search_depth="advanced"
        )
        return self._extract_treatment_costs(results.get('results', []))

    def get_clinical_trials(self, condition: str) -> List[Dict[str, Any]]:
        results = self._tavily_search(
            f"active clinical trials {condition} cancer treatment",
            search_depth="advanced"
        )
        return self._extract_clinical_trials(results.get('results', []))

    def get_cancer_statistics_from_serp(self, query: str = "") -> Dict[str, Any]:
        results = self._tavily_search(
            f"cancer statistics {query}",
            search_depth="advanced",
            include_answer=True
        )
        return self._extract_statistics(results.get('results', []))

    def search_medical_literature(self, query: str) -> List[Dict[str, Any]]:
        results = self._tavily_search(
            f"medical literature {query}",
            search_depth="advanced",
            include_answer=True,
            max_results=5
        )
        return self._extract_medical_literature(results.get('results', []))

    def get_funding_opportunities(self, condition: str) -> List[Dict[str, Any]]:
        results = self._tavily_search(
            f"cancer research funding opportunities for {condition}",
            search_depth="advanced",
            max_results=10
        )
        return self._extract_funding(results.get('results', []))

    def get_hospitals_by_location(self, location: str) -> List[Dict[str, Any]]:
        results = self._tavily_search(
            f"best cancer treatment centers in {location} with address and rating",
            search_depth="advanced",
            max_results=10
        )
        return self._extract_hospitals(results.get('results', []))

    def _extract_treatment_costs(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [
            {"title": r.get("title", "Unknown"), "description": r.get("content", "")[:200], "url": r.get("url", "")} 
            for r in results
        ]

    def _extract_clinical_trials(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        trials = []
        for res in results:
            title = res.get('title', '')
            content = res.get('content', '')
            phase_match = re.search(r'phase (i{1,3}|[1-3])', (title + ' ' + content).lower())
            status_match = re.search(r'(recruiting|completed|active)', content.lower())
            trials.append({
                "title": title,
                "description": content,
                "phase": phase_match.group(0).title() if phase_match else "Unknown",
                "status": status_match.group(0).title() if status_match else "Unknown",
                "source_url": res.get('url', '')
            })
        return trials

    def _extract_statistics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not results:
            return {}
        return {
            "sources": [
                {"title": r.get("title", ""), "snippet": r.get("content", "")[:200], "url": r.get("url", "")} 
                for r in results
            ]
        }

    def _extract_medical_literature(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        literature = []
        for res in results:
            literature.append({
                "title": res.get('title', 'Untitled'),
                "snippet": res.get('content', '')[:200],
                "source": self._extract_source(res.get('url', '')),
                "url": res.get('url', '')
            })
        return literature

    def _extract_funding(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [
            {"title": r.get("title", "Unknown"), "description": r.get("content", "")[:200], "source_url": r.get("url", "")} 
            for r in results
        ]

    def _extract_hospitals(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        hospitals = []
        for res in results:
            content = res.get("content", "")
            address_match = re.search(r"\d{1,5}\s+\w+[\w\s,]+", content)
            rating_match = re.search(r"(\d\.\d)\s*/\s*5", content)
            hospitals.append({
                "name": res.get("title", "Unknown"),
                "address": address_match.group(0) if address_match else "Unknown address",
                "rating": float(rating_match.group(1)) if rating_match else None,
                "source_url": res.get("url", "")
            })
        return hospitals

    def _extract_source(self, url: str) -> str:
        try:
            return urlparse(url).netloc.replace('www.', '')
        except:
            return "Unknown Source"

    def _extract_location(self, query: str) -> str:
        # Look for 'in LOCATION', 'at LOCATION', or 'near LOCATION'
        for pat in [r'in ([A-Z][\w\s,]+)', r'at ([A-Z][\w\s,]+)', r'near ([A-Z][\w\s,]+)']:
            m = re.search(pat, query)
            if m:
                return m.group(1).strip()
        return "United States"

    def get_all_web_data(self, query: str) -> Dict[str, Any]:
        logger.info(f"Running full web search pipeline for: {query}")
        loc = self._extract_location(query)
        return {
            "statistics": self.get_cancer_statistics_from_serp(query),
            "literature": self.search_medical_literature(query),
            "treatment_costs": self.get_treatment_costs_from_serp(query),
            "clinical_trials": self.get_clinical_trials(query),
            "hospitals_in_region": self.get_hospitals_by_location(loc),
        }
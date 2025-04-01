import requests
import pandas as pd
import streamlit as st
from typing import Dict, List, Optional, Any
import plotly.express as px
import plotly.graph_objects as go
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv
from datetime import datetime

class WebAgent:
    def __init__(self):
        """Initialize WebAgent with necessary APIs and endpoints"""
        load_dotenv()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Add API keys from environment variables
        self.pubmed_api_key = os.getenv('PUBMED_API_KEY')
        self.who_api_key = os.getenv('WHO_API_KEY')
        self.base_urls = {
            'pubmed': 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/',
            'who': 'https://www.who.int/data/gho/data/indicators/',
            'clinicaltrials': 'https://clinicaltrials.gov/api/'
        }

    def search_medical_literature(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search medical literature using PubMed API"""
        try:
            # Search PubMed
            search_url = f"{self.base_urls['pubmed']}esearch.fcgi"
            params = {
                'db': 'pubmed',
                'term': query,
                'retmax': max_results,
                'format': 'json',
                'api_key': self.pubmed_api_key
            }
            
            response = requests.get(search_url, params=params)
            search_results = response.json()
            
            if 'esearchresult' not in search_results:
                return []
                
            article_ids = search_results['esearchresult']['idlist']
            
            # Fetch article details
            articles = []
            for article_id in article_ids:
                article_data = self._fetch_article_details(article_id)
                if article_data:
                    articles.append(article_data)
                    
            return articles
            
        except Exception as e:
            st.error(f"Error searching medical literature: {str(e)}")
            return []

    def _fetch_article_details(self, article_id: str) -> Optional[Dict[str, Any]]:
        """Fetch detailed information for a specific article"""
        try:
            fetch_url = f"{self.base_urls['pubmed']}efetch.fcgi"
            params = {
                'db': 'pubmed',
                'id': article_id,
                'format': 'json',
                'api_key': self.pubmed_api_key
            }
            
            response = requests.get(fetch_url, params=params)
            article_data = response.json()
            
            # Extract relevant information
            return {
                'id': article_id,
                'title': article_data.get('title', ''),
                'abstract': article_data.get('abstract', ''),
                'authors': article_data.get('authors', []),
                'publication_date': article_data.get('publication_date', ''),
                'journal': article_data.get('journal', ''),
                'doi': article_data.get('doi', '')
            }
            
        except Exception as e:
            st.error(f"Error fetching article details: {str(e)}")
            return None

    def get_clinical_trials(self, condition: str, status: str = 'recruiting') -> List[Dict[str, Any]]:
        """Fetch clinical trials information"""
        try:
            url = f"{self.base_urls['clinicaltrials']}query/study_fields"
            params = {
                'expr': f"{condition} AND AREA[RecruitmentStatus]{status}",
                'fields': 'NCTId,BriefTitle,Condition,InterventionType,Phase,EnrollmentCount,StartDate,CompletionDate',
                'fmt': 'json',
                'max_rnk': 100
            }
            
            response = requests.get(url, params=params)
            trials_data = response.json()
            
            return self._process_clinical_trials(trials_data)
            
        except Exception as e:
            st.error(f"Error fetching clinical trials: {str(e)}")
            return []

    def _process_clinical_trials(self, trials_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process and structure clinical trials data"""
        processed_trials = []
        
        for trial in trials_data.get('StudyFieldsResponse', {}).get('StudyFields', []):
            processed_trials.append({
                'id': trial.get('NCTId', [''])[0],
                'title': trial.get('BriefTitle', [''])[0],
                'condition': trial.get('Condition', []),
                'intervention_type': trial.get('InterventionType', []),
                'phase': trial.get('Phase', []),
                'enrollment': trial.get('EnrollmentCount', ['0'])[0],
                'start_date': trial.get('StartDate', [''])[0],
                'completion_date': trial.get('CompletionDate', [''])[0]
            })
            
        return processed_trials

    def get_cancer_statistics(self, region: str = 'global') -> Dict[str, Any]:
        """Fetch cancer statistics from WHO database"""
        try:
            url = f"{self.base_urls['who']}cancer-mortality"
            params = {
                'region': region,
                'api_key': self.who_api_key
            }
            
            response = requests.get(url, params=params)
            stats_data = response.json()
            
            return self._process_cancer_statistics(stats_data)
            
        except Exception as e:
            st.error(f"Error fetching cancer statistics: {str(e)}")
            return {}

    def _process_cancer_statistics(self, stats_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and structure cancer statistics data"""
        processed_stats = {
            'mortality_rate': {},
            'incidence_rate': {},
            'survival_rate': {},
            'last_updated': datetime.now().isoformat()
        }
        
        # Process the raw statistics data
        # This is a placeholder for the actual data processing logic
        # You would need to adapt this based on the actual WHO API response structure
        
        return processed_stats

    def get_treatment_centers(self, location: str) -> List[Dict[str, Any]]:
        """Fetch information about cancer treatment centers"""
        try:
            # This is a placeholder for actual API integration
            # You would need to integrate with a real healthcare facility database
            centers = [
                {
                    'name': 'Example Cancer Center',
                    'location': location,
                    'specialties': ['Medical Oncology', 'Radiation Therapy'],
                    'rating': 4.5,
                    'contact': {
                        'phone': '123-456-7890',
                        'email': 'info@example.com'
                    }
                }
            ]
            
            return centers
            
        except Exception as e:
            st.error(f"Error fetching treatment centers: {str(e)}")
            return []

    def generate_visualizations(self, data: Dict[str, Any]) -> List[go.Figure]:
        """Generate visualizations from the collected data"""
        try:
            visualizations = []
            
            # Create visualizations based on available data
            if 'mortality_rate' in data:
                fig = px.line(
                    data['mortality_rate'],
                    title='Cancer Mortality Rate Over Time'
                )
                visualizations.append(fig)
                
            if 'treatment_centers' in data:
                fig = px.scatter_mapbox(
                    data['treatment_centers'],
                    title='Cancer Treatment Centers Location'
                )
                visualizations.append(fig)
                
            return visualizations
            
        except Exception as e:
            st.error(f"Error generating visualizations: {str(e)}")
            return []

    def save_data_to_cache(self, data: Dict[str, Any], cache_file: str) -> None:
        """Save fetched data to local cache"""
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            st.error(f"Error saving data to cache: {str(e)}")

    def load_data_from_cache(self, cache_file: str) -> Optional[Dict[str, Any]]:
        """Load data from local cache"""
        try:
            if os.path.exists(cache_file):
                with open(cache_file, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            st.error(f"Error loading data from cache: {str(e)}")
            return None

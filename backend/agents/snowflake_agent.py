import snowflake.connector
import pandas as pd
import streamlit as st
from typing import Dict, List, Optional, Any
import plotly.express as px
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

class SnowflakeAgent:
    def __init__(self):
        """Initialize Snowflake connection using environment variables"""
        # Load environment variables from .env file
        load_dotenv()
        self.conn = self._get_snowflake_connection()

    def _get_snowflake_connection(self):
        """Establish Snowflake connection using credentials from environment variables"""
        try:
            return snowflake.connector.connect(
                user=os.getenv('SNOWFLAKE_USER'),
                password=os.getenv('SNOWFLAKE_PASSWORD'),
                account=os.getenv('SNOWFLAKE_ACCOUNT'),
                warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
                database=os.getenv('SNOWFLAKE_DATABASE'),
                schema=os.getenv('SNOWFLAKE_SCHEMA')
            )
        except Exception as e:
            st.error(f"Error connecting to Snowflake: {str(e)}")
            return None

    def get_cancer_statistics(self) -> Dict[str, pd.DataFrame]:
        """Retrieve cancer statistics from Snowflake"""
        try:
            stats = {}
            
            # Historical Statistics
            historical_query = """
            SELECT 
                YEAR,
                SUM(NEW_CASES) as NEW_CASES,
                SUM(DEATHS) as DEATHS,
                AVG(SURVIVAL_RATE) as SURVIVAL_RATE
            FROM CANCER_STATISTICS
            WHERE YEAR BETWEEN 2015 AND 2023
            GROUP BY YEAR
            ORDER BY YEAR;
            """
            stats['historical'] = pd.read_sql(historical_query, self.conn)
            
            # Regional Statistics
            regional_query = """
            SELECT 
                REGION,
                AVG(CASES_PER_100K) as CASES_PER_100K,
                AVG(DEATH_RATE) as DEATH_RATE,
                COUNT(DISTINCT TREATMENT_CENTER_ID) as TREATMENT_CENTERS
            FROM REGIONAL_STATISTICS
            GROUP BY REGION;
            """
            stats['regional'] = pd.read_sql(regional_query, self.conn)
            
            # Cancer Type Statistics
            cancer_types_query = """
            SELECT 
                CANCER_TYPE,
                AVG(INCIDENCE_RATE) as INCIDENCE_RATE,
                AVG(MORTALITY_RATE) as MORTALITY_RATE,
                AVG(FIVE_YEAR_SURVIVAL) as FIVE_YEAR_SURVIVAL
            FROM CANCER_TYPES
            GROUP BY CANCER_TYPE;
            """
            stats['cancer_types'] = pd.read_sql(cancer_types_query, self.conn)
            
            return stats
            
        except Exception as e:
            st.error(f"Error fetching cancer statistics: {str(e)}")
            return {}

    def get_visualizations(self) -> List[go.Figure]:
        """Generate visualizations from Snowflake data"""
        try:
            visualizations = []
            
            # Time series visualization
            historical_data = self.get_cancer_statistics().get('historical')
            if historical_data is not None:
                fig1 = px.line(historical_data, 
                              x='YEAR', 
                              y=['NEW_CASES', 'DEATHS'],
                              title='Cancer Cases and Deaths Over Time')
                visualizations.append(fig1)
            
            # Regional comparison
            regional_data = self.get_cancer_statistics().get('regional')
            if regional_data is not None:
                fig2 = px.bar(regional_data,
                             x='REGION',
                             y='CASES_PER_100K',
                             title='Cancer Cases per 100,000 by Region')
                visualizations.append(fig2)
            
            return visualizations
            
        except Exception as e:
            st.error(f"Error generating visualizations: {str(e)}")
            return []

    def get_treatment_costs(self) -> Optional[pd.DataFrame]:
        """Get treatment cost analysis from Snowflake"""
        try:
            query = """
            SELECT 
                TREATMENT_TYPE,
                AVG(COST) as AVERAGE_COST,
                MIN(COST) as MIN_COST,
                MAX(COST) as MAX_COST
            FROM TREATMENT_COSTS
            GROUP BY TREATMENT_TYPE;
            """
            return pd.read_sql(query, self.conn)
        except Exception as e:
            st.error(f"Error fetching treatment costs: {str(e)}")
            return None

    def close_connection(self):
        """Close Snowflake connection"""
        if self.conn:
            self.conn.close()

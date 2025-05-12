
# import snowflake.connector
# import os
# import logging
# from dotenv import load_dotenv
# from typing import List, Dict, Any

# # Configure logging
# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# class SnowflakeAgent:
#     def __init__(self):
#         load_dotenv()

#         self.account = os.getenv('SNOWFLAKE_ACCOUNT')
#         self.user = os.getenv('SNOWFLAKE_USER')
#         self.password = os.getenv('SNOWFLAKE_PASSWORD')
#         self.warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
#         self.database = os.getenv('SNOWFLAKE_DATABASE')
#         self.schema = os.getenv('SNOWFLAKE_SCHEMA', 'cdc')

#         if not all([self.account, self.user, self.password, self.warehouse, self.database]):
#             raise ValueError("Missing Snowflake credentials")

#         try:
#             self.conn = snowflake.connector.connect(
#                 user=self.user,
#                 password=self.password,
#                 account=self.account,
#                 warehouse=self.warehouse,
#                 database=self.database,
#                 schema=self.schema
#             )
#             logger.info("✅ Connected to Snowflake")
#         except Exception as e:
#             logger.error(f"❌ Snowflake connection failed: {str(e)}")
#             raise

#     def execute_query(self, query: str) -> List[Dict[str, Any]]:
#         try:
#             with self.conn.cursor() as cur:
#                 cur.execute(query)
#                 columns = [desc[0] for desc in cur.description]
#                 results = [dict(zip(columns, row)) for row in cur.fetchall()]
#                 return results
#         except Exception as e:
#             logger.error(f"Query failed: {e}")
#             return []

#     def get_cancer_statistics(self) -> Dict[str, List[Dict[str, Any]]]:
#         try:
#             return {
#                 "by_site": self.execute_query("""
#                     SELECT 
#                         YEAR, 
#                         SEX, 
#                         SITE, 
#                         TRY_TO_NUMBER(COUNT) AS COUNT, 
#                         POPULATION, 
#                         EVENT_TYPE
#                     FROM by_site
#                     WHERE TRY_TO_NUMBER(COUNT) IS NOT NULL AND POPULATION IS NOT NULL   
#                 """),

#                 "incident": self.execute_query("""
#                     SELECT AREA, CANCERTYPE, YEAR, SEX, TYPE, CASECOUNT, POPULATION
#                     FROM CANCER_INCIDENT
#                     WHERE CASECOUNT IS NOT NULL AND POPULATION IS NOT NULL
#                 """),

#                 "mortality": self.execute_query("""
#                     SELECT SITE, YEAR
#                     FROM CANCER_MORTALITY_RATE
#                 """),

#                 "child_cases": self.execute_query("""
#                     SELECT SITE, YEAR, AGE, COUNT, POPULATION, EVENT_TYPE
#                     FROM CHILD_AGE_GROUP
#                     WHERE COUNT IS NOT NULL AND POPULATION IS NOT NULL
#                 """)
#             }
#         except Exception as e:
#             logger.error(f"❌ Failed to fetch cancer statistics: {e}")
#             return {
#                 "by_site": [],
#                 "incident": [],
#                 "mortality": [],
#                 "child_cases": []
#             }

#     def close(self):
#         if self.conn:
#             self.conn.close()
#             logger.info("✅ Snowflake connection closed")



import snowflake.connector
import os
import logging
from dotenv import load_dotenv
from typing import List, Dict, Any

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Disable Snowflake OCSP cert validation
os.environ["SF_OCSP_FAIL_OPEN"] = "true"
os.environ["SF_OCSP_RESPONSE_CACHE_SERVER_ENABLED"] = "false"
os.environ["SF_OCSP_TESTMODE"] = "true"

class SnowflakeAgent:
    def __init__(self):
        load_dotenv()

        self.account = os.getenv('SNOWFLAKE_ACCOUNT')
        self.user = os.getenv('SNOWFLAKE_USER')
        self.password = os.getenv('SNOWFLAKE_PASSWORD')
        self.warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
        self.database = os.getenv('SNOWFLAKE_DATABASE')
        self.schema = os.getenv('SNOWFLAKE_SCHEMA', 'cdc')

        if not all([self.account, self.user, self.password, self.warehouse, self.database]):
            raise ValueError("Missing Snowflake credentials")

        try:
            self.conn = snowflake.connector.connect(
                user=self.user,
                password=self.password,
                account=self.account,
                warehouse=self.warehouse,
                database=self.database,
                schema=self.schema
            )
            logger.info("✅ Connected to Snowflake")
        except Exception as e:
            logger.error(f"❌ Snowflake connection failed: {str(e)}")
            raise

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        try:
            with self.conn.cursor() as cur:
                cur.execute(query)
                columns = [desc[0] for desc in cur.description]
                results = [dict(zip(columns, row)) for row in cur.fetchall()]
                return results
        except Exception as e:
            logger.error(f"Query failed: {e}")
            return []

    def get_cancer_statistics(self) -> Dict[str, List[Dict[str, Any]]]:
        try:
            return {
                
                "by_site": self.execute_query("""
                    SELECT YEAR, SEX, SITE, COUNT, POPULATION, EVENT_TYPE
                    FROM BY_SITE
                """),

                "incident": self.execute_query("""
                    SELECT AREA, CANCERTYPE, YEAR, SEX, TYPE, CASECOUNT, POPULATION
                    FROM CANCER_INCIDENT
                    WHERE CASECOUNT IS NOT NULL AND POPULATION IS NOT NULL
                """),

                "mortality": self.execute_query("""
                    SELECT SITE, YEAR
                    FROM CANCER_MORTALITY_RATE
                """),

                "child_cases": self.execute_query("""
                    SELECT SITE, YEAR, AGE, COUNT, POPULATION, EVENT_TYPE
                    FROM CHILD_AGE_GROUP
                    WHERE COUNT IS NOT NULL AND POPULATION IS NOT NULL
                """)
            }
        except Exception as e:
            logger.error(f"❌ Failed to fetch cancer statistics: {e}")
            return {
                "by_site": [],
                "incident": [],
                "mortality": [],
                "child_cases": []
            }

    def close(self):
        if self.conn:
            self.conn.close()
            logger.info("✅ Snowflake connection closed")

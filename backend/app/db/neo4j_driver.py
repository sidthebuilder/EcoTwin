from neo4j import GraphDatabase, AsyncGraphDatabase
from app.core.config import settings
from loguru import logger
from typing import Optional
import os

class Neo4jDriver:
    """
    Enterprise-grade Singleton for Neo4j Connection.
    Uses generic driver for sync and AsyncGraphDatabase for async contexts.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Neo4jDriver, cls).__new__(cls)
            cls._instance._driver = None
        return cls._instance

    def connect(self):
        if self._driver:
            return
            
        uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "password")
        
        try:
            # We use the sync driver for simplicity in this PoC, but AsyncGraphDatabase is preferred for high load
            self._driver = GraphDatabase.driver(uri, auth=(user, password))
            # Verify connection
            self._driver.verify_connectivity()
            logger.info(f"Connected to Neo4j at {uri}")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise e

    def close(self):
        if self._driver:
            self._driver.close()
            logger.info("Neo4j connection closed.")

    def get_session(self):
        if not self._driver:
            self.connect()
        return self._driver.session()

# Global instance
neo4j_driver = Neo4jDriver()

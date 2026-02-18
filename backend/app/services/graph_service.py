from app.db.neo4j_driver import neo4j_driver
from loguru import logger
from typing import List, Dict, Any

class GraphService:
    """
    Production Graph Service interacting with Neo4j.
    Handles node creation, relationship linking, and impact propagation queries.
    """
    def __init__(self):
        self.driver = neo4j_driver

    def create_node(self, label: str, properties: Dict[str, Any]):
        """
        Creates a node in Neo4j with the given label and properties.
        SECURITY: Validates label against allowlist to prevent Cypher Injection.
        """
        ALLOWED_LABELS = {"User", "Activity", "Location", "Source"}
        if label not in ALLOWED_LABELS:
            logger.error(f"Security Alert: Attempted to use invalid node label '{label}'")
            return None

        query = (
            f"MERGE (n:{label} {{id: $id}}) "
            "SET n += $props "
            "RETURN n"
        )
        try:
            with self.driver.get_session() as session:
                result = session.run(query, id=properties.get("id"), props=properties)
                return result.single()[0]
        except Exception as e:
            logger.error(f"Graph Error (Create Node): {e}")
            return None

    def create_relationship(self, source_id: str, target_id: str, rel_type: str, weight: float = 1.0):
        """
        Creates a directed relationship between two nodes.
        SECURITY: Validates rel_type against allowlist.
        """
        ALLOWED_RELS = {"PERFORMED", "LOCATED_AT", "HAS_SOURCE", "IMPACTS"}
        if rel_type not in ALLOWED_RELS:
            logger.error(f"Security Alert: Attempted to use invalid relationship type '{rel_type}'")
            return

        query = (
            "MATCH (a), (b) "
            "WHERE a.id = $source_id AND b.id = $target_id "
            f"MERGE (a)-[r:{rel_type}]->(b) "
            "SET r.weight = $weight "
            "RETURN r"
        )
        try:
            with self.driver.get_session() as session:
                session.run(query, source_id=source_id, target_id=target_id, weight=weight)
        except Exception as e:
            logger.error(f"Graph Error (Link): {e}")

    def simulate_impact(self, start_node_id: str, delta: float) -> List[Dict[str, Any]]:
        """
        Executes a Cypher query to simulate cascading impact.
        Finds downstream nodes and calculates 'felt' impact based on edge weights.
        """
        query = (
            "MATCH (start {id: $start_id})-[r]->(downstream) "
            "RETURN downstream.id as target, labels(downstream) as label, type(r) as action, r.weight as weight"
        )
        
        impact_results = []
        try:
            with self.driver.get_session() as session:
                records = session.run(query, start_id=start_node_id)
                for record in records:
                    # Simple propagation logic: New Delta = Input Delta * Edge Weight
                    propagated_delta = delta * record["weight"]
                    impact_results.append({
                        "target": record["target"],
                        "label": record["label"][0] if record["label"] else "Unknown",
                        "action": record["action"],
                        "magnitude": propagated_delta
                    })
        except Exception as e:
            logger.error(f"Graph Error (Simulation): {e}")
        
        return impact_results

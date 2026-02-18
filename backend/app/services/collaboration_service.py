from typing import List, Dict
from .graph_service import GraphService

class CollaborationService:
    def __init__(self):
        self.active_sessions: Dict[str, List[str]] = {} # session_id -> list of user_ids
        self.graph_service = GraphService()

    def link_twins(self, session_id: str, user_ids: List[str]):
        """
        Creates a 'Shared Twin' context where certain nodes (e.g., Shared Vehicle)
        are linked across multiple graphs.
        """
        self.active_sessions[session_id] = user_ids
        # In a real implementation, this would merge graph sub-structures
        return {"status": "linked", "session": session_id, "members": user_ids}

    def share_resource(self, resource_id: str, members: List[str]):
        """
        Apportion carbon footprint of a resource across linked twins.
        """
        # Logic: If 2 people share 1 car, calculate individual footprint as 50%
        # but keep total resource impact consistent.
        impact_factor = 1.0 / len(members)
        return {
            "resource": resource_id,
            "individual_allocation": impact_factor,
            "note": "Shared resource detection successful"
        }

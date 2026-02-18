import pandas as pd
from typing import Dict, Any

class SimulationEngine:
    def __init__(self):
        # Baseline emission factors (kg CO2e per unit)
        self.factors = {
            "sedan_km": 0.2,
            "ev_km": 0.05,
            "meat_meal": 4.5,
            "veggie_meal": 1.5,
            "grid_kwh": 0.4,
            "solar_kwh": 0.02
        }

    def calculate_delta(self, baseline: Dict[str, Any], modified: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculates the carbon and resource footprint delta.
        """
        results = {
            "carbon_reduction": 0.0,
            "cost_savings": 0.0,
            "resource_efficiency": 0.0
        }
        
        # Example: Transport simulation
        if "transport" in baseline and "transport" in modified:
            b_km = baseline["transport"].get("annual_km", 10000)
            b_type = baseline["transport"].get("vehicle", "sedan")
            m_type = modified["transport"].get("vehicle", "ev")
            
            b_emissions = b_km * self.factors.get(f"{b_type}_km", 0.2)
            m_emissions = b_km * self.factors.get(f"{m_type}_km", 0.05)
            
            results["carbon_reduction"] += (b_emissions - m_emissions)
            
        # Example: Diet simulation
        if "diet" in baseline and "diet" in modified:
            b_meals = 365 * 3
            b_meat_ratio = baseline["diet"].get("meat_ratio", 0.7)
            m_meat_ratio = modified["diet"].get("meat_ratio", 0.1)
            
            b_emissions = (b_meals * b_meat_ratio * self.factors["meat_meal"]) + \
                          (b_meals * (1 - b_meat_ratio) * self.factors["veggie_meal"])
            m_emissions = (b_meals * m_meat_ratio * self.factors["meat_meal"]) + \
                          (b_meals * (1 - m_meat_ratio) * self.factors["veggie_meal"])
            
            results["carbon_reduction"] += (b_emissions - m_emissions)

        return results

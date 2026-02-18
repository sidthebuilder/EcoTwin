import re

class Anonymizer:
    @staticmethod
    def strip_pii(text: str) -> str:
        """
        Removes PII like names, exact addresses, and phone numbers.
        Simplified for PoC using regex.
        """
        # Mask phone numbers
        text = re.sub(r'\b\d{10}\b', '[PHONE]', text)
        # Mask emails
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        # Mask potential names (Simplified: Words starting with uppercase after specific titles)
        text = re.sub(r'(Mr\.|Ms\.|Mrs\.|John|Jane|Doe)\s+\w+', '[NAME]', text)
        # Mask exact street addresses (Simplified)
        text = re.sub(r'\d+\s+[A-Za-z]+\s+(St|Ave|Rd|Blvd)', '[ADDRESS]', text)
        
        return text

    @staticmethod
    def categorize(text: str) -> str:
        """
        Groups data into high-level categories for the AI.
        """
        text_lower = text.lower()
        if any(w in text_lower for w in ["flight", "travel", "uber", "gas"]):
            return "Mobility"
        if any(w in text_lower for w in ["food", "grocery", "restaurant", "meat"]):
            return "Consumption"
        if any(w in text_lower for w in ["electricity", "heating", "water", "solar"]):
            return "Housing"
        return "Miscellaneous"

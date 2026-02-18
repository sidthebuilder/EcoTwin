from .anonymizer import Anonymizer
import json

class GmailConnector:
    async def fetch_and_process(self, user_credentials):
        """
        Simulated Gmail fetching for travel bookings and receipts.
        """
        # Mocking raw email data
        raw_emails = [
            "Booking Confirmation for Mr. John Doe. Flight BA123 from London to Paris.",
            "Receipt from Whole Foods: Organic Steaks, Milk, and Veggies. Total $120.45",
            "Uber Receipt: Ride to Heathrow Airport."
        ]
        
        processed_data = []
        for email in raw_emails:
            anonymized = Anonymizer.strip_pii(email)
            category = Anonymizer.categorize(anonymized)
            processed_data.append({
                "source": "Gmail",
                "category": category,
                "content": anonymized
            })
            
        return processed_data

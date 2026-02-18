"""
EcoTwin - AI Inference Engine
-----------------------------
This module is the 'brain' of the Digital Twin. It translates messy, real-world
data (emails, logs, CSVs) into structured Activity nodes for our graph.

Developer Note: We're using LangChain for the heavy lifting, but keep an eye on 
token costs. I've added a fallback to basic heuristics if the LLM is flaky.
"""

from typing import Dict, Any, Optional
import os
from loguru import logger
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .anonymizer import Anonymizer

class InferenceEngine:
    def __init__(self, api_key: Optional[str] = None):
        # We prefer an explicit key, but fallback to environment vars
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key:
            logger.warning("No Google API Key found. Inference engine will run in 'Offline Heuristic' mode.")
            self.llm = None
        else:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-pro", 
                google_api_key=self.api_key,
                temperature=0.2 # Keep it creative but grounded
            )

        # Define what we want back from the AI
        # Human touch: We add 'confidence_reasoning' to help debug AI logic in the UI later
        self.response_schemas = [
            ResponseSchema(name="activity_type", description="Category: Travel, Food, Housing, or Lifestyle"),
            ResponseSchema(name="description", description="Plain English summary of what happened"),
            ResponseSchema(name="carbon_estimate", description="ESTIMATED kg CO2e", type="float"),
            ResponseSchema(name="confidence", description="0 to 1 score", type="float"),
            ResponseSchema(name="reasoning", description="Short explanation for why the AI picked these numbers")
        ]
        self.output_parser = StructuredOutputParser.from_response_schemas(self.response_schemas)

    @retry(
        stop=stop_after_attempt(3), 
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def run_inference(self, raw_blob: str) -> Dict[str, Any]:
        """
        Main entry point for processing data. 
        Sanitize -> Infer -> Parse -> Return.
        """
        # Step 1: Privacy First. 
        # Scrub names/emails before it ever touches the cloud.
        clean_text = Anonymizer.strip_pii(raw_blob)
        logger.info(f"Processing inference for blob: {clean_text[:50]}...")

        # Step 2: Fallback Logic
        if not self.llm:
            return self._heuristic_fallback(clean_text)

        # Step 3: Prompt Engineering
        # We want the AI to act like an environmental scientist.
        prompt = ChatPromptTemplate.from_template(
            "SYSTEM: You are the EcoTwin Lifestyle Modeler.\n"
            "CONTEXT: A user just provided raw data from a source (like an email).\n"
            "TASK: Create a carbon-aware activity log entry.\n"
            "DATA: {data}\n\n"
            "INSTRUCTIONS: {format_instructions}"
        )

        try:
            formatted_input = prompt.format_messages(
                data=clean_text,
                format_instructions=self.output_parser.get_format_instructions()
            )
            
            response = await self.llm.ainvoke(formatted_input)
            structured_data = self.output_parser.parse(response.content)
            
            # Add a 'source' flag so the UI knows this was 'Premium' inference
            structured_data["inference_method"] = "llm_gemini"
            return structured_data

        except Exception as e:
            logger.error(f"LLM Inference failed: {e}. Falling back to basic matching.")
            return self._heuristic_fallback(clean_text)

    def _heuristic_fallback(self, text: str) -> Dict[str, Any]:
        """
        Safety net logic. If the AI is down, we don't want the user's dashboard to break.
        """
        text = text.lower()
        # Basic patterns for common stuff
        if "flight" in text or "airport" in text:
            return {
                "activity_type": "Travel",
                "description": "Likely air travel (estimated)",
                "carbon_estimate": 250.0,
                "confidence": 0.6,
                "reasoning": "Keyword match: flight/airport",
                "inference_method": "heuristic_fallback"
            }
        
        return {
            "activity_type": "General",
            "description": "Activity detected from logs",
            "carbon_estimate": 1.2,
            "confidence": 0.3,
            "reasoning": "Default fallback",
            "inference_method": "heuristic_fallback"
        }

"""
This module implements the IAService class for AI interactions.
"""

import json
from typing import Dict, Any, Optional

from config.aws_bedrock import AWSBedrockService
from utils.prompt_builder import PromptBuilder
from config.logging import logger


class IAService:
    """
    Service for interacting with AI models and processing their responses.
    """

    def __init__(self):
        """Initialize the IAService with a PromptBuilder."""
        self.prompt_builder = PromptBuilder()

    def build_prompt(self, action_type: str, data: Dict[str, Any]) -> str:
        """
        Build a prompt for the AI model.

        Args:
            action_type: The type of action ("register", "update_quantity", or "update_delivery_date").
            data: The domain data to include in the prompt.

        Returns:
            str: The complete prompt.
        """
        return self.prompt_builder.build(action_type, data)

    async def call(self, prompt: str, model_id: Optional[str] = None, temperature: float = 0.4) -> str:
        """
        Call the AWS Bedrock client with the given prompt.

        Args:
            prompt: The prompt to send to the AI model.
            model_id: Optional custom model ID for fine-tuned models.
            temperature: Optional temperature parameter for model inference.

        Returns:
            str: The AI model's response.
        """
        try:
            # Call AWS Bedrock service with optional custom model
            response = AWSBedrockService.invoke_model(
                prompt=prompt,
                model_id=model_id,
                temperature=temperature
            )
            return response
        except Exception as e:
            logger.error(f"Error calling AI service: {str(e)}")
            return ""

    def parse_response(self, response: str) -> Optional[Dict[str, Any]]:
        """
        Parse the text output from the AI model into a JSON object.

        Args:
            response: The text response from the AI model.

        Returns:
            Optional[Dict[str, Any]]: The parsed JSON object, or None if parsing fails.
        """
        try:
            # Extract JSON from the response
            # First, try to parse the entire response as JSON
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                # If that fails, try to extract JSON from the text
                # Look for JSON-like patterns (starting with { and ending with })
                start_idx = response.find("{")
                end_idx = response.rfind("}")

                if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                    json_str = response[start_idx : end_idx + 1]
                    return json.loads(json_str)

                # If no JSON-like pattern is found, return None
                logger.error(f"Failed to extract JSON from response: {response}")
                return None
        except Exception as e:
            logger.error(f"Error parsing AI response: {str(e)}")
            return None
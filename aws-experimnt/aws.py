import os
import json
import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AWSBedrockService:
    """AWS Bedrock service configuration."""

    client = None

    @classmethod
    def configure(cls):
        """Configure AWS Bedrock client."""
        cls.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    @classmethod
    def get_client(cls):
        """Get AWS Bedrock client."""
        if cls.client is None:
            cls.configure()
        return cls.client

    @classmethod
    def invoke_model(cls, prompt, model_id=None, temperature=0.4):
        """
        Invoke the Bedrock model with a prompt.

        Args:
            prompt (str): The input text to send to the model
            model_id (str, optional): The ID of the model to use. If None, uses the default model from env vars.
                For fine-tuned models, use the full model ID provided by Bedrock.
            temperature (float, optional): Controls randomness in the output. Defaults to 0.4.
                Higher values (e.g., 0.8) make output more random, lower values make it more deterministic.

        Returns:
            str: The model's response text
        """
        client = cls.get_client()

        # Use environment variable for model ID if not specified
        if model_id is None:
            model_id = os.getenv("BEDROCK_MODEL_ID", "amazon.nova-pro-v1:0")

        # Prepare the request body
        body = json.dumps(
            {
                "messages": [{"role": "user", "content": [{"text": prompt}]}],
                "inferenceConfig": {"temperature": temperature},
            }
        )

        try:
            response = client.invoke_model(
                modelId=model_id,
                body=body,
                contentType="application/json",
                accept="application/json",
            )

            # Parse and return the response
            response_body = json.loads(response.get("body").read())
            return response_body["output"]["message"]["content"][0]["text"]
        except Exception as e:
            raise Exception(f"Error invoking Bedrock model {model_id}: {str(e)}")
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
    def invoke_model(cls, prompt, model_id="amazon.nova-pro-v1:0"):
        """
        Invoke the Bedrock model with a prompt.
        """
        client = cls.get_client()
        body = json.dumps(
            {
                "messages": [{"role": "user", "content": [prompt]}],
                "inferenceConfig": {"temperature": 0.4},
            }
        )

        response = client.invoke_model(
            modelId=model_id,
            body=body,
            contentType="application/json",
            accept="application/json",
        )

        # Parse and return the response
        response_body = json.loads(response.get("body").read())
        return response_body["output"]["message"]["content"][0]["text"]

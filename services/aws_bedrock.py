"""
AWS Bedrock service configuration.
This file contains configuration for AWS Bedrock service.
"""

import boto3
import os
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
            'bedrock-runtime',
            region_name=os.getenv('AWS_REGION', 'us-east-1'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        
    @classmethod
    def get_client(cls):
        """Get AWS Bedrock client."""
        if cls.client is None:
            cls.configure()
        return cls.client
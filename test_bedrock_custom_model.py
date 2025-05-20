"""
Example script demonstrating how to use a fine-tuned Amazon Bedrock model.
"""

import os
from dotenv import load_dotenv
from config.aws_bedrock import AWSBedrockService

# Load environment variables
load_dotenv()

def test_custom_model():
    """Test the custom fine-tuned model."""
    
    # Get the custom model ID from environment variable
    custom_model_id = os.getenv("CUSTOM_MODEL_ID")
    if not custom_model_id:
        raise ValueError("Please set CUSTOM_MODEL_ID environment variable to your fine-tuned model ID")

    # Example prompt - adjust based on your model's training
    test_prompt = "Your test prompt here"

    try:
        # Initialize the Bedrock service
        response = AWSBedrockService.invoke_model(
            prompt=test_prompt,
            model_id=custom_model_id,
            temperature=0.4  # Adjust temperature as needed
        )
        
        print(f"Prompt: {test_prompt}")
        print(f"Response: {response}")
        return response
        
    except Exception as e:
        print(f"Error testing custom model: {str(e)}")
        return None

if __name__ == "__main__":
    test_custom_model()
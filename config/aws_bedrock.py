import boto3
import json
from typing import Dict, Any, Optional


def initialize_bedrock_client():
    """
    Initialize and return a Bedrock client
    """
    bedrock_client = boto3.client(
        service_name='bedrock-runtime',
        region_name='us-east-1'
    )
    return bedrock_client


def invoke_bedrock_model(client, prompt: Dict[str, Any], model_id: str = "amazon.nova-pro-v1:0", temperature: float = 0.3) -> str:
    """
    Invoke the Bedrock model with a structured prompt
    
    Args:
        client: The Bedrock client
        prompt: A dictionary containing the prompt data
        model_id: The ID of the model to use
        temperature: The temperature parameter for the model
        
    Returns:
        str: The model's response text
    """
    # Convert the prompt to a format suitable for the model
    # If prompt is already a string, use it directly
    if isinstance(prompt, str):
        prompt_content = prompt
    else:
        # If it's a dictionary, convert it to a string representation
        prompt_content = json.dumps(prompt)
    
    body = json.dumps({
        "messages": [
            {"role": "user", "content": [{"text": prompt_content}]}
        ],
        "inferenceConfig": {
            "temperature": temperature
        },
    })

    response = client.invoke_model(
        modelId=model_id,
        body=body,
        contentType='application/json',
        accept='application/json'
    )

    # Parse and return the response
    response_body = json.loads(response.get('body').read())
    return response_body['output']['message']['content'][0]['text']
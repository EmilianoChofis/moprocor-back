# Using Custom Fine-tuned Bedrock Models

This guide explains how to use your fine-tuned Amazon Bedrock model with this codebase.

## Configuration

1. Set up your environment variables in a `.env` file:

```env
AWS_REGION=your-aws-region
CUSTOM_MODEL_ID=your-fine-tuned-model-id
```

2. Make sure you have the proper AWS IAM permissions configured for Bedrock access.

## Using the Custom Model

There are two ways to use your fine-tuned model:

### 1. Direct Usage via AWSBedrockService

```python
from config.aws_bedrock import AWSBedrockService

# Use your custom model
response = AWSBedrockService.invoke_model(
    prompt="Your prompt here",
    model_id="your-fine-tuned-model-id",
    temperature=0.4  # Optional: adjust as needed
)
```

### 2. Using the IAService Class

```python
from services.ia_service import IAService

ia_service = IAService()
response = await ia_service.call(
    prompt="Your prompt here",
    model_id="your-fine-tuned-model-id"  # Will use CUSTOM_MODEL_ID from env if not specified
)
```

## Testing

1. Run the example test script:
```bash
python test_bedrock_custom_model.py
```

2. The script will use your custom model ID from the environment variables and run a test prompt.

## Error Handling

The code includes proper error handling for:
- Missing model ID
- API invocation errors
- Response parsing errors

## Best Practices

1. Always store your model ID in environment variables, not in code
2. Test with different temperature values to find the optimal setting
3. Monitor your model's performance and costs
4. Keep your AWS credentials secure and use IAM roles when possible

## Troubleshooting

If you encounter issues:

1. Verify your AWS credentials are properly configured
2. Check that your model ID is correct
3. Ensure you have the necessary IAM permissions
4. Check the AWS Bedrock console for model status
5. Review the error messages in the logs
import os
import json
import boto3


class BedrockClient:
    def __init__(self, region: str | None = None, model_id: str | None = None, client=None):
        self.region = region or os.getenv("AWS_REGION", "us-east-1")
        self.model_id = model_id or os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")
        self.client = client or boto3.client("bedrock-runtime", region_name=self.region)


def chat(self, message: str) -> str:
    body = {
    "messages": [{"role": "user", "content": message}],
    "max_tokens": 500,
    "anthropic_version": "bedrock-2023-05-31",
    }
    resp = self.client.invoke_model(
    modelId=self.model_id,
    body=json.dumps(body),
    contentType="application/json",
    accept="application/json",
    )
    data = json.loads(resp["body"].read())
    return data["content"][0]["text"]


# FastAPI DI helper


def get_client() -> BedrockClient:
    return BedrockClient()
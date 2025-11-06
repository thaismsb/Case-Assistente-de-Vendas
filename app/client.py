import os
import json
import boto3

class BedrockClient:
    def __init__(self, region: str | None = None, model_id: str | None = None, client=None):
        self.region = region or os.getenv("AWS_REGION", "us-east-1")
        self.model_id = model_id or os.getenv(
            "BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0"
        )
        self.system_prompt = os.getenv(
            "SYSTEM_PROMPT",
            "Você é um assistente virtual de vendas especializado em e-commerce do setor pet, representando uma empresa completa que oferece produtos e serviços para pets. Seu objetivo é ajudar os clientes a encontrar os melhores produtos para seus animais, aumentar as conversões e fortalecer o relacionamento com a marca."
        )
        self.client = client or boto3.client("bedrock-runtime", region_name=self.region)

    def chat(self, text: str) -> str:
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "system": self.system_prompt,  
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": text}  #
                    ],
                }
            ],
            "max_tokens": 500,
        }
        resp = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json",
        )
        data = json.loads(resp["body"].read())
        return data["content"][0]["text"]


def get_bedrock_client() -> BedrockClient:
    return BedrockClient()

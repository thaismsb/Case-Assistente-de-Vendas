# tests/test_app.py
from fastapi.testclient import TestClient
from app.main import app
import app.routes as routes  # vamos monkeypatchar a factory aqui

class FakeClient:
    def chat(self, text: str) -> str:
        return f"eco: {text}"

def fake_factory() -> FakeClient:
    return FakeClient()

# substitui a factory usada pela rota /api/question-and-answer
routes.get_bedrock_client = fake_factory

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_chat():
    r = client.post("/api/question-and-answer", json={"message": "hello"})
    assert r.status_code == 200
    assert r.json()["resposta"] == "eco: hello"

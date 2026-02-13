import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"   # MUST match `ollama list`

def generate_answer(context: str, question: str) -> str:
    prompt = f"""
You are a document assistant.

Answer ONLY using the document below.
If the answer is not present, say:
"Answer not found in the document."

Document:
{context}

Question:
{question}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    if "response" in data:
        return data["response"]

    return str(data)

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def generate_answer(context: str, question: str) -> str:
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
        http_options={"api_version": "v1"}
    )

    prompt = f"""
You are a document assistant.

Answer ONLY from the document.
If the answer is not present, say:
"Answer not found in the document."

Document:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model="models/gemini-1.5-pro-002",
        contents=prompt
    )

    return response.text.strip()


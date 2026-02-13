import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(context: str, question: str) -> str:
    """
    Generates a grounded answer using OpenAI
    """
    prompt = f"""
You are a document assistant.
Answer ONLY using the information in the document below.
If the answer is not present, say "Answer not found in the document."

Document:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You answer strictly from the document."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()

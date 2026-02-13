from fastapi import APIRouter, UploadFile, File
from transformers import pipeline
from pypdf import PdfReader
import io

from app.utils.text_cleaner import clean_text

router = APIRouter()

# Load sentiment model once
sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

@router.post("/sentiment/")
async def analyze_sentiment(file: UploadFile = File(...)):
    contents = await file.read()
    reader = PdfReader(io.BytesIO(contents))

    raw_text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            raw_text += extracted

    cleaned_text = clean_text(raw_text)

    # Split text into smaller chunks
    chunk_size = 500
    chunks = [
        cleaned_text[i:i + chunk_size]
        for i in range(0, len(cleaned_text), chunk_size)
    ]

    positive = 0
    negative = 0

    for chunk in chunks:
        result = sentiment_model(chunk[:512])[0]
        if result["label"] == "POSITIVE":
            positive += 1
        else:
            negative += 1

    overall_sentiment = "POSITIVE" if positive >= negative else "NEGATIVE"

    return {
        "overall_sentiment": overall_sentiment,
        "positive_chunks": positive,
        "negative_chunks": negative,
        "total_chunks": len(chunks)
    }

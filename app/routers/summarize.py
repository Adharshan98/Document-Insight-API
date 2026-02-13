from fastapi import APIRouter, UploadFile, File
from transformers import pipeline
from pypdf import PdfReader
import io

from app.utils.text_cleaner import clean_text

router = APIRouter()

# Load summarization model (loads once)
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

@router.post("/summary/")
async def summarize_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    reader = PdfReader(io.BytesIO(contents))

    raw_text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            raw_text += extracted

    cleaned_text = clean_text(raw_text)

    # Limit text length to avoid model crash
    cleaned_text = cleaned_text[:2000]

    summary = summarizer(
        cleaned_text,
        max_length=150,
        min_length=50,
        do_sample=False
    )

    return {
        "summary": summary[0]["summary_text"]
    }

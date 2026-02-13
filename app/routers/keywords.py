from fastapi import APIRouter, UploadFile, File
from pypdf import PdfReader
import io
import re
from collections import Counter
import nltk

from app.utils.text_cleaner import clean_text

# Download stopwords once
nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords

router = APIRouter()

@router.post("/keywords/")
async def extract_keywords(file: UploadFile = File(...), top_k: int = 10):
    contents = await file.read()
    reader = PdfReader(io.BytesIO(contents))

    raw_text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            raw_text += extracted

    cleaned_text = clean_text(raw_text).lower()

    # Tokenize words
    words = re.findall(r"\b[a-zA-Z]{3,}\b", cleaned_text)

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    filtered_words = [w for w in words if w not in stop_words]

    # Count word frequency
    word_freq = Counter(filtered_words)

    # Get top keywords
    keywords = [word for word, _ in word_freq.most_common(top_k)]

    return {
        "keywords": keywords
    }

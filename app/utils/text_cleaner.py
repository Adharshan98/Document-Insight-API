import re

def clean_text(text: str) -> str:
    """
    Cleans raw extracted PDF text for NLP processing
    """
    if not text:
        return ""

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    # Remove unwanted characters (optional)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    return text.strip()

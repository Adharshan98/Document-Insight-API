from fastapi import APIRouter, UploadFile, File, Form
from app.utils.pdf_reader import extract_text_from_pdf
from app.utils.chunker import chunk_text
from app.utils.ollama_client import generate_answer

router = APIRouter()

@router.post("/qa/")
async def document_qa(
    file: UploadFile = File(...),
    question: str = Form(...)
):
    text = extract_text_from_pdf(file.file)
    chunks = chunk_text(text)

    context = " ".join(chunks[:3])  # use first 3 chunks
    answer = generate_answer(context, question)

    return {
        "question": question,
        "answer": answer,
        "chunks_used": len(chunks[:3])
    }


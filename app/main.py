from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.qa import router as qa_router

app = FastAPI(title="Document Insight API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(qa_router)

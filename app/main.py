from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from extractor import extract_text_from_url
import uvicorn
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Text Extractor API starting up...")
    yield
    logger.info("Text Extractor API shutting down...")

class FileExtractRequest(BaseModel):
    fileUrl: str

app = FastAPI(
    title="Text Extractor API",
    description="Extracts text from PDF and DOCX files via URL",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status")
def get_status():
    logger.info("Status check called")
    return {
        "status": "ok",
        "message": "Text Extractor API is alive and kicking!",
        "version": "1.0.0",
    }

@app.post("/extract")
async def extract_text(request: FileExtractRequest):
    try:
        text = extract_text_from_url(request.fileUrl)
        if not text:
            raise HTTPException(status_code=400, detail="Unsupported file type or empty file.")
        return {"text": text, "character_count": len(text)}
    except ValueError as ve:
        logger.error(str(ve))
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.exception(f"Unexpected extraction failure: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error.")


if __name__ == "__main__":
    # This allows running the app directly for debugging
    import os
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting FastAPI server in debug mode on port {port}...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )

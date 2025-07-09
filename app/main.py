from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from extractor import extract_pdf_text_from_url
import uvicorn
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("PDF Extractor API starting up...")
    yield
    # Shutdown
    logger.info("PDF Extractor API shutting down...")

class FileURLRequest(BaseModel):
    fileUrl: str

app = FastAPI(
    title="PDF Text Extractor API",
    description="API for extracting text from PDF files via URL",
    version="1.0.0",
    lifespan=lifespan
)

# CORS config (adjust origins for security in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your Vercel domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status")
def get_status():
    logger.info("Status endpoint called")
    return {
        "status": "ok",
        "message": "PDF Extractor API is alive and kicking!",
        "version": "1.0.0"
    }
    
@app.post("/extract")
async def extract_text(req: FileURLRequest):
    logger.info(f"Extracting text from URL: {req.fileUrl}")
    try:
        text = extract_pdf_text_from_url(req.fileUrl)
        if text is None:
            logger.error(f"Failed to extract text from {req.fileUrl}")
            raise HTTPException(status_code=400, detail="PDF extraction failed")
        
        logger.info(f"Successfully extracted {len(text)} characters from PDF")
        return {"pdfText": text, "character_count": len(text)}
    except Exception as e:
        logger.error(f"Error during extraction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

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

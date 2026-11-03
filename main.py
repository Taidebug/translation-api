from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from transformers import pipeline


MODEL_NAME = "Helsinki-NLP/opus-mt-en-vi"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading the translation model...")

    app.state.translator = pipeline(
        "translation",
        model=MODEL_NAME,
        device=-1,  # Run on CPU
    )

    print("The model is ready!")
    yield

    app.state.translator = None


app = FastAPI(
    title="English to Vietnamese Translation API",
    description="Translate English text into Vietnamese.",
    version="1.0.0",
    lifespan=lifespan,
)


class TranslationRequest(BaseModel):
    text: str = Field(strict=True, min_length=1, max_length=500)

    @field_validator("text")
    @classmethod
    def check_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Text must not be empty or whitespace only.")

        return value


@app.get("/")
def home():
    return {
        "message": "Welcome to the English to Vietnamese Translation API",
        "model": MODEL_NAME,
        "docs": "/docs",
    }


@app.get("/health")
def health():
    ready = getattr(app.state, "translator", None) is not None

    if not ready:
        raise HTTPException(
            status_code=503,
            detail="The model is not ready.",
        )

    return {
        "status": "ok",
        "model_ready": True,
    }


@app.post("/predict")
def predict(data: TranslationRequest):
    translator = getattr(app.state, "translator", None)

    if translator is None:
        raise HTTPException(
            status_code=503,
            detail="The model is not ready.",
        )

    try:
        result = translator(data.text, max_new_tokens=256)

        return {
            "input": data.text,
            "translation": result[0]["translation_text"],
            "model": MODEL_NAME,
        }

    except Exception as error:
        print(f"Translation error: {error}")

        raise HTTPException(
            status_code=500,
            detail="Unable to translate the text. Please try again.",
        ) from error
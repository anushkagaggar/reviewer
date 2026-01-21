from fastapi import APIRouter
from app.schemas.input_schema import ReviewInput
from app.schemas.output_schema import ReviewOutput
from app.core.llm import LocalLLM
from pathlib import Path
import json

router = APIRouter()

PROMPT_PATH = Path("prompts/reviewer_v1.txt")
MODEL_PATH = "models/mistral-7b-instruct-q4.gguf"

llm = LocalLLM(MODEL_PATH)


@router.post("/review", response_model=ReviewOutput)
def review_design(payload: ReviewInput):
    system_prompt = PROMPT_PATH.read_text()

    user_input = payload.model_dump_json(indent=2)

    raw_output = llm.generate(system_prompt, user_input)
    print("\n===== RAW MODEL OUTPUT =====\n", raw_output)

    # Intentionally fragile
    parsed = json.loads(raw_output)

    return parsed

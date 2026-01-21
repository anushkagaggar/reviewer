from fastapi import APIRouter
from app.schemas.input_schema import ReviewInput
from app.schemas.output_schema import ReviewOutput

router = APIRouter()


@router.post("/review", response_model=ReviewOutput)
def review_design(payload: ReviewInput):
    return {
        "overall_assessment": {
            "verdict": "RISKY",
            "confidence_level": "LOW",
            "summary": "This is a placeholder review generated without LLM reasoning."
        },
        "critical_issues": [],
        "moderate_issues": [],
        "assumptions_detected": payload.assumptions,
        "missing_information": ["Embedding model not specified"],
        "questions_for_author": ["How is retrieval quality evaluated?"],
        "phase_1_limitations": [
            "LLM reasoning not yet integrated",
            "No grounding or retrieval validation"
        ]
    }

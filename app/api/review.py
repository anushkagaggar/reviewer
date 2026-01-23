from fastapi import APIRouter
from app.schemas.input_schema import ReviewInput
from app.schemas.output_schema import ReviewOutput
from app.core.llm import LocalLLM
from pathlib import Path
import json
from copy import deepcopy
from app.core.review_template import REVIEW_TEMPLATE
from fastapi import HTTPException
from app.core.retriever import SimpleRetriever
from app.core.normalizer import normalize_list
from app.core.memory import MemoryManager
from app.core.memory_formatter import format_memory

memory = MemoryManager()

router = APIRouter()

PROMPT_PATH = Path("prompts/reviewer_v1.txt")
MODEL_PATH = "models/mistral-7b-instruct-q4.gguf"

llm = LocalLLM(MODEL_PATH)
retriever = SimpleRetriever("knowledge_base")


@router.post("/review", response_model=ReviewOutput)
def review_design(payload: ReviewInput):
    system_prompt = PROMPT_PATH.read_text()
    user_input = payload.model_dump_json(indent=2)

    retrieved_docs = retriever.retrieve(payload.problem_statement)

    context_blocks = []

    for doc in retrieved_docs:
        block = f"[Source: {doc['source']}]\n{doc['content']}"
        context_blocks.append(block)

    grounding_context = "\n\n".join(context_blocks)
    stm_history = memory.get_stm(
    payload.system_name,
    payload.version
    )

    ltm_history = memory.get_ltm(
        payload.system_name,
        payload.version
    )

    memory_summary = format_memory(stm_history, ltm_history)

    full_prompt = f"""
    {system_prompt}

    You are reviewing a new version of an existing system.

    You MUST compare this version with past reviews.

    If issues are unresolved, mark them as recurring.
    If issues are fixed, acknowledge improvement.
    If regressions appear, highlight them.

    PAST REVIEW SUMMARY:
    {memory_summary}

    REFERENCE MATERIAL:
    {grounding_context}

    USER INPUT:
    {user_input}
    """

    raw_output = llm.generate(full_prompt, "")

    print("\n===== RAW MODEL OUTPUT =====\n", raw_output)
    with open("logs/raw_llm_outputs_versioning.txt", "a", encoding="utf-8") as f:
        f.write("\n\n==== NEW OUTPUT ====\n")
        f.write(raw_output)

    # Intentionally fragile
    try:
        model_response = json.loads(raw_output)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Model did not return valid JSON"
        )

    # Merge model response into template
    result = deepcopy(REVIEW_TEMPLATE)

    result["overall_assessment"] = model_response.get(
    "overall_assessment",
    result["overall_assessment"])

    result["critical_issues"] = normalize_list(
        model_response.get("critical_issues", []),
        "Critical Issue"
    )

    result["moderate_issues"] = normalize_list(
        model_response.get("moderate_issues", []),
        "Moderate Issue"
    )

    result["assumptions_detected"] = normalize_list(
        model_response.get("assumptions_detected", []),
        "Assumption"
    )

    result["missing_information"] = normalize_list(
        model_response.get("missing_information", []),
        "Missing Information"
    )

    result["questions_for_author"] = model_response.get(
        "questions_for_author",
        []
    )

    result["phase_1_limitations"] = model_response.get(
        "phase_1_limitations",
        []
    )

    # Extract issue titles for memory
    issues = []

    for section in ["critical_issues", "moderate_issues", "assumptions_detected", "missing_information"]:
        for item in result.get(section, []):
            title = item.get("title")
            if title:
                issues.append(title)

    # Update memories
    memory.update_stm(
        payload.system_name,
        payload.version,
        issues
    )

    memory.update_ltm(
        payload.system_name,
        payload.version,
        issues
    )

    return result
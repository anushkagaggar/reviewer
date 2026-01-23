from pydantic import BaseModel, Field
from typing import List


class LLMUsage(BaseModel):
    model_name: str
    context_window: str
    temperature: float


class Constraints(BaseModel):
    latency_target_ms: int
    cost_target_usd_per_month: float
    deployment_environment: str


class ReviewInput(BaseModel):
    system_name: str = Field(..., description="Unique project/system name")
    version: str = Field(..., description="Design version (e.g., v1, v2, v3)")

    problem_statement: str
    architecture_description: str

    llm_usage: LLMUsage

    retrieval_description: str
    assumptions: List[str]

    constraints: Constraints
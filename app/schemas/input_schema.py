from pydantic import BaseModel
from typing import List


class LLMUsage(BaseModel):
    model_name: str
    context_window: str
    temperature: float


class Constraints(BaseModel):
    latency_target_ms: int
    cost_target_usd_per_month: int
    deployment_environment: str


class ReviewInput(BaseModel):
    system_name: str
    problem_statement: str
    architecture_description: str
    llm_usage: LLMUsage
    retrieval_description: str
    assumptions: List[str]
    constraints: Constraints

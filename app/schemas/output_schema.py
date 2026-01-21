from pydantic import BaseModel
from typing import List


class Assessment(BaseModel):
    verdict: str
    confidence_level: str
    summary: str


class Issue(BaseModel):
    issue: str
    severity: str
    reasoning: str
    suggested_fix: str
    impact: str | None = None


class ReviewOutput(BaseModel):
    overall_assessment: Assessment
    critical_issues: List[Issue]
    moderate_issues: List[Issue]
    assumptions_detected: List[str]
    missing_information: List[str]
    questions_for_author: List[str]
    phase_1_limitations: List[str]

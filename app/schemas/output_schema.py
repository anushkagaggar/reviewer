from pydantic import BaseModel
from typing import List, Optional, Union, Any


class AssumptionDetail(BaseModel):
    assumption: str
    impact: str
    suggestion: str


class MissingInfoDetail(BaseModel):
    information: str
    description: str



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
    critical_issues: List[Any]
    moderate_issues: List[Any]
    assumptions_detected: List[Union[str, AssumptionDetail, dict]]
    missing_information: List[Union[str, MissingInfoDetail, dict]]
    questions_for_author: List[str]
    phase_1_limitations: List[str]

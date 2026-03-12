from pydantic import BaseModel


class CodingAlternative(BaseModel):
    job_number: str | None = None
    cost_code: str | None = None
    confidence: float
    reasoning: str


class CodingPrediction(BaseModel):
    predicted_job_number: str | None = None
    predicted_cost_code: str | None = None
    confidence: float
    method: str  # po_match, job_reference, vendor_history, material_analysis, manual_required
    reasoning: str
    alternatives: list[CodingAlternative] = []

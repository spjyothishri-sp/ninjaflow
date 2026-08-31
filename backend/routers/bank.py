from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class BankRequest(BaseModel):
    entity_id: int
    amount: float
    duration_days: int


@router.post("/bank/check-eligibility")
def check_eligibility(request: BankRequest):
    """
    Simulated Bank/NBFC eligibility check.

    NOTE:
    This is NOT a real banking API.
    It is only for the NinjaFlow hackathon demo.
    """

    # Simulated bank eligibility rule
    # For demo purposes, requests up to ₹5,00,000 are eligible.
    eligible = request.amount <= 1000000

    # Interest rate based on duration
    if request.duration_days <= 15:
        interest_rate = 12.5
    else:
        interest_rate = 14.0

    # Simulated approved amount
    if eligible:
        approved_amount = request.amount
    else:
        approved_amount = request.amount * 0.7

    return {
        "entity_id": request.entity_id,
        "eligible": eligible,
        "approved_amount": approved_amount,
        "interest_rate": interest_rate,
        "duration_days": request.duration_days,
        "status": "OFFERED",
        "message": "Simulated Bank/NBFC offer — Demo Only"
    }
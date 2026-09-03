from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.bank_service import check_bank_eligibility

router = APIRouter()


class BankRequest(BaseModel):
    entity_id: int
    amount: float
    duration_days: int


@router.post("/bank/check-eligibility")
def check_eligibility(request: BankRequest):
    """
    Simulated Bank/NBFC API endpoint.

    NOTE:
    This is NOT a real banking API.
    It is only for the NinjaFlow hackathon demo.
    """

    return check_bank_eligibility(
        request.entity_id,
        request.amount,
        request.duration_days
    )
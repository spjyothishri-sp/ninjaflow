from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.financing_service import recommend_financing

router = APIRouter()


class FinancingRequest(BaseModel):
    entity_id: int
    financing_input: dict


@router.post("/financing/recommend")
def financing_recommendation(request: FinancingRequest):

    result = recommend_financing(
        request.entity_id,
        request.financing_input
    )

    return result
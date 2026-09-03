from backend.services.bank_service import check_bank_eligibility


def recommend_financing(entity_id, financing_input):
    """
    Generate a financing recommendation and simulated
    Bank/NBFC offer.

    NOTE:
    All financing and banking values are simulated
    for the NinjaFlow hackathon demo.
    """

    if not financing_input:
        return None

    if not financing_input.get("required"):
        return {
            "entity_id": entity_id,
            "financing_required": False,
            "message": "No financing required."
        }

    amount = float(financing_input["amount"])
    duration_days = int(financing_input["duration_days"])
    priority = financing_input["priority"]

    # Financing recommendation
    recommendation = {
        "entity_id": entity_id,
        "recommended_amount": round(amount, 2),
        "duration_days": duration_days,
        "priority": priority,
        "reason": (
            f"Financing of ₹{amount:,.0f} recommended for "
            f"{duration_days} days based on the projected "
            f"liquidity requirement."
        )
    }

    # Send recommendation to simulated bank
    bank_offer = check_bank_eligibility(
        entity_id,
        amount,
        duration_days
    )

    # Calculate remaining funding gap
    approved_amount = float(bank_offer["approved_amount"])
    remaining_gap = max(0, amount - approved_amount)

    return {
        "financing_required": True,
        "recommendation": recommendation,
        "bank_offer": bank_offer,
        "remaining_gap": round(remaining_gap, 2)
    }


if __name__ == "__main__":

    demo_input = {
        "required": True,
        "amount": 1546618.92,
        "duration_days": 30,
        "priority": "MEDIUM"
    }

    result = recommend_financing(1, demo_input)

    print("Financing Recommendation:")
    print(result)
def check_bank_eligibility(entity_id, amount, duration_days):
    """
    Simulated Bank/NBFC eligibility check.

    NOTE:
    This is NOT a real banking API.
    It is only for the NinjaFlow hackathon demo.
    """

    # Simulated eligibility rule
    eligible = amount <= 1000000

    # Simulated interest rate
    if duration_days <= 15:
        interest_rate = 12.5
    else:
        interest_rate = 14.0

    # Simulated approved amount
    if eligible:
        approved_amount = amount
    else:
        approved_amount = amount * 0.7

    return {
        "entity_id": entity_id,
        "eligible": eligible,
        "approved_amount": round(approved_amount, 2),
        "interest_rate": interest_rate,
        "duration_days": duration_days,
        "status": "OFFERED",
        "message": "Simulated Bank/NBFC offer - Demo Only"
    }
def recommend_financing(entity_id, db):
    """
    Generate a financing recommendation based on the
    projected liquidity gap.

    NOTE:
    All values used by NinjaFlow are simulated demo data.
    """

    # For now, use dummy forecast data.
    # We will connect this to the real forecast later.
    forecast = {
        "gap_amount": 800000,
        "days_until_gap": 11,
        "predicted_delay_days": 8
    }

    gap = forecast["gap_amount"]
    days_until = forecast["days_until_gap"]
    predicted_delay = forecast["predicted_delay_days"]

    # No financing required if there is no liquidity gap
    if gap <= 0:
        return None

    # Add 5% safety buffer
    amount = round(gap * 1.05, -3)

    # Cover predicted payment delay + 7 day margin
    duration = predicted_delay + 7

    # Determine priority
    if days_until <= 7:
        priority = "HIGH"
    elif days_until <= 15:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    # Explanation shown to the user
    reason = (
        f"Projected ₹{gap:,.0f} shortfall in {days_until} days "
        f"due to predicted payment delays and upcoming supplier obligations."
    )

    return {
        "entity_id": entity_id,
        "amount": amount,
        "duration_days": duration,
        "reason": reason,
        "priority": priority
    }


# Test the function directly
if __name__ == "__main__":
    result = recommend_financing(1, None)
    print("Financing Recommendation:")
    print(result)
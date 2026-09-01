import os
import joblib
import pandas as pd


# Load the trained model once when this file is imported
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "model.pkl"
)

model = joblib.load(MODEL_PATH)


# These must be in exactly the same order used during training
FEATURE_COLUMNS = [
    "historical_average_delay",
    "current_cash",
    "outstanding_receivables",
    "upcoming_payables",
    "order_frequency_per_month",
    "season_index",
    "order_amount",
    "invoice_amount",
    "days_since_transaction",
    "credit_term_days",
]


def predict_delay(features_dict):
    """
    Predict payment delay for one transaction/entity.

    Input:
        Dictionary containing the required ML features.

    Output:
        Dictionary containing predicted delay and delay probability.
    """

    # Create a DataFrame with the exact training feature order
    features = pd.DataFrame(
        [[features_dict.get(column, 0) for column in FEATURE_COLUMNS]],
        columns=FEATURE_COLUMNS
    )

    # Make prediction
    predicted_delay = float(model.predict(features)[0])

    # Delay cannot be negative for our business interpretation
    predicted_delay = max(0.0, predicted_delay)

    # Simple probability heuristic
    # 30 days is treated as the maximum reference delay
    delay_probability = min(
        1.0,
        predicted_delay / 30.0
    )

    return {
        "predicted_delay_days": round(predicted_delay, 2),
        "delay_probability": round(delay_probability, 2)
    }


def compute_risk(
    predicted_delay_days,
    delay_probability,
    current_cash,
    gap_amount,
    days_until_gap
):
    """
    Calculate an explainable liquidity risk score from 0-100.
    """

    # Normalize predicted delay
    delay_factor = min(
        1.0,
        predicted_delay_days / 30.0
    )

    # Normalize gap relative to available cash
    if current_cash <= 0:
        gap_factor = 1.0
    else:
        gap_factor = min(
            1.0,
            gap_amount / current_cash
        )

    # Earlier gap = higher urgency
    urgency_factor = min(
        1.0,
        1.0 / max(days_until_gap, 1)
    )

    risk_score = (
        0.4 * delay_factor +
        0.3 * gap_factor +
        0.3 * urgency_factor
    ) * 100

    risk_score = round(
        max(0.0, min(100.0, risk_score)),
        2
    )

    if risk_score < 35:
        risk_level = "HEALTHY"
    elif risk_score < 65:
        risk_level = "AT_RISK"
    else:
        risk_level = "CRITICAL"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level
    }


if __name__ == "__main__":

    # Test prediction using sample data
    sample_features = {
        "historical_average_delay": 7.0,
        "current_cash": 150000,
        "outstanding_receivables": 500000,
        "upcoming_payables": 800000,
        "order_frequency_per_month": 12,
        "season_index": 0.8,
        "order_amount": 50000,
        "invoice_amount": 50000,
        "days_since_transaction": 10,
        "credit_term_days": 15
    }

    result = predict_delay(sample_features)

    print("=" * 60)
    print("NinjaFlow ML Prediction Test")
    print("=" * 60)

    print(f"Predicted delay : {result['predicted_delay_days']} days")
    print(f"Delay probability: {result['delay_probability'] * 100:.1f}%")

    risk = compute_risk(
        predicted_delay_days=result["predicted_delay_days"],
        delay_probability=result["delay_probability"],
        current_cash=150000,
        gap_amount=80000,
        days_until_gap=5
    )

    print(f"Risk score      : {risk['risk_score']}")
    print(f"Risk level      : {risk['risk_level']}")

    print("=" * 60)
    print("Prediction module working successfully!")
    print("=" * 60)
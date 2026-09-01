import sys
import os
from datetime import date

from fastapi import FastAPI, HTTPException

# Add the project root folder to Python's import path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from db import get_connection
from ml.predict import predict_delay, compute_risk


app = FastAPI(
    title="NinjaFlow API",
    description="AI-Powered Supply-Chain Liquidity Intelligence",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "NinjaFlow Backend is running!"
    }


@app.get("/entities")
def get_entities():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            entity_id,
            entity_name,
            entity_type,
            region,
            historical_avg_delay_days,
            current_cash
        FROM entities
    """)

    entities = cursor.fetchall()

    connection.close()

    return [
        dict(entity)
        for entity in entities
    ]


@app.get("/risk/{entity_id}")
def get_risk(entity_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    # Get entity information
    cursor.execute("""
        SELECT
            entity_id,
            entity_name,
            historical_avg_delay_days,
            current_cash
        FROM entities
        WHERE entity_id = ?
    """, (entity_id,))

    entity = cursor.fetchone()

    if entity is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Entity not found"
        )

    # Get transactions for this entity
    cursor.execute("""
        SELECT
            order_amount,
            invoice_amount,
            transaction_date,
            payment_due_date,
            payment_delay_days,
            transaction_type,
            status
        FROM transactions
        WHERE entity_id = ?
        ORDER BY transaction_date DESC
    """, (entity_id,))

    transactions = cursor.fetchall()

    # Entity values
    historical_average_delay = (
        entity["historical_avg_delay_days"] or 0
    )

    current_cash = (
        entity["current_cash"] or 0
    )

    # Default ML feature values
    outstanding_receivables = 0
    upcoming_payables = 0
    order_frequency_per_month = 0
    season_index = 1.0
    order_amount = 0
    invoice_amount = 0
    days_since_transaction = 0
    credit_term_days = 30

    # Calculate transaction features
    if transactions:

        latest_transaction = transactions[0]

        order_amount = (
            latest_transaction["order_amount"] or 0
        )

        invoice_amount = (
            latest_transaction["invoice_amount"] or 0
        )

        # Calculate receivables and payables
        for transaction in transactions:

            amount = (
                transaction["invoice_amount"]
                or transaction["order_amount"]
                or 0
            )

            if transaction["transaction_type"] == "RECEIVABLE":

                if transaction["status"] in (
                    "PENDING",
                    "OVERDUE"
                ):
                    outstanding_receivables += amount

            elif transaction["transaction_type"] == "PAYABLE":

                if transaction["status"] in (
                    "PENDING",
                    "OVERDUE"
                ):
                    upcoming_payables += amount

        # Calculate days since latest transaction
        latest_date = latest_transaction["transaction_date"]

        try:
            transaction_date = date.fromisoformat(
                latest_date
            )

            days_since_transaction = max(
                0,
                (date.today() - transaction_date).days
            )

        except (ValueError, TypeError):
            days_since_transaction = 0

        # Simple transaction frequency
        order_frequency_per_month = len(transactions)

    # Build ML feature dictionary
    features = {
        "historical_average_delay": historical_average_delay,
        "current_cash": current_cash,
        "outstanding_receivables": outstanding_receivables,
        "upcoming_payables": upcoming_payables,
        "order_frequency_per_month": order_frequency_per_month,
        "season_index": season_index,
        "order_amount": order_amount,
        "invoice_amount": invoice_amount,
        "days_since_transaction": days_since_transaction,
        "credit_term_days": credit_term_days
    }

    # Run ML prediction
    prediction = predict_delay(features)

    # Calculate cash-flow gap
    available_funds = (
        current_cash + outstanding_receivables
    )

    gap_amount = max(
        0,
        upcoming_payables - available_funds
    )

    # Temporary value until forecasting is connected
    days_until_gap = 30

    # Calculate risk
    risk = compute_risk(
        predicted_delay_days=prediction[
            "predicted_delay_days"
        ],
        delay_probability=prediction[
            "delay_probability"
        ],
        current_cash=current_cash,
        gap_amount=gap_amount,
        days_until_gap=days_until_gap
    )

    # Save prediction
    cursor.execute("""
        INSERT INTO risk_predictions (
            entity_id,
            predicted_delay_days,
            delay_probability,
            risk_score,
            risk_level,
            expected_gap_amount,
            gap_expected_in_days
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        entity_id,
        prediction["predicted_delay_days"],
        prediction["delay_probability"],
        risk["risk_score"],
        risk["risk_level"],
        gap_amount,
        days_until_gap
    ))

    connection.commit()
    connection.close()

    # Return result
    return {
        "entity_id": entity_id,
        "entity_name": entity["entity_name"],
        "predicted_delay_days": prediction[
            "predicted_delay_days"
        ],
        "delay_probability": prediction[
            "delay_probability"
        ],
        "risk_score": risk["risk_score"],
        "risk_level": risk["risk_level"],
        "expected_gap_amount": gap_amount,
        "gap_expected_in_days": days_until_gap
    }
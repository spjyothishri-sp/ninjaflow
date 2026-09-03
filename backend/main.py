import sys
import os
from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# =========================================================
# IMPORTS
# =========================================================

from db import get_connection
from ml.predict import predict_delay, compute_risk
from backend.routers.financing import router as financing_router


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="NinjaFlow API",
    description="AI-Powered Supply-Chain Liquidity Intelligence",
    version="1.0.0"
)

# Register Member 4 financing routes
app.include_router(financing_router)


# =========================================================
# SIMULATE REQUEST MODEL
# =========================================================

class SimulateRequest(BaseModel):
    entity_id: int


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "message": "NinjaFlow Backend is running!"
    }


# =========================================================
# GET ALL ENTITIES
# =========================================================

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


# =========================================================
# GET RISK FOR ENTITY
# =========================================================

@app.get("/risk/{entity_id}")
def get_risk(entity_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    # -----------------------------------------------------
    # GET ENTITY
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # GET TRANSACTIONS
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # ENTITY VALUES
    # -----------------------------------------------------

    historical_average_delay = (
        entity["historical_avg_delay_days"] or 0
    )

    current_cash = (
        entity["current_cash"] or 0
    )

    # -----------------------------------------------------
    # DEFAULT ML FEATURES
    # -----------------------------------------------------

    outstanding_receivables = 0
    upcoming_payables = 0
    order_frequency_per_month = 0
    season_index = 1.0
    order_amount = 0
    invoice_amount = 0
    days_since_transaction = 0
    credit_term_days = 30

    # -----------------------------------------------------
    # CALCULATE FEATURES
    # -----------------------------------------------------

    if transactions:

        latest_transaction = transactions[0]

        order_amount = (
            latest_transaction["order_amount"] or 0
        )

        invoice_amount = (
            latest_transaction["invoice_amount"] or 0
        )

        # -----------------------------------------------
        # RECEIVABLES / PAYABLES
        # -----------------------------------------------

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

        # -----------------------------------------------
        # DAYS SINCE TRANSACTION
        # -----------------------------------------------

        latest_date = latest_transaction[
            "transaction_date"
        ]

        try:

            transaction_date = date.fromisoformat(
                latest_date
            )

            days_since_transaction = max(
                0,
                (
                    date.today() -
                    transaction_date
                ).days
            )

        except (ValueError, TypeError):

            days_since_transaction = 0

        # -----------------------------------------------
        # TRANSACTION FREQUENCY
        # -----------------------------------------------

        order_frequency_per_month = len(
            transactions
        )

    # -----------------------------------------------------
    # ML FEATURES
    # -----------------------------------------------------

    features = {

        "historical_average_delay":
            historical_average_delay,

        "current_cash":
            current_cash,

        "outstanding_receivables":
            outstanding_receivables,

        "upcoming_payables":
            upcoming_payables,

        "order_frequency_per_month":
            order_frequency_per_month,

        "season_index":
            season_index,

        "order_amount":
            order_amount,

        "invoice_amount":
            invoice_amount,

        "days_since_transaction":
            days_since_transaction,

        "credit_term_days":
            credit_term_days
    }

    # -----------------------------------------------------
    # ML PREDICTION
    # -----------------------------------------------------

    prediction = predict_delay(
        features
    )

    # -----------------------------------------------------
    # CASH FLOW GAP
    # -----------------------------------------------------

    available_funds = (
        current_cash +
        outstanding_receivables
    )

    gap_amount = max(
        0,
        upcoming_payables -
        available_funds
    )

    # Temporary value.
    # This can later be connected to forecasting.
    days_until_gap = 30

    # -----------------------------------------------------
    # RISK CALCULATION
    # -----------------------------------------------------

    risk = compute_risk(

        predicted_delay_days=
            prediction["predicted_delay_days"],

        delay_probability=
            prediction["delay_probability"],

        current_cash=
            current_cash,

        gap_amount=
            gap_amount,

        days_until_gap=
            days_until_gap
    )

    # -----------------------------------------------------
    # SAVE RISK PREDICTION
    # -----------------------------------------------------

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

        prediction[
            "predicted_delay_days"
        ],

        prediction[
            "delay_probability"
        ],

        risk[
            "risk_score"
        ],

        risk[
            "risk_level"
        ],

        gap_amount,

        days_until_gap
    ))

    connection.commit()
    connection.close()

    # -----------------------------------------------------
    # RESPONSE
    # -----------------------------------------------------

    return {

        "entity_id":
            entity_id,

        "entity_name":
            entity["entity_name"],

        "predicted_delay_days":
            prediction[
                "predicted_delay_days"
            ],

        "delay_probability":
            prediction[
                "delay_probability"
            ],

        "risk_score":
            risk[
                "risk_score"
            ],

        "risk_level":
            risk[
                "risk_level"
            ],

        "expected_gap_amount":
            gap_amount,

        "gap_expected_in_days":
            days_until_gap
    }


# =========================================================
# SIMULATE
# =========================================================

@app.post("/simulate")
def simulate(
    request: SimulateRequest
):

    connection = get_connection()
    cursor = connection.cursor()

    # -----------------------------------------------------
    # 1. GET ENTITY
    # -----------------------------------------------------

    cursor.execute("""
        SELECT
            entity_id,
            entity_name,
            entity_type,
            region,
            historical_avg_delay_days,
            current_cash
        FROM entities
        WHERE entity_id = ?
    """, (
        request.entity_id,
    ))

    entity = cursor.fetchone()

    if entity is None:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Entity not found"
        )

    # -----------------------------------------------------
    # 2. GET TRANSACTIONS
    # -----------------------------------------------------

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
    """, (
        request.entity_id,
    ))

    transactions = cursor.fetchall()

    # -----------------------------------------------------
    # 3. ENTITY VALUES
    # -----------------------------------------------------

    historical_average_delay = (
        entity["historical_avg_delay_days"] or 0
    )

    current_cash = (
        entity["current_cash"] or 0
    )

    # -----------------------------------------------------
    # 4. INITIAL FEATURES
    # -----------------------------------------------------

    outstanding_receivables = 0
    upcoming_payables = 0
    order_frequency_per_month = 0
    season_index = 1.0
    order_amount = 0
    invoice_amount = 0
    days_since_transaction = 0
    credit_term_days = 30

    # -----------------------------------------------------
    # 5. CALCULATE FEATURES
    # -----------------------------------------------------

    if transactions:

        latest_transaction = transactions[0]

        order_amount = (
            latest_transaction["order_amount"]
            or 0
        )

        invoice_amount = (
            latest_transaction["invoice_amount"]
            or 0
        )

        # -----------------------------------------------
        # RECEIVABLES AND PAYABLES
        # -----------------------------------------------

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

        # -----------------------------------------------
        # DAYS SINCE TRANSACTION
        # -----------------------------------------------

        latest_date = latest_transaction[
            "transaction_date"
        ]

        try:

            transaction_date = date.fromisoformat(
                latest_date
            )

            days_since_transaction = max(
                0,
                (
                    date.today() -
                    transaction_date
                ).days
            )

        except (ValueError, TypeError):

            days_since_transaction = 0

        # -----------------------------------------------
        # FREQUENCY
        # -----------------------------------------------

        order_frequency_per_month = len(
            transactions
        )

    # -----------------------------------------------------
    # 6. BUILD ML INPUT
    # -----------------------------------------------------

    features = {

        "historical_average_delay":
            historical_average_delay,

        "current_cash":
            current_cash,

        "outstanding_receivables":
            outstanding_receivables,

        "upcoming_payables":
            upcoming_payables,

        "order_frequency_per_month":
            order_frequency_per_month,

        "season_index":
            season_index,

        "order_amount":
            order_amount,

        "invoice_amount":
            invoice_amount,

        "days_since_transaction":
            days_since_transaction,

        "credit_term_days":
            credit_term_days
    }

    # -----------------------------------------------------
    # 7. RUN ML
    # -----------------------------------------------------

    prediction = predict_delay(
        features
    )

    # -----------------------------------------------------
    # 8. CALCULATE CASH GAP
    # -----------------------------------------------------

    available_funds = (
        current_cash +
        outstanding_receivables
    )

    gap_amount = max(
        0,
        upcoming_payables -
        available_funds
    )

    # Temporary forecasting value.
    days_until_gap = 30

    # -----------------------------------------------------
    # 9. CALCULATE RISK
    # -----------------------------------------------------

    risk = compute_risk(

        predicted_delay_days=
            prediction[
                "predicted_delay_days"
            ],

        delay_probability=
            prediction[
                "delay_probability"
            ],

        current_cash=
            current_cash,

        gap_amount=
            gap_amount,

        days_until_gap=
            days_until_gap
    )

    # -----------------------------------------------------
    # 10. SAVE SIMULATION RESULT
    # -----------------------------------------------------

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

        request.entity_id,

        prediction[
            "predicted_delay_days"
        ],

        prediction[
            "delay_probability"
        ],

        risk[
            "risk_score"
        ],

        risk[
            "risk_level"
        ],

        gap_amount,

        days_until_gap
    ))

    connection.commit()
    connection.close()

    # -----------------------------------------------------
    # 11. FINANCING INPUT FOR MEMBER 4
    # -----------------------------------------------------

    financing_required = (
        gap_amount > 0
    )

    if risk["risk_level"] == "CRITICAL":

        priority = "HIGH"

    elif risk["risk_level"] == "AT_RISK":

        priority = "MEDIUM"

    else:

        priority = "LOW"

    # -----------------------------------------------------
    # 12. FINAL SIMULATION RESPONSE
    # -----------------------------------------------------

    return {

        "simulation":
            "completed",

        "entity": {

            "entity_id":
                entity["entity_id"],

            "entity_name":
                entity["entity_name"],

            "entity_type":
                entity["entity_type"],

            "region":
                entity["region"]
        },

        "risk": {

            "predicted_delay_days":
                prediction[
                    "predicted_delay_days"
                ],

            "delay_probability":
                prediction[
                    "delay_probability"
                ],

            "risk_score":
                risk[
                    "risk_score"
                ],

            "risk_level":
                risk[
                    "risk_level"
                ]
        },

        "cashflow": {

            "current_cash":
                current_cash,

            "outstanding_receivables":
                outstanding_receivables,

            "upcoming_payables":
                upcoming_payables,

            "available_funds":
                available_funds,

            "expected_gap_amount":
                gap_amount,

            "gap_expected_in_days":
                days_until_gap
        },

        "financing_input": {

            "required":
                financing_required,

            "amount":
                gap_amount,

            "duration_days":
                days_until_gap,

            "priority":
                priority
        }
    }
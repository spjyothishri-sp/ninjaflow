import csv
import os
import sqlite3
from datetime import datetime

from db import get_connection


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)

CSV_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "transactions.csv"
)


# ---------------------------------------------------------
# CHECK CSV
# ---------------------------------------------------------

if not os.path.exists(CSV_FILE):
    raise FileNotFoundError(
        f"Dataset not found: {CSV_FILE}"
    )


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def to_float(value, default=0.0):
    if value is None or value == "":
        return default

    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def to_int(value, default=0):
    if value is None or value == "":
        return default

    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default


def clean_date(value):
    if value is None or value == "":
        return None

    return str(value)


# ---------------------------------------------------------
# START
# ---------------------------------------------------------

print("=" * 60)
print("NinjaFlow Database Seeder")
print("=" * 60)

print("Reading dataset:")
print(CSV_FILE)


# ---------------------------------------------------------
# READ CSV
# ---------------------------------------------------------

with open(
    CSV_FILE,
    "r",
    encoding="utf-8-sig",
    newline=""
) as file:

    reader = csv.DictReader(file)

    rows = list(reader)


if not rows:
    raise ValueError(
        "transactions.csv is empty."
    )


print(f"CSV rows found: {len(rows)}")


# ---------------------------------------------------------
# CONNECT DATABASE
# ---------------------------------------------------------

connection = get_connection()
cursor = connection.cursor()


# ---------------------------------------------------------
# CLEAR EXISTING DATA
# ---------------------------------------------------------

cursor.execute("DELETE FROM bank_offers")
cursor.execute("DELETE FROM financing_recommendations")
cursor.execute("DELETE FROM risk_predictions")
cursor.execute("DELETE FROM cashflow")
cursor.execute("DELETE FROM transactions")
cursor.execute("DELETE FROM entities")


# ---------------------------------------------------------
# BUILD ENTITY INFORMATION
# ---------------------------------------------------------

entities = {}


for row in rows:

    entity_id = to_int(
        row.get("entity_id")
    )

    if entity_id <= 0:
        continue

    if entity_id not in entities:

        entity_type = (
            row.get("entity_type")
            or "BUYER"
        ).upper()

        if entity_type not in (
            "SUPPLIER",
            "BUYER",
            "NINJACART"
        ):
            entity_type = "BUYER"

        entities[entity_id] = {

            "entity_id":
                entity_id,

            "entity_name":
                f"{entity_type.title()}_{entity_id:02d}",

            "entity_type":
                entity_type,

            "region":
                row.get("region"),

            "historical_avg_delay_days":
                to_float(
                    row.get(
                        "historical_average_delay"
                    )
                ),

            "current_cash":
                to_float(
                    row.get("current_cash")
                )
        }


# ---------------------------------------------------------
# INSERT ENTITIES
# ---------------------------------------------------------

for entity_id in sorted(entities):

    entity = entities[entity_id]

    cursor.execute(
        """
        INSERT INTO entities (
            entity_id,
            entity_name,
            entity_type,
            region,
            onboarded_date,
            historical_avg_delay_days,
            current_cash
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            entity["entity_id"],
            entity["entity_name"],
            entity["entity_type"],
            entity["region"],
            "2026-01-01",
            entity["historical_avg_delay_days"],
            entity["current_cash"]
        )
    )


# ---------------------------------------------------------
# INSERT TRANSACTIONS
# ---------------------------------------------------------

transaction_count = 0


for row in rows:

    entity_id = to_int(
        row.get("entity_id")
    )

    if entity_id not in entities:
        continue


    entity_type = entities[
        entity_id
    ]["entity_type"]


    # Supplier = payable
    # Buyer = receivable

    if entity_type == "SUPPLIER":
        transaction_type = "PAYABLE"
    else:
        transaction_type = "RECEIVABLE"


    transaction_date = clean_date(
        row.get("transaction_date")
    )

    order_amount = to_float(
        row.get("order_amount")
    )

    invoice_amount = to_float(
        row.get("invoice_amount")
    )

    payment_due_date = clean_date(
        row.get("payment_due_date")
    )

    actual_payment_date = clean_date(
        row.get("actual_payment_date")
    )

    payment_delay_days = to_int(
        row.get("payment_delay_days")
    )


    # -----------------------------------------------------
    # DETERMINE STATUS
    # -----------------------------------------------------

    if actual_payment_date:

        if payment_delay_days <= 0:
            status = "PAID"
        else:
            status = "OVERDUE"

    else:

        if payment_due_date:

            try:

                due_date = datetime.strptime(
                    payment_due_date,
                    "%Y-%m-%d"
                )

                if due_date < datetime(
                    2026,
                    7,
                    1
                ):
                    status = "OVERDUE"
                else:
                    status = "PENDING"

            except ValueError:

                status = "PENDING"

        else:

            status = "PENDING"


    # -----------------------------------------------------
    # INSERT TRANSACTION
    # -----------------------------------------------------

    cursor.execute(
        """
        INSERT INTO transactions (
            entity_id,
            transaction_date,
            order_amount,
            invoice_amount,
            payment_due_date,
            actual_payment_date,
            payment_delay_days,
            transaction_type,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            entity_id,
            transaction_date,
            order_amount,
            invoice_amount,
            payment_due_date,
            actual_payment_date,
            payment_delay_days,
            transaction_type,
            status
        )
    )

    transaction_count += 1


# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

connection.commit()


# ---------------------------------------------------------
# VERIFY
# ---------------------------------------------------------

entity_count = cursor.execute(
    "SELECT COUNT(*) FROM entities"
).fetchone()[0]


transaction_count_db = cursor.execute(
    "SELECT COUNT(*) FROM transactions"
).fetchone()[0]


connection.close()


# ---------------------------------------------------------
# RESULT
# ---------------------------------------------------------

print()
print("=" * 60)
print("DATABASE SEEDING COMPLETE")
print("=" * 60)

print(
    f"Entities inserted     : "
    f"{entity_count}"
)

print(
    f"Transactions inserted : "
    f"{transaction_count_db}"
)

print()
print("Database:")
print(
    os.path.join(
        BACKEND_DIR,
        "database",
        "ninjaflow.db"
    )
)

print("=" * 60)
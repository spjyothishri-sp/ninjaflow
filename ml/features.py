import pandas as pd
import numpy as np


def create_features(input_file="../data/transactions.csv"):
    """
    Load NinjaFlow's fully synthetic transaction dataset
    and create model-ready features.

    This dataset contains NO real customer or company data.
    """

    df = pd.read_csv(input_file)

    # Convert date columns to datetime
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["payment_due_date"] = pd.to_datetime(df["payment_due_date"])
    df["actual_payment_date"] = pd.to_datetime(
        df["actual_payment_date"],
        errors="coerce"
    )

    # Days since the transaction
    latest_date = df["transaction_date"].max()
    df["days_since_transaction"] = (
        latest_date - df["transaction_date"]
    ).dt.days

    # Days between order and payment due date
    df["credit_term_days"] = (
        df["payment_due_date"] - df["transaction_date"]
    ).dt.days

    # Whether the payment was delayed
    df["was_delayed"] = (
        df["label_delay_days"] > 0
    ).astype(int)

    # Select features for the ML model
    feature_columns = [
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

    X = df[feature_columns].copy()

    # Target: payment delay in days
    y = df["label_delay_days"].copy()

    # Replace any missing/infinite values
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(0)

    return X, y, df


if __name__ == "__main__":
    X, y, df = create_features()

    print("=" * 60)
    print("NinjaFlow Feature Engineering")
    print("=" * 60)

    print(f"Total rows       : {len(X)}")
    print(f"Number of features: {X.shape[1]}")
    print()
    print("Features:")
    
    for column in X.columns:
        print(f"  - {column}")

    print()
    print("Target: label_delay_days")
    print()
    print("First 5 feature rows:")
    print(X.head())

    print()
    print("First 5 target values:")
    print(y.head())

    print("=" * 60)
    print("Feature engineering completed successfully!")
    print("=" * 60)
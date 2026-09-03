PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS entities (
    entity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_name TEXT NOT NULL,
    entity_type TEXT NOT NULL CHECK(entity_type IN ('SUPPLIER', 'BUYER', 'NINJACART')),
    region TEXT,
    onboarded_date DATE,
    historical_avg_delay_days REAL DEFAULT 0,
    current_cash REAL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id INTEGER NOT NULL,
    transaction_date DATE NOT NULL,
    order_amount REAL,
    invoice_amount REAL,
    payment_due_date DATE,
    actual_payment_date DATE,
    payment_delay_days INTEGER,
    transaction_type TEXT CHECK(transaction_type IN ('RECEIVABLE', 'PAYABLE')),
    status TEXT CHECK(status IN ('PAID', 'PENDING', 'OVERDUE')) DEFAULT 'PENDING',

    FOREIGN KEY (entity_id) REFERENCES entities(entity_id)
);

CREATE TABLE IF NOT EXISTS cashflow (
    cashflow_id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id INTEGER NOT NULL,
    date DATE NOT NULL,
    projected_cash_in REAL,
    projected_cash_out REAL,
    projected_balance REAL,
    is_forecast BOOLEAN DEFAULT 1,

    FOREIGN KEY (entity_id) REFERENCES entities(entity_id)
);

CREATE TABLE IF NOT EXISTS risk_predictions (
    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id INTEGER NOT NULL,
    predicted_delay_days REAL,
    delay_probability REAL,
    risk_score REAL,
    risk_level TEXT CHECK(risk_level IN ('HEALTHY', 'AT_RISK', 'CRITICAL')),
    expected_gap_amount REAL,
    gap_expected_in_days INTEGER,
    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (entity_id) REFERENCES entities(entity_id)
);

CREATE TABLE IF NOT EXISTS financing_recommendations (
    recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id INTEGER NOT NULL,
    recommended_amount REAL,
    recommended_duration_days INTEGER,
    reason TEXT,
    priority TEXT CHECK(priority IN ('LOW', 'MEDIUM', 'HIGH')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (entity_id) REFERENCES entities(entity_id)
);

CREATE TABLE IF NOT EXISTS bank_offers (
    offer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recommendation_id INTEGER NOT NULL,
    eligible BOOLEAN,
    approved_amount REAL,
    interest_rate REAL,
    duration_days INTEGER,
    status TEXT CHECK(
        status IN ('OFFERED', 'APPROVED', 'DISBURSED', 'REJECTED')
    ) DEFAULT 'OFFERED',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (recommendation_id)
        REFERENCES financing_recommendations(recommendation_id)
);
DROP TABLE IF EXISTS bank_settlements;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT,
    customer_email TEXT,
    order_total_cents INT,
    currency TEXT,
    is_test INT,
    created_at TIMESTAMP
);

CREATE TABLE payments (
    payment_id TEXT PRIMARY KEY,
    order_id TEXT,
    attempt_no INT,
    provider TEXT,
    provider_ref TEXT,
    status TEXT,
    amount_cents INT,
    attempted_at TIMESTAMP
);

CREATE TABLE bank_settlements (
    settlement_id TEXT PRIMARY KEY,
    payment_id TEXT,
    provider_ref TEXT,
    status TEXT,
    settled_amount_cents INT,
    currency TEXT,
    settled_at TIMESTAMP
);

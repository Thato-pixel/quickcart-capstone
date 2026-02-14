WITH successful_payments AS (
    SELECT
        p.payment_id,
        p.order_id,
        p.amount_cents,
        p.attempted_at,
        ROW_NUMBER() OVER (
            PARTITION BY p.order_id
            ORDER BY p.attempted_at DESC
        ) AS rn
    FROM payments p
    WHERE p.status = 'SUCCESS'
),

deduped_payments AS (
    SELECT *
    FROM successful_payments
    WHERE rn = 1
),

internal_sales AS (
    SELECT
        SUM(amount_cents)/100.0 AS total_successful_sales_usd
    FROM deduped_payments
),

bank_total AS (
    SELECT
        SUM(settled_amount_cents)/100.0 AS total_bank_settled_usd
    FROM bank_settlements
    WHERE status = 'SETTLED'
)

SELECT
    i.total_successful_sales_usd,
    b.total_bank_settled_usd,
    (i.total_successful_sales_usd - b.total_bank_settled_usd)
        AS discrepancy_gap_usd
FROM internal_sales i
CROSS JOIN bank_total b;

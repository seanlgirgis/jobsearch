# SQL Drills

## 1) Inner join
```sql
SELECT o.id, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;
```

## 2) Left join
```sql
SELECT c.customer_id, o.id
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```

## 3) Group by total
```sql
SELECT customer_id, SUM(amount) total
FROM orders
GROUP BY customer_id;
```

## 4) Having clause
```sql
SELECT customer_id, COUNT(*) cnt
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 5;
```

## 5) Window row_number
```sql
SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) rn
FROM customer_events;
```

## 6) Latest row per customer
```sql
SELECT *
FROM (
  SELECT e.*, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) rn
  FROM customer_events e
) t
WHERE rn = 1;
```

## 7) Duplicate detection
```sql
SELECT business_key, COUNT(*) cnt
FROM staging
GROUP BY business_key
HAVING COUNT(*) > 1;
```

## 8) Null handling COALESCE
```sql
SELECT order_id, COALESCE(discount, 0) discount
FROM orders;
```

## 9) CASE expression
```sql
SELECT amount,
       CASE WHEN amount >= 1000 THEN 'HIGH' ELSE 'NORMAL' END bucket
FROM orders;
```

## 10) Anti-join pattern
```sql
SELECT s.id
FROM source s
LEFT JOIN target t ON s.id = t.id
WHERE t.id IS NULL;
```

## 11) EXISTS
```sql
SELECT c.customer_id
FROM customers c
WHERE EXISTS (
  SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
);
```

## 12) NOT EXISTS
```sql
SELECT c.customer_id
FROM customers c
WHERE NOT EXISTS (
  SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
);
```

## 13) Running total
```sql
SELECT customer_id, order_date, amount,
       SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date) running_total
FROM orders;
```

## 14) Dense rank top spenders
```sql
SELECT customer_id, total_spend,
       DENSE_RANK() OVER (ORDER BY total_spend DESC) rnk
FROM customer_spend;
```

## 15) Count distinct
```sql
SELECT COUNT(DISTINCT customer_id) AS unique_customers
FROM orders;
```

## 16) Percent of total
```sql
SELECT customer_id, amount,
       amount * 1.0 / SUM(amount) OVER () pct_total
FROM customer_spend;
```

## 17) Join + filter recent
```sql
SELECT o.id, c.segment
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date >= DATE '2026-01-01';
```

## 18) Performance explanation prompt
Q: Why slow?
A: Large scans, missing predicates, heavy joins, skew, no pre-aggregation.

## 19) Reconciliation count
```sql
SELECT 'source' src, COUNT(*) cnt FROM src
UNION ALL
SELECT 'target' src, COUNT(*) cnt FROM tgt;
```

## 20) Null spike check
```sql
SELECT biz_date,
       SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END) null_amount_rows
FROM fact_orders
GROUP BY biz_date
ORDER BY biz_date DESC;
```

-- Simple PostgreSQL KEDA scaler query
-- Basic worker count-based scaling
-- Use this for simple scenarios or testing

SELECT COUNT(*) FROM workers WHERE status = 1
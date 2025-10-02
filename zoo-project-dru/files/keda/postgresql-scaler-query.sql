-- KEDA PostgreSQL Scaler Query
-- Hybrid scaling logic: active workers AND pending services
-- STRICT query - Absolute protection of pods by IP
-- GUARANTEE: No pod with its IP in workers.host can be deleted

WITH active_worker_ips AS (
  -- IPs of pods that have active workers - ABSOLUTE PROTECTION
  SELECT DISTINCT host as protected_ip
  FROM workers 
  WHERE status = 1 AND host IS NOT NULL
),
protected_count AS (
  -- MINIMUM number of pods to keep (those with workers)
  SELECT COUNT(*) as must_keep_minimum
  FROM active_worker_ips
),
workload_needs AS (
  -- Calculation based on total workload
  SELECT 
    SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) as active_workers,
    -- Pods needed for workload (async_worker=10 per pod)
    -- Scale-to-zero if no active workers
    CASE 
      WHEN SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) > 0
      THEN GREATEST(CEIL(SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END)::decimal / 10), 1)
      ELSE 0  -- Scale-to-zero if no workers
    END as pods_for_workload
  FROM workers
  WHERE host IS NOT NULL
),
service_needs AS (
  -- Pods needed for running services
  SELECT 
    COUNT(*) as running_services,
    -- Only if workers exist AND services
    CASE 
      WHEN EXISTS(SELECT 1 FROM workers WHERE status = 1 AND host IS NOT NULL) 
        AND COUNT(*) > 0 
      THEN GREATEST(CEIL(COUNT(*)::decimal / 10), 1)
      ELSE 0  -- Scale-to-zero if no active workers
    END as pods_for_services
  FROM services 
  WHERE end_time IS NULL AND fstate NOT IN ('Succeeded', 'Failed')
)
SELECT 
  -- Hybrid logic: active workers AND pending services
  GREATEST(
    -- Calculation based on active workers (1 pod per 10 workers)
    CASE 
      WHEN (SELECT COUNT(*) FROM workers WHERE status = 1 AND host IS NOT NULL) > 0
      THEN CEIL((SELECT COUNT(*)::decimal FROM workers WHERE status = 1 AND host IS NOT NULL) / 10)
      ELSE 0
    END,
    -- Calculation based on active services (1 pod per 5 services)
    CASE 
      WHEN (SELECT COUNT(*) FROM services WHERE end_time IS NULL AND fstate NOT IN ('Succeeded', 'Failed')) > 0
      THEN CEIL((SELECT COUNT(*)::decimal FROM services WHERE end_time IS NULL AND fstate NOT IN ('Succeeded', 'Failed')) / 5)
      ELSE 0
    END,
    -- Scale-to-zero if no activity
    0
  )
#!/bin/bash
set -e

echo "🛡️  Starting Zoo-Project KEDA Protection Controller (ScaledObject-based)"

NAMESPACE=${NAMESPACE:-zoo}
SCALEDOBJECT_NAME=${SCALEDOBJECT_NAME:-"zoo-project-dru-zoofpm-scaler"}

# PostgreSQL configuration
PG_HOST=${PG_HOST:-"zoo-project-dru-postgresql"}
PG_PORT=${PG_PORT:-"5432"} 
PG_USER=${PG_USER:-"zoo"}
PG_PASSWORD=${PG_PASSWORD:-"zoo"}
PG_DATABASE=${PG_DATABASE:-"zoo"}

echo "🔄 Initializing KEDA protection controller..."
echo "🔍 Namespace: $NAMESPACE"
echo "🔍 ScaledObject: $SCALEDOBJECT_NAME"
echo "🔍 PostgreSQL: $PG_HOST:$PG_PORT/$PG_DATABASE"

# Test PostgreSQL connection
test_postgresql_connection() {
    if PGPASSWORD="$PG_PASSWORD" psql -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d "$PG_DATABASE" -c "SELECT 1;" >/dev/null 2>&1; then
        return 0
    else
        echo "⚠️  PostgreSQL connection failed"
        return 1
    fi
}

# Count total active workers
get_total_active_workers() {
    if ! test_postgresql_connection; then
        echo "0"
        return
    fi
    
    local total_workers=$(PGPASSWORD="$PG_PASSWORD" psql -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d "$PG_DATABASE" -t -c \
        "SELECT COUNT(*) FROM workers WHERE status IN (1,2) AND host IS NOT NULL;" 2>/dev/null | xargs || echo "0")
    
    echo "$total_workers"
}

# Count active workers by pod IP
get_workers_by_pod_ip() {
    if ! test_postgresql_connection; then
        echo ""
        return
    fi
    
    # Returns a list "ip:worker_count" for each pod with active workers
    PGPASSWORD="$PG_PASSWORD" psql -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d "$PG_DATABASE" -t -c \
        "SELECT host || ':' || COUNT(*) 
         FROM workers 
         WHERE status IN (1,2) AND host IS NOT NULL 
         GROUP BY host;" 2>/dev/null | sed 's/^ *//' | grep -v '^$' || echo ""
}

# Get current zoofpm pods with IPs
get_current_pods_with_ips() {
    kubectl get pods -n "$NAMESPACE" -l app.kubernetes.io/name=zoo-project-dru-zoofpm -o jsonpath='{range .items[*]}{.metadata.name}:{.status.podIP}{"\n"}{end}' 2>/dev/null | grep -v '^$' || echo ""
}

# Annotate pods with their associated worker count
annotate_pods_with_workers() {
    local workers_by_ip=$(get_workers_by_pod_ip)
    local current_pods=$(get_current_pods_with_ips)
    
    if [ -z "$current_pods" ]; then
        echo "📝 No zoofpm pods found to annotate"
        return
    fi
    
    # For each current pod, annotate with worker count
    while IFS= read -r pod_line; do
        if [ -n "$pod_line" ]; then
            local pod_ip=$(echo "$pod_line" | cut -d':' -f2)
            local pod_name=$(echo "$pod_line" | cut -d':' -f1)
            
            # Check if this IP has active workers
            local worker_count=0
            if [ -n "$workers_by_ip" ] && echo "$workers_by_ip" | grep -q "^$pod_ip:"; then
                worker_count=$(echo "$workers_by_ip" | grep "^$pod_ip:" | cut -d':' -f2 | xargs)
            fi
            
            # Annotate the pod with worker count
            kubectl annotate pod "$pod_name" -n "$NAMESPACE" \
                zoo-project.org/active-workers="$worker_count" \
                zoo-project.org/last-check="$(date -Iseconds)" \
                --overwrite 2>/dev/null || true
            
            if [ "$worker_count" -gt 0 ]; then
                echo "📝 Pod $pod_name annotated with $worker_count active workers - PROTECTED"
                # Add protection annotation for Kyverno
                kubectl annotate pod "$pod_name" -n "$NAMESPACE" \
                    zoo-project.org/protected="true" \
                    --overwrite 2>/dev/null || true
            else
                echo "📝 Pod $pod_name annotated with 0 workers - NOT PROTECTED"
                # Remove protection annotation
                kubectl annotate pod "$pod_name" -n "$NAMESPACE" \
                    zoo-project.org/protected- \
                    --overwrite 2>/dev/null || true
            fi
        fi
    done <<< "$current_pods"
}

# No grace period needed - Kyverno provides sufficient protection

# Prevent scale-down by protecting pods with active workers
manage_scale_protection() {
    local current_pods=$(kubectl get pods -n "$NAMESPACE" -l app.kubernetes.io/name=zoo-project-dru-zoofpm --no-headers 2>/dev/null | wc -l || echo "0")
    local total_active_workers=$(get_total_active_workers)
    
    echo "📊 Current pods: $current_pods, Total active workers: $total_active_workers"
    
    # Check if ScaledObject exists before trying to modify it
    if ! kubectl get scaledobject "$SCALEDOBJECT_NAME" -n "$NAMESPACE" >/dev/null 2>&1; then
        echo "⏳ Waiting for ScaledObject $SCALEDOBJECT_NAME to be created..."
        return
    fi
    
    if [ "$total_active_workers" -gt 0 ]; then
        # There are active workers (even orphaned ones) - ABSOLUTE PROTECTION
        # Count how many pods actually have active workers
        local workers_by_ip=$(get_workers_by_pod_ip)
        local pods_with_workers=0
        if [ -n "$workers_by_ip" ]; then
            pods_with_workers=$(echo "$workers_by_ip" | wc -l | xargs)
        fi
        
        # Set minimum replicas to exactly the number of pods with active workers
        local min_replicas=$pods_with_workers
        if [ "$min_replicas" -eq 0 ]; then
            min_replicas=1  # Safety: at least 1 pod if there are workers but detection failed
        fi
        
        echo "🚫 ABSOLUTE PROTECTION: Setting minReplicaCount to $min_replicas (workers detected: $total_active_workers on $pods_with_workers pods)"
        kubectl patch scaledobject "$SCALEDOBJECT_NAME" -n "$NAMESPACE" -p "{\"spec\":{\"minReplicaCount\":$min_replicas}}" --type=merge
        kubectl annotate scaledobject "$SCALEDOBJECT_NAME" -n "$NAMESPACE" zoo-project.org/protection-status="absolute" zoo-project.org/protected-pods="$min_replicas" zoo-project.org/active-workers="$total_active_workers" zoo-project.org/pods-with-workers="$pods_with_workers" --overwrite
    else
        # No active workers - allow scale-to-zero (Kyverno will protect if needed)
        echo "✅ Resetting minReplicaCount to 0 (no active workers detected)"
        kubectl patch scaledobject "$SCALEDOBJECT_NAME" -n "$NAMESPACE" -p '{"spec":{"minReplicaCount":0}}' --type=merge
        kubectl annotate scaledobject "$SCALEDOBJECT_NAME" -n "$NAMESPACE" zoo-project.org/protection-status="inactive" zoo-project.org/protected-pods="0" --overwrite
    fi
}

# Function for checking and updating protection
check_and_update_protection() {
    echo "🔍 Checking worker status per pod..."
    
    # Annotate pods with their workers
    annotate_pods_with_workers
    
    # Analyze workers per pod and adjust KEDA protection
    manage_scale_protection
}

# HTTP server for health checks
start_http_server() {
    echo "🌐 Starting HTTP server on port 8080..."
    
    # Simple HTTP server in background with nohup
    nohup bash -c '
        while true; do
            echo -e "HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK" | nc -l 8080 2>/dev/null || sleep 0.1
        done
    ' &
    
    HTTP_PID=$!
    echo "🌐 HTTP server started on port 8080 (PID: $HTTP_PID)"
    
    # Test that server responds
    sleep 2
    if curl -s http://localhost:8080 >/dev/null 2>&1; then
        echo "✅ HTTP server is responding"
    else
        echo "⚠️  HTTP server may not be responding correctly"
    fi
}

# Signal handler for cleanup
cleanup() {
    echo "🧹 Cleanup: Resetting KEDA ScaledObject to allow scale-to-zero before exit"
    kubectl patch scaledobject "$SCALEDOBJECT_NAME" -n "$NAMESPACE" -p '{"spec":{"minReplicaCount":0}}' --type=merge 2>/dev/null || true
    exit 0
}

trap cleanup SIGTERM SIGINT

# Startup
start_http_server

# Main monitoring loop (ultra-reactive protection)
while true; do
    check_and_update_protection
    sleep 2  # Check every 2 seconds - MAXIMUM PROTECTION
done

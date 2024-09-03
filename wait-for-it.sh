#!/bin/bash

# Label to identify the deployment and pod
LABEL="app.kubernetes.io/instance=zoo-project-dru"
NAMESPACE="zoo"

# Function to get the status of the deployment
get_deployment_status() {
    kubectl get deployment zoo-project-dru-zookernel -n $NAMESPACE -o "jsonpath={.status.availableReplicas}"
}

# Function to get the status of the pod
get_pod_status() {
    kubectl get pods -l $LABEL -n $NAMESPACE -o "jsonpath={.items[0].status.phase}"
}

# Check if the deployment and pod are running
while true; do
    # Get the current status of the deployment
    DEPLOYMENT_STATUS=$(get_deployment_status)
    echo "Deployment replicas: $DEPLOYMENT_STATUS"

    # Get the current status of the pod
    POD_STATUS=$(get_pod_status)
    echo "Pod status: $POD_STATUS"

    # Check if the deployment has 1 available replica and the pod is running
    if [ "$DEPLOYMENT_STATUS" = "1" ] && [ "$POD_STATUS" = "Running" ]; then
        echo "Deployment with label $LABEL is running and a pod is in Running state"
        break
    else
        echo "Waiting for deployment and pod to be running..."
    fi

    # Wait for 5 seconds before checking again
    sleep 5
done
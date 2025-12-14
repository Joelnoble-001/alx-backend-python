#!/bin/bash

# kubctl-0x03.sh
# Objective: Apply rolling update and monitor downtime

DEPLOYMENT_NAME=django-blue
SERVICE_URL=http://localhost:8000/  # update if using different Service or minikube URL

echo "Applying updated blue deployment..."
kubectl apply -f blue_deployment.yaml

echo "Monitoring rolling update..."
kubectl rollout status deployment/$DEPLOYMENT_NAME

echo "Starting continuous requests to test downtime..."
# Send requests every 1 second for 30 seconds
for i in {1..30}; do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" $SERVICE_URL)
    echo "Request $i: HTTP status $STATUS"
    sleep 1
done

echo "Rolling update complete. Current pods:"
kubectl get pods -l version=blue

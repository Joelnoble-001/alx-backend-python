#!/bin/bash

# kubctl-0x01.sh
# Objective: Scale Django app deployment and monitor resources

# Name of your deployment
DEPLOYMENT_NAME=django-messaging-app
NAMESPACE=default   # adjust if using a different namespace

echo "Scaling deployment $DEPLOYMENT_NAME to 3 replicas..."
kubectl scale deployment $DEPLOYMENT_NAME --replicas=3

# Verify scaling
echo "Verifying pods..."
kubectl get pods -n $NAMESPACE

# Optional: wait a few seconds for pods to be ready
echo "Waiting for pods to be ready..."
sleep 10
kubectl get pods -n $NAMESPACE

# Load testing with wrk (assumes wrk is installed and Service is accessible)
SERVICE_IP=$(kubectl get svc messaging-service -n $NAMESPACE -o jsonpath='{.spec.clusterIP}')
SERVICE_PORT=8000

echo "Starting load test with wrk on $SERVICE_IP:$SERVICE_PORT..."
wrk -t2 -c10 -d10s http://$SERVICE_IP:$SERVICE_PORT/

# Monitor resource usage
echo "Monitoring resource usage..."
kubectl top pods -n $NAMESPACE
kubectl top nodes

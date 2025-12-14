#!/bin/bash

# kubctl-0x02.sh
# Objective: Deploy Blue-Green strategy and check logs

# Apply blue deployment
echo "Deploying Blue version..."
kubectl apply -f blue_deployment.yaml

# Apply green deployment
echo "Deploying Green version..."
kubectl apply -f green_deployment.yaml

# Apply Service
echo "Applying Service..."
kubectl apply -f kubeservice.yaml

# Wait a few seconds for pods to start
echo "Waiting for pods to be ready..."
sleep 10

# Check pods
echo "Current pods:"
kubectl get pods

# Check logs of green version pods for errors
echo "Logs from Green version pods:"
GREEN_PODS=$(kubectl get pods -l version=green -o jsonpath='{.items[*].metadata.name}')
for pod in $GREEN_PODS; do
    echo "Logs for $pod:"
    kubectl logs $pod
done

# Instructions to switch traffic
echo "To switch traffic to green version, update kubeservice.yaml selector to 'version: green' and apply."

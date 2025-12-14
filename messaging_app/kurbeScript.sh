# kurbeScript.sh
# Objective: Start a Kubernetes cluster locally and verify it

# Step 1: Check if minikube is installed
if ! command -v minikube &> /dev/null
then
    echo "Minikube is not installed. Please install it first."
    exit 1
fi

# Step 2: Start the Kubernetes cluster
echo "Starting Minikube Kubernetes cluster..."
minikube start

# Step 3: Verify the cluster is running
echo "Verifying Kubernetes cluster..."
kubectl cluster-info

# Step 4: List all available pods
echo "Listing all pods in all namespaces..."
kubectl get pods --all-namespaces

echo "Kubernetes setup complete!"

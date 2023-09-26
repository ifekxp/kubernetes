# Kubernetes day-01

## Start Minikube

Note down the external IP

```bash
minikube start --memory 4096 --cpus 2
minikube ip
```

## Build image

```bash
minikube image build -t myfastapi:1.0 .
```

## Deploy app and validate deployment

```bash
kubectl apply -f .\deployment.yaml
kubectl get all -n myfastapi-dev
kubectl get ingress -n myfastapi-dev
```

## Test app

```bash
curl -H "Host: myfastapi.com" http://<minikube ip>:80/
```


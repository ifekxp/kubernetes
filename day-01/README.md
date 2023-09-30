# Kubernetes Day 01

## Start Minikube

Start Minikube, enable addons and note down the external IP

```bash
# configure driver and resource
minikube delete
minikube config set driver hyperv
minikube config set cpus 2
minikube config set memory 8gb

# start minikube
minikube start

# enable useful addons
minikube addons enable metrics-server
minikube addons enable dashboard
minikube addons enable registry

# enable and configure ingress addons
minikube addons enable ingress
minikube addons enable ingress-dns

# note down cluster ip
minikube ip
```

## Build image

```bash
minikube image build -t myfastapi:1.0 .
```

## Deploy app and validate deployment

```bash
kubectl apply -f .\deployment.yaml

kubectl config set-context --current --namespace=myfastapi-dev

kubectl get all -n myfastapi-dev
kubectl get ingress -n myfastapi-dev
```

## Test app

```bash
curl -H "Host: my-minikube.com" http://<minikube ip>:80/fastapi/

kubectl logs pod/<podname> -n myfastapi-dev
```


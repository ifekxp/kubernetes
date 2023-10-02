# Kubernetes Day 01

This demonstrates following topic:

1. Ingress load balancer
2. Kubernetes secret
3. Pod security context, resource and probes
4. Python FastAPI and [Alphavantage API](https://www.alphavantage.co/documentation/) 

## Prerequisite

Create an account on Alphavantage to generate API key

## Start Minikube

Start Minikube, enable addons and note down the external IP

```powershell
# configure driver and resource
$ minikube delete
$ minikube config set driver hyperv
$ minikube config set cpus 2
$ minikube config set memory 8gb

# start minikube
$ minikube start -n 1

# enable useful addons
$ minikube addons enable metrics-server
$ minikube addons enable dashboard
$ minikube addons enable registry

# enable and configure ingress addons
$ minikube addons enable ingress
$ minikube addons enable ingress-dns

# note down cluster ip
$ $MINIKUBE_IP=minikube ip
```

## Build image

```powershell
$ minikube image build -t myfastapi:1.0 .
```
exit
## Deploy app and validate deployment

```powershell
$ echo "<Alphavantage API KEY>" > .secret/alphavantage.secret

$ kubectl create ns myfastapi-dev

$ kubectl config set-context --current --namespace=myfastapi-dev

$ kubectl create secret generic alphavantage --from-file=.secret/alphavantage.secret

$ kubectl apply -f .\deployment.yaml

$ kubectl get all -n myfastapi-dev
$ kubectl get ingress -n myfastapi-dev
```

## Test app

```powershell
$ curl -H "Host: myfastapi.com" http:///"$MINIKUBE_IP":80/healthz

$ curl -H "Host: myfastapi.com" http:///"$MINIKUBE_IP":80/stock/quote/ibm

$ curl -H "Host: myfastapi.com" http:///"$MINIKUBE_IP":80/stock/quote/shop.trt

$ kubectl logs pod/<podname> -n myfastapi-dev
```


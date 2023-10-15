# Kubernetes Day 01

This demonstrates following topic:

1. Ingress load balancer
2. Kubernetes secret
3. Pod security context, resource and probes
4. Python FastAPI and [Alphavantage API](https://www.alphavantage.co/documentation/) 

## Prerequisite

Create an account on Alphavantage to generate API key

```powershell
# install jq using chocolatey
$ choco install jq

# install k9s dashboard
$ choco install k9s
```


## Start Minikube

Start Minikube, enable addons and note down the external IP

```powershell
# configure driver and resource
$ minikube delete
$ minikube config set driver hyperv
$ minikube config set cpus 4
$ minikube config set memory 8gb

# start minikube
$ minikube start -n 1

# enable useful addons
$ minikube addons enable metrics-server
$ minikube addons enable registry

# enable and configure ingress addons
$ minikube addons enable ingress
$ minikube addons enable ingress-dns

# note down cluster ip
$ $MINIKUBE_IP=minikube ip
```

## Build image

```powershell
$ cd day-01

$ minikube image build -t myfastapi:1.0 .
```

## Deploy app and validate deployment

```powershell
$ echo "<Alphavantage API KEY>" > .secret/alphavantage.secret

$ kubectl apply -f .\namespace.yml

$ kubectl config set-context --current --namespace=myfastapi-dev

$ kubectl create secret generic alphavantage --from-file=../.secret/alphavantage.secret

$ kubectl apply -f .\deployment.yml

# wait for the pod to be in running state
$ kubectl get pod -n myfastapi-dev -w

# wait for ingress pod is assigned to ip address 
$ kubectl get ingress -n myfastapi-dev -w

$ kubectl get all -n myfastapi-dev
```

## Test app

```powershell
$ curl -H "Host: myfastapi.com" http:///"$MINIKUBE_IP":80/healthz
"Ok"

$ curl -s -H "Host: myfastapi.com" http:///"$MINIKUBE_IP":80/stock/quote/ibm | jq '.'
 "Global Quote": {
    "01. symbol": "IBM",
    "02. open": "139.7700",
    "03. high": "140.1200",
    "04. low": "138.2700",
    "05. price": "138.4600",
    "06. volume": "4583553",
    "07. latest trading day": "2023-10-13",
    "08. previous close": "141.2400",
    "09. change": "-2.7800",
    "10. change percent": "-1.9683%"
  }
}

$ curl -s -H "Host: myfastapi.com" http:///"$MINIKUBE_IP":80/stock/quote/shop.trt | jq '.'
{
  "Global Quote": {
    "01. symbol": "SHOP.TRT",
    "02. open": "73.0500",
    "03. high": "74.0500",
    "04. low": "69.2300",
    "05. price": "70.4300",
    "06. volume": "3429549",
    "07. latest trading day": "2023-10-13",
    "08. previous close": "73.0400",
    "09. change": "-2.6100",
    "10. change percent": "-3.5734%"
  }
}

$ $POD_NAME=kubectl get pod -o name
$ kubectl logs "$POD_NAME" --since=1m -f -n myfastapi-dev
```

## Browse kubernetes resources using K9s terminal

```powershell
# Press 0 to see all resources. Press :q to quit.
$ k9s -n myfastapi-dev
```
## Reference
[Minikube](https://minikube.sigs.k8s.io/docs/start/)

[K9s](https://k9scli.io/topics/commands/)

[Jq](https://jqlang.github.io/jq/manual/)

[Chocolatey](https://docs.chocolatey.org/en-us/getting-started)


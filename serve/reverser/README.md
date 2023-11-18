# Reverse

A trivial example of a ray serve service which reverses a string.

This is en example config to test the ray serve components.

This example shows:
1. How to configure a github based working dir and pip env
2. How to deploy a service using `kubectl`
3. Matched Ray Versions and images.

## Key Points

> Ray Version: 2.8.0
> Ray Image: ray:2.8.0

# Prerequisits

The Service is deployed to kalavai through 'kubectl`. As such you must have the following packages installed:

```
kubectl
```
You must have a valid kubectl user configuration at ~/.kube/config. Ask *Carlos* for access.

# Deployment

The Service is deployed to kalavai through `kubectl` deploying a yaml CRD, using the apply method:

```kubectl apply -f ray-service.reverser.yaml```

This will create a new rayservice, `rs-reverser` which can be seen, and monitored with:

```
kubectl get rayservice
kubectl describe rayservice rs-reverser
```

You can further inspect this rayservice through the dashboard, which can be accessed locally through port forwarding using:

```
kubectl port-forward --address 0.0.0.0 services/rs-reverser-head-svc  8265
```

where `rs-reverser-head-svc` is the name of the `service` (not ray service) which is spawned by the ray service.

This can be found by using the command:
```
kubectl get services
```

This port forwarding will give access to the dashboard at `http:127.0.0.1:8265`

## Usage

To use this service can be exposed locally through a port forward of the head service using:

```
kubectl port-forward --address 0.0.0.0 services/rs-reverser-head-svc 8000
```

This allows you to call the service locally with `python call.py`, which you can inspect.


## Troubleshooting

The first port of call for troubleshooting is to port-forward the head service dashboard and check the logs under /serve

If there are no logs under serve, likely the service was never able to be established.

One easily missed reasons is not having equal Ray versions on your Image (`159.65.30.72:32000/ray:2.8.0`) and your spec ray version `rayVersion: '2.8.0'`.


### Ray Service Works Not Initialised

You can check if your ray service workers are all initialised with `kubectl get pods`

Here we use a local private docker on the server to make downloading the image faster. sing the default ray_projects image may cause workers to hang an never become initialised. 


### Code changes not reflected in service.

1. Remember that the service uses the github repo for its runtime environment, so local changes must be pushed to github.
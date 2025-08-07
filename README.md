# charts
![example workflow](https://github.com/ZOO-Project/charts/actions/workflows/release.yaml/badge.svg)
[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/zoo-project)](https://artifacthub.io/packages/search?repo=zoo-project)

Helm charts for ZOO-Project including OGC API - Processes: Part 2: Deploy, Replace, Undeploy draft specification with CWL conformance class

## How to use

First add this repo https://zoo-project.github.io/charts/ from helm, using the following command:

```
helm repo add zoo-project https://zoo-project.github.io/charts/
```

Create your `myvalue.yaml` file to change the configuration you want, then use the command bellow:

```
helm upgrade --install zoo-project-dru ./ -f myvalues.yaml -n zoo-project-dru --create-namespace
```

## Using Skaffold for local deployment

### Requirements

* skaffold [installation](https://skaffold.dev/docs/install/#standalone-binary)
* Minikube [installation](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download)
* kubectl [installation](https://kubernetes.io/docs/tasks/tools/)

### Setup

Start your minikube cluster:

```
minikube start
```

Create the `zoo` namespace:

```
kubectl create namespace zoo
```

Deploy the ZOO-Project-DRU:

```
skaffold dev
```

Wait for the deployment to stabilize, the logs will show:

```
Completed post-deploy hooks
Port forwarding service/s3-service in namespace zoo, remote port 9000 -> http://127.0.0.1:9000
Port forwarding service/zoo-project-dru-service in namespace zoo, remote port 80 -> http://127.0.0.1:8080
Port forwarding service/s3-service in namespace zoo, remote port 9001 -> http://127.0.0.1:9001
No artifacts found to watch
Press Ctrl+C to exit
Watching for changes...
```

Open the browser on http://127.0.0.1:8080/ogc-api/api.html to access the ZOO-Project-DRU API documentation
Open the browser on http://127.0.0.1:9001 to access the Minio console (minio-admin/minio-admin)

#### KEDA Autoscaling profile

The ZOO-Project-DRU chart now includes advanced [KEDA](https://keda.sh/) (Kubernetes Event-driven Autoscaler) configuration for intelligent pod autoscaling based on PostgreSQL and RabbitMQ metrics.

In addition to KEDA, which will be deployed from the chart directly, you will need to setup [Kyverno](https://kyverno.io/) on your cluster.

```bash
# Add the Helm repository to your repo list
helm repo add kyverno https://kyverno.github.io/kyverno/

skaffold dev -p keda
```

Ensure that the Kyverno resources are properly removed from the cluster before starting using the `keda` profile. Consult [the official documentation](https://kyverno.io/docs/troubleshooting/) for more information.

#### Apple silicon profile

A dedicated hostpath profile is available for users deploying the solution on Apple silicon platforms and can be combined with other.

```bash
# Traditional startup
skaffold dev -p hostpath
# Activating keda
skaffold dev -p hostpath,keda
```

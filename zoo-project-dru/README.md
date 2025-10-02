# ZOO-Project with DRU and CWL support package

> The **ZOO-Project** is an open source processing platform, released under MIT/X11 Licence.

[Overview of ZOO-Project](http://zoo-project.org)

Trademarks: This software listing is packaged by the ZOO-Project developper team. The respective trademarks mentioned in the offering are owned by the respective companies, and use of them does not imply any affiliation or endorsement.

## Introduction

This chart bootstraps a [ZOO-Project](http://zoo-project.org) deployment on a cluster using the [Helm](https://helm.sh/) package manager.

## Prerequisites

 * Kubernetes 1.19+
 * Helm 3.2.0+
 * PV provisioner support in the underlying infrastructure
 * **Optional**: KEDA 2.14+ for autoscaling capabilities
 * **Optional**: Kyverno 3.5+ for advanced pod protection

## Installing the Chart

### Quick Start

To install the chart with the release name `my-zoo-project-dru`:

````bash
helm repo add zoo-project https://zoo-project.github.io/charts/
helm install my-zoo-project-dru zoo-project/zoo-project-dru --version 0.8.0
````

### Development with Skaffold

For development environments with enhanced capabilities:

````bash
# Basic deployment
skaffold dev

# With KEDA autoscaling and monitoring
skaffold dev -p keda

# With Argo Workflows support (optimized to avoid Helm secret size limit)
skaffold dev -p argo
````

**⚠️ Important Note for Argo Profile**: The `argo` profile uses an optimized configuration (`values_argo.yaml`) with `monitoring.enabled=false` to stay under the 1MB Helm secret size limit. For full monitoring capabilities, deploy the monitoring stack separately after Skaffold deployment. See the [Monitoring Deployment Strategies](#helm-secret-size-limitations-and-monitoring-deployment-strategies) section for details.

## Parameters

### Persistence

There are two persistent storage: `procServices` and `tmp`. The ZOO-Project uses the first for storing the deployed services (in a dedicated user's namespace) and the second for temporary files.

| Name                                       | Description                                              | Value                    |
|:-------------------------------------------|:---------------------------------------------------------|:-------------------------|
| persistence.enabled            | The persistence is enabled | true                      |
| persistence.storageClass            | The storage class | standard                      |
| persistence.userDataAccessMode            | The access mode | ReadWriteOnce                      |
| persistence.userDataSize            | The size allocated | 10Gi                      |
| persistence.procServicesAccessMode            | The access mode | ReadWriteOnce                      |
| persistence.procServicesStorageClass            | The storage class | standard                      |
| persistence.procServicesSize            | The size allocated | 5Gi                      |
| persistence.servicesNamespacePath            | The services namespace path (directory where user namespaces are created) | /opt/zooservices_user                      |
| persistence.tmpAccessMode            | The access mode | ReadWriteMany                      |
| persistence.tmpStorageClass            | The storage class | standard                      |
| persistence.tmpSize            | The size allocated | 2Gi                      |
| persistence.tmpPath            | The temporary diratory path | /tmp/zTmp                      |

### Global parameters

See the configuration parameters below for the official PostgreSQL Docker image integration.

| Name                                       | Description                                              | Value                    |
|:-------------------------------------------|:---------------------------------------------------------|:-------------------------|
| global.postgresql.auth.username            | User that will be used to connect to postgresql database | zoo                      |
| global.postgresql.auth.password            | Password for the user                                    | zoo                      |
| global.postgresql.auth.database            | Database name                                            | zoo                      |
| global.postgresql.service.ports.postgresql | PostgreSQL port                                          | "5432"                   |
| global.postgresql.auth.existingSecret      | Use an existing secrets to store the connection string   | zoo                      |

When using the `global.postgresql.auth.existingSecret`, it is required that the secret contains at the bare minimum the following keys: 

 * `postgres-password` is the password for the PostgreSQL administrator,
 * `password` is the password used to authenticate as a ¨PostgreSQL user.

The other keys can be added and will be added to the environment variables (`PGHOST`,`PGPORT`,`PGDATABASE`,`PGUSER`)

 * `host` the hostname/IP address where the PostgreSQL Server can be reached
 * `port` the port used to access the server
 * `database` the database to connect to
 * `username` the user to use for authenticating to the server

You can create a minimal secret using the command below.

````bash
kubectl create secret generic postgresql-secret \
  --from-literal=password=zoo \
  --from-literal=username=zoo \
  --from-literal=postgres-password=zoo \
  -n myNamespace --dry-run -o yaml | kubectl apply -f -
````

Then, you can use the following:

````bash
global.postgresql.auth.existingSecret: postgresql-secret
````

If an environment variable for PostgreSQL is available from the ZOO-Kernel or ZOO-FPM pods, it means that the database setting will use these variables rather than the one defined in the `main.cfg` available from the configmap.

### Dependency Management

#### MinIO

See the reference [MinIO chart documentation](https://artifacthub.io/packages/helm/minio-official/minio) for more informations.

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| minio.enabled                                            | Enable MinIO for storage | false |
| minio.mode                                               | MinIO deployment mode | "standalone" |
| minio.replicas                                           | Number of MinIO replicas | 1 |
| minio.rootUser                                           | MinIO root username | "minio-admin" |
| minio.rootPassword                                       | MinIO root password | "minio-secret-password" |
| minio.fullnameOverride                                   | MinIO service name override | "s3-service" |
| minio.buckets                                            | Default buckets to create | [{"name": "eoepca", "policy": "none"}, {"name": "results", "policy": "none"}] |
| minio.persistence.enabled                                | Enable MinIO persistence | true |
| minio.persistence.size                                   | MinIO storage size | "10Gi" |
| minio.persistence.storageClass                           | Storage class for MinIO | "" |
| minio.service.type                                       | MinIO service type | "ClusterIP" |
| minio.service.port                                       | MinIO service port | 9000 |
| minio.consoleService.port                                | MinIO console port | 9001 |

#### PostgreSQL

This chart deploys PostgreSQL using the official [PostgreSQL Docker image](https://hub.docker.com/_/postgres).


| Name                                       | Description                                                     | Value                    |
|:-------------------------------------------|:----------------------------------------------------------------|:-------------------------|
| postgresql.enabled                         | Enable PostgreSQL deployment                                   | true                     |
| postgresql.name                           | Name of the PostgreSQL deployment                              | postgresql-db            |
| postgresql.serviceName                    | Name of the PostgreSQL service                                 | postgresql-db-service    |
| postgresql.image.repository               | PostgreSQL Docker image repository                             | postgres                 |
| postgresql.image.tag                      | PostgreSQL Docker image tag                                    | 16-alpine                |
| postgresql.image.pullPolicy               | Image pull policy                                              | IfNotPresent             |
| postgresql.resources.limits.cpu           | CPU limit for PostgreSQL                                       | 1000m                    |
| postgresql.resources.limits.memory        | Memory limit for PostgreSQL                                    | 1Gi                      |
| postgresql.resources.requests.cpu         | CPU request for PostgreSQL                                     | 250m                     |
| postgresql.resources.requests.memory      | Memory request for PostgreSQL                                  | 256Mi                    |
| postgresql.persistence.enabled            | Enable persistent storage                                       | true                     |
| postgresql.persistence.size               | Size of the persistent volume                                   | 8Gi                      |
| postgresql.persistence.accessMode         | Access mode for the persistent volume                          | ReadWriteOnce            |
| postgresql.persistence.storageClass       | Storage class for the persistent volume                        | ""                       |
| postgresql.auth.createSecret              | Automatically create a secret for PostgreSQL credentials       | false                    |
| postgresql.primary.initdb.scriptsConfigMap | ConfigMap containing initialization scripts                     | postgresql-primary-init-scripts |

When `postgresql.enabled` is set to true, the environment variables for PostgreSQL (`PGHOST`,`PGPORT`,`PGUSER`,`PGPASSWORD`,`PGDATABASE`) will be defined for the ZOO-Kernel and the ZOO-FPM pods.

If an environment variable for PostgreSQL is available from the ZOO-Kernel or ZOO-FPM pods, it means that the database setting will use these variables rather than the one defined in the `main.cfg` available from the configmap.

#### RabbitMQ

This chart now integrates RabbitMQ using the [official Docker image](https://hub.docker.com/_/rabbitmq).


| Name                                       | Description                                              | Value                                        |
|:-------------------------------------------|:---------------------------------------------------------|:---------------------------------------------|
| rabbitmq.enabled                           | Enable integrated RabbitMQ deployment                    | true                                         |
| rabbitmq.image.repository                  | RabbitMQ image repository                                | rabbitmq                                     |
| rabbitmq.image.tag                         | RabbitMQ image tag                                       | 4.1.4-alpine                                 |
| rabbitmq.auth.username                     | RabbitMQ default user                                    | zoo                                          |
| rabbitmq.auth.password                     | RabbitMQ default password                                | CHANGEME                                     |
| rabbitmq.config                            | Override RabbitMQ configuration (if empty, uses files/rabbitmq/rabbitmq.conf) | ""                          |
| rabbitmq.autoSetup.enabled                 | Enable automatic RabbitMQ configuration via HTTP API     | true                                         |
| rabbitmq.autoSetup.ttlSecondsAfterFinished | Cleanup setup job after completion (seconds)             | 30                                           |
| rabbitmq.definitions                        | RabbitMQ definitions for queues, exchanges, bindings    | Automatically templated                      |

#### Redis

This chart deploys Redis using the official [Redis Docker image](https://hub.docker.com/_/redis).

| Name                                       | Description                                              | Value                    |
|:-------------------------------------------|:---------------------------------------------------------|:-------------------------|
| redis.enabled                              | Enable Redis deployment                                 | true                     |
| redis.name                                 | Name of the Redis deployment                            | redis-db                 |
| redis.serviceName                          | Name of the Redis service                               | redis-db-service         |
| redis.port                                 | Redis port                                              | 6379                     |
| redis.image.repository                     | Redis Docker image repository                           | redis                    |
| redis.image.tag                            | Redis Docker image tag                                  | 7-alpine                 |
| redis.image.pullPolicy                     | Image pull policy                                       | IfNotPresent             |
| redis.auth.enabled                         | Enable Redis authentication                             | false                    |
| redis.auth.password                        | Redis password (if auth enabled)                        | ""                       |
| redis.resources.limits.cpu                 | CPU limit for Redis                                     | 500m                     |
| redis.resources.limits.memory              | Memory limit for Redis                                  | 512Mi                    |
| redis.resources.requests.cpu               | CPU request for Redis                                   | 100m                     |
| redis.resources.requests.memory            | Memory request for Redis                                | 128Mi                    |
| redis.persistence.enabled                  | Enable persistent storage                               | true                     |
| redis.persistence.size                     | Size of the persistent volume                           | 4Gi                      |
| redis.persistence.accessMode               | Access mode for the persistent volume                   | ReadWriteOnce            |
| redis.persistence.storageClass             | Storage class for the persistent volume                 | ""                       |

For high-availability requirements, consider external Redis cluster solutions

### CookieCutter

| Name                     | Description                                          | Value                                               |
|:-------------------------|:-----------------------------------------------------|:----------------------------------------------------|
| cookiecutter.templateUrl | Where to download the cookiecutter from              | https://github.com/EOEPCA/proc-service-template.git |
| cookiecutter.templateBranch         | The branch to fetch the cookiecutter (optional)    | undefined                    |

### ZOO-Project

| Name                             | Description                                                        | Value                                                |
|:---------------------------------|:-------------------------------------------------------------------|:-----------------------------------------------------|
| zoo.promoteHead            | Expose endpoints using the HEAD HTTP method in the OpenAPI    | true                    |
| zoo.detectEntrypoint         | Dynamically deploy a pod and its associated service to detect docker `ENTRYPOINT` to prepend to existing baseCommand   | false                   |
| zoo.rabbitmq.definitions         | The `definition.json` file containing initial RabbitMQ settings    | "files/rabbitmq/definitions.json"                    |
| zookernel.env                    | The environment variables defined in the main.cfg `env` section    | {}                    |
| zookernel.extraMountPoints         | In case you add files in one or more `files/<DIR>` subdirectories and want to access them from the ZOO-Kernel     | []                    |
| zoofpm.extraMountPoints         | In case you add files in one or more `files/<DIR>` subdirectories and want to access them from the ZOO-FPM     | []                    |

### KEDA

KEDA (Kubernetes Event-driven Autoscaler) provides intelligent event-driven autoscaling with worker protection and scale-to-zero capabilities.

#### KEDA Autoscaling Configuration

| Name                                       | Description                                              | Value                    |
|:-------------------------------------------|:---------------------------------------------------------|:-------------------------|
| keda.enabled                               | Enable KEDA autoscaling and worker protection           | false                    |
| keda.minReplicas                           | Minimum number of replicas (0 allows scale-to-zero)     | 0                        |
| keda.maxReplicas                           | Maximum number of replicas                               | 10                       |
| keda.pollingInterval                       | Interval for checking metrics (seconds)                 | 10                       |
| keda.cooldownPeriod                        | Cooldown period after scaling (seconds)                 | 60                       |

#### PostgreSQL Trigger

Monitors active processing jobs and workers for intelligent scaling:

| Name                                        | Description                                                    | Value                    |
|:--------------------------------------------|:---------------------------------------------------------------|:-------------------------|
| keda.triggers.postgresql.enabled            | Enable PostgreSQL trigger for scaling                         | true                     |
| keda.triggers.postgresql.targetQueryValue   | Target scaling ratio for steady state                         | "0.5"                    |
| keda.triggers.postgresql.activationTargetQueryValue | Threshold for scale-up activation                    | "0.1"                    |
| keda.triggers.postgresql.host               | PostgreSQL host (auto-generated if empty)                     | ""                       |
| keda.triggers.postgresql.port               | PostgreSQL port                                                | "5432"                   |
| keda.triggers.postgresql.dbName             | Database name (uses global.postgresql.auth.database if empty) | ""                       |
| keda.triggers.postgresql.userName           | Username (uses global.postgresql.auth.username if empty)      | ""                       |
| keda.triggers.postgresql.sslmode            | SSL mode for connection                                        | "disable"                |

#### RabbitMQ Trigger

Monitors queue length for immediate scaling response:

| Name                                       | Description                                              | Value                    |
|:-------------------------------------------|:---------------------------------------------------------|:-------------------------|
| keda.triggers.rabbitmq.enabled             | Enable RabbitMQ queue length trigger                    | true                     |
| keda.triggers.rabbitmq.queueName           | RabbitMQ queue name to monitor                          | zoo_service_queue        |
| keda.triggers.rabbitmq.value               | Target queue length for scaling                         | 1                        |
| keda.triggers.rabbitmq.host                | RabbitMQ host (auto-generated if empty)                 | ""                       |
| keda.triggers.rabbitmq.username            | RabbitMQ username for trigger auth                      | zoo                      |
| keda.triggers.rabbitmq.password            | RabbitMQ password for trigger auth                      | CHANGEME                 |

#### KEDA Authentication

KEDA supports two authentication methods:

**Method 1: Using existing PostgreSQL secret (recommended)**

When `global.postgresql.auth.existingSecret` is configured, KEDA automatically uses the existing secret:

```yaml
global:
  postgresql:
    auth:
      existingSecret: postgresql-secret
```

**Method 2: Using values from configuration**

When no existing secret is configured, KEDA uses values from `global.postgresql.auth.*` and creates a dedicated secret.


#### KEDA Eviction Controller

The eviction controller provides intelligent worker protection and pod annotation management.

| Name                                       | Description                                              | Value                    |
|:-------------------------------------------|:---------------------------------------------------------|:-------------------------|
| keda.evictionController.enabled            | Enable intelligent eviction controller                  | false                    |
| keda.evictionController.image.repository   | Eviction controller container image repository          | ghcr.io/zoo-project/zoofpm-eviction-controller |
| keda.evictionController.image.tag          | Eviction controller container image tag                 | latest                   |
| keda.evictionController.image.pullPolicy   | Image pull policy                                       | IfNotPresent             |
| keda.evictionController.resources.requests.cpu   | CPU resource requests                             | 50m                      |
| keda.evictionController.resources.requests.memory | Memory resource requests                        | 64Mi                     |
| keda.evictionController.resources.limits.cpu     | CPU resource limits                               | 200m                     |
| keda.evictionController.resources.limits.memory  | Memory resource limits                            | 128Mi                    |

#### Kyverno Integration

Kyverno provides admission-level protection for pods with active workers.

| Name                                                    | Description                                              | Value                    |
|:--------------------------------------------------------|:---------------------------------------------------------|:-------------------------|
| keda.kyverno.enabled                                    | Enable Kyverno deployment (usually managed separately)  | false                    |
| keda.kyverno.namespaceOverride                          | Namespace where Kyverno is installed                    | kyverno-system           |
| keda.kyverno.policies.zoofpmProtection.enabled         | Enable Kyverno pod protection policy                    | true                     |
| keda.kyverno.policies.zoofpmProtection.failurePolicy   | Policy failure action (Enforce or Audit)                | Enforce                  |
| keda.kyverno.policies.zoofpmProtection.background      | Enable background policy processing                     | false                    |
| keda.kyverno.policies.zoofpmProtection.protectZoofpm   | Enable protection for zoofpm pods                       | true                     |

**Note:** Kyverno must be installed separately in the cluster. The chart only creates policy definitions.

#### Quick Start with KEDA

For rapid deployment with KEDA autoscaling capabilities:

```bash
# Deploy with Skaffold (includes KEDA operator installation)
skaffold dev -p keda

# Or manual Helm deployment (requires KEDA operator pre-installed)
helm install zoo-project-dru ./zoo-project-dru \
  --values ./zoo-project-dru/values_minikube.yaml \
  --set keda.enabled=true \
  --set keda.skipScaledObject=false \
  --namespace zoo --create-namespace
```

**Important Configuration Notes**:
- KEDA operator must be installed cluster-wide before enabling `keda.enabled=true`
- Set `keda.skipScaledObject=false` to enable automatic ScaledObject creation
- PostgreSQL triggers require worker tracking tables (automatically created)
- Scale-to-zero works when `keda.minReplicas=0` (default)

#### Scaling Logic and Protection

The autoscaler implements a hybrid approach:

1. **Worker-based scaling**: Scales based on active workers in PostgreSQL
2. **Service-based scaling**: Scales based on running services and pending jobs
3. **Pod protection**: Pods with active workers are protected using `zoo-project.org/protected="true"`
4. **Scale-to-zero**: Supports scaling to 0 when no work is available (if minReplicas=0)

#### Worker Protection Features

- **Dynamic annotations**: Automatically updates pod annotations based on worker activity
- **Eviction protection**: Prevents cluster autoscaler from evicting pods with active workers
- **Health probes**: Provides readiness and startup probes for reliable operation

#### Monitoring KEDA Autoscaling

```bash
# Check KEDA ScaledObject status
kubectl get scaledobjects -n <namespace>

# View HPA created by KEDA
kubectl get hpa -n <namespace>

# Monitor scaling events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Check worker protection status
kubectl get pods -n <namespace> -o jsonpath='{range .items[*]}{.metadata.name}{": safe-to-evict="}{.metadata.annotations.cluster-autoscaler\.kubernetes\.io/safe-to-evict}{", workers="}{.metadata.annotations.zoo-project\.org/has-active-workers}{"\n"}{end}'
```

### Identity and Access Management

| Name                             | Description                                                        | Value                                                |
|:---------------------------------|:-------------------------------------------------------------------|:-----------------------------------------------------|
| iam.enabled | The Identity and Access Management (IAM)                        | true |
| iam.openIdConnectUrl | The OpenIDConnect configuration URL                    | https://auth.geolabs.fr/realms/zooproject/.well-known/openid-configuration |
| iam.type | The IAM type                        | openIdConnect |
| iam.name | The IAM name                        | OpenIDAuth |
| iam.realm | The realm associated with the IAM | Secured section |
| iam.clientId | The clientId to access the IAM (optional) | undefined |
| iam.clientSecret | The clientSecret to access the IAM (optional) | undefined |
| iam.userinfoUrl | The userInfo url to access the user details from the IAM (optional) | undefined |
| iam.openeoAuth.enabled | Enable the openEO authentication mechanism | false |
| iam.openeoAuth.title | The title used for the default client | OpenId Connect Secured Access |
| iam.openeoAuth.grant_types | The required grant types to be supported | ["implicit","authorization_code+pkce","urn:ietf:params:oauth:grant-type:device_code+pkce"] |
| iam.openeoAuth.redirect_uris | The redirect urls the be supported | ["https://m-mohr.github.io/gdc-web-editor/"] |

When both `iam.enabled` and `iam.openeoAuth.enabled` are set to `true`, two new endpoints are added to the exposed OpenAPI:
 * `GET /credentials/oidc` to access the openid connect metadata information required by the client to authenticate (similar to the `.well-known/openid-configuration` with additional metadata).
 * `GET /me` to access metadata information about the authenticated user. 

When in IAM is enabled, you cannot use all interfaces from the Basic HTML UI provided by the ZOO-Project.

### WebUI 

The WebUI lets you interact with the ZOO-Project-DRU when authentication is required to use the service.


| Name                             | Description                                                        | Value                                                |
|:---------------------------------|:-------------------------------------------------------------------|:-----------------------------------------------------|
| webui.enabled | Activate the webui service                        | false |
| webui.url | The fully defined URL to access the WebUI                        | http://localhost:3058 |
| webui.port | Port                         | 3000 |
| webui.image.repository | WebUI container image repository | zooproject/nuxt-client |
| webui.image.tag | WebUI container image tag | 0.0.3 |
| webui.image.pullPolicy | WebUI image pull policy | Always |
| webui.enforce | Should apache handle security before the requests are sent to the ZOO-Project?                         | false |
| webui.oidc | The specific OpenIDConnect configuration                         | {"issuer":https://auth.geolabs.fr/realms/zooproject,"remoteUserClaim": email, "providerTokenEndpointAuth": client_secret_basic, "authVerifyJwksUri": https://auth.geolabs.fr/realms/zooproject/protocol/openid-connect/certs, "scope": "openid email"} |


If you set `enabled` to `true`, you should ensure that the `webui.oidc` object contains the following informations.

```yaml
  enabled: true
  oidc:
    issuer: <AUTH_URL>/realms<REALM>
    clientId: YOUR_CLIENT_ID
    clientSecret: YOUR_CLIENT_SECRET
    remoteUserClaim: email
    providerTokenEndpointAuth: client_secret_basic
    authVerifyJwksUri: <AUTH_URL>/realms/<REALM>/protocol/openid-connect/certs
    scope: "openid email"
```

WHere `<AUTH_URL>` is pointing to your keycloak instance (ie. `https://auth.geolabs.fr`), `<REALM>` (ie. `zooproject`) the realm you are willing to use. You can set the `YOUR_CLIENT_ID` and `YOUR_CLIENT_SECRET` to enable authentication.


### Documentation

| Name                             | Description                                                        | Value                                                |
|:---------------------------------|:-------------------------------------------------------------------|:-----------------------------------------------------|
| documentation.enabled | The Swagger-UI should include the documentation available from files/openapi-config/*                        | false |

### Websocketd

In case you have enabled redis and disabled IAM, you can activate the websocketd server.

| Name                             | Description                                                        | Value                                                |
|:---------------------------------|:-------------------------------------------------------------------|:-----------------------------------------------------|
| websocketd.enabled | The websocketd server is enabled                        | true |
| websocketd.port | The websocketd server listen port                        | 8888 |


### filter_in process

| Name                             | Description                                                        | Value                                                |
|:---------------------------------|:-------------------------------------------------------------------|:-----------------------------------------------------|
| filter_in.enabled | The filter_in process is enabled                        | true |
| filter_in.path | The filter_in process path                        | /usr/lib/cgi-bin |
| filter_in.service | The filter_in process name                         | securityIn |

### filter_out process

| Name                             | Description                                                        | Value                                                |
|:---------------------------------|:-------------------------------------------------------------------|:-----------------------------------------------------|
| filter_out.enabled | The filter_out process is enabled                        | true |
| filter_out.path | The filter_out process path                        | /usr/lib/cgi-bin |
| filter_out.service | The filter_out process name                         | securityOut |

### Workflow

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| workflow.storageClass                                    | The storage class used.             | standard                                                              |
| workflow.defaultVolumeSize                               | The default volume size allocated.  | 10190                                                                 |
| workflow.defaultMaxRam                                   | The default max ram allocated.      | 1024                                                                  |
| workflow.defaultMaxCores                                 | The default max cores allocated.    | 2                                                                     |
| workflow.calrissianImage                                 | The calrissian image version.       | "terradue/calrissian:0.12.0"                                          |
| workflow.dedicatedNamespace                              | Reuse an existing namespace rather createing a new one for every job | {"enabled":false} |
| workflow.additionalInputs                                | The additional inputs passed as attributes to wrapped CWL Application.        | {}                                          |
| workflow.imagePullSecrets                                | ImagePullSecrets is an optional list of references to secrets for the processing namespace to use for pulling any of the images used by the processing pods. If specified, these secrets will be passed to individual puller implementations for them to use. For example, in the case of docker, only DockerConfig type secrets are honored. More info: https://kubernetes.io/docs/concepts/containers/images#specifying-imagepullsecrets-on-a-pod       | {}                                          |
| workflow.additionalImagePullSecrets                      | additionalImagePullSecrets is an optional list of references to existing secrets for the processing namespace to use for pulling any of the images used by the processing pods. If specified, these secrets will be passed to individual puller implementations for them to use. For example, in the case of docker, only DockerConfig type secrets are honored. More info: https://kubernetes.io/docs/concepts/containers/images#specifying-imagepullsecrets-on-a-pod       | {}                                          |
| workflow.nodeSelector                                    | Constrain on which nodes the processing pods are eligible to run based on the node label.       | {}                                          |
| workflow.inputs                                          | Environmental variables for the ZOO-FPM pod (from where the processing is started).         | {}                                          |
| workflow.podAnnotations                                          | Use an object of key value pairs containing the annotations you want to flag your pods with.         | Not defined                                          |
| workflow.env                                             | Environmental variables for the processing pods.       | {}                                          |

#### Reuse an existing namespace

The zoo-calrissian-runner can be configured to use an existing namespace to handle the pods responsible for the workflow execution. 

You can set the `workflow.dedicatedNamespace.enabled` configuration to true to enable this feature. Then you need to specify the namespace's name with the `name` and optionally a service account with the `serviceAccount` parameter.

````yaml
dedicatedNamespace:
  enabled: true
  name: "my-dedicated-namespace"
  # Below is an example value, uncomment and provide an existing service acount name available in the namespace
  #service_account: "my-dedicated-service-account"
````

Below is an example demonstrating how to setup a `my-dedicated-namespace` namespace to be used by pycalrissian to run the workflow.
Note that the default service account is `"default"`.

````bash
kubectl create ns my-dedicated-namespace
# Apply a Role
kubectl apply -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: my-dedicated-namespace
  name: pod-reader
rules:
- apiGroups: [""] # "" indicates the core API group
  resources: ["pods","pods/log"]
  verbs: ["get", "watch", "list"]
EOF
# Apply a RoleBinding
kubectl apply -n my-dedicated-namespace -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
subjects:
- kind: User
  name: default
  namespace: my-dedicated-namespace
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
EOF
# Apply RoleBinding
kubectl apply -n my-dedicated-namespace -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: default-cluster-admin
subjects:
  - kind: ServiceAccount
    name: default
    namespace: my-dedicated-namespace
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
EOF
````

This is a very basic example and it does not provide a one-to-one mapping for every user, but only for a single user.

If you want to define a one-to-one mapping, you can implement the following methods in the handler of your service template: 
 * `get_namespace`: should return the Kubernetes namespace to use for executing the process, or `None` if a new namespace should be created for each process execution.
 * `get_service_account`: should return the Kubernetes service account to use, or `None` if the default service account should be used.

#### imagePullSecrets

The `workflow.imagePullSecrets` is used at runtime by Calrissian to dynamically create a secret containing the object attributes defined for pulling an image from a resgistry.
The syntaxe is as presenter below.

````yaml
auths:
  fake\.registry\.io:
    username: fakeuser
    password: fakepassword
    email: fake@example.com
    auth: ''
````

In addition, you can also use secrets already available in the namespace where the ZOO-Project-DRU Helm chart was deployed. 
For doing so, you can use the `workflow.additionalImagePullSecrets` with an array of object with a name pointing to the existing secret's name.

Example:

Create the secret in the dedicated namespace.

````bash
kubectl create secret docker-registry my-secret \
  --docker-email=tiger@acme.example \
  --docker-username=tiger \
  --docker-password=pass1234 \
  --docker-server=my-registry.example:5000 \
  -n given-namespace
````

Then, you can define the `workflow.additionalImagePullSecrets` as below.

````yaml
workflow:
  additionalImagePullSecrets:
  - name: my-secret
````

### WES support

ZOO-Project-DRU can execute CWL workflows through the toil Workflow Execution Service (WES).
See [reference documentation](https://zoo-project.github.io/zoo-wes-runner/) for more informations.

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| workflow.inputs.WES_URL                                    | The toil Workflow Execution Service (WES) URL | "http://192.168.1.59:8100/ga4gh/wes/v1/" |
| workflow.inputs.WES_USER                               | The user name to authenticate to access the WES | "test" |
| workflow.inputs.WES_PASSWORD                          | The password to authenticate to access the WES | `"$$2y$$12$$ci.4U63YX83CwkyUrjqxAucnmi2xXOIlEF6T/KdP9824f1Rf1iyNG"` |


### Argo Workflows Support

ZOO-Project-DRU can execute CWL workflows through the official Argo Workflows chart (v3.7.1).
See [reference documentation](https://artifacthub.io/packages/helm/argo/argo-workflows) for more information.

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| argo.enabled                                    | Activate Argo support by setting this to `true` | true |
| argo.instanceID                                 | Instance ID for workflow isolation | "zoo" |
| argo.cwlwrapperImage                            | CWL wrapper image version | "eoepca/cwl-wrapper:0.12.1" |
| argo.stageOutImage                              | Stage-out image version | "ghcr.io/eoap/mastering-app-package/stage:1.1.0" |
| argo.serviceAccount.name                        | ServiceAccount name for workflow execution | "argo-workflow" |
| argo.autoTokenManagement                        | Enable automatic token retrieval from ServiceAccount | true |
| argo.restartOnTokenUpdate                       | Restart ZOO-Kernel pods when token is updated | false |


| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| workflow.argo.enabled                                    | Activate Argo support by setting this to `true` | true |
| workflow.argo.storageClass                               | The storage class to use for temporary data | standard |
| workflow.argo.defaultVolumeSize                          | The default volume size | "12Gi" |
| workflow.argo.defaultMaxRam                              | The default maximum allocated ram | "2Gi" |
| workflow.argo.wfServer                                   | The Argo server URL  | "http://zoo-project-dru-argo-workflows-server.zoo.svc.cluster.local:2746" |
| workflow.argo.wfToken                                    | The Argo server token (auto-retrieved if autoTokenManagement enabled) | "" |
| workflow.argo.wfNamespace                                | The namespace where Argo workflows will be executed | "zoo" |
| workflow.argo.wfSynchronizationCm                        | The configmap name for workflow synchronization | "semaphore-argo-cwl-runner-stage-in-out" |
| workflow.argo.CwlRunnerTemplare                          | The workflow template name to use as CWL Runner | "argo-cwl-runner-stage-in-out" |
| workflow.argo.CwlRunnerEndpoint                          | The entry point to use from the CWL Runner Template | "calrissian-runner" |

**Event Monitoring Configuration**: Enable real-time workflow monitoring with Argo Events integration.

See [reference documentation](https://artifacthub.io/packages/helm/argo/argo-events) for more information.

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| argo.events.enabled                            | Enable Argo Events integration for real-time monitoring | true |
| argo.events.eventBus.enabled                   | Enable EventBus (JetStream backend) for persistent event streaming | true |
| argo.events.eventBus.nats.native.replicas      | Number of NATS replicas for EventBus | 1 |
| argo.events.eventBus.nats.native.auth          | NATS authentication method | "token" |
| argo.events.eventSource.enabled                | Enable EventSource for monitoring Argo Workflows API | true |
| argo.events.eventSource.name                   | Name of the EventSource | "workflow-monitor" |
| argo.events.eventSource.namespace              | Namespace for EventSource | "zoo" |
| argo.events.sensor.enabled                     | Enable Sensor for webhook notifications | true |
| argo.events.sensor.name                        | Name of the Sensor | "webhook-sensor" |
| argo.events.sensor.namespace                   | Namespace for Sensor | "zoo" |
| argo.events.webhook.enabled                    | Enable webhook service for event notifications | true |
| argo.events.webhook.port                       | Port for the webhook service | 12000 |
| argo.events.webhook.path                       | Path for webhook endpoint | "/workflow-events" |
| argo.events.webhook.enabled                    | Enable webhook sensor for notifications | true |
| argo.events.webhook.endpoint                   | External webhook endpoint URL | "" |
| argo.events.webhook.method                     | HTTP method for webhook calls | "POST" |

**Artifact Storage Configuration**: The chart automatically configures S3-compatible artifact storage using the built-in MinIO service.

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| argo.s3.bucket                                  | S3 bucket name for artifacts | "eoepca" |
| argo.s3.endpoint                                | S3 endpoint URL | "s3-service.zoo.svc.cluster.local:9000" |
| argo.s3.insecure                                | Use insecure S3 connection | true |
| argo.s3.secretName                              | Secret containing S3 credentials | "s3-service" |
| argo.s3.accessKeySecretKey                      | Secret key for S3 access key | "root-user" |
| argo.s3.secretKeySecretKey                      | Secret key for S3 secret key | "root-password" |

**Token Management**: When `autoTokenManagement` is enabled, the Argo Workflows token is automatically retrieved from the ServiceAccount and made available to ZOO-Kernel. This eliminates the need to manually configure `wfToken`.

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| argo-workflows.fullnameOverride                          | Full name override for Argo resources | "zoo-project-dru-argo-workflows" |
| argo-workflows.singleNamespace                           | Restrict Argo to single namespace operation | true |
| argo-workflows.images.tag                                | Argo Workflows version | "v3.7.1" |
| argo-workflows.images.pullPolicy                         | Image pull policy | "IfNotPresent" |

#### Artifact Repository Configuration

The chart automatically configures artifact storage using S3-compatible MinIO:

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| argo-workflows.artifactRepository.archiveLogs            | Archive workflow logs as artifacts | true |
| argo-workflows.artifactRepository.s3.endpoint            | S3 endpoint for artifact storage | "s3-service.zoo.svc.cluster.local:9000" |
| argo-workflows.artifactRepository.s3.bucket              | S3 bucket name | "eoepca" |
| argo-workflows.artifactRepository.s3.insecure            | Use insecure S3 connection | true |
| argo-workflows.artifactRepository.s3.accessKeySecret.name | Secret name for S3 access key | "s3-service" |
| argo-workflows.artifactRepository.s3.accessKeySecret.key  | Secret key for S3 access key | "root-user" |
| argo-workflows.artifactRepository.s3.secretKeySecret.name | Secret name for S3 secret key | "s3-service" |
| argo-workflows.artifactRepository.s3.secretKeySecret.key  | Secret key for S3 secret key | "root-password" |

#### Workflow Controller Configuration

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| argo-workflows.controller.enabled                        | Enable the workflow controller | true |
| argo-workflows.controller.instanceID.enabled             | Enable instance ID for isolation | true |
| argo-workflows.controller.instanceID.useReleaseName      | Use release name for instance ID | false |
| argo-workflows.controller.instanceID.explicitID          | Explicit instance ID | "zoo" |
| argo-workflows.controller.extraArgs                      | Additional controller arguments | ["--managed-namespace=zoo"] |
| argo-workflows.controller.clusterWorkflowTemplates.enabled | Enable cluster-wide workflow templates | false |
| argo-workflows.controller.workflowDefaults.spec.serviceAccountName | Default service account for workflows | "argo-workflow" |

#### Server Configuration

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| argo-workflows.server.enabled                            | Enable the Argo server (UI) | true |
| argo-workflows.server.serviceType                        | Server service type | "ClusterIP" |
| argo-workflows.server.servicePort                        | Server service port | 2746 |
| argo-workflows.server.authModes                          | Authentication modes | ["server"] |
| argo-workflows.server.secure                             | Enable HTTPS | false |
| argo-workflows.server.namespaced                         | Run server in namespaced mode | true |
| argo-workflows.server.extraArgs                          | Additional server arguments | ["--namespaced"] |
| argo-workflows.server.clusterWorkflowTemplates.enabled   | Enable cluster templates in server | false |

#### RBAC and Security

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| argo-workflows.rbac.create                               | Create RBAC resources | true |
| argo-workflows.serviceAccount.create                     | Create service account | true |
| argo-workflows.crds.install                              | Install CRDs (disabled if already present) | false |
| argo-workflows.crds.keep                                 | Keep CRDs on uninstall | true |


#### Access Configuration

**Access the Argo Workflows UI**:
```bash
kubectl port-forward -n zoo svc/zoo-project-dru-argo-workflows-server 2746:2746
# Open: http://localhost:2746
```

**Access MinIO Console**:
```bash
kubectl port-forward -n zoo svc/s3-service 9001:9001
# Open: http://localhost:9001
# Credentials: minio-admin / minio-secret-password
```

#### Deployment Examples

**Basic deployment with official Argo Workflows**:
```bash
helm install zoo-project-dru ./zoo-project-dru -f zoo-project-dru/values_argo.yaml -n zoo
```

**Production deployment with monitoring**:
```yaml
workflow:
  argo:
    enabled: true
    instanceID: "production"

monitoring:
  enabled: true
  kube-prometheus-stack:
    grafana:
      adminPassword: "secure-password"

argo-workflows:
  artifactRepository:
    s3:
      bucket: "production-artifacts"
```

### Argo Events Integration

The chart includes optional Argo Events integration for real-time workflow monitoring and event-driven automation. This provides reactive capabilities that automatically respond to workflow state changes.

#### Overview

Argo Events complements Argo Workflows by providing:
- **Real-time workflow monitoring**: Automatically capture workflow state changes (Running, Succeeded, Failed)
- **Event-driven triggers**: Execute actions based on workflow completion or failure
- **Metrics integration**: Real-time updates to Prometheus metrics and Grafana dashboards
- **Webhook notifications**: Send notifications to external systems when workflows complete

#### Core Configuration

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| argo.events.enabled                            | Enable Argo Events integration for real-time monitoring | false |
| argo.events.webhook.enabled                    | Enable webhook service for receiving event notifications | true |
| argo.events.webhook.port                       | Port for the webhook service | 8080 |
| argo.events.webhook.path                       | Path for webhook endpoint | "/webhook" |

#### Argo Events Chart Configuration

The chart uses the official Argo Events Helm chart (v2.4.8) to provide event-driven capabilities:

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| argo-events.enabled                                      | Enable Argo Events deployment | true |
| argo-events.crds.install                                 | Install Argo Events CRDs (disable if already present) | false |
| argo-events.crds.keep                                    | Keep CRDs on chart uninstall | true |
| argo-events.controller.replicas                          | Number of controller replicas | 1 |
| argo-events.controller.resources.requests.cpu            | Controller CPU requests | "100m" |
| argo-events.controller.resources.requests.memory         | Controller memory requests | "128Mi" |
| argo-events.controller.resources.limits.cpu              | Controller CPU limits | "500m" |
| argo-events.controller.resources.limits.memory           | Controller memory limits | "256Mi" |

#### EventSource Configuration

EventSources define what events to listen for. The chart automatically creates an EventSource for workflow monitoring:

```yaml
workflow:
  argo:
    events:
      enabled: true
      eventSource:
        # Listen to workflow events in the current namespace
        workflowEvents:
          group: argoproj.io
          version: v1alpha1
          resource: workflows
          eventTypes:
            - ADD      # Workflow created
            - UPDATE   # Workflow updated
            - DELETE   # Workflow deleted
```

**Event Filtering**: The EventSource automatically filters relevant events:
- Workflow creation (status: Running)
- Workflow completion (status: Succeeded)
- Workflow failure (status: Failed, Error)

#### Sensor Configuration

Sensors define what actions to take when events are received. The chart includes a webhook sensor for notifications:

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| argo.events.sensor.webhook.enabled             | Enable webhook sensor for notifications | true |
| argo.events.sensor.webhook.endpoint            | Webhook endpoint URL | "http://zoo-project-dru-webhook-service.zoo.svc.cluster.local:8080/webhook" |
| argo.events.sensor.webhook.method              | HTTP method for webhook calls | "POST" |
| argo.events.sensor.webhook.headers             | Additional HTTP headers | {"Content-Type": "application/json"} |

#### EventBus Configuration

The EventBus handles event routing between EventSources and Sensors:

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| argo-events.eventBusConfig.jetstream.versions           | JetStream versions for EventBus | ["latest"] |
| argo-events.global.image.tag                            | Argo Events image tag | "v1.9.1" |

#### Monitoring Integration

When Argo Events is enabled with monitoring, additional metrics and dashboards are available:

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| argo-events.controller.metrics.enabled                  | Enable controller metrics for Prometheus | true |
| argo-events.controller.metrics.port                     | Metrics port | 8080 |
| argo-events.controller.serviceMonitor.enabled           | Enable ServiceMonitor for Prometheus discovery | true |
| argo-events.controller.serviceMonitor.additionalLabels  | Additional labels for ServiceMonitor selection | {"release": "zoo-project-dru"} |

#### Real-time Dashboard Updates

With Argo Events enabled, Grafana dashboards receive real-time updates:

1. **Workflow metrics**: Automatically updated when workflows change state
2. **Event statistics**: Track event processing rates and success/failure ratios
3. **Latency monitoring**: Monitor time between workflow completion and notification delivery

#### Webhook Integration

The chart includes a webhook service that receives event notifications:

```yaml
# Webhook service configuration
apiVersion: v1
kind: Service
metadata:
  name: zoo-project-dru-webhook-service
spec:
  selector:
    app.kubernetes.io/name: zoo-project-dru-webhook
  ports:
    - port: 8080
      targetPort: 8080
      protocol: TCP
```

**Webhook Payload**: The webhook receives JSON payloads with workflow information:

```json
{
  "eventType": "UPDATE",
  "workflowName": "sample-workflow-12345",
  "workflowNamespace": "zoo",
  "status": "Succeeded",
  "startTime": "2025-08-19T10:00:00Z",
  "finishTime": "2025-08-19T10:05:30Z",
  "message": "Workflow completed successfully"
}
```

#### RBAC Configuration

Argo Events requires specific permissions to monitor workflows:

| Resource                  | Permissions               | Purpose                           |
|:--------------------------|:--------------------------|:----------------------------------|
| workflows.argoproj.io     | get, list, watch          | Monitor workflow state changes    |
| events                    | create, patch             | Create Kubernetes events          |
| configmaps                | get, list, create, patch  | EventBus configuration            |
| secrets                   | get, list                 | EventBus authentication           |

#### Troubleshooting

**Check EventSource status**:
```bash
kubectl get eventsource -n zoo
kubectl describe eventsource zoo-project-dru-workflow-events -n zoo
```

**Check Sensor status**:
```bash
kubectl get sensor -n zoo
kubectl describe sensor zoo-project-dru-webhook-sensor -n zoo
```

**Check EventBus status**:
```bash
kubectl get eventbus -n zoo
kubectl describe eventbus default -n zoo
```

**View event logs**:
```bash
# EventSource logs
kubectl logs -l eventsource-name=zoo-project-dru-workflow-events -n zoo

# Sensor logs  
kubectl logs -l sensor-name=zoo-project-dru-webhook-sensor -n zoo

# Controller logs
kubectl logs deployment/zoo-project-dru-argo-events-controller-manager -n zoo
```

**Test webhook manually**:
```bash
# Forward webhook port
kubectl port-forward svc/zoo-project-dru-webhook-service 8080:8080 -n zoo

# Send test event
curl -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -d '{"test": "event", "workflowName": "test-workflow"}'
```

#### Security Considerations

- **Network policies**: Consider restricting EventBus network access
- **Authentication**: Use secrets for external webhook authentication  
- **RBAC**: Apply principle of least privilege for service accounts
- **TLS**: Enable TLS for external webhook endpoints

### Monitoring

The chart includes comprehensive monitoring capabilities using the Prometheus stack (Prometheus, Grafana, Alertmanager, and node-exporter) with real-time Argo Workflows integration.
See [reference documentation](https://artifacthub.io/packages/helm/prometheus-community/kube-prometheus-stack) for more information.

#### Core Monitoring Configuration

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| monitoring.enabled                                       | Enable monitoring stack (Prometheus, Grafana, etc.) | true |
| monitoring.disableProblematicTargets                    | Disable problematic Kubernetes targets for local environments | true |
| monitoring.kube-prometheus-stack.prometheus.enabled      | Enable Prometheus server | true |
| monitoring.kube-prometheus-stack.prometheus.retention    | Prometheus data retention period | "15d" |
| monitoring.kube-prometheus-stack.prometheus.storageSpec.volumeClaimTemplate.spec.storageClassName | Storage class for Prometheus | "standard" |
| monitoring.kube-prometheus-stack.prometheus.storageSpec.volumeClaimTemplate.spec.resources.requests.storage | Prometheus storage size | "10Gi" |
| monitoring.kube-prometheus-stack.grafana.enabled         | Enable Grafana dashboard | true |
| monitoring.kube-prometheus-stack.grafana.adminPassword   | Grafana admin password | "admin" |
| monitoring.kube-prometheus-stack.grafana.persistence.enabled | Enable Grafana data persistence | true |
| monitoring.kube-prometheus-stack.grafana.persistence.size | Grafana storage size | "5Gi" |
| monitoring.kube-prometheus-stack.alertmanager.enabled    | Enable Alertmanager for notifications | true |

#### Helm Secret Size Limitations and Monitoring Deployment Strategies

⚠️ **Important**: The complete monitoring stack (kube-prometheus-stack) adds ~670KB to the Helm secret, which can cause deployments to exceed Kubernetes' 1MB secret size limit, resulting in installation failures.

##### Problem Description

When deploying with full monitoring enabled (especially with Argo profiles), you may encounter this error:
```
Error: INSTALLATION FAILED: create: failed to create: Secret "sh.helm.release.v1.zoo-project-dru.v1" is invalid: data: Too long: must have at most 1048576 bytes
```

This happens because the monitoring stack includes:
- **Grafana Dashboards**: ~400KB of dashboard configurations
- **Prometheus Rules**: ~200KB of alerting and recording rules  
- **CRDs and Templates**: ~70KB of additional Kubernetes resources

##### Recommended Solutions

**Solution 1: Separate Monitoring Deployment (Recommended)**

Deploy monitoring as a separate Helm release to avoid secret size issues:

```bash
# 1. Deploy ZOO-Project without integrated monitoring
skaffold dev -p argo  # Uses optimized values_argo.yaml with monitoring.enabled=false

# 2. Deploy monitoring stack separately
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  --set grafana.adminPassword=admin \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false

# 3. Access services
kubectl port-forward -n zoo svc/zoo-project-dru-service 8080:80           # ZOO-Project
kubectl port-forward -n zoo svc/zoo-project-dru-argo-workflows-server 2746:2746  # Argo UI
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80         # Grafana
```

**Solution 2: Minimal Integrated Monitoring**

Use a lightweight monitoring configuration that stays under the 1MB limit:

```bash
# Create optimized values file
cat > values_argo_with_monitoring.yaml << EOF
# Include all content from values_argo.yaml, then override:
monitoring:
  enabled: true
  kube-prometheus-stack:
    # Minimal Prometheus configuration
    prometheus:
      enabled: true
      prometheusSpec:
        retention: "7d"
        storageSpec: null  # Disable persistent storage
    # Lightweight Grafana without default dashboards  
    grafana:
      enabled: true
      adminPassword: admin
      defaultDashboardsEnabled: false  # Saves ~400KB
      sidecar:
        dashboards:
          enabled: false
    # Disable heavy components
    alertmanager:
      enabled: false      # Saves ~50KB
    kube-state-metrics:
      enabled: false      # Saves ~100KB
    prometheus-node-exporter:
      enabled: false      # Saves ~30KB
    defaultRules:
      create: false       # Saves ~200KB
EOF

# Deploy with minimal monitoring
helm install zoo-project-dru ./zoo-project-dru \
  --values values_argo_with_monitoring.yaml \
  --namespace zoo --create-namespace
```

**Solution 3: Post-Deployment Dashboard Addition**

Add Grafana dashboards after the initial deployment:

```bash
# 1. Deploy with minimal monitoring (Solution 2)
# 2. Add custom dashboards via ConfigMaps
kubectl create configmap argo-workflows-dashboard \
  --from-file=dashboard.json=files/argo-workflows/grafana-dashboard.json \
  --namespace zoo
kubectl label configmap argo-workflows-dashboard grafana_dashboard=1

# Grafana will automatically detect and load the dashboard
```

##### Size Optimization Summary

| Configuration | Helm Secret Size | Monitoring Level | Recommended Use |
|:-------------|:-----------------|:-----------------|:----------------|
| Full monitoring | ~970KB+ | Complete | Separate deployment |
| Minimal monitoring | ~300KB | Basic metrics only | Integrated deployment |
| No monitoring | ~240KB | None | Development only |
| Separate deployment | ~240KB + separate | Complete | **Production** |

##### Troubleshooting Size Issues

Check your deployment size before installing:
```bash
# Check template size
helm template zoo-project-dru ./zoo-project-dru \
  --values ./zoo-project-dru/values_argo.yaml | wc -c

# If > 900,000 bytes, consider using separate monitoring deployment
```

### Prometheus Node Exporter Configuration

The node-exporter component is configured for compatibility with Docker Desktop and other development environments:

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| monitoring.kube-prometheus-stack.prometheus-node-exporter.enabled | Enable node-exporter for system metrics | true |
| monitoring.kube-prometheus-stack.prometheus-node-exporter.service.port | Node exporter service port | 9101 |
| monitoring.kube-prometheus-stack.prometheus-node-exporter.service.targetPort | Node exporter target port | 9101 |
| monitoring.kube-prometheus-stack.prometheus-node-exporter.extraArgs | Additional node exporter arguments | ["--web.listen-address=0.0.0.0:9101"] |
| monitoring.kube-prometheus-stack.prometheus-node-exporter.prometheus.monitor.enabled | Enable Prometheus monitoring | true |
| monitoring.kube-prometheus-stack.kube-state-metrics.enabled | Enable kube-state-metrics for Kubernetes metrics | true |

### Grafana Dashboard Configuration

The chart includes optimized Grafana dashboards with real-time synchronization:

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| monitoring.grafana.dashboards.enabled                   | Enable custom Argo Workflows dashboards | true |
| monitoring.grafana.dashboards.refresh                   | Dashboard auto-refresh interval | "5s" |
| monitoring.grafana.dashboards.maxDataPoints             | Maximum data points for real-time charts | 300 |
| monitoring.grafana.dashboards.timeWindows.default       | Default time window for dashboards | "5m" |
| monitoring.grafana.dashboards.timeWindows.options       | Available time window options | ["5m", "15m", "30m", "1h", "6h"] |

### Local Development Optimizations

For local environments (Docker Desktop, Minikube), the chart automatically applies optimizations:

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| monitoring.disableProblematicTargets                    | Disable inaccessible Kubernetes component targets | true |
| monitoring.prometheus.nodeExporter.dockerDesktopMode    | Enable Docker Desktop compatibility mode | true |
| monitoring.prometheus.serviceMonitor.autoPatching       | Enable automatic ServiceMonitor patching | true |

**Docker Desktop Compatibility**: The chart automatically patches problematic targets by:
- Disabling kube-scheduler, kube-proxy, etcd, and kube-controller-manager targets that cause "connection refused" errors
- Using port 9101 for node-exporter instead of the default 9100 to avoid conflicts
- Applying post-install patches to remove unsupported mount configurations
- Automatic cleanup of completed patch jobs after 5 minutes

**ServiceMonitor Patching**: When `monitoring.disableProblematicTargets` is enabled, a post-install job automatically:
- Patches kube-prometheus-stack ServiceMonitors to disable problematic endpoints
- Corrects node-exporter port configuration
- Ensures clean monitoring stack deployment without connection errors

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| monitoring.kube-prometheus-stack.prometheus-node-exporter.enabled | Enable node-exporter for system metrics | true |
| monitoring.kube-prometheus-stack.prometheus-node-exporter.service.port | Node exporter service port | 9101 |
| monitoring.kube-prometheus-stack.prometheus-node-exporter.service.targetPort | Node exporter target port | 9101 |
| monitoring.kube-prometheus-stack.prometheus-node-exporter.extraArgs | Additional node exporter arguments | ["--web.listen-address=0.0.0.0:9101"] |
| monitoring.kube-prometheus-stack.prometheus-node-exporter.prometheus.monitor.enabled | Enable Prometheus monitoring | true |

**Docker Desktop Compatibility**: The chart automatically patches node-exporter for Docker Desktop compatibility by:
- Using port 9101 instead of the default 9100 to avoid conflicts
- Applying post-install patches to remove unsupported mount configurations
- Cleaning up completed patch jobs automatically after 5 minutes


### ingress

Defines the ingress through which the `zoo-dru` service is exposed for access outside of the cluster.

In addition, the values specified here are used to derive the service URL that `zoo-dru` uses to reference its own resources - for example, the URLs returned in API responses regarding the location of job status and processing results, etc. Accordingly, the service URL is deduced in the following order of priority...
* `ingress.hosturl` (if specified)
* `ingress.hosts.host[0]` if `ingress.enabled: true`
* `http://localhost:8080` if all else fails

| Name | Descriptoin | Value |
|:-----|:------------|:------|
| ingress.enabled | Enables creation of ingress resource for the `zoo-dru` service.<br>In the case that `enabled: false` is set, then other values (with the exception of `hosturl`) do not apply | `false` |
| ingress.hosturl | (optional) The URL through which the `zoo-dru` service is externally exposed.<br>_See explanation in preamble above._ | _not specified_ |
| ingress.className | Identifies the class of ingress controller that should satisfy the ingress request | "" |
| ingress.annotations | Additional parameters that are passed as configuration to the ingress controller that satisfies the ingress.<br>_See documentation of specific ingress controller for details._  | {} |
| ingress.hosts | Array of one or more host specifications that provide ingress rules | _see following items_ |
| ingress.hosts[n].host | Hostname to match for the ingress rule | `chart-example.local` |
| ingress.hosts[n].paths | Array of paths to match for the ingress rule | _see following items_ |
| ingress.hosts[n].paths[m].path | Path to match for the ingress rule | `/` |
| ingress.hosts[n].paths[m].pathType | Paths matching policy for the ingress rule | `ImplementationSpecific` |
| ingress.tls | (optional) Array of zero or more specifications providing details of TLS certificate to be used for specific hostnames | []<br>_see following items_ |
| ingress.tls[n].hosts | Array of hostnames to be associated with the TLS certificate | _not specified_ |
| ingress.tls[n].secretName | Name of secret that holds the TLS certificate | _not specified_ |


### customConfig

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| customConfig.main                                    | Optional sections to include in the main.cfg file.             | {}                                                              |

The customConfig can be used to define new section in the ZOO-Project-DRU `main.cfg` configuration file.

The sections that will be passed per default are the following:

 * `additional_parameters`: corresponds to the `workflow.additionalInputs` parameter, used to provide parameters for accessing the S3 bucket foir storing results,
 * `pod_env_vars`: corresponds to the `workflow.env` parameter, used to define specific environmenet variables for the pod executing workflow steps,
 * `pod_node_selector`: corresponds to the `workflow.nodeSelector` parameter, used to define specific node selection constraints.

The syntaxe should use the key-value pairs definition is in the example below (cf. [main.cfg](https://zoo-project.github.io/docs/kernel/configuration.html#default-main-cfg)):

````yaml
customConfig.main.mySection: |-
  myKey=myValue
  mySecondKey=mySecondValue
````

All these sections will be added to the `sections_list` from the `servicesNamespace` section.

### Advanced Usage

#### Working with KEDA and Worker Protection

When KEDA is enabled, the system provides intelligent protection for running jobs:

##### Monitoring Worker Status

Check the status of pods and their associated workers:

```bash
# View pod annotations showing worker count
kubectl get pods -n zoo -l app.kubernetes.io/name=zoo-project-dru-zoofpm -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.annotations.zoo-project\.org/active-workers}{"\t"}{.metadata.annotations.zoo-project\.org/protected}{"\n"}{end}'

# Check ScaledObject status
kubectl get scaledobjects -n zoo

# View eviction controller logs
kubectl logs -n zoo deployment/zoo-project-dru-eviction-controller --tail=50
```

##### Understanding Protection Annotations

The system uses several annotations to manage pod protection:

- `zoo-project.org/active-workers`: Number of active workers on this pod
- `zoo-project.org/protected`: Whether the pod is protected from deletion (`true`/`false`)
- `zoo-project.org/last-check`: Timestamp of last worker status check
- `zoo-project.org/emergency-delete`: Emergency override for forced deletion

##### Emergency Pod Deletion

If you need to force delete a protected pod:

```bash
# Add emergency annotation to bypass protection
kubectl annotate pod <pod-name> -n zoo zoo-project.org/emergency-delete=true

# Then delete the pod
kubectl delete pod <pod-name> -n zoo
```

##### Scaling Behavior

The system implements intelligent scaling:

1. **Scale-up**: Triggered by PostgreSQL worker count or RabbitMQ queue length
2. **Protection**: Pods with active workers are automatically protected
3. **Scale-down**: Only pods without active workers can be terminated
4. **Scale-to-zero**: When no workers are active, all pods can be terminated after grace period



### Notification using Knative

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| notification.enabled                                    | Define if notification using Knative CloudEvents should be activated             | false                                      |
| notification.ksink                                    | Define the ksink to use to send [CloudEvents](https://cloudevents.io/)             | {"kind":"Broker","namespace":"default","name":"default"}                                      |

You can refer to the tutorial available [here](https://knative.dev/docs/install/operator/knative-with-operators/) to install by using the Knative Operator.
We provide below an example of deployment with the default values set in the `values.yaml`.

#### Setup the required components

````bash
helm repo add knative-operator https://knative.github.io/operator
helm install knative-operator --create-namespace --namespace knative-operator knative-operator/knative-operator
kubectl config set-context --current --namespace=knative-operator
kubectl get deployment knative-operator
kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: knative-serving
---
apiVersion: operator.knative.dev/v1beta1
kind: KnativeServing
metadata:
  name: knative-serving
  namespace: knative-serving
spec:
  config:
    network:
      ingress-class: kourier.ingress.networking.knative.dev
  ingress:
    kourier:
      enabled: true
EOF
kubectl get deployment -n knative-serving
kubectl --namespace knative-serving get service kourier
kubectl get KnativeServing knative-serving -n knative-serving
````

After some time, you should see the following output for the last command:

````bash
NAME               VERSION   READY   REASON
knative-serving   1.18.0    True
````

You can proceed with deploying `knative-eventing`.

````bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: knative-eventing
---
apiVersion: operator.knative.dev/v1beta1
kind: KnativeEventing
metadata:
  name: knative-eventing
  namespace: knative-eventing
EOF
kubectl get deployment -n knative-eventing
kubectl get KnativeEventing knative-eventing -n knative-eventing
````

After some time, you should see the following output for the last command:

````bash
NAME               VERSION   READY   REASON
knative-eventing   1.18.1    True    
````

Then, it means everything is in place and you can now proceed with creating the Broker then the trigger.

````bash
kubectl apply -f - <<EOF
apiVersion: eventing.knative.dev/v1
kind: Broker
metadata:
  name: default
  namespace: default
EOF
````

#### Enable notifications

From there, you are able to deploy the ZOO-Project-DRU with the `notifications.enabled` parameter set to true in your `values.yaml` file.

The following settings should work properly with the setup illustrated here. The `ksink` attributes are the values defined per default.

````yaml
notifications:
  enabled: true
  ksink:
    kind: Broker
    namespace: default
    name: default
````

#### Debugging

In case you want to display the CloudEvents received by the broker for debugging purpose, you can use the commands below.

````bash
kn service create event-display --image gcr.io/knative-releases/knative.dev/eventing/cmd/event_display -n default --scale-min 1
kn trigger create mytrigger --broker default --sink ksvc:event-display -n default
````

Then, using the command below, you can get the pod name to access its log (using `kubectl logs -f <POD_NAME> -n default`).

````bash
kubectl get pods -n default
````

## Troubleshooting

### Common Migration Issues

**Helm secret size limit exceeded**:
```bash
# Error: Secret "sh.helm.release.v1.zoo-project-dru.v1" is invalid: 
# data: Too long: must have at most 1048576 bytes

# Common causes: Full monitoring stack (~670KB), Large dashboards, Complex configurations

# Solution 1: Use optimized values with disabled optional components
helm install zoo-project-dru ./zoo-project-dru \
  --values ./zoo-project-dru/values_minikube.yaml \
  --namespace zoo --create-namespace

# Solution 2: Deploy monitoring separately (recommended for full features)
# See "Helm Secret Size Limitations and Monitoring Deployment Strategies" section above
```

**PostgreSQL connection issues after migration**:
```bash
# Check if PostgreSQL is running with new image
kubectl get pods -n zoo -l app.kubernetes.io/name=zoo-project-dru-postgresql

# Check initialization logs
kubectl logs -n zoo deployment/zoo-project-dru-postgresql --tail=50

# Verify database creation
kubectl exec -it -n zoo deployment/zoo-project-dru-postgresql -- psql -U zoo -d zoo -c "\dt"
```

**RabbitMQ setup issues**:
```bash
# Check auto-setup job completion
kubectl get jobs -n zoo -l app.kubernetes.io/component=rabbitmq-setup

# Check management plugin status
kubectl port-forward -n zoo svc/zoo-project-dru-rabbitmq 15672:15672
# Access: http://localhost:15672 (zoo/CHANGEME)

# Verify queue creation
kubectl logs -n zoo -l app.kubernetes.io/component=rabbitmq-setup
```

### KEDA-Specific Issues

#### Common KEDA Issues

**Pods not scaling to zero:**
```bash
# Check if pods have active workers
kubectl describe pods -n zoo -l app.kubernetes.io/name=zoo-project-dru-zoofpm

# Check ScaledObject configuration
kubectl describe scaledobject -n zoo

# Verify eviction controller is running
kubectl get pods -n zoo -l app.kubernetes.io/component=eviction-controller
```

**Protection not working:**
```bash
# Check Kyverno policies (if enabled)
kubectl get clusterpolicy

# Test pod deletion (dry run)
kubectl delete pod <pod-name> -n zoo --dry-run=server

# Check eviction controller permissions
kubectl auth can-i patch pods --as=system:serviceaccount:zoo:zoo-project-dru-eviction-controller -n zoo
```

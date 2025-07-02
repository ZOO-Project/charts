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

## Installing the Chart

To install the chart with the release name `my-zoo-project-dru`:

````bash
helm repo add zoo-project https://zoo-project.github.io/charts/
helm install my-zoo-project-dru zoo-project/zoo-project-dru --version 0.5.0
````

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

See the reference [PostgreSQL chart documentation](https://artifacthub.io/packages/helm/bitnami/postgresql#global-parameters) for other options.

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

### Dependencies

#### PostgreSQL

See the reference [PostgreSQL chart documentation](https://artifacthub.io/packages/helm/bitnami/postgresql) for more parameters.

| Name                                       | Description                                                     | Value                    |
|:-------------------------------------------|:----------------------------------------------------------------|:-------------------------|
| postgresql.defineEnvironmentVariables      | Set it to true to get PostgreSQL environment variables defined  | false                    |
| postgresql.enabled                         | Is database used to store process execution status              | true                     |
| postgresql.primary.initdb.scriptsConfigMap | The init script config map                                      | true                     |

When `postgresql.defineEnvironmentVariables` is set to true, the environment variables for PostgreSQL (`PGHOST`,`PGPORT`,`PGUSER`,`PGPASSWORD`,`PGDATABASE`) will be defined for the ZOO-Kernel and the ZOO-FPM pods.

If an environment variable for PostgreSQL is available from the ZOO-Kernel or ZOO-FPM pods, it means that the database setting will use these variables rather than the one defined in the `main.cfg` available from the configmap.

#### RabbitMQ

See the reference [RabbitMQ chart documentation](https://artifacthub.io/packages/helm/bitnami/rabbitmq) for more parameters.

| Name                                       | Description                                              | Value                                        |
|:-------------------------------------------|:---------------------------------------------------------|:---------------------------------------------|
| rabbitmq.auth.username                     | User that will be used to connect to RabbitMQ            | RABBITMQ_USERNAME                            |
| rabbitmq.auth.password                     | Password for the user                                    | CHANGEME                                     |
| rabbitmq.loadDefinition.enabled            | Enable loading a RabbitMQ definitions file to configure RabbitMQ                               | true                                         |
| rabbitmq.loadDefinition.existingSecret     | Existing secret with the load definitions file                              | load-definition                              |
| rabbitmq.extraConfiguration                | Configuration file content: extra configuration to be appended to RabbitMQ configuration                              | load_definitions = /app/load_definition.json |

#### MinIO

See the reference [MinIO chart documentation](https://artifacthub.io/packages/helm/bitnami/minio) for more parameters.

| Name          | Description                                          | Value |
|:--------------|:-----------------------------------------------------|:------|
| minio.enabled | Is MinIO used for storage in place of AWS            | false |
| minio.defaultBuckets | Comma, semi-colon or space separated list of buckets to create at initialization (only in standalone mode)            | "processingresults" |
| minio.fullnameOverride | String to fully override the MinIO's common.names.fullname template            | "s3-service" |


#### Redis

See the reference [Redis chart documentation](https://artifacthub.io/packages/helm/bitnami/redis) for more parameters.

| Name          | Description                                          | Value |
|:--------------|:-----------------------------------------------------|:------|
| redis.enabled | Is Redis used by the current deployment              | false |
| redis.replica.replicaCount | Number of Redis replica                 | 1     |
| redis.auth.enabled | Number of Redis replica                         | false |


### CookieCutter

| Name                     | Description                                          | Value                                               |
|:-------------------------|:-----------------------------------------------------|:----------------------------------------------------|
| cookiecutter.templateUrl | Where to download the cookiecutter from              | https://github.com/EOEPCA/proc-service-template.git |
| cookiecutter.templateBranch         | The branch to fetch the cookiecutter (optional)    | undefined                    |

### ZOO-Project

| Name                             | Description                                                        | Value                                                |
|:---------------------------------|:-------------------------------------------------------------------|:-----------------------------------------------------|
| zoo.rabbitmq.definitions         | The `definition.json` file containing initial RabbitMQ settings    | "files/rabbitmq/definitions.json"                    |
| zookernel.env                    | The environment variables defined in the main.cfg `env` section    | {}                    |
| zookernel.extraMountPoints         | In case you add files in one or more `files/<DIR>` subdirectories and want to access them from the ZOO-Kernel     | []                    |
| zoofpm.extraMountPoints         | In case you add files in one or more `files/<DIR>` subdirectories and want to access them from the ZOO-FPM     | []                    |
 

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

#### WES support

ZOO-Project-DRU can execute CWL workflows through the toil Workflow Execution Service (WES).
See [reference documentation](https://zoo-project.github.io/zoo-wes-runner/) for more informations.

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| workflow.inputs.WES_URL                                    | The toil Workflow Execution Service (WES) URL | "http://192.168.1.59:8100/ga4gh/wes/v1/" |
| workflow.inputs.WES_USER                               | The user name to authenticate to access the WES | "test" |
| workflow.inputs.WES_PASSWORD                          | The password to authenticate to access the WES | `"$$2y$$12$$ci.4U63YX83CwkyUrjqxAucnmi2xXOIlEF6T/KdP9824f1Rf1iyNG"` |


#### Argo support

ZOO-Project-DRU can execute CWL workflows through Argo Workflow.
See [reference documentation](https://github.com/EOEPCA/zoo-argowf-runner) for more informations.

| Name                                                     | Description                        | Value                                                                 |
|:---------------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| workflow.argo.enabled                                    | Activate Argo support by setting this to `true` | true |
| workflow.argo.storageClass                               | The storage class to use for temporary data | standard |
| workflow.argo.defaultVolumeSize                          | The default volume size | "12Gi" |
| workflow.argo.defaultMaxRam                              | The default maximum allocated ram | "2Gi" |
| workflow.argo.wfServer                                   | The Argo server URL  | "http://argo-server.ns1.svc.cluster.local:2746" |
| workflow.argo.wfToken                                    | The Argo server token | "aaaabbbbccccdddd" |
| workflow.argo.wfSynchronizationCm                        | The configmap name | "semaphore-argo-cwl-runner-stage-in-out" |
| workflow.argo.CwlRunnerTemplare                          | The workflow name (available from the Argo workflow templates) to use as CWL Runner Template  | "argo-cwl-runner-stage-in-out" |
| workflow.argo.CwlRunnerEndpoint                          | The entry point to use from the CWL Runner Template | "calrissian-runner" |


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
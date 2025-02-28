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

````
helm repo add zoo-project https://zoo-project.github.io/charts/
helm install my-zoo-project-dru zoo-project/zoo-project-dru --version 0.0.3
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

| Name                                       | Description                                              | Value                    |
|:-------------------------------------------|:---------------------------------------------------------|:-------------------------|
| global.postgresql.auth.username            | User that will be used to connect to postgresql database | zoo                      |
| global.postgresql.auth.password            | Password for the user                                    | zoo                      |
| global.postgresql.auth.database            | Database name                                            | zoo                      |
| global.postgresql.service.ports.postgresql | PostgreSQL port                                          | "5432"                   |

### Dependencies

#### PostgreSQL

See the reference [PostgreSQL chart documentation](https://artifacthub.io/packages/helm/bitnami/postgresql) for more parameters.

| Name                                       | Description                                              | Value                    |
|:-------------------------------------------|:---------------------------------------------------------|:-------------------------|
| postgresql.enabled                         | Is database used to store process execution status       | true                     |
| postgresql.primary.initdb.scriptsConfigMap | The init script config map                               | true                     |


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
| zookernel.extraMountPoints         | In case you add files in one or more `files/<DIR>` subdirectories and want to access them from the ZOO-Kernel     | []                    |
| zoofpm.extraMountPoints         | In case you add files in one or more `files/<DIR>` subdirectories and want to access them from the ZOO-FPM     | []                    |
 

### Identity and Access Management

| Name                             | Description                                                        | Value                                                |
|:---------------------------------|:-------------------------------------------------------------------|:-----------------------------------------------------|
| iam.enabled | The Identity and Access Management (IAM)                        | true |
| iam.openIdConnectUrl | The OpenIDConnect configuration URL                    | https://testbed19.geolabs.fr:8099/realms/ZOO_DEMO/.well-known/openid-configuration |
| iam.type | The IAM type                        | openIdConnect |
| iam.name | The IAM name                        | OpenIDAuth |
| iam.realm | The realm associated with the IAM | Secured section |
| iam.clientId | The clientId to access the IAM (optional) | undefined |
| iam.clientSecret | The clientSecret to access the IAM (optional) | undefined |
| iam.userinfoUrl | The userInfo url to access the user details from the IAM (optional) | undefined |

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
| workflow.storageClass                                    | The storage class used             | standard                                                              |
| workflow.defaultVolumeSize                               | The default volume size allocated  | 10190                                                                 |
| workflow.defaultMaxRam                                   | The default max ram allocated      | 1024                                                                  |
| workflow.defaultMaxCores                                 | The default max cores allocated    | 2                                                                     |
| workflow.calrissianImage                                 | The calrissian image version       | "terradue/calrissian:0.12.0"                                          |
| workflow.additionalInputs                                 | The additiona inputs        | {}                                          |
| workflow.imagePullSecrets                                | ImagePullSecrets is an optional list of references to secrets for the processing namespace to use for pulling any of the images used by the processing pods. If specified, these secrets will be passed to individual puller implementations for them to use. For example, in the case of docker, only DockerConfig type secrets are honored. More info: https://kubernetes.io/docs/concepts/containers/images#specifying-imagepullsecrets-on-a-pod       | []                                          |
| workflow.nodeSelector                                    | Constrain on which nodes the processing pods are eligible to run based on the node label       | {}                                          |
| workflow.env                                             | Environmental variables for the processing pods       | {}                                          |


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

 * additional_parameters: used to provide parameters for accessing the S3 bucket foir storing results,
 * pod_env_vars: used to define specific environmenet variables for the pod executing workflow steps,
 * pod_node_selector: used to define specific node selection constraints (cf. [nodeSelector](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector)).

The syntaxe should use the key-value pairs definition is in the example below (cf. [main.cfg](https://zoo-project.github.io/docs/kernel/configuration.html#default-main-cfg)):

`````
customConfig.main.additional_parameters: |-
  s3_bucket=bucket-name
  region_name=region-name
  aws_secret_access_key=secret-access-key
  aws_access_key_id=access-key
  endpoint_url=endpoint:port
`````


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

### PostgreSQL

| Name                                       | Description                                              | Value                    |
|:-------------------------------------------|:---------------------------------------------------------|:-------------------------|
| postgresql.enabled                         | Is database used to store process execution status       | true                     |
| postgresql.primary.initdb.scriptsConfigMap | The init script config map                               | true                     |


### RabbitMQ

| Name                                       | Description                                              | Value                                        |
|:-------------------------------------------|:---------------------------------------------------------|:---------------------------------------------|
| rabbitmq.auth.username                     | User that will be used to connect to RabbitMQ            | RABBITMQ_USERNAME                            |
| rabbitmq.auth.password                     | Password for the user                                    | CHANGEME                                     |
| rabbitmq.loadDefinition.enabled            | Enable loading a RabbitMQ definitions file to configure RabbitMQ                               | true                                         |
| rabbitmq.loadDefinition.existingSecret     | Existing secret with the load definitions file                              | load-definition                              |
| rabbitmq.extraConfiguration                | Configuration file content: extra configuration to be appended to RabbitMQ configuration                              | load_definitions = /app/load_definition.json |

### MinIO

| Name          | Description                                          | Value |
|:--------------|:-----------------------------------------------------|:------|
| minio.enabled | Is MinIO used for storage in place of AWS            | false |


### CookieCutter

| Name                     | Description                                          | Value                                               |
|:-------------------------|:-----------------------------------------------------|:----------------------------------------------------|
| cookiecutter.templateUrl | Where to download the cookiecutter from              | https://github.com/EOEPCA/proc-service-template.git |
| cookiecutter.templateBranch         | The branch to fetch the cookiecutter (optional)    | undefined                    |

### ZOO-Project

| Name                             | Description                                                        | Value                                                |
|:---------------------------------|:-------------------------------------------------------------------|:-----------------------------------------------------|
| zoo.rabbitmq.definitions         | The `definition.json` file containing initial RabbitMQ settings    | "files/rabbitmq/definitions.json"                    |


### Identity and Access Management

| Name                             | Description                                                        | Value                                                |
|:---------------------------------|:-------------------------------------------------------------------|:-----------------------------------------------------|
| iam.enabled | The Identity and Access Management (IAM)                        | true |
| iam.openIdConnectUrl | The OpenIDConnect configuration URL                    | https://testbed19.geolabs.fr:8099/realms/ZOO_DEMO/.well-known/openid-configuration |
| iam.type | The IAM type                        | openIdConnect |
| iam.name | The IAM name                        | OpenIDAuth |
| iam.realm | The realm associated with the IAM                        | Secured section |

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
| workflow.imagePullSecrets                                | ImagePullSecrets is an optional list of references to secrets for the processing namespace to use for pulling any of the images used by the processing pods. If specified, these secrets will be passed to individual puller implementations for them to use. For example, in the case of docker, only DockerConfig type secrets are honored. More info: https://kubernetes.io/docs/concepts/containers/images#specifying-imagepullsecrets-on-a-pod       | []                                          |
| workflow.nodeSelector                                    | Constrain on which nodes the processing pods are eligible to run based on the node label       | {}                                          |
| workflow.env                                             | Environmental variables for the processing pods       | {}                                          |






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
| rabbitmq.loadDefinition.enabled            | The init script config map                               | true                                         |
| rabbitmq.loadDefinition.existingSecret     | The init script config map                               | load-definition                              |
| rabbitmq.extraConfiguration                | The init script config map                               | load_definitions = /app/load_definition.json |

### MinIO

| Name          | Description                                          | Value |
|:--------------|:-----------------------------------------------------|:------|
| minio.enabled | Is MinIO used for storage in place of AWS            | false |

### CookieCutter

| Name                     | Description                                          | Value                                               |
|:-------------------------|:-----------------------------------------------------|:----------------------------------------------------|
| cookiecutter.templateUrl | Where to download the cookiecutter from              | https://github.com/EOEPCA/proc-service-template.git |

### ZOO-Project

| Name                             | Description                                                        | Value                                                |
|:---------------------------------|:-------------------------------------------------------------------|:-----------------------------------------------------|
| zoo.kernel.maincfgtpl            | The main.cfg file to use as configuration for the ZOO-Project      | "files/zoo-kernel/main.cfg.tpl"                      |
| zoo.kernel.oas                   | The oas.cfg file to use as OpenAPI definitions for the ZOO-Project | "files/zoo-kernel/oas.cfg"                           |
| zoo.kernel.htaccess              | The htaccess file to store in Apache root folder                   | "files/zoo-kernel/htaccess"                          |
| zoo.openapi.startupsh            | The `startUp.sh` script to start the ZOO-FPM                       | "files/openapi/server/startUp.sh"                    |
| zoo.rabbitmq.rabbitmq            | The `definition.json` file containing initial RabbitMQ settings    | "files/rabbitmq/definitions.json"                    |
| zoo.services.cookiecutter_config | The `cookiecutter_config.yaml` file to uses                        | "files/zoo-services/assets/cookiecutter_config.yaml" |

### Workflow

| Name                                           | Description                        | Value                                                                 |
|:-----------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------|
| workflow.storageClass                          | The storage class used             | standard                                                              |
| workflow.defaultVolumeSize                     | The default volume size allocated  | 10190                                                                 |
| workflow.defaultMaxRam                         | The default max ram allocated      | 1024                                                                  |
| workflow.defaultMaxCores                       | The default max cores allocated    | 2                                                                     |
| workflow.calrissianImage                       | The calrissian image version       | "terradue/calrissian:0.12.0"                                          |
| workflow.inputs.APP                            | The application name               | zoo-project-dru                                                       |
| workflow.inputs.STAGEIN_AWS_REGION             | The stagein AWS region             | RegionOne                                                             |
| workflow.inputs.STAGEIN_AWS_ACCESS_KEY_ID      | The stagein AWS access key id      | minio-admin                                                           |
| workflow.inputs.STAGEIN_AWS_SECRET_ACCESS_KEY  | The stagein AWS secret access key  | minio-secret-password                                                 |
| workflow.inputs.STAGEIN_AWS_SERVICE_URL        | The stagein AWS service url        | http://zoo-project-dru-minio.zp.svc.cluster.local:9000                |
| workflow.inputs.STAGEOUT_AWS_REGION            | The stageout AWS region            | RegionOne                                                             |
| workflow.inputs.STAGEOUT_AWS_ACCESS_KEY_ID     | The stageout AWS access key id     | minio-admin                                                           |
| workflow.inputs.STAGEOUT_AWS_SECRET_ACCESS_KEY | The stageout AWS secret access key | minio-secret-password                                                 |
| workflow.inputs.STAGEOUT_AWS_SERVICE_URL       | The stageout AWS secret access key | [minio-admin](http://zoo-project-dru-minio.zp.svc.cluster.local:9000) |
| workflow.inputs.STAGEOUT_OUTPUT                | The location where to store output | s3://processingresults                                                |






# EOEPCA BiDS 2023 workshop 

> The **ZOO-Project** is an open source processing platform, released under MIT/X11 Licence.

[Overview of ZOO-Project](http://zoo-project.org)

Trademarks: This software listing is packaged by the ZOO-Project developper team. The respective trademarks mentioned in the offering are owned by the respective companies, and use of them does not imply any affiliation or endorsement.

## Introduction

This chart bootstraps a [ZOO-Project](http://zoo-project.org) deployment dedicated to the EOEPCA workshop held in BiDS 2023 conference on a cluster using the [Helm](https://helm.sh/) package manager.

## Prerequisites

 * Kubernetes 1.19+
 * Helm 3.2.0+
 * PV provisioner support in the underlying infrastructure

## Installing the Chart

To install the chart with the release name `my-zoo-project`:

````
helm repo add zoo-project https://zoo-project.github.io/charts/
helm install my-zoo-project zoo-project/zoo-project-workshop --version 0.0.7 -n zoo --create-namespace
````

## Parameters

See the parameters from the [ZOO-Project-DRU](https://artifacthub.io/packages/helm/zoo-project/zoo-project-dru) dependency.
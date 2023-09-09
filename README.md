# charts
![example workflow](https://github.com/ZOO-Project/charts/actions/workflows/publish-charts.yml/badge.svg)
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


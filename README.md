# charts
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


x\{{/*
Expand the name of the chart.
*/}}
{{- define "zoo-project-dru.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "zoo-project-dru.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "zoo-project-dru.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "zoo-project-dru.labels" -}}
helm.sh/chart: {{ include "zoo-project-dru.chart" . }}
{{ include "zoo-project-dru.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "zoo-project-dru.selectorLabels" -}}
app.kubernetes.io/name: {{ include "zoo-project-dru.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "zoo-project-dru.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "zoo-project-dru.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}



{{- define "zoo-project-dru.release_name" -}}
{{- default .Release.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "zoo-project-dru.hosturl" -}}
{{- if .Values.ingress.hosturl }}
  {{- .Values.ingress.hosturl }}
{{- else }}
  {{- if .Values.ingress.enabled }}
    {{- with (first .Values.ingress.hosts) }}
    {{- printf "https://%s" .host }}
    {{- end }}
  {{- else }}
    {{- "http://localhost:8080" }}
  {{- end }}
{{- end }}
{{- end }}

{{- define "zoo-project-dru.hosturlws" -}}
{{- $hosturl := include "zoo-project-dru.hosturl" . }}
{{- $hosturlParsed := urlParse $hosturl }}
{{- $scheme := index $hosturlParsed "scheme" }}
{{- $scheme := replace "http" "ws" $scheme }}
{{- $host := index $hosturlParsed "host" }}
{{- printf "%s://%s:8888" $scheme $host }}
{{- end }}

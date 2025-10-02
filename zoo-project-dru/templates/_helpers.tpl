{{/*
Expand the name of the chart.
*/}}
{{- define "zoo-project-dru.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Redis service name  
*/}}
{{- define "zoo-project-dru.redis.servicename" -}}
{{- include "zoo-project-dru.fullname" . }}-redis-service
{{- end }}

{{/*
RabbitMQ Service name
*/}}
{{- define "zoo-project-dru.rabbitmq.serviceName" -}}
{{- include "zoo-project-dru.fullname" . }}-rabbitmq
{{- end }}

{{/* fully qualified app name.
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

{{- define "zoo-project-dru.localhosturl" -}}
{{- if .Values.ingress.hosturl }}
  {{- .Values.ingress.hosturl }}
{{- else }}
  {{- if .Values.ingress.enabled }}
    {{- with (first .Values.ingress.hosts) }}
    {{- printf "https://%s" .host }}
    {{- end }}
  {{- else }}
    {{- "http://localhost" }}
  {{- end }}
{{- end }}
{{- end }}

{{- define "zoo-project-dru.hosturlws" -}}
{{- $hosturl := include "zoo-project-dru.hosturl" . }}
{{- $hosturlParsed := urlParse $hosturl }}
{{- $scheme := index $hosturlParsed "scheme" }}
{{- $scheme := replace "http" "ws" $scheme }}
{{- $hostOrigin := index $hosturlParsed "host" }}
{{- $host := trimAll ":8080" $hostOrigin }}
{{- printf "%s://%s:8888" $scheme $host }}
{{- end }}

{{/*
Argo Workflows MinIO endpoint helper
*/}}
{{- define "zoo-project-dru.argo.minio.endpoint" -}}
{{- $endpoint := .Values.argo.s3.endpoint | default "s3-service:9000" -}}
{{- if and (not (hasPrefix "http://" $endpoint)) (not (hasPrefix "https://" $endpoint)) -}}
{{- printf "http://%s" $endpoint -}}
{{- else -}}
{{- $endpoint -}}
{{- end -}}
{{- end }}

{{/*
Argo Workflows MinIO access key helper
*/}}
{{- define "zoo-project-dru.argo.minio.accessKey" -}}
{{- .Values.minio.rootUser | default "minio-admin" }}
{{- end }}

{{/*
Argo Workflows MinIO secret key helper
*/}}
{{- define "zoo-project-dru.argo.minio.secretKey" -}}
{{- .Values.minio.rootPassword | default "minio-secret-password" }}
{{- end }}

{{/*
RabbitMQ readiness init container
This template creates an init container that waits for RabbitMQ to be ready
with management API and definitions loaded.
*/}}
{{- define "zoo-project-dru.rabbitmq.initContainer" -}}
- name: init-wait-for-dependencies-{{ .componentName }}
  image: curlimages/curl:latest
  imagePullPolicy: IfNotPresent
  command: [ "/bin/sh" ]
  args:
    - -c
    - |
      set -e
      echo "Waiting for RabbitMQ to be ready with management API and definitions loaded..."

      while true; do
        # Check if RabbitMQ management API is accessible
        if curl -f -u {{ .Values.rabbitmq.auth.username }}:{{ .Values.rabbitmq.auth.password }} \
          http://{{ include "zoo-project-dru.rabbitmq.serviceName" . }}:15672/api/overview >/dev/null 2>&1; then

          # Check if both zoo_service_queue and unroutable_messages_queue exist
          if curl -f -u {{ .Values.rabbitmq.auth.username }}:{{ .Values.rabbitmq.auth.password }} \
            http://{{ include "zoo-project-dru.rabbitmq.serviceName" . }}:15672/api/queues/%2F/zoo_service_queue >/dev/null 2>&1 && \
            curl -f -u {{ .Values.rabbitmq.auth.username }}:{{ .Values.rabbitmq.auth.password }} \
            http://{{ include "zoo-project-dru.rabbitmq.serviceName" . }}:15672/api/queues/%2F/unroutable_messages_queue >/dev/null 2>&1; then
            echo "RabbitMQ is fully ready!"
            break
          else
            echo "RabbitMQ is up but zoo_service_queue not created yet..."
          fi
        else
          echo "Waiting for RabbitMQ management API..."
        fi
        sleep 5
      done
  env:
    - name: ZOO_RABBITMQ_HOST
      value: {{ include "zoo-project-dru.rabbitmq.serviceName" . }}
{{- end }}

{{/*
PostgreSQL service name
*/}}
{{- define "zoo-project-dru.postgresql.servicename" -}}
{{- include "zoo-project-dru.fullname" . }}-postgresql-service
{{- end }}

{{/*
KEDA PostgreSQL query ConfigMap name
*/}}
{{- define "zoo-project-dru.keda.postgresql.configmap" -}}
{{- include "zoo-project-dru.fullname" . }}-keda-postgresql-query
{{- end }}

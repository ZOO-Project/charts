{{- if and .Values.argo.enabled .Values.argo.autoTokenManagement }}
# Template to inject an initContainer that retrieves the Argo token
# To be used in the main zoo-kernel deployment

initContainers:
- name: argo-token-retriever
  image: bitnami/kubectl:latest
  command:
  - /bin/bash
  - -c
  - |
    set -e
    echo "🔑 Retrieving Argo token for zoo-kernel..."
    
    # Wait for the secret with the token to be available
    for i in {1..60}; do
      if kubectl get secret {{ include "zoo-project-dru.fullname" . }}-argo-workflows.service-account-token -n {{ .Release.Namespace }} > /dev/null 2>&1; then
        echo "✅ Secret with token found"
        break
      fi
      echo "⏳ Waiting for secret with token... ($i/60)"
      sleep 5
    done
    
    # Retrieve the token from the secret (same as dp-zoofpm.yaml)
    TOKEN=$(kubectl get secret {{ include "zoo-project-dru.fullname" . }}-argo-workflows.service-account-token -n {{ .Release.Namespace }} -o jsonpath='{.data.token}' | base64 -d)
    
    if [ -z "$TOKEN" ]; then
      echo "❌ Error: Unable to retrieve token from secret"
      exit 1
    fi
    
    echo "✅ Token retrieved successfully from secret"
    
    # Write the token to a shared file
    echo "$TOKEN" > /shared/argo-token
    chmod 644 /shared/argo-token
    
    echo "✅ Token saved to /shared/argo-token"
  volumeMounts:
  - name: shared-token
    mountPath: /shared

# Shared volume for the token
volumes:
- name: shared-token
  emptyDir: {}

# To be added to the main container's volumeMounts:
# - name: shared-token
#   mountPath: /shared
#   readOnly: true

# Environment variable for the main container:
# - name: ARGO_TOKEN_FILE
#   value: "/shared/argo-token"

{{- end }}

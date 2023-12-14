window.onload = function() {
    //<editor-fold desc="Changeable Configuration Block">
  
    // the following lines will be replaced by docker/configurator, when it runs in a docker-container
    window.ui = SwaggerUIBundle({
      {{- if .Values.ingress.enabled }}
      {{- with (first .Values.ingress.hosts) }}
      url: "https://{{ .host }}/ogc-api/api",
      {{- end }}
      {{- else }}
      url: "http://localhost:8080/ogc-api/api",
      {{- end }}
      dom_id: '#swagger-ui',
      deepLinking: true,
      presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIStandalonePreset
      ],
      plugins: [
        SwaggerUIBundle.plugins.DownloadUrl
      ],
      layout: "StandaloneLayout"
    });
  
    //</editor-fold>
  };
{
  "rabbit_version": "3.8.9",
  "rabbitmq_version": "3.8.9",
  "product_name": "RabbitMQ",
  "product_version": "3.8.9",
  "users": [
    {
      "name": "{{ .Values.rabbitmq.auth.username }}",
      "password": "{{ .Values.rabbitmq.auth.password }}",
      "tags": "administrator"
    }
  ],
  "vhosts": [
    {
      "name": "{{ .Values.rabbitmq.auth.vhost }}"
    }
  ],
  "permissions": [
    {
      "user": "{{ .Values.rabbitmq.auth.username }}",
      "vhost": "{{ .Values.rabbitmq.auth.vhost }}",
      "configure": ".*",
      "write": ".*",
      "read": ".*"
    }
  ],
  "topic_permissions": [],
  "parameters": [],
  "global_parameters": [
    {
      "name": "cluster_name",
      "value": "rabbit@{{ include "zoo-project-dru.fullname" . }}-rabbitmq"
    },
    {
      "name": "internal_cluster_id",
      "value": "rabbitmq-cluster-id-{{ randAlphaNum 32 }}"
    }
  ],
  "policies": [],
  "queues": [
    {
      "name": "zoo_service_queue",
      "vhost": "{{ .Values.rabbitmq.auth.vhost }}",
      "durable": true,
      "auto_delete": false,
      "arguments": {
        "x-queue-type": "classic"
      }
    },
    {
      "name": "unroutable_messages_queue",
      "vhost": "{{ .Values.rabbitmq.auth.vhost }}",
      "durable": true,
      "auto_delete": false,
      "arguments": {
        "x-queue-type": "classic"
      }
    }
  ],
  "exchanges": [
    {
      "name": "main_exchange",
      "vhost": "{{ .Values.rabbitmq.auth.vhost }}",
      "type": "direct",
      "durable": true,
      "auto_delete": false,
      "internal": false,
      "arguments": {
        "alternate-exchange": "unroutable_exchange"
      }
    },
    {
      "name": "unroutable_exchange",
      "vhost": "{{ .Values.rabbitmq.auth.vhost }}",
      "type": "fanout",
      "durable": true,
      "auto_delete": false,
      "internal": false,
      "arguments": {}
    }
  ],
  "bindings": [
    {
      "source": "main_exchange",
      "vhost": "{{ .Values.rabbitmq.auth.vhost }}",
      "destination": "zoo_service_queue",
      "destination_type": "queue",
      "routing_key": "zoo",
      "arguments": {}
    },
    {
      "source": "unroutable_exchange",
      "vhost": "{{ .Values.rabbitmq.auth.vhost }}",
      "destination": "unroutable_messages_queue",
      "destination_type": "queue",
      "routing_key": "",
      "arguments": {}
    }
  ]
}

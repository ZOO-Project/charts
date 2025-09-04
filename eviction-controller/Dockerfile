# Simple bash-based eviction controller
FROM alpine:3.18

# Install required tools
RUN apk --no-cache add \
    bash \
    curl \
    netcat-openbsd \
    ca-certificates \
    postgresql-client

# Install kubectl
RUN echo "Build timestamp: $(date)" && \
    ARCH=$(uname -m) && \
    if [ "$ARCH" = "aarch64" ]; then ARCH="arm64"; fi && \
    if [ "$ARCH" = "x86_64" ]; then ARCH="amd64"; fi && \
    echo "Downloading kubectl for architecture: $ARCH" && \
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/$ARCH/kubectl" && \
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && \
    rm kubectl

WORKDIR /app

# Copy the controller script
COPY run.sh /app/eviction-controller.sh
RUN chmod +x /app/eviction-controller.sh

# Create non-root user
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup && \
    mkdir -p /home/appuser && \
    chown -R appuser:appgroup /home/appuser

USER 1001

EXPOSE 8080

CMD ["/app/eviction-controller.sh"]

# Apache Kafka 3.9.0 Docker Container

Production-ready Apache Kafka with Zookeeper in a single container. Configurable host settings for any deployment environment.

## Quick Start

```bash
docker run -p 2181:2181 -p 9092:9092 -e KAFKA_HOST=localhost hatakekakashihk/kafka:latest
```

## What This Image Does

- Runs Apache Kafka 3.9.0 and Zookeeper 3.8.4 in one container
- Automatically configures advertised listeners based on `KAFKA_HOST` environment variable
- Provides production-ready configuration with data persistence
- Supports both development and production deployments

## How to Run It

### Basic Usage
```bash
# For localhost development
docker run -d --name kafka \
  -p 2181:2181 -p 9092:9092 \
  -e KAFKA_HOST=localhost \
  hatakekakashihk/kafka:latest

# For production with custom host
docker run -d --name kafka \
  -p 2181:2181 -p 9092:9092 \
  -e KAFKA_HOST=your-server.com \
  --restart unless-stopped \
  hatakekakashihk/kafka:latest
```

### Docker Compose
```yaml
version: '3.8'
services:
  kafka:
    image: hatakekakashihk/kafka:latest
    ports:
      - "2181:2181"
      - "9092:9092"
    environment:
      - KAFKA_HOST=${KAFKA_HOST:-localhost}
    restart: unless-stopped
```

## Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `KAFKA_HOST` | Hostname/IP for external connections | `localhost` |

| Port | Service |
|------|---------|
| `2181` | Zookeeper |
| `9092` | Kafka |

## Test Your Setup

```bash
# Create a topic
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh \
  --create --topic test --bootstrap-server localhost:9092

# Send a message
echo "Hello Kafka" | docker exec -i kafka /opt/kafka/bin/kafka-console-producer.sh \
  --topic test --bootstrap-server localhost:9092

# Read messages
docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh \
  --topic test --from-beginning --bootstrap-server localhost:9092
```

## Technical Details

- **Base**: Ubuntu 22.04 LTS
- **Java**: OpenJDK 21
- **Kafka**: 3.9.0 (Scala 2.13)
- **Zookeeper**: 3.8.4
- **Architectures**: AMD64, ARM64

## Links

- [GitHub Repository](https://github.com/HATAKEkakshi/Kafka)
- [Apache Kafka Docs](https://kafka.apache.org/documentation/)

---
**Maintained by:** [Hemant Kumar](https://github.com/HATAKEkakshi)
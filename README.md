# Apache Kafka Docker Container

[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-kafka--zookeeper-blue?logo=docker)](https://hub.docker.com)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](https://opensource.org/licenses/Apache-2.0)
[![Kafka Version](https://img.shields.io/badge/Kafka-3.9.0-orange)](https://kafka.apache.org/)
[![Zookeeper Version](https://img.shields.io/badge/Zookeeper-3.8.4-yellow)](https://zookeeper.apache.org/)
[![Java](https://img.shields.io/badge/Java-21-red)](https://openjdk.java.net/)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)](https://github.com)

A production-ready Docker container for Apache Kafka with Zookeeper, featuring configurable host settings and easy deployment.

## 🚀 Quick Start

### Using Docker Compose (Recommended)
```bash
KAFKA_HOST=your-host.com docker-compose up --build
```

### Using Docker CLI
```bash
docker build -t kafka-zookeeper .
docker run -p 2181:2181 -p 9092:9092 -e KAFKA_HOST=your-host.com kafka-zookeeper
```

### Pull from Docker Hub
```bash
docker pull your-username/kafka-zookeeper:latest
docker run -p 2181:2181 -p 9092:9092 -e KAFKA_HOST=localhost your-username/kafka-zookeeper:latest
```

## 📋 Features

- ✅ **Apache Kafka 3.9.0** with Zookeeper 3.8.4
- ✅ **Configurable Host Settings** via environment variables
- ✅ **Production Ready** with proper data persistence
- ✅ **Single Container** deployment for simplicity
- ✅ **Auto-configuration** of advertised listeners
- ✅ **Health Checks** and monitoring ready
- ✅ **ARM64 & AMD64** multi-architecture support

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `KAFKA_HOST` | Hostname/IP for external connections | `localhost` | No |

### Ports

| Port | Service | Description |
|------|---------|-------------|
| `2181` | Zookeeper | Client connections |
| `9092` | Kafka | Broker connections |

## 📖 Usage Examples

### Development Environment
```bash
docker run -d \
  --name kafka-dev \
  -p 2181:2181 \
  -p 9092:9092 \
  -e KAFKA_HOST=localhost \
  your-username/kafka-zookeeper:latest
```

### Production Deployment
```bash
docker run -d \
  --name kafka-prod \
  -p 2181:2181 \
  -p 9092:9092 \
  -e KAFKA_HOST=your-production-host.com \
  --restart unless-stopped \
  -v kafka-data:/opt/kafka/data \
  your-username/kafka-zookeeper:latest
```

### Docker Compose
```yaml
version: '3.8'
services:
  kafka:
    image: your-username/kafka-zookeeper:latest
    ports:
      - "2181:2181"
      - "9092:9092"
    environment:
      - KAFKA_HOST=${KAFKA_HOST:-localhost}
    volumes:
      - kafka-data:/opt/kafka/data
    restart: unless-stopped

volumes:
  kafka-data:
```

## 🧪 Testing Connection

### Using Kafka CLI Tools
```bash
# Create a topic
docker exec -it kafka-container /opt/kafka/bin/kafka-topics.sh \
  --create --topic test-topic \
  --bootstrap-server localhost:9092

# List topics
docker exec -it kafka-container /opt/kafka/bin/kafka-topics.sh \
  --list --bootstrap-server localhost:9092

# Send messages
docker exec -it kafka-container /opt/kafka/bin/kafka-console-producer.sh \
  --topic test-topic --bootstrap-server localhost:9092

# Consume messages
docker exec -it kafka-container /opt/kafka/bin/kafka-console-consumer.sh \
  --topic test-topic --from-beginning \
  --bootstrap-server localhost:9092
```

### Using FastAPI Test Application
A complete test application is included in the `test-app/` directory:

```bash
cd test-app
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Test endpoints
curl http://localhost:8000/kafka/status
curl -X POST http://localhost:8000/kafka/send \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Kafka!"}'
```

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│           Docker Container          │
├─────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐   │
│  │  Zookeeper  │  │    Kafka    │   │
│  │   :2181     │◄─┤   :9092     │   │
│  └─────────────┘  └─────────────┘   │
├─────────────────────────────────────┤
│         Ubuntu 22.04 Base          │
│         OpenJDK 21                  │
└─────────────────────────────────────┘
```

## 📁 Directory Structure

```
.
├── Configuration/           # Kafka & Zookeeper configs
│   ├── server.properties   # Kafka broker configuration
│   ├── zookeeper.properties # Zookeeper configuration
│   └── *.service           # Systemd service files
├── test-app/               # FastAPI test application
│   ├── main.py            # API endpoints
│   ├── requirements.txt   # Python dependencies
│   └── README.md          # Test app documentation
├── Dockerfile             # Container build instructions
├── docker-compose.yml     # Compose configuration
├── mankafka.sh           # Setup script
└── README.md             # This file
```

## 🔍 Health Checks

The container includes built-in health monitoring:

```bash
# Check if services are running
docker exec kafka-container ps aux | grep -E "(kafka|zookeeper)"

# Check Kafka broker status
docker exec kafka-container /opt/kafka/bin/kafka-broker-api-versions.sh \
  --bootstrap-server localhost:9092
```

## 🐛 Troubleshooting

### Common Issues

**Connection Refused**
- Ensure `KAFKA_HOST` matches your actual hostname/IP
- Check if ports 2181 and 9092 are accessible
- Verify firewall settings

**Out of Memory**
- Increase Docker memory limits
- Adjust JVM heap settings in configuration

**Topic Creation Fails**
- Wait for Kafka to fully start (30-60 seconds)
- Check Zookeeper connectivity

### Logs
```bash
# View container logs
docker logs kafka-container

# Follow logs in real-time
docker logs -f kafka-container
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Zookeeper Documentation](https://zookeeper.apache.org/doc/)
- [Docker Hub Repository](https://hub.docker.com/r/your-username/kafka-zookeeper)
- [GitHub Repository](https://github.com/your-username/kafka-docker)

## ⭐ Support

If this project helped you, please give it a ⭐ on GitHub!

---

**Maintained by:** [Your Name](https://github.com/your-username)  
**Last Updated:** $(date +%Y-%m-%d)
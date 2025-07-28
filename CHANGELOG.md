# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2025-01-28

### Fixed
- Minor issues in documentation and configuration

## [1.0.0] - 2025-01-28

### Added
- Initial release of Apache Kafka Docker container with Zookeeper
- Apache Kafka 3.9.0 with Zookeeper 3.8.4 integration
- Configurable advertised listeners via `KAFKA_HOST` environment variable
- Single container deployment running both Kafka and Zookeeper
- Automated setup script (`mankafka.sh`) for service initialization
- FastAPI test application with Kafka producer/consumer endpoints
- Docker Compose configuration for easy deployment
- Comprehensive README with professional badges and documentation

### Features
- **Production Ready**: Proper data persistence and configuration
- **Environment Variable Support**: Dynamic host configuration for different environments
- **Single Container Architecture**: Simplified deployment with both services
- **Auto-configuration**: Automatic replacement of advertised.listeners in server.properties
- **Health Monitoring**: Built-in endpoints for service status checking
- **Multi-platform Support**: Compatible with ARM64 and AMD64 architectures

### Technical Specifications
- **Base Image**: Ubuntu 22.04 LTS
- **Java Runtime**: OpenJDK 21
- **Kafka Version**: 3.9.0 (Scala 2.13)
- **Zookeeper Version**: 3.8.4
- **Exposed Ports**: 
  - 2181 (Zookeeper client connections)
  - 9092 (Kafka broker connections)
- **Data Directories**: 
  - `/root/kafka_2.13-3.9.0/Data/kafka` (Kafka logs)
  - `/root/kafka_2.13-3.9.0/Data/zookeeper` (Zookeeper data)

### Configuration Files
- `Configuration/server.properties` - Kafka broker configuration with placeholder support
- `Configuration/zookeeper.properties` - Zookeeper server configuration
- `Configuration/*.service` - Systemd service files (for reference)
- `docker-compose.yml` - Container orchestration configuration
- `Dockerfile` - Container build instructions

### Test Application
- FastAPI-based test application in `test-app/` directory
- Endpoints for Kafka connection testing, message sending, and status monitoring
- Uses confluent-kafka library for reliable Kafka integration
- Simple REST API for testing Kafka functionality

### Usage Examples
```bash
# Quick start with custom host
KAFKA_HOST=your-host.com docker-compose up --build

# Direct Docker run
docker run -p 2181:2181 -p 9092:9092 -e KAFKA_HOST=localhost kafka-setup
```

### Documentation
- Professional README with badges and comprehensive examples
- Architecture diagrams and directory structure
- Troubleshooting guide and common issues
- API documentation for test application
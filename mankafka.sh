#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# Update profile if exists
if [ -f /tmp/profile ]; then
    cp /tmp/profile /etc/profile
    source /etc/profile
fi

# Copy Kafka and ZooKeeper configs
cp /root/Kafka/Configuration/zookeeper.properties /root/zookeeper.properties
cp /root/Kafka/Configuration/server.properties /root/server.properties
cp /root/Kafka/Configuration/kafka-server-start.sh /root/kafka-server-start.sh
# Copy systemd service files
cp /root/Kafka/Configuration/kafka.service /etc/systemd/system/kafka.service
cp /root/Kafka/Configuration/zookeeper.service /etc/systemd/system/zookeeper.service

# Install Java and wget
apt update -y
apt install -y openjdk-21-jdk wget

# Download and extract Kafka
cd /root
wget -q https://dlcdn.apache.org/kafka/3.9.0/kafka_2.13-3.9.0.tgz
tar -xzf kafka_2.13-3.9.0.tgz

# Configure Kafka and ZooKeeper
cp /root/zookeeper.properties /root/kafka_2.13-3.9.0/config/zookeeper.properties
# Replace KAFKA_HOST_PLACEHOLDER with environment variable
sed "s|KAFKA_HOST_PLACEHOLDER|${KAFKA_HOST:-localhost}|g" /root/server.properties > /root/kafka_2.13-3.9.0/config/server.properties
cp /root/kafka-server-start.sh /root/kafka_2.13-3.9.0/bin/kafka-server-start.sh
# Create data directories
mkdir -p /root/kafka_2.13-3.9.0/Data/zookeeper
mkdir -p /root/kafka_2.13-3.9.0/Data/kafka

# Start Zookeeper in background
echo "####################################### Starting Zookeeper #######################################"
/root/kafka_2.13-3.9.0/bin/zookeeper-server-start.sh /root/kafka_2.13-3.9.0/config/zookeeper.properties &

# Wait for Zookeeper to start
sleep 10

echo "####################################### Starting Kafka #######################################"
# Start Kafka (this will run in foreground to keep container alive)
/root/kafka_2.13-3.9.0/bin/kafka-server-start.sh /root/kafka_2.13-3.9.0/config/server.properties

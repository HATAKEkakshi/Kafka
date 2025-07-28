FROM ubuntu:22.04

# Set environment variable with default value
ENV KAFKA_HOST=localhost

# Copy all configuration files and scripts
COPY . /root/Kafka/

# Copy the setup script and make it executable
COPY mankafka.sh /root/mankafka.sh
RUN chmod +x /root/mankafka.sh

# Expose ports
EXPOSE 2181 9092

# Run the setup script
CMD ["/root/mankafka.sh"]
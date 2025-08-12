# Kafka Producer & Consumer Integration Guide

## 🚀 Quick Setup

### 1. Start Kafka Container
```bash
# Using Docker Compose
KAFKA_HOST=localhost docker-compose up -d

# Or using Docker CLI
docker run -d --name kafka -p 2181:2181 -p 9092:9092 -e KAFKA_HOST=localhost hatakekakashihk/kafka:latest
```

### 2. Install Dependencies
```bash
# For confluent-kafka (recommended)
pip install confluent-kafka

# For kafka-python (alternative)
pip install kafka-python
```

## 📤 Producer Setup

### Basic Producer (confluent-kafka)
```python
from confluent_kafka import Producer
import json

def create_producer():
    config = {
        'bootstrap.servers': 'localhost:9092',
        'client.id': 'my-producer'
    }
    return Producer(config)

def send_message(producer, topic, message):
    producer.produce(topic, json.dumps(message).encode('utf-8'))
    producer.flush()  # Wait for delivery

# Usage
producer = create_producer()
send_message(producer, 'user_events', {'user_id': 123, 'action': 'login'})
```

### Producer with Error Handling
```python
def delivery_callback(err, msg):
    if err:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def send_message_async(producer, topic, message):
    producer.produce(
        topic, 
        json.dumps(message).encode('utf-8'),
        callback=delivery_callback
    )
    producer.poll(0)  # Trigger callbacks
```

### Docker Environment Producer
```python
import os

def get_kafka_config():
    env = os.getenv("ENVIRONMENT", "local")
    
    if env == "docker":
        return {'bootstrap.servers': 'kafka:9092'}
    else:
        return {'bootstrap.servers': 'localhost:9092'}

producer = Producer(get_kafka_config())
```

## 📥 Consumer Setup

### Basic Consumer (confluent-kafka)
```python
from confluent_kafka import Consumer
import json

def create_consumer():
    config = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'my-consumer-group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True
    }
    return Consumer(config)

def consume_messages(consumer, topic):
    consumer.subscribe([topic])
    
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                print(f'Consumer error: {msg.error()}')
                continue
                
            # Process message
            data = json.loads(msg.value().decode('utf-8'))
            print(f'Received: {data}')
            
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

# Usage
consumer = create_consumer()
consume_messages(consumer, 'user_events')
```

### Manual Commit Consumer
```python
def create_manual_consumer():
    config = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'manual-commit-group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False  # Manual commit
    }
    return Consumer(config)

def process_with_manual_commit(consumer, topic):
    consumer.subscribe([topic])
    
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            continue
            
        try:
            # Process message
            data = json.loads(msg.value().decode('utf-8'))
            process_business_logic(data)
            
            # Commit only after successful processing
            consumer.commit(msg)
            
        except Exception as e:
            print(f'Processing failed: {e}')
            # Don't commit on error
```

## 🐳 Docker Integration

### Docker Compose Setup
```yaml
version: '3.8'
services:
  kafka:
    image: hatakekakashihk/kafka:latest
    ports:
      - "2181:2181"
      - "9092:9092"
    environment:
      - KAFKA_HOST=kafka
    networks:
      - kafka-net

  producer-app:
    build: ./producer
    environment:
      - KAFKA_BOOTSTRAP_SERVERS=kafka:9092
    depends_on:
      - kafka
    networks:
      - kafka-net

  consumer-app:
    build: ./consumer
    environment:
      - KAFKA_BOOTSTRAP_SERVERS=kafka:9092
    depends_on:
      - kafka
    networks:
      - kafka-net

networks:
  kafka-net:
```

### Environment-Based Configuration
```python
import os

class KafkaConfig:
    def __init__(self):
        self.env = os.getenv("ENVIRONMENT", "local")
        
    def get_bootstrap_servers(self):
        if self.env == "docker":
            return "kafka:9092"
        elif self.env == "production":
            return os.getenv("KAFKA_BOOTSTRAP_SERVERS", "prod-kafka:9092")
        else:
            return "localhost:9092"
    
    def get_producer_config(self):
        return {
            'bootstrap.servers': self.get_bootstrap_servers(),
            'client.id': f'producer-{self.env}'
        }
    
    def get_consumer_config(self, group_id):
        return {
            'bootstrap.servers': self.get_bootstrap_servers(),
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        }

# Usage
config = KafkaConfig()
producer = Producer(config.get_producer_config())
consumer = Consumer(config.get_consumer_config('my-group'))
```

## 🔧 Advanced Patterns

### Producer with Retry Logic
```python
import time
from confluent_kafka import KafkaError

def send_with_retry(producer, topic, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            producer.produce(topic, json.dumps(message).encode('utf-8'))
            producer.flush(timeout=10)
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise e
    return False
```

### Consumer with Error Handling
```python
def robust_consumer(consumer, topic, process_func):
    consumer.subscribe([topic])
    
    while True:
        try:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f'Consumer error: {msg.error()}')
                    break
                    
            # Process message
            data = json.loads(msg.value().decode('utf-8'))
            success = process_func(data)
            
            if success and not consumer._conf['enable.auto.commit']:
                consumer.commit(msg)
                
        except json.JSONDecodeError:
            print(f'Invalid JSON in message: {msg.value()}')
        except Exception as e:
            print(f'Processing error: {e}')
```

## 🧪 Testing Setup

### Create Test Topic
```bash
# Inside Kafka container
docker exec kafka-container /opt/kafka/bin/kafka-topics.sh \
  --create --topic test-topic \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1
```

### Simple Test Script
```python
import time
import threading
from confluent_kafka import Producer, Consumer

def test_producer_consumer():
    # Producer
    producer = Producer({'bootstrap.servers': 'localhost:9092'})
    
    # Consumer
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'test-group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe(['test-topic'])
    
    # Send message
    producer.produce('test-topic', b'Hello Kafka!')
    producer.flush()
    
    # Consume message
    msg = consumer.poll(timeout=5.0)
    if msg and not msg.error():
        print(f'Received: {msg.value().decode("utf-8")}')
    
    consumer.close()

test_producer_consumer()
```

## 🚨 Common Issues & Solutions

### Connection Issues
```python
# Add connection validation
def validate_kafka_connection(bootstrap_servers):
    try:
        producer = Producer({'bootstrap.servers': bootstrap_servers})
        metadata = producer.list_topics(timeout=5)
        return True
    except Exception as e:
        print(f'Connection failed: {e}')
        return False

# Use before creating consumers/producers
if not validate_kafka_connection('localhost:9092'):
    raise Exception('Kafka not available')
```

### Docker Network Issues
```python
# Try multiple bootstrap servers
def get_bootstrap_servers():
    servers = [
        'kafka:9092',      # Docker internal
        'kafka:29092',     # Docker external
        'localhost:9092'   # Local
    ]
    
    for server in servers:
        if validate_kafka_connection(server):
            return server
    
    raise Exception('No Kafka servers available')
```

### Topic Management
```python
from confluent_kafka.admin import AdminClient, NewTopic

def create_topic_if_not_exists(topic_name, num_partitions=1):
    admin = AdminClient({'bootstrap.servers': 'localhost:9092'})
    
    # Check if topic exists
    metadata = admin.list_topics(timeout=5)
    if topic_name in metadata.topics:
        return
    
    # Create topic
    topic = NewTopic(topic_name, num_partitions=num_partitions)
    admin.create_topics([topic])
```

## 📊 Monitoring & Debugging

### Consumer Lag Monitoring
```python
def get_consumer_lag(consumer, topic):
    partitions = consumer.list_consumer_group_offsets()
    watermarks = consumer.get_watermark_offsets()
    
    for partition, offset in partitions.items():
        high_water = watermarks[partition][1]
        lag = high_water - offset.offset
        print(f'Partition {partition.partition}: lag = {lag}')
```

### Health Check Endpoints
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health/kafka")
def kafka_health():
    try:
        producer = Producer({'bootstrap.servers': 'localhost:9092'})
        metadata = producer.list_topics(timeout=5)
        return {"status": "healthy", "topics": len(metadata.topics)}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

This guide covers the essential patterns for integrating Kafka producers and consumers in both local and Docker environments.
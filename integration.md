# Kafka Producer & Consumer Setup Guide

## 1. Start Kafka
```bash
# Start Kafka container
docker run -d --name kafka -p 2181:2181 -p 9092:9092 -e KAFKA_HOST=localhost hatakekakashihk/kafka:latest

# Install Python library
pip install confluent-kafka
```

## 2. Simple Producer
```python
from confluent_kafka import Producer
import json

# Create producer
producer = Producer({'bootstrap.servers': 'localhost:9092'})

# Send message
message = {'user_id': 123, 'action': 'login'}
producer.produce('my-topic', json.dumps(message))
producer.flush()
```

## 3. Simple Consumer
```python
from confluent_kafka import Consumer
import json

# Create consumer
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
})

# Subscribe and consume
consumer.subscribe(['my-topic'])

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        continue
        
    data = json.loads(msg.value())
    print(f'Received: {data}')
```

## 4. Docker Environment

### For apps running inside Docker containers:
```python
# Use 'kafka:9092' instead of 'localhost:9092'
producer = Producer({'bootstrap.servers': 'kafka:9092'})
consumer = Consumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
})
```

### Docker Compose:
```yaml
version: '3.8'
services:
  kafka:
    image: hatakekakashihk/kafka:latest
    ports:
      - "9092:9092"
      - "2181:2181"
  
  my-app:
    build: .
    depends_on:
      - kafka
    environment:
      - KAFKA_HOST=kafka:9092
```

## 5. Environment-Based Config
```python
import os

def get_kafka_host():
    if os.getenv('ENVIRONMENT') == 'docker':
        return 'kafka:9092'
    return 'localhost:9092'

producer = Producer({'bootstrap.servers': get_kafka_host()})
```

## 6. Manual Commit (Reliable Processing)
```python
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False  # Manual commit
})

consumer.subscribe(['my-topic'])

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        continue
        
    try:
        # Process message
        data = json.loads(msg.value())
        process_data(data)
        
        # Commit only after successful processing
        consumer.commit(msg)
    except Exception as e:
        print(f'Error: {e}')
        # Don't commit on error
```

## 7. Common Issues

### Connection Problems:
```python
# Test connection first
def test_kafka():
    try:
        producer = Producer({'bootstrap.servers': 'localhost:9092'})
        producer.list_topics(timeout=5)
        return True
    except:
        return False

if not test_kafka():
    print('Kafka not available')
```

### Docker Network Issues:
```python
# Try different hosts
hosts = ['kafka:9092', 'localhost:9092']
for host in hosts:
    try:
        producer = Producer({'bootstrap.servers': host})
        producer.list_topics(timeout=5)
        print(f'Connected to {host}')
        break
    except:
        continue
```

## 8. Create Topic
```bash
# Create topic before using
docker exec kafka /opt/kafka/bin/kafka-topics.sh \
  --create --topic my-topic \
  --bootstrap-server localhost:9092
```

## 9. Complete Example
```python
from confluent_kafka import Producer, Consumer
import json
import threading
import time

# Producer function
def send_messages():
    producer = Producer({'bootstrap.servers': 'localhost:9092'})
    
    for i in range(5):
        message = {'id': i, 'text': f'Message {i}'}
        producer.produce('test-topic', json.dumps(message))
        time.sleep(1)
    
    producer.flush()
    print('Sent 5 messages')

# Consumer function
def consume_messages():
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'test-group',
        'auto.offset.reset': 'earliest'
    })
    
    consumer.subscribe(['test-topic'])
    
    for _ in range(5):
        msg = consumer.poll(5.0)
        if msg and not msg.error():
            data = json.loads(msg.value())
            print(f'Received: {data}')
    
    consumer.close()

# Run both
producer_thread = threading.Thread(target=send_messages)
consumer_thread = threading.Thread(target=consume_messages)

producer_thread.start()
consumer_thread.start()

producer_thread.join()
consumer_thread.join()
```

That's it! Start with the simple examples and add complexity as needed.
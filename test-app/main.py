from fastapi import FastAPI, HTTPException
import json
import time
import threading
from typing import List

app = FastAPI(title="Kafka Test API")

KAFKA_HOST = "localhost:9092"
TOPIC_NAME = "test-topic"

# Global variables to store messages
sent_messages = []
consumed_messages = []
consumer_running = False

def get_kafka_producer():
    try:
        from confluent_kafka import Producer
        config = {'bootstrap.servers': KAFKA_HOST}
        return Producer(config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kafka connection failed: {str(e)}")

def get_kafka_consumer():
    try:
        from confluent_kafka import Consumer
        config = {
            'bootstrap.servers': KAFKA_HOST,
            'group.id': 'test-group',
            'auto.offset.reset': 'earliest'
        }
        return Consumer(config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kafka consumer connection failed: {str(e)}")

def consume_messages():
    global consumed_messages, consumer_running
    try:
        consumer = get_kafka_consumer()
        consumer.subscribe([TOPIC_NAME])
        consumer_running = True
        
        while consumer_running:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                continue
                
            message_data = {
                "topic": msg.topic(),
                "partition": msg.partition(),
                "offset": msg.offset(),
                "value": json.loads(msg.value().decode('utf-8')),
                "timestamp": time.time()
            }
            consumed_messages.append(message_data)
            
    except Exception as e:
        print(f"Consumer error: {e}")
    finally:
        if 'consumer' in locals():
            consumer.close()

@app.get("/")
def health_check():
    return {"status": "Kafka Test API is running"}

@app.get("/kafka/status")
def kafka_status():
    try:
        producer = get_kafka_producer()
        # Test connection by getting metadata
        metadata = producer.list_topics(timeout=5)
        return {"status": "Connected to Kafka", "broker": KAFKA_HOST, "topics": len(metadata.topics)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kafka connection failed: {str(e)}")

@app.post("/kafka/send")
def send_message(message: dict):
    try:
        producer = get_kafka_producer()
        
        # Send message
        producer.produce(TOPIC_NAME, json.dumps(message).encode('utf-8'))
        producer.flush()
        
        # Store message locally for demo
        sent_messages.append({
            "message": message,
            "topic": TOPIC_NAME,
            "timestamp": time.time()
        })
        
        return {"status": "Message sent", "message": message, "topic": TOPIC_NAME}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")

@app.get("/kafka/messages")
def get_messages():
    return {"sent_messages": sent_messages, "count": len(sent_messages)}

@app.post("/kafka/consumer/start")
def start_consumer():
    global consumer_running
    if consumer_running:
        return {"status": "Consumer already running"}
    
    consumer_thread = threading.Thread(target=consume_messages, daemon=True)
    consumer_thread.start()
    return {"status": "Consumer started", "topic": TOPIC_NAME}

@app.post("/kafka/consumer/stop")
def stop_consumer():
    global consumer_running
    consumer_running = False
    return {"status": "Consumer stopped"}

@app.get("/kafka/consumer/messages")
def get_consumed_messages():
    return {"consumed_messages": consumed_messages, "count": len(consumed_messages)}

@app.delete("/kafka/messages")
def clear_messages():
    global sent_messages, consumed_messages
    sent_messages = []
    consumed_messages = []
    return {"status": "All messages cleared"}
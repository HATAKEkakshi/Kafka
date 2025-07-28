from fastapi import FastAPI, HTTPException
import json
import time

app = FastAPI(title="Kafka Test API")

KAFKA_HOST = "localhost:9092"
TOPIC_NAME = "test-topic"

# Global variable to store sent messages for demo
sent_messages = []

def get_kafka_producer():
    try:
        from confluent_kafka import Producer
        config = {'bootstrap.servers': KAFKA_HOST}
        return Producer(config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kafka connection failed: {str(e)}")

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

@app.delete("/kafka/messages")
def clear_messages():
    global sent_messages
    sent_messages = []
    return {"status": "Messages cleared"}
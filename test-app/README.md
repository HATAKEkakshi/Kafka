# Kafka Test API

FastAPI application to test Kafka connection and messaging.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start your Kafka container:
```bash
docker-compose up --build
```

3. Run the FastAPI app:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /` - Health check
- `GET /kafka/status` - Check Kafka connection
- `POST /kafka/send` - Send message to Kafka
- `GET /kafka/messages` - Get consumed messages
- `DELETE /kafka/messages` - Clear message history

## Test Commands

```bash
# Check Kafka status
curl http://localhost:8000/kafka/status

# Send a message
curl -X POST http://localhost:8000/kafka/send \
  -H "Content-Type: application/json" \
  -d '{"user": "test", "message": "Hello Kafka!"}'

# Get messages
curl http://localhost:8000/kafka/messages
```
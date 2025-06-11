# ./scripts/producer/producer_city_events.py

import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer

# --- Configuration ---
# This producer will run on your host machine and connect to the Kafka broker's external port.
KAFKA_BROKER_URL = 'localhost:19091'  # Connect to kafka1's external port
TOPIC_NAME = 'city-events'

CITIES = [
    "Taipei", "New Taipei", "Taoyuan", "Taichung", "Tainan", "Kaohsiung"
]

def generate_event():
    """
    Generates a fake city event in JSON format.
    """
    city = random.choice(CITIES)
    event = {
        "city_name": city,
        "temperature": round(random.uniform(18.0, 35.0), 2),
        "humidity": round(random.uniform(40.0, 90.0), 2),
        "pm25": random.randint(5, 75),
        "traffic_index": round(random.uniform(1.0, 10.0), 1),
        "event_type": random.choice(['none', 'concert', 'road_closure', 'festival']),
        "timestamp": datetime.utcnow().isoformat() + "Z"  # ISO 8601 format with Z for UTC
    }
    return event

def main():
    """
    Main function to run the Kafka producer.
    """
    producer = None
    try:
        # Create a KafkaProducer instance
        # value_serializer helps to encode our dictionary to JSON bytes
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER_URL,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            api_version=(0, 10, 1) # Specify api version to avoid potential warnings
        )
        
        print("Kafka Producer started. Press Ctrl+C to stop.")
        
        # Loop to continuously send messages
        while True:
            event_data = generate_event()
            
            # Send the event to the specified topic
            producer.send(TOPIC_NAME, value=event_data)
            
            print(f"Sent event: {event_data}")
            
            # Wait for a short interval before sending the next message
            time.sleep(random.uniform(0.5, 2.0))
            
    except KeyboardInterrupt:
        print("\nProducer stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if producer:
            print("Flushing messages and closing producer...")
            producer.flush() # Ensure all pending messages are sent
            producer.close()
            print("Producer closed.")

if __name__ == "__main__":
    main()
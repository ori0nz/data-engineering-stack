## 🚀 Running the Kafka Producer

Now, go back to your terminal and execute the following Python script:

### Bash

```bash
python ./scripts/producer_city_events.py
```

If everything goes well, you should see output like this, showing that new messages are being generated and sent:

```
Kafka Producer started. Press Ctrl+C to stop.
Sent event: {'city_name': 'Taichung', 'temperature': 25.8, 'humidity': 78.93, 'pm25': 23, 'traffic_index': 4.5, 'event_type': 'none', 'timestamp': '2025-06-11T05:43:45.123456Z'}
Sent event: {'city_name': 'Taipei', 'temperature': 31.2, 'humidity': 65.4, 'pm25': 45, 'traffic_index': 8.2, 'event_type': 'road_closure', 'timestamp': '2025-06-11T05:43:46.789012Z'}
...
```

---

## ✅ How to Verify That Data Really Entered Kafka (Very Important)

Just looking at the producer’s output is not enough. We need to **visually confirm** that the messages actually exist in the Kafka topic. This is a very useful debugging technique.

> ⚠️ **Do not stop the producer yet!**  
> Open a new terminal window, go to your project directory, and run:

### Bash

```bash
docker-compose exec kafka1 kafka-console-consumer.sh \
--bootstrap-server kafka1:9092 \
--topic city-events \
--from-beginning
```

### 🔍 Command Explanation

- `docker-compose exec kafka1`: Enter the `kafka1` container to run the following command.
- `kafka-console-consumer.sh`: Kafka’s built-in CLI consumer tool.
- `--bootstrap-server kafka1:9092`: Connect to Kafka using the internal service name and port.
- `--topic city-events`: Specify the topic to consume.
- `--from-beginning`: Read all messages from the beginning of the topic.

After executing the command, you should see the JSON messages sent by the producer being printed out line by line in the new terminal window. This confirms that your data has successfully traveled from the local Python script, through the network, and into your Docker-based Kafka cluster.

### 🛑 How to Stop

When you’re done testing, press `Ctrl + C` in **both terminal windows** to stop the producer and the consumer.

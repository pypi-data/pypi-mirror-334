### Base Consumer

The Base Consumer is a class that you will extend to create your own consumer. 
It provides a few helper methods that make it easier to interact with the Kafka cluster.
It also offers built-in logging capabilities.
Example:

```python
from base_consumer import BaseKafkaConsumer

class EmailConsumer(BaseKafkaConsumer):
    def __init__(self):
        super().__init__(
            broker_url="localhost:9092",
            topic="email",
            group_id="email-consumer",
            log_file="email_consumer.log",
        )
        log_level = os.environ.get("LOG_LEVEL", "INFO")
        self.set_logger_level(log_level) # default is INFO if not set

    def process_message(self, message: dict):
        # do something with the message
        print(message)


if __name__ == "__main__":
    consumer = EmailConsumer()
    consumer.consume()

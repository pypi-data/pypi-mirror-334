import json
import logging
from abc import ABC, abstractmethod

from confluent_kafka import Consumer


def setup_logger(name: str, log_file: str = None):
    """Setup logger for a specific consumer with optional file logging."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


class BaseKafkaConsumer(ABC):
    """Abstract base class for Kafka consumers."""

    def __init__(
        self, broker_url: str, topic: str, group_id: str, log_file: str = None
    ):
        self.logger = setup_logger(self.__class__.__name__, log_file)
        self.topic = topic
        self.conf = {
            "bootstrap.servers": f"{broker_url}",
            "group.id": group_id,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
            "partition.assignment.strategy": "roundrobin",
        }
        self.logger.info(
            f"Connecting to Kafka broker at {self.conf['bootstrap.servers']}"
        )
        self.consumer = Consumer(self.conf)
        self.consumer.subscribe([self.topic])

    def set_logger_level(self, level: str):
        """Set the log level for the consumer logger."""
        if not level:
            raise ValueError("Log level must be provided")
        self.logger.setLevel(level)

    @abstractmethod
    def process_message(self, message: dict):
        """Abstract method to process Kafka messages."""
        pass

    def consume(self):
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    self.logger.error(f"Consumer error: {msg.error()}")
                    continue
                self.logger.debug(f"Received message: {msg.value()}")
                try:
                    msg_data = json.loads(msg.value())
                    self.process_message(msg_data)
                except json.JSONDecodeError:
                    self.logger.error("Failed to decode message")
                except Exception as e:
                    self.logger.error(f"Error processing message: {e}")
                self.consumer.commit(asynchronous=False)
        except KeyboardInterrupt:
            self.logger.info("Consumer interrupted. Exiting...")

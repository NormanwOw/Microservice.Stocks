import json

from aiokafka import AIOKafkaConsumer

from src.config import Settings


class KafkaConsumer(AIOKafkaConsumer):
    def __init__(self, settings: Settings):
        super().__init__(
            settings.STOCKS_COMMANDS_TOPIC,
            bootstrap_servers=settings.KAFKA_HOSTS,
            group_id='stocks_group',
            enable_auto_commit=False,
            auto_offset_reset='earliest',
            value_deserializer=lambda msg: json.loads(msg.decode()),
        )

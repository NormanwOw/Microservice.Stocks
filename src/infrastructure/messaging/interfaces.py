from abc import ABC

from aiokafka import AIOKafkaConsumer


class IKafkaConsumer(AIOKafkaConsumer, ABC): ...

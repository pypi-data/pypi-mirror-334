from finalsa.sqs.consumer.app.get_function_attrs import get_function_attrs
from finalsa.sqs.consumer.app.get_missing_attrs import get_missing_attrs
from finalsa.sqs.consumer.app.build_sqs_depends import build_sqs_depends
from finalsa.sqs.consumer.app.exceptions import (
    TopicAlreadyRegisteredException
)
from typing import Dict, Callable, get_type_hints, Any
from finalsa.common.models import SqsMessage
from logging import getLogger, Logger
from asyncio import sleep


class SqsConsumer():

    __handlers__: Dict[str, Callable]

    def __init__(
        self,
    ) -> None:
        self.__handlers__: Dict[str, Callable] = {}
        self.logger: Logger = getLogger("finalsa.sqs.consumer")

    def include_consumer(self, consumer: 'SqsConsumer'):
        for topic in consumer.__handlers__:
            if topic in self.__handlers__:
                raise TopicAlreadyRegisteredException(topic)
            self.__handlers__[topic] = consumer.__handlers__[topic]
        consumer.logger = self.logger

    async def __call_handler__(
        self,
        handler: Callable,
        request_attrs:  Dict[str, Any],
        missing_attrs: Dict[str, Any],
        function_defaults: Dict[str, Any],
        message: SqsMessage,
        retries: int,
        retry_delay: int
    ):
        dependencies = build_sqs_depends(
            missing_attrs,
            None,
            function_defaults,
            builded_dependencies={}
        )
        for i in range(retries):
            try:
                attrs = {
                    **request_attrs,
                    **dependencies
                }
                await handler(**attrs)
                break
            except Exception as ex:
                self.logger.error(
                    f"Error processing message {message.id} for topic {message.topic} retrying {i+1} of {retries}")
                self.logger.exception(ex)
                if (i == retries - 1):
                    self.logger.error(
                        f"Error processing message {message.id} for topic {message.topic} max retries reached")
                    raise ex
                await sleep(retry_delay)

    def __decorator__(self, topic: str = '', retries: int = 10, retry_delay: int = 3):
        self.logger.info(f"Adding handler for topic {topic}")

        def decorator(handler: Callable):
            function_attrs = get_type_hints(handler)
            function_defaults = handler.__defaults__

            async def async_wrapper(message: SqsMessage):
                request_attrs = get_function_attrs(message, function_attrs)
                missing_attrs = get_missing_attrs(
                    request_attrs, function_attrs)
                await self.__call_handler__(
                    handler, request_attrs, missing_attrs, function_defaults, message, retries, retry_delay
                )

            self.__handlers__[topic] = async_wrapper
        return decorator

    @DeprecationWarning
    def add_handler(self, topic: str = '', retries: int = 1, retry_delay: int = 1):
        """
        DEPRECATED: Use handler decorator instead
        """
        return self.__decorator__(topic, retries, retry_delay)

    def handler(self, topic: str = '', retries: int = 1, retry_delay: int = 1):
        """
        Decorator to add a handler to a topic
        topic: str - Topic to add the handler
        retries: int - Number of retries to process the message
        retry_delay: int - Delay between retries in seconds
        """
        return self.__decorator__(topic, retries, retry_delay)

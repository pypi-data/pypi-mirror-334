from orjson import dumps


class InvalidMessageException(Exception):

    def __init__(self, attrs, body) -> None:
        super().__init__(
            f'Topic not found in message attributes {dumps(attrs)} or body {dumps(body)}')


class TopicAlreadyRegisteredException(Exception):

    def __init__(self, topic) -> None:
        super().__init__(f"Topic {topic} already registered in this consumer")


class TopicNotFoundException(Exception):

    def __init__(self, topic) -> None:
        super().__init__(f"Handler not found for topic {topic}")

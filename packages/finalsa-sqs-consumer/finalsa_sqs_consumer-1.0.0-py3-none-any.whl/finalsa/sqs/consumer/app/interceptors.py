from finalsa.common.models import SqsMessage
from abc import ABC, abstractmethod
from typing import Callable


class AsyncConsumerInterceptor(ABC):

    @abstractmethod
    async def __call__(self, message: SqsMessage, call_next: Callable) -> SqsMessage:
        pass


def get_handler_interceptor(fn_handler) -> Callable[[Callable], AsyncConsumerInterceptor]:
    class HandlerInterceptor(AsyncConsumerInterceptor):
        async def __call__(self, message, _):
            await fn_handler(message)

    return HandlerInterceptor

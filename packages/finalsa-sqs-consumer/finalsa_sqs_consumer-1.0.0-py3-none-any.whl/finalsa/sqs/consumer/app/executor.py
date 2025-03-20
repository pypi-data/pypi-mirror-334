from typing import List, Callable
from finalsa.common.models import SqsMessage


class Executor():

    def __init__(self, __interceptors__: List[Callable]):
        self.__interceptors__ = __interceptors__

    async def call(self, message: SqsMessage):
        if len(self.__interceptors__) == 0:
            return
        await self.call_interceptor(self.__interceptors__.pop(0), message)

    async def call_interceptor(self, interceptor: Callable, message: SqsMessage):
        def caller():
            async def next_fn(message):
                await self.call(message)
            return next_fn
        await interceptor(message, caller())

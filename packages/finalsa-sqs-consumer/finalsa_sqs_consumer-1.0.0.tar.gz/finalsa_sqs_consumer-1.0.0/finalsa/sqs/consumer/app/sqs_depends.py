from typing import Callable


class SqsDepends():

    def __init__(self, interface: Callable) -> None:
        self.interface = interface

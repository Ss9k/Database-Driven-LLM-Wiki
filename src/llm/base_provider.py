from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def invoke(self, prompt: str) -> str:
        pass
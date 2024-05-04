from abc import ABC, abstractmethod

class RunnableInterface(ABC):
    @abstractmethod
    def get_promtp(self):
        pass

    @abstractmethod
    def get_runnable(self):
        pass
from abc import ABC, abstractmethod

class RunnableInterface(ABC):
    @abstractmethod
    def get_prompt(self):
        pass

    @abstractmethod
    def get_runnable(self):
        pass
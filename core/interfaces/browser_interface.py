from abc import ABC, abstractmethod

class IBrowser(ABC):
    @abstractmethod
    def open(self, url: str):
        pass

    @abstractmethod
    def close(self):
        pass

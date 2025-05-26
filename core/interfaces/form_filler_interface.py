from abc import ABC, abstractmethod
from core.entities.form_data import FormData

class IFormFiller(ABC):
    @abstractmethod
    def fill_form(self, data: FormData):
        pass


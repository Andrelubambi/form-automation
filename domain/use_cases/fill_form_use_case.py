from core.entities.form_data import FormData
from core.interfaces.form_filler_interface import IFormFiller

class FillFormUseCase:
    def __init__(self, form_filler: IFormFiller):
        self.form_filler = form_filler

    def execute(self, form_data: FormData):
        self.form_filler.fill_form(form_data)
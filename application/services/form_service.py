from core.entities.form_data import FormData
from domain.use_cases.fill_form_use_case import FillFormUseCase

class FormService:
    def __init__(self, fill_form_use_case: FillFormUseCase):
        self.fill_form_use_case = fill_form_use_case

    def run(self):
        form_data = FormData(
            name="Lubambi Tester",
            email="lubambi@example.com",
            message="Mensagem de teste para preenchimento de formulário."
        )
        self.fill_form_use_case.execute(form_data)
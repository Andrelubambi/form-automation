from config import settings
from infrastructure.selenium.selenium_browser import SeleniumBrowser
from infrastructure.selenium.selenium_form_filler import SeleniumFormFiller
from domain.use_cases.fill_form_use_case import FillFormUseCase
from application.services.form_service import FormService

# Configura dependências
browser = SeleniumBrowser()
browser.open(settings.URL)

form_filler = SeleniumFormFiller(browser)
use_case = FillFormUseCase(form_filler)
service = FormService(use_case)

# Executa serviço
try:
    service.run()
finally:
    browser.close()

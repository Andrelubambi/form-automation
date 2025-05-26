from selenium.webdriver.common.by import By
from core.interfaces.form_filler_interface import IFormFiller
from core.entities.form_data import FormData

class SeleniumFormFiller(IFormFiller):
    def __init__(self, browser):
        self.browser = browser

    def fill_form(self, data: FormData):
        driver = self.browser.get_driver()
        driver.find_element(By.NAME, "my-text").send_keys(data.name)
        driver.find_element(By.NAME, "my-email").send_keys(data.email)
        driver.find_element(By.NAME, "my-textarea").send_keys(data.message)
        driver.find_element(By.TAG_NAME, "form").submit()

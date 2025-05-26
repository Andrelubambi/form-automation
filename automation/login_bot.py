import time
from selenium.webdriver.common.by import By
from automation.config import URL_LOGIN, USUARIO, SENHA

def realizar_login(driver):
    driver.get(URL_LOGIN)
    time.sleep(2)
    driver.find_element(By.NAME, "usuario").send_keys(USUARIO)
    driver.find_element(By.NAME, "senha").send_keys(SENHA)
    driver.find_element(By.XPATH, '//button[text()="Entrar"]').click()
    time.sleep(3)

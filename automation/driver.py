from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from automation.config import CAMINHO_DRIVER

def iniciar_driver():
    service = Service(CAMINHO_DRIVER)
    driver = webdriver.Chrome(service=service)
    return driver

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from core.interfaces.browser_interface import IBrowser

class SeleniumBrowser(IBrowser):
    def __init__(self):
        self.driver = None

    def open(self, url: str):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(url)

    def get_driver(self):
        return self.driver

    def close(self):
        if self.driver:
            self.driver.quit()
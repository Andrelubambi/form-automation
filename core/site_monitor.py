from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

class SiteMonitor:
    def __init__(self, url, check_interval=60):
        self.url = url
        self.check_interval = check_interval
        self.setup_driver()
        
    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Executar em segundo plano
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def check_availability(self, selector, condition):
        """
        Verifica se há vagas disponíveis baseado no seletor CSS e condição
        """
        try:
            self.driver.get(self.url)
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return condition(element)
        except Exception as e:
            logging.error(f"Erro ao verificar disponibilidade: {str(e)}")
            return False
            
    def start_monitoring(self, selector, condition, callback):
        """
        Inicia o monitoramento contínuo do site
        """
        while True:
            if self.check_availability(selector, condition):
                callback()
            time.sleep(self.check_interval)
            
    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit() 
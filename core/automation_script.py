from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import json
import time
from .video_handler import VideoHandler

class AutomationScript:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.steps = []
        self.form_data = {}
        self.video_path = None
        
    def add_step(self, action_type, selector, value=None, wait_time=0):
        """
        Adiciona um passo ao script
        action_type: click, input, wait, submit
        selector: seletor CSS do elemento
        value: valor para campos de input
        wait_time: tempo de espera após a ação
        """
        self.steps.append({
            'type': action_type,
            'selector': selector,
            'value': value,
            'wait_time': wait_time
        })
        
    def set_form_data(self, data):
        """
        Define os dados do formulário
        data: dicionário com os dados a serem preenchidos
        """
        self.form_data = data
        
    def set_video(self, video_path):
        """
        Define o vídeo a ser usado
        """
        self.video_path = video_path
        
    def save(self, filename):
        """
        Salva o script em um arquivo JSON
        """
        data = {
            'name': self.name,
            'description': self.description,
            'steps': self.steps,
            'form_data': self.form_data,
            'video_path': self.video_path
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
            
    @classmethod
    def load(cls, filename):
        """
        Carrega um script de um arquivo JSON
        """
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        script = cls(data['name'], data['description'])
        script.steps = data['steps']
        script.form_data = data['form_data']
        script.video_path = data['video_path']
        return script
        
    def execute(self, url, headless=False):
        """
        Executa o script de automação
        """
        # Configurar o navegador
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        
        try:
            # Inicializar manipulador de vídeo se necessário
            video_handler = None
            if self.video_path:
                video_handler = VideoHandler(self.video_path)
            
            # Acessar a URL
            driver.get(url)
            
            # Executar cada passo
            for step in self.steps:
                # Esperar elemento estar presente
                element = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, step['selector']))
                )
                
                # Executar ação baseado no tipo
                if step['type'] == 'click':
                    element.click()
                elif step['type'] == 'input':
                    element.clear()
                    # Verificar se é um campo de vídeo
                    if step.get('is_video', False) and video_handler:
                        # Aqui você implementaria a lógica para usar o vídeo
                        pass
                    else:
                        # Usar valor do form_data se disponível
                        value = self.form_data.get(step['value'], step['value'])
                        element.send_keys(value)
                elif step['type'] == 'submit':
                    element.submit()
                
                # Esperar tempo adicional se especificado
                if step['wait_time'] > 0:
                    time.sleep(step['wait_time'])
                    
            return True
            
        except Exception as e:
            print(f"Erro durante a execução: {str(e)}")
            return False
            
        finally:
            driver.quit()
            if video_handler:
                del video_handler 
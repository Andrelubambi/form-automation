from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def executar_automacao(url, dados_formulario=None, video_path=None):
    """
    Função básica de automação
    url: URL do site a ser automatizado
    dados_formulario: dicionário com os dados a serem preenchidos
    video_path: caminho do vídeo (opcional)
    """
    try:
        # Configurar o Chrome
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        
        # Abrir o site
        print(f"Abrindo {url}...")
        driver.get(url)
        
        # Exemplo de preenchimento de formulário
        if dados_formulario:
            for campo, valor in dados_formulario.items():
                try:
                    # Esperar o campo ficar visível
                    elemento = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, campo))
                    )
                    # Preencher o campo
                    elemento.clear()
                    elemento.send_keys(valor)
                    print(f"Campo {campo} preenchido com {valor}")
                except Exception as e:
                    print(f"Erro ao preencher campo {campo}: {str(e)}")
        
        # Manter o navegador aberto por 30 segundos
        print("Aguardando 30 segundos...")
        time.sleep(30)
        
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")
    finally:
        # Fechar o navegador
        driver.quit()

if __name__ == "__main__":
    # Exemplo de uso
    url = input("Digite a URL do site: ")
    
    # Exemplo de dados para formulário
    dados = {
        'input[name="q"]': 'teste automação python',  # Para Google
        '#email': 'teste@exemplo.com',                # Para formulários de email
        '#senha': '123456'                           # Para campos de senha
    }
    
    executar_automacao(url, dados) 
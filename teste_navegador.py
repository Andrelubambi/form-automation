from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

def executar_automacao():
    # Configurar o Chrome para aceitar a webcam virtual
    chrome_options = Options()
    chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Desativa o popup de permissão da câmera
    chrome_options.add_argument("--start-maximized")  # Inicia maximizado
    
    # Iniciar o Chrome
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Lista de sites para testar
        sites = [
            "https://webcamtests.com/",  # Teste de webcam
            "https://www.google.com/meet",  # Google Meet
            "https://zoom.us/test",  # Teste do Zoom
        ]
        
        print("Sites disponíveis para teste:")
        for i, site in enumerate(sites, 1):
            print(f"{i}. {site}")
        
        escolha = input("\nEscolha o número do site para testar (ou digite uma URL personalizada): ")
        
        # Determinar a URL
        if escolha.isdigit() and 1 <= int(escolha) <= len(sites):
            url = sites[int(escolha) - 1]
        else:
            url = escolha if escolha.startswith("http") else "https://" + escolha
        
        # Abrir o site
        print(f"\nAbrindo {url}...")
        driver.get(url)
        
        print("\nNavegador aberto com a webcam virtual ativada!")
        print("A webcam virtual do OBS está sendo usada como câmera.")
        print("\nInstruções:")
        print("1. Se solicitado, permita o acesso à câmera no navegador")
        print("2. Você deve ver o vídeo que configurou no OBS")
        print("3. Para encerrar, pressione Enter")
        
        input("\nPressione Enter para fechar o navegador...")
        
    except Exception as e:
        print(f"\nErro: {str(e)}")
    finally:
        print("\nFechando navegador...")
        driver.quit()

if __name__ == "__main__":
    print("Sistema de Automação de Webcam Virtual para Navegador")
    print("-" * 50)
    
    # Verificar se o OBS Virtual Camera está instalado
    print("\nVerificando requisitos...")
    
    executar_automacao() 
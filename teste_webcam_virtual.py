import cv2
import pyvirtualcam
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Caminho direto para o vídeo
VIDEO_PATH = r"C:\Users\ksolidpca2\Videos\Gravações de Ecrã\Gravação de Ecrã 2025-05-27 122454.mp4"

class WebcamVirtual:
    def __init__(self, width=1280, height=720, fps=30):
        if not os.path.exists(VIDEO_PATH):
            raise ValueError(f"Arquivo de vídeo não encontrado: {VIDEO_PATH}")
            
        self.video = cv2.VideoCapture(VIDEO_PATH)
        if not self.video.isOpened():
            raise ValueError(f"Não foi possível abrir o vídeo: {VIDEO_PATH}")
            
        # Configurar dimensões
        self.width = width
        self.height = height
        self.fps = fps
        
        # Inicializar webcam virtual
        self.cam = pyvirtualcam.Camera(width=width, height=height, fps=fps)
        print(f"Webcam virtual criada: {self.cam.device}")
        
    def iniciar_transmissao(self):
        """Inicia a transmissão do vídeo para a webcam virtual"""
        try:
            print("Iniciando transmissão de vídeo...")
            while True:
                # Ler frame do vídeo
                ret, frame = self.video.read()
                if not ret:
                    # Voltar ao início do vídeo
                    self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                
                # Redimensionar frame se necessário
                if frame.shape[0] != self.height or frame.shape[1] != self.width:
                    frame = cv2.resize(frame, (self.width, self.height))
                
                # Converter BGR para RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Enviar frame para a webcam virtual
                self.cam.send(frame)
                
                # Esperar pelo próximo frame
                self.cam.sleep_until_next_frame()
                
        except KeyboardInterrupt:
            print("\nTransmissão interrompida pelo usuário")
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Limpa os recursos"""
        if hasattr(self, 'video'):
            self.video.release()
        if hasattr(self, 'cam'):
            self.cam.close()

def executar_automacao_reconhecimento(url):
    """
    Executa a automação no site que requer reconhecimento facial
    """
    try:
        # Configurar Chrome
        options = webdriver.ChromeOptions()
        options.add_argument("--use-fake-ui-for-media-stream")
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        
        # Abrir site
        print(f"Abrindo {url}...")
        driver.get(url)
        
        # Aguardar interação do usuário
        input("Pressione Enter quando terminar de usar o reconhecimento facial...")
        
    except Exception as e:
        print(f"Erro durante a automação: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    print("Sistema de Webcam Virtual para Reconhecimento Facial")
    print("-" * 50)
    print(f"Usando vídeo: {VIDEO_PATH}")
    print("-" * 50)
    
    try:
        # Criar e iniciar webcam virtual
        print("\nIniciando sistema...")
        print("1. Criando webcam virtual")
        webcam = WebcamVirtual()
        
        # Solicitar URL do site
        url = input("\nDigite a URL do site de reconhecimento facial (ou pressione Enter para apenas testar o vídeo): ")
        
        print("\n2. Iniciando transmissão de vídeo")
        print("Para interromper, pressione Ctrl+C")
        
        # Iniciar transmissão
        if url:
            # Se forneceu URL, executa automação
            executar_automacao_reconhecimento(url)
        else:
            # Senão, apenas transmite o vídeo
            webcam.iniciar_transmissao()
        
    except Exception as e:
        print(f"\nErro: {str(e)}")
    finally:
        print("\nEncerrando sistema...") 
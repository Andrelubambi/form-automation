import cv2
import pyvirtualcam
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebcamVirtual:
    def __init__(self, video_path, width=1280, height=720, fps=30):
        self.video = cv2.VideoCapture(video_path)
        if not self.video.isOpened():
            raise ValueError("Não foi possível abrir o vídeo")
            
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
    
    # Configurar vídeo
    video_path = input("Digite o caminho do vídeo (ex: videos/seu_video.mp4): ")
    
    # Criar e iniciar webcam virtual em uma thread separada
    try:
        webcam = WebcamVirtual(video_path)
        
        # Solicitar URL do site
        url = input("Digite a URL do site de reconhecimento facial: ")
        
        # Iniciar transmissão de vídeo
        print("\nIniciando sistema...")
        print("1. Iniciando transmissão de vídeo para webcam virtual")
        print("2. Abrindo navegador para o site de reconhecimento")
        print("\nPara interromper, pressione Ctrl+C")
        
        # Iniciar transmissão
        webcam.iniciar_transmissao()
        
        # Executar automação
        executar_automacao_reconhecimento(url)
        
    except Exception as e:
        print(f"\nErro: {str(e)}")
    finally:
        print("\nEncerrando sistema...") 
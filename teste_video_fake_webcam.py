from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cv2
import time
import os
import numpy as np

class VideoFakeWebcam:
    def __init__(self, video_path):
        self.video = cv2.VideoCapture(video_path)
        if not self.video.isOpened():
            raise ValueError("Não foi possível abrir o vídeo")
        
        # Obter propriedades do vídeo
        self.frame_width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.video.get(cv2.CAP_PROP_FPS))
        
    def get_frame(self):
        """Retorna o próximo frame do vídeo"""
        ret, frame = self.video.read()
        if not ret:
            # Se chegou ao fim do vídeo, volta ao início
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.video.read()
        return frame
        
    def __del__(self):
        if hasattr(self, 'video'):
            self.video.release()

def executar_automacao_video(url, video_path):
    """
    Função para automatizar sites que requerem vídeo em tempo real
    url: URL do site
    video_path: Caminho para o vídeo que será usado como webcam
    """
    try:
        # Verificar se o vídeo existe
        if not os.path.exists(video_path):
            print(f"Erro: Vídeo não encontrado em {video_path}")
            return
            
        # Inicializar o manipulador de vídeo
        print("Inicializando vídeo...")
        video_handler = VideoFakeWebcam(video_path)
        
        # Configurar o Chrome
        print("Configurando navegador...")
        options = webdriver.ChromeOptions()
        
        # Adicionar permissões para webcam
        options.add_argument("--use-fake-ui-for-media-stream")  # Evita diálogo de permissão
        options.add_argument("--use-fake-device-for-media-stream")  # Permite dispositivo fake
        
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        
        # Abrir o site
        print(f"Abrindo {url}...")
        driver.get(url)
        
        # Exemplo de como interagir com elementos comuns em páginas de reconhecimento facial
        botoes_comuns = {
            'iniciar_camera': ['button[contains(text(), "Iniciar Câmera")]', 
                             'button[contains(text(), "Start Camera")]',
                             '#start-camera',
                             '.camera-button'],
            'capturar_foto': ['button[contains(text(), "Capturar")]',
                             'button[contains(text(), "Capture")]',
                             '#capture-button',
                             '.capture-button'],
            'confirmar': ['button[contains(text(), "Confirmar")]',
                         'button[contains(text(), "Confirm")]',
                         '#confirm-button',
                         '.confirm-button']
        }
        
        # Tentar clicar nos botões comuns
        for acao, seletores in botoes_comuns.items():
            for seletor in seletores:
                try:
                    botao = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, seletor)))
                    botao.click()
                    print(f"Clicou no botão: {acao}")
                    time.sleep(2)  # Esperar a ação ser processada
                    break
                except:
                    continue
        
        # Manter o navegador aberto por um tempo para visualização
        print("Mantendo navegador aberto por 60 segundos...")
        time.sleep(60)
        
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    # Exemplo de uso
    print("Sistema de Automação com Vídeo")
    print("-" * 30)
    
    # Solicitar informações
    url = input("Digite a URL do site: ")
    video_path = input("Digite o caminho do vídeo (ex: videos/seu_video.mp4): ")
    
    # Executar automação
    executar_automacao_video(url, video_path) 
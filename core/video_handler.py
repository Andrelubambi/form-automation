import cv2
import numpy as np
from PIL import Image
import io
import base64

class VideoHandler:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError("Não foi possível abrir o arquivo de vídeo")
            
    def get_frame(self):
        """
        Retorna o próximo frame do vídeo
        """
        ret, frame = self.cap.read()
        if not ret:
            # Reinicia o vídeo quando chegar ao fim
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
        
        return frame
        
    def frame_to_base64(self, frame):
        """
        Converte um frame para base64 string
        """
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer).decode()
        return jpg_as_text
        
    def get_frame_as_base64(self):
        """
        Retorna o próximo frame como string base64
        """
        frame = self.get_frame()
        return self.frame_to_base64(frame)
        
    def __del__(self):
        if hasattr(self, 'cap'):
            self.cap.release() 
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
from urllib.parse import unquote

class VideoHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Configurar headers para permitir CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        # Se for uma requisição para /video, servir o arquivo de vídeo
        if self.path == '/video':
            video_path = os.path.expanduser("~/Videos/Gravações de Ecrã/Gravação de Ecrã 2025-05-27 122454.mp4")
            if os.path.exists(video_path):
                self.send_header('Content-Type', 'video/mp4')
                self.end_headers()
                with open(video_path, 'rb') as video:
                    self.wfile.write(video.read())
            else:
                self.send_error(404, "Arquivo de vídeo não encontrado")
        else:
            super().do_GET()

# Iniciar servidor na porta 8000
print("Iniciando servidor na porta 8000...")
print("Para acessar o vídeo, use: http://localhost:8000/video")
HTTPServer(('localhost', 8000), VideoHandler).serve_forever() 
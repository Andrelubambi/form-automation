from flask import Flask, request, jsonify, render_template, send_from_directory
import threading
from core.site_monitor import SiteMonitor
from core.video_handler import VideoHandler
import os
from dotenv import load_dotenv

app = Flask(__name__, 
    template_folder='../templates',
    static_folder='../static'
)
load_dotenv()

# Armazenar instâncias ativas
active_monitors = {}
video_handlers = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/monitor/start', methods=['POST'])
def start_monitoring():
    data = request.json
    url = data.get('url')
    selector = data.get('selector')
    interval = data.get('interval', 60)
    
    if not url or not selector:
        return jsonify({'error': 'URL e seletor são obrigatórios'}), 400
        
    def on_vacancy_found():
        # Implementar notificação quando vaga for encontrada
        print(f"Vaga encontrada em {url}")
        
    monitor = SiteMonitor(url, interval)
    condition = lambda element: "vaga disponível" in element.text.lower()
    
    # Iniciar monitoramento em thread separada
    thread = threading.Thread(
        target=monitor.start_monitoring,
        args=(selector, condition, on_vacancy_found)
    )
    thread.daemon = True
    thread.start()
    
    monitor_id = len(active_monitors)
    active_monitors[monitor_id] = {
        'monitor': monitor,
        'thread': thread,
        'url': url,
        'interval': interval
    }
    
    return jsonify({
        'status': 'success',
        'monitor_id': monitor_id,
        'message': 'Monitoramento iniciado com sucesso'
    })

@app.route('/api/monitor/stop/<int:monitor_id>', methods=['POST'])
def stop_monitoring(monitor_id):
    if monitor_id not in active_monitors:
        return jsonify({'error': 'Monitor não encontrado'}), 404
        
    monitor_data = active_monitors[monitor_id]
    monitor = monitor_data['monitor']
    
    # Parar o monitor
    if hasattr(monitor, 'driver'):
        monitor.driver.quit()
    
    # Remover da lista de monitores ativos
    del active_monitors[monitor_id]
    
    return jsonify({
        'status': 'success',
        'message': 'Monitoramento parado com sucesso'
    })

@app.route('/api/monitor/list', methods=['GET'])
def list_monitors():
    monitors = [
        {
            'id': monitor_id,
            'url': data['url'],
            'interval': data['interval']
        }
        for monitor_id, data in active_monitors.items()
    ]
    return jsonify(monitors)

@app.route('/api/video/register', methods=['POST'])
def register_video():
    if 'video' not in request.files:
        return jsonify({'error': 'Nenhum arquivo de vídeo enviado'}), 400
        
    video_file = request.files['video']
    video_path = os.path.join('uploads', video_file.filename)
    os.makedirs('uploads', exist_ok=True)
    video_file.save(video_path)
    
    try:
        video_handler = VideoHandler(video_path)
        video_id = len(video_handlers)
        video_handlers[video_id] = video_handler
        
        return jsonify({
            'status': 'success',
            'video_id': video_id,
            'message': 'Vídeo registrado com sucesso'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/video/frame/<int:video_id>', methods=['GET'])
def get_video_frame(video_id):
    if video_id not in video_handlers:
        return jsonify({'error': 'ID de vídeo não encontrado'}), 404
        
    video_handler = video_handlers[video_id]
    frame_base64 = video_handler.get_frame_as_base64()
    
    return jsonify({
        'frame': frame_base64
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
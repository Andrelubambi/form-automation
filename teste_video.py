from core.automation_script import AutomationScript
import os

def teste_video():
    print("Iniciando teste com vídeo...")
    
    # Verificar se existe um vídeo de teste
    video_path = 'videos/teste.mp4'
    if not os.path.exists(video_path):
        print(f"ATENÇÃO: Coloque um arquivo de vídeo em {video_path}")
        print("O vídeo deve estar no formato MP4")
        return
    
    # Criar script
    script = AutomationScript(
        name="Teste Vídeo",
        description="Teste de upload de vídeo"
    )
    
    # Configurar script para um site de teste
    # Neste exemplo, usamos o Google Meet, mas você pode adaptar para qualquer site
    script.add_step('click', '#join-meeting-button', wait_time=2)
    script.add_step('input', '#video-input', is_video=True, wait_time=2)
    
    # Configurar vídeo
    script.set_video(video_path)
    
    # Solicitar URL para teste
    print("\nVocê pode testar em sites como:")
    print("- Google Meet (https://meet.google.com/XXX-YYYY-ZZZ)")
    print("- Zoom (https://zoom.us/join)")
    print("- Microsoft Teams (https://teams.microsoft.com/XXX)")
    url = input("\nDigite a URL para testar: ")
    
    if url:
        print("\nExecutando teste...")
        if script.execute(url):
            print("Teste com vídeo executado com sucesso!")
        else:
            print("Erro ao executar teste com vídeo")

if __name__ == '__main__':
    # Criar diretório de vídeos se não existir
    os.makedirs('videos', exist_ok=True)
    teste_video() 
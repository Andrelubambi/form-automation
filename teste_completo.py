from core.automation_script import AutomationScript
import os

def criar_e_executar_teste():
    # Criar diretório para vídeos se não existir
    os.makedirs('videos', exist_ok=True)
    
    # Criar arquivo de vídeo de teste (pode substituir por um vídeo real)
    video_path = 'videos/teste.mp4'
    if not os.path.exists(video_path):
        print(f"ATENÇÃO: Coloque um arquivo de vídeo em {video_path}")
        return
    
    # Criar script de teste
    script = AutomationScript(
        name="Teste Completo",
        description="Script de teste com vídeo e formulário"
    )
    
    # Configurar passos do script
    # Exemplo para meet.google.com (ajuste os seletores conforme necessário)
    script.add_step('click', '#join-meeting-button', wait_time=2)
    script.add_step('input', '#email-input', 'email')
    script.add_step('input', '#name-input', 'nome')
    script.add_step('input', '#video-input', is_video=True)
    script.add_step('click', '#join-button', wait_time=1)
    
    # Configurar dados do formulário
    script.set_form_data({
        'email': 'teste@exemplo.com',
        'nome': 'Usuário Teste'
    })
    
    # Configurar vídeo
    script.set_video(video_path)
    
    # Salvar script
    script.save('scripts/teste_completo.json')
    print("Script criado com sucesso!")
    
    # Executar script
    url = input("Digite a URL para testar (ex: https://meet.google.com/XXX-YYYY-ZZZ): ")
    if url:
        print("\nExecutando script...")
        if script.execute(url):
            print("Teste executado com sucesso!")
        else:
            print("Erro ao executar teste")

if __name__ == '__main__':
    criar_e_executar_teste() 
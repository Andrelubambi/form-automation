from core.automation_script import AutomationScript

def criar_script_exemplo():
    # Criar novo script
    script = AutomationScript(
        name="Preenchimento de Formulário",
        description="Script para preencher formulário com vídeo"
    )
    
    # Adicionar passos do script
    script.add_step('click', '#botao-iniciar', wait_time=2)
    script.add_step('input', '#nome', 'nome')
    script.add_step('input', '#email', 'email')
    script.add_step('input', '#telefone', 'telefone')
    script.add_step('input', '#video-upload', is_video=True)
    script.add_step('click', '#enviar', wait_time=1)
    
    # Definir dados do formulário
    script.set_form_data({
        'nome': 'João Silva',
        'email': 'joao@email.com',
        'telefone': '123456789'
    })
    
    # Definir vídeo
    script.set_video('videos/meu_video.mp4')
    
    # Salvar script
    script.save('scripts/formulario.json')
    
def executar_script():
    # Carregar script
    script = AutomationScript.load('scripts/formulario.json')
    
    # Executar script
    url = 'https://exemplo.com/formulario'
    sucesso = script.execute(url)
    
    if sucesso:
        print("Script executado com sucesso!")
    else:
        print("Erro ao executar script")

if __name__ == '__main__':
    # Criar novo script
    criar_script_exemplo()
    
    # Executar script
    executar_script() 
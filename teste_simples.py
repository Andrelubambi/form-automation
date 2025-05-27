from core.automation_script import AutomationScript

def teste_simples():
    print("Iniciando teste simples...")
    
    # Criar script
    script = AutomationScript(
        name="Teste Simples",
        description="Teste de busca no Google"
    )
    
    # Adicionar passos simples
    script.add_step('input', 'input[name="q"]', 'busca', wait_time=1)
    script.add_step('submit', 'form[role="search"]', wait_time=2)
    
    # Configurar dados
    script.set_form_data({
        'busca': 'teste automação python'
    })
    
    print("Executando busca no Google...")
    
    # Executar script
    if script.execute('https://www.google.com'):
        print("Teste executado com sucesso!")
    else:
        print("Erro ao executar teste")

if __name__ == '__main__':
    teste_simples() 
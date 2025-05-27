import click
import json
import os
from core.automation_script import AutomationScript

@click.group()
def cli():
    """Gerenciador de Scripts de Automação"""
    pass

@cli.command()
@click.argument('nome')
@click.option('--descricao', '-d', help='Descrição do script')
def criar(nome, descricao):
    """Criar novo script de automação"""
    script = AutomationScript(nome, descricao or "")
    
    while True:
        click.echo("\nAdicionar passo ao script:")
        click.echo("1. Click")
        click.echo("2. Input")
        click.echo("3. Submit")
        click.echo("4. Finalizar")
        
        opcao = click.prompt("Escolha uma opção", type=int)
        
        if opcao == 4:
            break
            
        selector = click.prompt("Digite o seletor CSS")
        wait_time = click.prompt("Tempo de espera (segundos)", type=int, default=0)
        
        if opcao == 1:  # Click
            script.add_step('click', selector, wait_time=wait_time)
        elif opcao == 2:  # Input
            campo = click.prompt("Nome do campo")
            is_video = click.confirm("É um campo de vídeo?")
            script.add_step('input', selector, campo, wait_time=wait_time, is_video=is_video)
        elif opcao == 3:  # Submit
            script.add_step('submit', selector, wait_time=wait_time)
            
    # Dados do formulário
    form_data = {}
    while click.confirm("Adicionar dados do formulário?"):
        campo = click.prompt("Nome do campo")
        valor = click.prompt("Valor")
        form_data[campo] = valor
    script.set_form_data(form_data)
    
    # Vídeo
    if click.confirm("Adicionar vídeo?"):
        video_path = click.prompt("Caminho do vídeo")
        script.set_video(video_path)
        
    # Salvar script
    os.makedirs('scripts', exist_ok=True)
    filename = f"scripts/{nome}.json"
    script.save(filename)
    click.echo(f"Script salvo em {filename}")

@cli.command()
@click.argument('nome')
@click.argument('url')
@click.option('--headless', is_flag=True, help='Executar em modo headless')
def executar(nome, url, headless):
    """Executar um script de automação"""
    try:
        filename = f"scripts/{nome}.json"
        script = AutomationScript.load(filename)
        
        if script.execute(url, headless):
            click.echo("Script executado com sucesso!")
        else:
            click.echo("Erro ao executar script")
    except Exception as e:
        click.echo(f"Erro: {str(e)}")

@cli.command()
def listar():
    """Listar scripts disponíveis"""
    if not os.path.exists('scripts'):
        click.echo("Nenhum script encontrado")
        return
        
    scripts = []
    for filename in os.listdir('scripts'):
        if filename.endswith('.json'):
            with open(f"scripts/{filename}", 'r') as f:
                data = json.load(f)
                scripts.append({
                    'nome': data['name'],
                    'descricao': data['description']
                })
                
    if not scripts:
        click.echo("Nenhum script encontrado")
        return
        
    click.echo("\nScripts disponíveis:")
    for script in scripts:
        click.echo(f"\nNome: {script['nome']}")
        if script['descricao']:
            click.echo(f"Descrição: {script['descricao']}")

@cli.command()
@click.argument('nome')
def remover(nome):
    """Remover um script"""
    filename = f"scripts/{nome}.json"
    if os.path.exists(filename):
        os.remove(filename)
        click.echo(f"Script {nome} removido com sucesso")
    else:
        click.echo("Script não encontrado")

if __name__ == '__main__':
    cli() 
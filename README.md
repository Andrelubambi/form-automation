# Sistema de Automação de Formulários

Este sistema permite automatizar o preenchimento de formulários web, monitorar sites em busca de vagas disponíveis e simular vídeos em tempo real.

## Funcionalidades

- Monitoramento automático de sites
- Simulação de vídeo em tempo real usando vídeos pré-gravados
- API REST para controle do sistema
- Suporte a múltiplos navegadores

## Requisitos

- Python 3.8+
- Chrome ou Firefox instalado
- Webcam (opcional, apenas para gravação de novos vídeos)

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd form-automation
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
Crie um arquivo `.env` com as seguintes variáveis:
```
FLASK_SECRET_KEY=sua_chave_secreta
```

## Uso

1. Inicie o servidor:
```bash
python application/app.py
```

2. Para iniciar o monitoramento de um site:
```bash
curl -X POST http://localhost:5000/api/monitor/start \
  -H "Content-Type: application/json" \
  -d '{"url": "https://exemplo.com", "selector": ".vaga-elemento", "interval": 60}'
```

3. Para registrar um vídeo:
```bash
curl -X POST http://localhost:5000/api/video/register \
  -F "video=@seu_video.mp4"
```

## Extensão do Navegador

Em desenvolvimento. A extensão permitirá controlar o sistema diretamente do navegador.

## Contribuição

Contribuições são bem-vindas! Por favor, leia o arquivo CONTRIBUTING.md para detalhes sobre nosso código de conduta e processo de envio de pull requests.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

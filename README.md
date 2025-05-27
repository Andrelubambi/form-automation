# Scripts de Automação

Este repositório contém scripts para automação de formulários e webcam virtual.

## 1. Automação de Formulário de Passaporte

### Arquivos
- `formulario_passaporte.html` - Página web com formulário de passaporte
- `preenchimento_passaporte.user.js` - Script Tampermonkey para preenchimento automático

### Como usar
1. Inicie o servidor Python local:
```bash
python -m http.server 8000
```

2. Acesse o formulário:
```
http://localhost:8000/formulario_passaporte.html
```

3. Instale a extensão Tampermonkey no seu navegador
4. Adicione o script `preenchimento_passaporte.user.js` ao Tampermonkey
5. No formulário, use o menu no canto inferior direito para:
   - Selecionar usuários predefinidos
   - Usar dados aleatórios

### Usuários Predefinidos
- João Silva Santos (Brasileiro)
- Maria Oliveira Costa (Brasileira)
- Pedro Henrique Ferreira (Português)
- Ana Carolina Lima (Italiana)
- Carlos Eduardo Santos (Espanhol)

## 2. Webcam Virtual

### Arquivos
- `generate_video_script.py` - Script Python para gerar o script da webcam
- `webcam_virtual.user.js` - Script Tampermonkey gerado para webcam virtual

### Como usar
1. Execute o script Python para gerar o script da webcam:
```bash
python generate_video_script.py
```

2. O script acima irá gerar o arquivo `webcam_virtual.user.js`
3. Instale este script no Tampermonkey
4. Acesse sites que usam webcam (ex: webcamtests.com, Google Meet)
5. Use o botão flutuante para ativar/desativar a webcam virtual

## Diferenças entre os Scripts

### Script de Formulário
- Foco em preenchimento automático de dados
- Múltiplos usuários predefinidos
- Interface com menu de seleção
- Ideal para testes de formulários

### Script de Webcam
- Simula uma webcam virtual
- Usa vídeo em base64
- Controles de ativação/desativação
- Ideal para testes de videoconferência

## Requisitos
- Python 3.x
- Navegador com extensão Tampermonkey
- Conexão com internet para acessar os sites

## Observações
- Os scripts funcionam independentemente
- Você pode usar um ou outro, ou ambos simultaneamente
- O servidor Python local é necessário apenas para o formulário
- A webcam virtual funciona em qualquer site que use webcam

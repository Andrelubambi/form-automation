// ==UserScript==
// @name         Automatizador de Formulários - Selenium Test Form
// @namespace    http://tampermonkey.net/
// @version      0.2
// @description  Preenche formulários automaticamente com dados de múltiplos usuários
// @author       Você
// @match        https://www.selenium.dev/selenium/web/web-form.html
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        GM_addStyle
// ==/UserScript==

(function () {
    'use strict';

    // Variáveis globais
    let usuarios = [];
    let usuarioSelecionado = null;

    // Estilos CSS
    GM_addStyle(`
        .form-auto-controls {
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 9999999;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            font-family: Arial, sans-serif;
            min-width: 250px;
            max-width: 300px;
            transition: all 0.3s ease;
            transform-origin: top left;
        }
        .form-auto-controls.minimized {
            transform: scale(0);
            opacity: 0;
            pointer-events: none;
        }
        .form-auto-toggle {
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 10000000;
            background: #4CAF50;
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            border: none;
            cursor: pointer;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            transition: all 0.3s ease;
        }
        .form-auto-toggle:hover {
            background: #45a049;
            transform: scale(1.1);
        }
        .form-auto-toggle.hidden {
            transform: scale(0);
            opacity: 0;
        }
        .form-auto-controls select {
            width: 100%;
            padding: 8px;
            margin: 5px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .form-auto-controls button {
            width: 100%;
            padding: 8px 16px;
            margin: 5px 0;
            border: none;
            border-radius: 4px;
            background: #4CAF50;
            color: white;
            cursor: pointer;
        }
        .form-auto-controls button:hover {
            background: #45a049;
        }
        .form-auto-status {
            margin: 10px 0;
            padding: 10px;
            border-radius: 4px;
            background: #f0f0f0;
            font-size: 12px;
        }
        .form-auto-header {
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .form-auto-close {
            background: none;
            border: none;
            color: #666;
            cursor: pointer;
            padding: 5px;
            font-size: 18px;
            width: auto;
        }
        .form-auto-close:hover {
            color: #000;
            background: none;
        }
        .form-auto-user-info {
            margin-top: 10px;
            padding: 10px;
            background: #f9f9f9;
            border-radius: 4px;
            font-size: 12px;
        }
    `);

    // Dados de exemplo
    usuarios = [
        {
            id: "user1",
            nome: "João Silva",
            texto: "Texto de exemplo",
            password: "senha123",
            textarea: "Esta é uma área de texto\nCom múltiplas linhas",
            select: "Two",
            datalist: "Opera",
            colors: "#FF0000",
            date: "2024-03-27",
            range: "5"
        },
        {
            id: "user2",
            nome: "Maria Santos",
            texto: "Outro texto de teste",
            password: "senha456",
            textarea: "Outro texto de exemplo\nPara testar",
            select: "Three",
            datalist: "Chrome",
            colors: "#00FF00",
            date: "2024-03-28",
            range: "8"
        }
    ];

    // Função para preencher campos do formulário
    function preencherFormulario() {
        if (!usuarioSelecionado) {
            alert('Por favor, selecione um usuário primeiro!');
            return;
        }

        // Mapeamento específico para o formulário do Selenium
        const campos = {
            'my-text-id': usuarioSelecionado.texto,
            'my-password': usuarioSelecionado.password,
            'my-textarea': usuarioSelecionado.textarea,
            'my-select': usuarioSelecionado.select,
            'my-datalist': usuarioSelecionado.datalist,
            'my-colors': usuarioSelecionado.colors,
            'my-date': usuarioSelecionado.date,
            'my-range': usuarioSelecionado.range
        };

        // Preencher cada campo
        Object.entries(campos).forEach(([id, valor]) => {
            const elemento = document.getElementById(id);
            if (elemento && !elemento.disabled && !elemento.readOnly) {
                elemento.value = valor;
                // Disparar eventos para garantir que o valor seja atualizado
                elemento.dispatchEvent(new Event('input', { bubbles: true }));
                elemento.dispatchEvent(new Event('change', { bubbles: true }));
                console.log(`Preenchendo campo ${id} com valor: ${valor}`);
            } else {
                console.log(`Campo não encontrado ou desabilitado: ${id}`);
            }
        });

        // Marcar checkboxes e radio buttons
        const checkbox = document.getElementById('my-check-1');
        if (checkbox) {
            checkbox.checked = true;
            checkbox.dispatchEvent(new Event('change', { bubbles: true }));
        }

        const radio = document.getElementById('my-radio-1');
        if (radio) {
            radio.checked = true;
            radio.dispatchEvent(new Event('change', { bubbles: true }));
        }

        atualizarStatus('Formulário preenchido com sucesso!');
    }

    // Função para atualizar a interface
    function atualizarInterface() {
        // Criar botão de toggle se não existir
        if (!document.querySelector('.form-auto-toggle')) {
            const toggleBtn = document.createElement('button');
            toggleBtn.className = 'form-auto-toggle';
            toggleBtn.innerHTML = '⚙️';
            toggleBtn.title = 'Abrir painel de automação';
            document.body.appendChild(toggleBtn);
        }

        // Criar ou atualizar painel de controle
        const controles = document.querySelector('.form-auto-controls');
        if (!controles) {
            const div = document.createElement('div');
            div.className = 'form-auto-controls minimized';

            // Cabeçalho com botão de fechar
            const header = document.createElement('div');
            header.className = 'form-auto-header';

            const titulo = document.createElement('span');
            titulo.textContent = 'Automatização - Selenium Form';
            header.appendChild(titulo);

            const closeBtn = document.createElement('button');
            closeBtn.className = 'form-auto-close';
            closeBtn.innerHTML = '×';
            closeBtn.title = 'Minimizar painel';
            header.appendChild(closeBtn);

            div.appendChild(header);

            // Select para usuários
            const select = document.createElement('select');
            select.innerHTML = '<option value="">Selecione um usuário...</option>' +
                usuarios.map(u => `<option value="${u.id}">${u.nome}</option>`).join('');

            select.onchange = (e) => {
                usuarioSelecionado = usuarios.find(u => u.id === e.target.value);
                atualizarInfoUsuario();
            };
            div.appendChild(select);

            // Botão de preencher
            const btnPreencher = document.createElement('button');
            btnPreencher.textContent = 'Preencher Formulário';
            btnPreencher.onclick = preencherFormulario;
            div.appendChild(btnPreencher);

            // Área de informações do usuário
            const userInfo = document.createElement('div');
            userInfo.className = 'form-auto-user-info';
            div.appendChild(userInfo);

            // Área de status
            const status = document.createElement('div');
            status.className = 'form-auto-status';
            status.textContent = 'Pronto para usar';
            div.appendChild(status);

            document.body.appendChild(div);

            // Adicionar eventos
            const toggle = document.querySelector('.form-auto-toggle');
            toggle.onclick = () => {
                div.classList.remove('minimized');
                toggle.classList.add('hidden');
            };

            closeBtn.onclick = () => {
                div.classList.add('minimized');
                toggle.classList.remove('hidden');
            };
        }
    }

    // Função para atualizar informações do usuário selecionado
    function atualizarInfoUsuario() {
        const infoDiv = document.querySelector('.form-auto-user-info');
        if (infoDiv && usuarioSelecionado) {
            infoDiv.innerHTML = `
                <strong>Usuário selecionado:</strong><br>
                Nome: ${usuarioSelecionado.nome}<br>
                Texto: ${usuarioSelecionado.texto}<br>
                Data: ${usuarioSelecionado.date}<br>
                Senha: ${usuarioSelecionado.password.replace(/./g, '*')}
            `;
        }
    }

    // Função para atualizar status
    function atualizarStatus(mensagem) {
        const statusDiv = document.querySelector('.form-auto-status');
        if (statusDiv) {
            statusDiv.textContent = mensagem;
        }
    }

    // Inicializar
    atualizarInterface();
})(); 
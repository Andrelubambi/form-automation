// ==UserScript==
// @name         Preenchimento Automático - Formulário de Passaporte
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Preenche automaticamente o formulário de passaporte
// @author       Seu Nome
// @match        http://localhost:8000/formulario_passaporte.html
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    // Lista de usuários predefinidos
    const usuarios = {
        'joao': {
            nome: 'João Silva Santos',
            passaporte: 'AB123456',
            nacionalidade: 'Brasileiro(a)',
            genero: 'M',
            dataNascimento: '1990-05-15',
            dataEmissao: '2023-12-01'
        },
        'maria': {
            nome: 'Maria Oliveira Costa',
            passaporte: 'CD789012',
            nacionalidade: 'Brasileiro(a)',
            genero: 'F',
            dataNascimento: '1985-08-22',
            dataEmissao: '2023-11-15'
        },
        'pedro': {
            nome: 'Pedro Henrique Ferreira',
            passaporte: 'EF345678',
            nacionalidade: 'Português(a)',
            genero: 'M',
            dataNascimento: '1995-03-10',
            dataEmissao: '2024-01-05'
        },
        'ana': {
            nome: 'Ana Carolina Lima',
            passaporte: 'GH901234',
            nacionalidade: 'Italiano(a)',
            genero: 'F',
            dataNascimento: '1988-11-30',
            dataEmissao: '2023-10-20'
        },
        'carlos': {
            nome: 'Carlos Eduardo Santos',
            passaporte: 'IJ567890',
            nacionalidade: 'Espanhol(a)',
            genero: 'M',
            dataNascimento: '1992-07-25',
            dataEmissao: '2024-02-01'
        }
    };

    // Função para gerar data aleatória entre duas datas
    function randomDate(start, end) {
        return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
    }

    // Função para gerar número de passaporte aleatório
    function generatePassportNumber() {
        const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        const numbers = '0123456789';
        let passport = '';

        // Formato: XX999999 (2 letras + 6 números)
        for (let i = 0; i < 2; i++) {
            passport += letters.charAt(Math.floor(Math.random() * letters.length));
        }
        for (let i = 0; i < 6; i++) {
            passport += numbers.charAt(Math.floor(Math.random() * numbers.length));
        }
        return passport;
    }

    // Lista de nacionalidades
    const nacionalidades = [
        "Brasileiro(a)",
        "Português(a)",
        "Espanhol(a)",
        "Italiano(a)",
        "Francês(a)",
        "Alemão(ã)",
        "Argentino(a)"
    ];

    // Função para preencher o formulário com dados de um usuário específico
    function preencherFormulario(usuario) {
        const dados = usuarios[usuario];

        // Preenche os campos com os dados do usuário
        document.getElementById('nome').value = dados.nome;
        document.getElementById('passaporte').value = dados.passaporte;
        document.getElementById('nacionalidade').value = dados.nacionalidade;
        document.getElementById('genero').value = dados.genero;
        document.getElementById('data_nascimento').value = dados.dataNascimento;
        document.getElementById('data_emissao').value = dados.dataEmissao;

        // Dispara eventos para calcular idade e data de validade
        const eventChange = new Event('change');
        document.getElementById('data_nascimento').dispatchEvent(eventChange);
        document.getElementById('data_emissao').dispatchEvent(eventChange);
    }

    // Criar menu flutuante
    const menuContainer = document.createElement('div');
    menuContainer.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        z-index: 9999;
        font-family: Arial, sans-serif;
        padding: 10px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    `;

    // Adicionar título
    const titulo = document.createElement('div');
    titulo.style.cssText = `
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 5px;
        text-align: center;
    `;
    titulo.innerHTML = 'Selecione um Usuário';
    menuContainer.appendChild(titulo);

    // Criar botões para cada usuário
    Object.keys(usuarios).forEach(usuario => {
        const botao = document.createElement('button');
        botao.style.cssText = `
            background-color: #2980b9;
            color: white;
            padding: 8px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            transition: background-color 0.3s;
        `;
        botao.innerHTML = usuarios[usuario].nome;
        botao.onclick = () => preencherFormulario(usuario);

        // Adicionar hover effect
        botao.addEventListener('mouseover', function () {
            this.style.backgroundColor = '#3498db';
        });
        botao.addEventListener('mouseout', function () {
            this.style.backgroundColor = '#2980b9';
        });

        menuContainer.appendChild(botao);
    });

    // Adicionar botão para dados aleatórios
    const botaoAleatorio = document.createElement('button');
    botaoAleatorio.style.cssText = `
        background-color: #27ae60;
        color: white;
        padding: 8px 15px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
        margin-top: 5px;
        transition: background-color 0.3s;
    `;
    botaoAleatorio.innerHTML = 'Dados Aleatórios';
    botaoAleatorio.onclick = () => {
        const usuarios_lista = Object.keys(usuarios);
        const usuario_aleatorio = usuarios_lista[Math.floor(Math.random() * usuarios_lista.length)];
        preencherFormulario(usuario_aleatorio);
    };

    // Adicionar hover effect para botão aleatório
    botaoAleatorio.addEventListener('mouseover', function () {
        this.style.backgroundColor = '#2ecc71';
    });
    botaoAleatorio.addEventListener('mouseout', function () {
        this.style.backgroundColor = '#27ae60';
    });

    menuContainer.appendChild(botaoAleatorio);

    // Adicionar menu à página
    document.body.appendChild(menuContainer);
})(); 
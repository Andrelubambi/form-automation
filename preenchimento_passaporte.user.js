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

    // Lista de nomes para gerar aleatoriamente
    const nomes = [
        "João Silva",
        "Maria Santos",
        "Pedro Oliveira",
        "Ana Souza",
        "Carlos Ferreira",
        "Juliana Lima",
        "Roberto Costa",
        "Patricia Almeida"
    ];

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

    // Função para preencher o formulário
    function preencherFormulario() {
        // Nome
        document.getElementById('nome').value = nomes[Math.floor(Math.random() * nomes.length)];

        // Passaporte
        document.getElementById('passaporte').value = generatePassportNumber();

        // Nacionalidade
        document.getElementById('nacionalidade').value = nacionalidades[Math.floor(Math.random() * nacionalidades.length)];

        // Gênero
        const generos = ['M', 'F'];
        document.getElementById('genero').value = generos[Math.floor(Math.random() * generos.length)];

        // Data de Nascimento (entre 18 e 70 anos atrás)
        const hoje = new Date();
        const dataNascimento = randomDate(
            new Date(hoje.getFullYear() - 70, hoje.getMonth(), hoje.getDate()),
            new Date(hoje.getFullYear() - 18, hoje.getMonth(), hoje.getDate())
        );
        document.getElementById('data_nascimento').value = dataNascimento.toISOString().split('T')[0];

        // Dispara evento para calcular idade
        const eventChange = new Event('change');
        document.getElementById('data_nascimento').dispatchEvent(eventChange);

        // Data de Emissão (últimos 6 meses)
        const dataEmissao = randomDate(
            new Date(hoje.getFullYear(), hoje.getMonth() - 6, hoje.getDate()),
            hoje
        );
        document.getElementById('data_emissao').value = dataEmissao.toISOString().split('T')[0];

        // Dispara evento para calcular data de validade
        document.getElementById('data_emissao').dispatchEvent(eventChange);
    }

    // Criar botão flutuante
    const botaoFloat = document.createElement('div');
    botaoFloat.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #2980b9;
        color: white;
        padding: 15px 25px;
        border-radius: 5px;
        cursor: pointer;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        z-index: 9999;
        font-family: Arial, sans-serif;
    `;
    botaoFloat.innerHTML = 'Preencher Formulário';
    botaoFloat.onclick = preencherFormulario;

    // Adicionar botão à página
    document.body.appendChild(botaoFloat);

    // Adicionar hover effect
    botaoFloat.addEventListener('mouseover', function () {
        this.style.backgroundColor = '#3498db';
    });
    botaoFloat.addEventListener('mouseout', function () {
        this.style.backgroundColor = '#2980b9';
    });
})(); 
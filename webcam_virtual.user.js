// ==UserScript==
// @name         Simulador de Webcam Virtual
// @namespace    http://tampermonkey.net/
// @version      0.3
// @description  Simula uma webcam usando um vídeo pré-gravado
// @author       Você
// @match        https://*/*
// @match        http://*/*
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        GM_addStyle
// @grant        unsafeWindow
// @run-at       document-start
// ==/UserScript==

(function () {
    'use strict';

    // Variáveis globais
    let originalGetUserMedia = null;
    let videoElement = null;
    let isActive = true;

    // Adicionar estilos CSS
    GM_addStyle(`
        .webcam-virtual-controls {
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 9999999;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            font-family: Arial, sans-serif;
        }
        .webcam-virtual-controls button {
            padding: 8px 16px;
            margin: 5px 0;
            border: none;
            border-radius: 4px;
            background: #2196F3;
            color: white;
            cursor: pointer;
        }
        .webcam-virtual-controls button:hover {
            background: #1976D2;
        }
        .webcam-virtual-status {
            margin-bottom: 10px;
            font-weight: bold;
        }
        .debug-info {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
    `);

    // URL do vídeo de exemplo (vídeo mais leve e compatível)
    const VIDEO_URL = 'https://upload.wikimedia.org/wikipedia/commons/transcoded/c/c0/Big_Buck_Bunny_4K.webm/Big_Buck_Bunny_4K.webm.360p.webm';

    async function initializeVideo() {
        if (!videoElement) {
            videoElement = document.createElement('video');
            videoElement.crossOrigin = "anonymous";
            videoElement.src = VIDEO_URL;
            videoElement.muted = true;
            videoElement.autoplay = true;
            videoElement.loop = true;

            // Pré-carregar o vídeo
            try {
                await videoElement.play();
                videoElement.currentTime = 0;
            } catch (error) {
                console.error('Erro ao inicializar vídeo:', error);
            }
        }
        return videoElement;
    }

    // Função para interceptar a API de mídia
    function interceptMediaDevices() {
        if (!originalGetUserMedia) {
            originalGetUserMedia = navigator.mediaDevices.getUserMedia;
        }

        let debugInfo = '';

        navigator.mediaDevices.getUserMedia = async (constraints) => {
            if (!isActive || !constraints.video) {
                debugInfo = 'Usando webcam real...';
                updateDebugInfo(debugInfo);
                return await originalGetUserMedia.call(navigator.mediaDevices, constraints);
            }

            try {
                debugInfo = 'Iniciando webcam virtual...';
                updateDebugInfo(debugInfo);

                const video = await initializeVideo();

                debugInfo += '\nCriando canvas...';
                updateDebugInfo(debugInfo);

                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                canvas.width = 1280;
                canvas.height = 720;

                debugInfo += '\nCriando stream virtual...';
                updateDebugInfo(debugInfo);

                const stream = canvas.captureStream(30);

                function updateCanvas() {
                    if (video.readyState === video.HAVE_ENOUGH_DATA) {
                        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                    }
                    if (isActive) {
                        requestAnimationFrame(updateCanvas);
                    }
                }
                updateCanvas();

                debugInfo += '\nWebcam virtual ativada com sucesso!';
                updateDebugInfo(debugInfo);

                return stream;
            } catch (error) {
                debugInfo += '\nErro: ' + error.message;
                updateDebugInfo(debugInfo);
                console.error('Erro na webcam virtual:', error);
                return await originalGetUserMedia.call(navigator.mediaDevices, constraints);
            }
        };
    }

    function updateDebugInfo(text) {
        const debugDiv = document.querySelector('.debug-info');
        if (debugDiv) {
            debugDiv.textContent = text;
        }
    }

    function adicionarControles() {
        const div = document.createElement('div');
        div.className = 'webcam-virtual-controls';

        const status = document.createElement('div');
        status.className = 'webcam-virtual-status';
        status.textContent = 'Webcam Virtual: Ativa';

        const debug = document.createElement('div');
        debug.className = 'debug-info';
        debug.textContent = 'Aguardando uso da webcam...';

        const botao = document.createElement('button');
        botao.textContent = 'Desativar Webcam Virtual';
        botao.onclick = function () {
            if (isActive) {
                isActive = false;
                navigator.mediaDevices.getUserMedia = originalGetUserMedia;
                status.textContent = 'Webcam Virtual: Inativa';
                botao.textContent = 'Ativar Webcam Virtual';
                debug.textContent = 'Webcam virtual desativada';
            } else {
                isActive = true;
                interceptMediaDevices();
                status.textContent = 'Webcam Virtual: Ativa';
                botao.textContent = 'Desativar Webcam Virtual';
                debug.textContent = 'Webcam virtual reativada';
            }
        };

        div.appendChild(status);
        div.appendChild(botao);
        div.appendChild(debug);
        document.body.appendChild(div);
    }

    // Pré-carregar o vídeo
    initializeVideo().then(() => {
        console.log('Vídeo pré-carregado com sucesso');
    }).catch(error => {
        console.error('Erro ao pré-carregar vídeo:', error);
    });

    // Iniciar interceptação
    interceptMediaDevices();

    // Adicionar controles após o carregamento da página
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', adicionarControles);
    } else {
        adicionarControles();
    }
})(); 
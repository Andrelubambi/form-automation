// ==UserScript==
// @name         Simulador de Webcam Virtual
// @namespace    http://tampermonkey.net/
// @version      0.4
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

    let originalGetUserMedia = null;
    let videoElement = null;
    let isActive = true;
    let videoURL = null;

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
            min-width: 200px;
        }
        .webcam-virtual-controls button {
            padding: 8px 16px;
            margin: 5px 0;
            border: none;
            border-radius: 4px;
            background: #2196F3;
            color: white;
            cursor: pointer;
            width: 100%;
        }
        .webcam-virtual-controls button:hover {
            background: #1976D2;
        }
        .webcam-virtual-controls input[type="file"] {
            margin: 10px 0;
            width: 100%;
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
        .video-preview {
            margin-top: 10px;
            width: 100%;
            max-width: 200px;
            display: none;
        }
    `);

    async function initializeVideo() {
        if (!videoElement) {
            videoElement = document.createElement('video');
            videoElement.muted = true;
            videoElement.autoplay = true;
            videoElement.loop = true;

            if (!videoURL) {
                throw new Error('Nenhum vídeo selecionado');
            }

            videoElement.src = videoURL;

            try {
                await videoElement.play();
                videoElement.currentTime = 0;
            } catch (error) {
                console.error('Erro ao inicializar vídeo:', error);
                throw error;
            }
        }
        return videoElement;
    }

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
                if (!videoURL) {
                    throw new Error('Por favor, selecione um arquivo de vídeo primeiro');
                }

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

    function handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            if (videoURL) {
                URL.revokeObjectURL(videoURL);
            }

            videoURL = URL.createObjectURL(file);

            const preview = document.querySelector('.video-preview');
            if (preview) {
                preview.src = videoURL;
                preview.style.display = 'block';
            }

            if (videoElement) {
                videoElement.src = videoURL;
            }

            updateDebugInfo('Vídeo carregado: ' + file.name);
        }
    }

    function adicionarControles() {
        const div = document.createElement('div');
        div.className = 'webcam-virtual-controls';

        const status = document.createElement('div');
        status.className = 'webcam-virtual-status';
        status.textContent = 'Webcam Virtual: Ativa';

        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = 'video/*';
        fileInput.onchange = handleFileSelect;

        const preview = document.createElement('video');
        preview.className = 'video-preview';
        preview.muted = true;
        preview.controls = true;

        const debug = document.createElement('div');
        debug.className = 'debug-info';
        debug.textContent = 'Selecione um arquivo de vídeo...';

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
                debug.textContent = videoURL ? 'Webcam virtual reativada' : 'Selecione um arquivo de vídeo...';
            }
        };

        div.appendChild(status);
        div.appendChild(fileInput);
        div.appendChild(preview);
        div.appendChild(botao);
        div.appendChild(debug);
        document.body.appendChild(div);
    }

    interceptMediaDevices();

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', adicionarControles);
    } else {
        adicionarControles();
    }
})(); 
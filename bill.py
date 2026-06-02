import streamlit as st

st.set_page_config(page_title="Para Ariana ❤️", page_icon="🐦", layout="centered")

# Estilos CSS y el motor del juego en JavaScript
juego_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        /* Estilos Retro / Pixel Art */
        body { 
            text-align: center; 
            font-family: 'Courier New', Courier, monospace; /* Fuente retro */
            background-color: #fdf2f8; 
            margin: 0; 
            padding: 0; 
        }
        h2 { color: #db2777; margin-top: 10px; font-weight: bold; text-transform: uppercase; }
        
        .game-container {
            position: relative;
            width: 400px;
            margin: 15px auto;
        }
        
        canvas { 
            display: block; 
            border: 6px solid #222; /* Borde grueso retro */
            background: #5c94fc; /* Azul cielo estilo Mario/Retro */
            box-shadow: 8px 8px 0px rgba(0,0,0,0.2); /* Sombra dura */
            image-rendering: pixelated; /* Fuerza renderizado de píxeles */
        }
        
        #mensaje { 
            font-size: 18px; 
            color: #fff; 
            background: #ff758c;
            border: 4px solid #222;
            font-weight: bold; 
            margin: 15px auto; 
            padding: 12px 20px;
            min-height: 30px; 
            width: 80%;
            max-width: 500px;
            box-shadow: 4px 4px 0px #222;
            transition: transform 0.1s;
        }
        
        .pop { animation: popAnim 0.4s ease-out; }
        @keyframes popAnim { 
            0% { transform: scale(1); } 
            50% { transform: scale(1.05); } 
            100% { transform: scale(1); } 
        }
        
        /* Diseño de la Carta Gigante Final Estilo Retro */
        #carta-final {
            display: none;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0);
            background: #fffafa;
            border: 6px solid #222;
            padding: 30px 20px;
            width: 320px;
            box-shadow: 10px 10px 0px rgba(0,0,0,0.8);
            z-index: 10;
            text-align: center;
            cursor: pointer;
        }
        
        .abrir-carta {
            animation: abrirAnim 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        }
        @keyframes abrirAnim {
            0% { transform: translate(-50%, -50%) scale(0); opacity: 0; }
            100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
        }

        .sello { font-size: 45px; margin-bottom: 5px; line-height: 1; }
        .texto-te-amo { font-size: 24px; color: #e11d48; font-weight: 900; margin-bottom: 10px; border-bottom: 2px dashed #222; padding-bottom: 5px; }
        
        .poema {
            font-size: 16px;
            color: #222;
            margin: 15px 0;
            font-weight: bold;
            line-height: 1.6;
        }

        .reinicio { font-size: 12px; color: #555; margin-top: 15px; font-weight: bold; }
        .instrucciones { color: #444; font-size: 14px; margin-bottom: 5px; font-weight: bold; }
    </style>
</head>
<body>

    <h2>🐦 Flappy Bird: Edición Amor ❤️</h2>
    <p class="instrucciones">Presiona la [BARRA ESPACIADORA] o [CLIC] para saltar.</p>
    
    <div class="game-container">
        <canvas id="canvas" width="400" height="500"></canvas>
        
        <div id="carta-final">
            <div class="sello">💌</div>
            <div class="texto-te-amo">Para Ariana ❤️</div>
            <div class="poema">
                Eres el cielo donde aprendí a volar,<br>
                la melodía que no dejo de cantar.<br>
                En cada latido y en cada mañana,<br>
                mi persona favorita siempre eres tú, Ariana.
            </div>
            <div class="reinicio">[ Haz clic aquí para volver a empezar ]</div>
        </div>
    </div>
    
    <div id="mensaje">✨ ¡Presiona espacio para empezar a volar! ✨</div>

    <script>
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");
    ctx.imageSmoothingEnabled = false; // CLAVE PARA EL PIXEL ART

    // Variables de estado
    let bird = { x: 100, y: 440, v: 0, g: 0.12, jump: -3.8, r: 14 }; 
    let pipes = [];
    let score = 0;
    let gameActive = false;
    let bgOffsetX = 0; 
    let pipesSpawned = 0;
    
    // Fases de animación final
    // 0: Inicio/Jugando, 1: Acercando casa, 2: Volando al buzón, 3: Cayendo carta, 4: Carta abierta
    let finalPhase = 0; 
    
    // Objetos de la escena final
    let endScene = {
        active: false,
        x: 0, // Se inicializará cuando lleguemos a nivel 10
        letterDropY: 0
    };

    const mensajes = {
        1: "❤️ ¡Cada segundo contigo es mi parte favorita!",
        2: "✨ Eres la personita que alegra mis días.",
        3: "🌹 Me encantas un poquito más cada vez.",
        4: "💫 Juntos somos el mejor equipo.",
        5: "🧸 Eres mi pensamiento favorito.",
        6: "🌙 Mi mayor deseo es estar contigo siempre.",
        7: "🎵 Mi canción favorita eres tú.",
        8: "⭐ Tienes la sonrisa más bonita.",
        9: "🔮 Todo es más hermoso a tu lado."
    };

    function resetGame(iniciarVuelo = true) {
        bird.x = 100;
        bird.y = 440; // Suelo pixel art
        bird.v = 0;
        pipes = [];
        score = 0;
        pipesSpawned = 0;
        gameActive = false;
        finalPhase = 0;
        endScene.active = false;
        
        let carta = document.getElementById("carta-final");
        carta.style.display = "none";
        carta.classList.remove("abrir-carta");
        document.getElementById("mensaje").style.display = "block";
        
        if (iniciarVuelo) {
            gameActive = true;
            bird.v = bird.jump;
            mostrarMensaje("¡Vamos mi amor, tú puedes! 🚀");
        } else {
            mostrarMensaje("✨ ¡Presiona espacio para empezar a volar! ✨");
        }
    }

    function mostrarMensaje(texto) {
        let msgDiv = document.getElementById("mensaje");
        msgDiv.innerText = texto;
        msgDiv.classList.remove("pop");
        void msgDiv.offsetWidth; 
        msgDiv.classList.add("pop");
    }

    function spawnPipe() {
        if (pipesSpawned >= 10) return; 

        let gap = 220; 
        let minH = 50;
        let maxH = canvas.height - gap - minH - 40; // Suelo más grueso
        let h = Math.floor(Math.random() * (maxH - minH + 1)) + minH;
        
        pipes.push({ 
            x: canvas.width, 
            top: h, 
            bottom: canvas.height - h - gap, 
            passed: false,
            esUltima: (pipesSpawned === 9) 
        });
        
        pipesSpawned++;
    }

    function bJump() {
        if (finalPhase === 4) {
            resetGame(false); 
        } else if (!gameActive && finalPhase === 0) {
            resetGame(true); 
        } else if (gameActive) {
            bird.v = bird.jump; 
        }
    }
    
    window.addEventListener("keydown", (e) => { 
        if(e.code === "Space") { bJump(); e.preventDefault(); } 
    });
    canvas.addEventListener("click", bJump);
    document.getElementById("carta-final").addEventListener("click", () => resetGame(false));

    // Utilidad para dibujar bloques con contorno (Estilo Pixel Art)
    function drawPixelBlock(x, y, w, h, fill, stroke="#222") {
        ctx.fillStyle = fill;
        ctx.fillRect(x, y, w, h);
        ctx.strokeStyle = stroke;
        ctx.lineWidth = 3;
        ctx.strokeRect(x, y, w, h);
    }

    function drawBackground() {
        // Cielo (limpio, color sólido)
        ctx.fillStyle = "#5c94fc";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Nubes Pixel Art
        let scrollSpeed = (gameActive || finalPhase === 1) ? 1.4 : 0;
        bgOffsetX -= scrollSpeed * 0.2; 
        if (bgOffsetX <= -canvas.width) bgOffsetX = 0;

        ctx.fillStyle = "#ffffff";
        for (let i = 0; i < 2; i++) {
            let offset = bgOffsetX + (i * canvas.width);
            // Nube 1 bloque
            ctx.fillRect(offset + 60, 80, 80, 30);
            ctx.fillRect(offset + 80, 60, 40, 70);
            // Nube 2 bloque
            ctx.fillRect(offset + 260, 180, 60, 20);
            ctx.fillRect(offset + 270, 170, 40, 40);
        }
        
        // Suelo Pixel Art
        let groundY = canvas.height - 40;
        
        // Base tierra
        ctx.fillStyle = "#d8a038"; 
        ctx.fillRect(0, groundY + 12, canvas.width, 28);
        
        // Pasto superior
        ctx.fillStyle = "#54ca2f"; 
        ctx.fillRect(0, groundY, canvas.width, 12);
        
        // Borde negro separador
        ctx.fillStyle = "#222";
        ctx.fillRect(0, groundY, canvas.width, 4);

        // Patrón de césped animado (cuadritos)
        let grassOffset = (bgOffsetX * 5) % 30;
        ctx.fillStyle = "#3da11d";
        for (let x = grassOffset - 30; x < canvas.width; x += 30) {
            ctx.fillRect(x, groundY + 4, 8, 8);
        }
        // Detalles de tierra
        ctx.fillStyle = "#c08020";
        for (let x = grassOffset - 30; x < canvas.width; x += 40) {
            ctx.fillRect(x + 10, groundY + 20, 12, 8);
            ctx.fillRect(x + 25, groundY + 30, 8, 8);
        }
    }

    // Dibujar la casita y el buzón (Escena final)
    function drawEndScene() {
        if (!endScene.active) return;
        
        let x = endScene.x;
        let groundY = canvas.height - 40;

        // --- CASITA PIXEL ART ---
        // Pared blanca
        drawPixelBlock(x + 60, groundY - 70, 80, 70, "#fffafa");
        // Techo rojo
        ctx.fillStyle = "#e11d48";
        ctx.beginPath();
        ctx.moveTo(x + 50, groundY - 70);
        ctx.lineTo(x + 100, groundY - 110);
        ctx.lineTo(x + 150, groundY - 70);
        ctx.fill();
        ctx.strokeStyle = "#222"; ctx.lineWidth = 4;
        ctx.stroke();
        // Puerta
        drawPixelBlock(x + 85, groundY - 35, 20, 35, "#a16207");
        ctx.fillStyle = "#fbbf24"; ctx.fillRect(x + 90, groundY - 20, 4, 4); // perilla
        // Ventana
        drawPixelBlock(x + 115, groundY - 50, 16, 16, "#38bdf8");
        ctx.fillStyle = "#222"; ctx.fillRect(x + 122, groundY - 50, 2, 16); // marco
        ctx.fillRect(x + 115, groundY - 43, 16, 2);

        // --- BUZÓN PIXEL ART ---
        let mailX = x + 10;
        // Poste
        drawPixelBlock(mailX + 6, groundY - 30, 8, 30, "#737373");
        // Caja del buzón
        drawPixelBlock(mailX, groundY - 45, 20, 15, "#3b82f6");
        // Bandera roja
        drawPixelBlock(mailX + 18, groundY - 55, 4, 10, "#ef4444");

        // --- CARTA CAYENDO (Fase 3) ---
        if (finalPhase === 3) {
            drawLetter(bird.x + 10, endScene.letterDropY);
        }
    }

    function drawLetter(x, y) {
        ctx.save();
        ctx.translate(x, y);
        drawPixelBlock(-8, -6, 16, 12, "#ffffff");
        // Sobre
        ctx.strokeStyle = "#222"; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(-8, -6); ctx.lineTo(0, 0); ctx.lineTo(8, -6); ctx.stroke();
        // Corazón pixel
        ctx.fillStyle = "#e11d48";
        ctx.fillRect(-2, 0, 4, 4);
        ctx.restore();
    }

    function update() {
        let scrollSpeed = 1.4;

        if (gameActive) {
            bird.v += bird.g;
            bird.y += bird.v;

            // Chocar con el suelo de textura (-40)
            if (bird.y + bird.r > canvas.height - 40 || bird.y - bird.r < 0) {
                gameActive = false;
                mostrarMensaje("💥 ¡Ups! Chocaste. Haz clic para reiniciar.");
            }

            if (pipes.length === 0 || pipes[pipes.length - 1].x < canvas.width - 200) {
                spawnPipe();
            }

            for (let i = pipes.length - 1; i >= 0; i--) {
                pipes[i].x -= scrollSpeed; 

                // Hitbox cuadrada para Pixel Art
                let hx = bird.x - 10;
                let hy = bird.y - 10;
                let hw = 20; let hh = 20;

                if (hx + hw > pipes[i].x && hx < pipes[i].x + 60) {
                    if (hy < pipes[i].top || hy + hh > canvas.height - pipes[i].bottom) {
                        gameActive = false;
                        mostrarMensaje("💥 ¡Casi! Inténtalo de nuevo, mi vida.");
                    }
                }

                if (!pipes[i].passed && pipes[i].x + 60 < bird.x) {
                    pipes[i].passed = true;
                    score++;
                    
                    if (score >= 10) {
                        gameActive = false; 
                        finalPhase = 1; // Inicia secuencia de la casa
                        document.getElementById("mensaje").style.display = "none";
                        endScene.active = true;
                        endScene.x = canvas.width + 50; // Aparece por la derecha
                    } else if (mensajes[score]) {
                        mostrarMensaje(mensajes[score]);
                    }
                }

                if (pipes[i].x + 60 < 0) pipes.splice(i, 1);
            }
            
        } else if (finalPhase === 1) {
            // Fase 1: La casa se acerca, el pajarito se estabiliza
            bird.v += bird.g;
            bird.y += bird.v;
            if (bird.y > canvas.height - 120) bird.v = -2; // Mini saltitos para mantenerse
            
            endScene.x -= scrollSpeed;
            for (let i = pipes.length - 1; i >= 0; i--) { pipes[i].x -= scrollSpeed; }

            // Cuando el buzón está en una buena posición, paramos el scroll
            if (endScene.x <= canvas.width / 2 + 20) {
                finalPhase = 2; // Ir hacia el buzón
            }
        } else if (finalPhase === 2) {
            // Fase 2: Pajarito vuela directo al buzón
            let targetX = endScene.x - 5; // Arriba del buzón
            let targetY = canvas.height - 40 - 55; 
            
            bird.x += (targetX - bird.x) * 0.05;
            bird.y += (targetY - bird.y) * 0.05;
            
            if (Math.abs(bird.x - targetX) < 2 && Math.abs(bird.y - targetY) < 2) {
                finalPhase = 3; // Soltar carta
                endScene.letterDropY = bird.y + 6;
            }
        } else if (finalPhase === 3) {
            // Fase 3: Carta cae al buzón
            endScene.letterDropY += 3;
            // Pajarito hace un saltito feliz
            bird.y += Math.sin(Date.now() / 100) * 1.5;

            // Si la carta entra al buzón
            if (endScene.letterDropY > canvas.height - 40 - 45) {
                finalPhase = 4;
                let carta = document.getElementById("carta-final");
                carta.style.display = "block";
                carta.classList.add("abrir-carta");
            }
        }

        draw();
        requestAnimationFrame(update);
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawBackground();

        // DIBUJAR TUBERÍAS PIXEL ART
        pipes.forEach(p => {
            let color = p.esUltima ? "#ef4444" : "#4ade80"; // Rojo o Verde
            let highlight = p.esUltima ? "#fca5a5" : "#86efac";
            
            // Cuerpo superior
            drawPixelBlock(p.x, 0, 60, p.top, color);
            ctx.fillStyle = highlight; ctx.fillRect(p.x + 6, 0, 8, p.top - 4); // Brillo

            // Tapa superior
            drawPixelBlock(p.x - 4, p.top - 24, 68, 24, color);
            ctx.fillStyle = highlight; ctx.fillRect(p.x + 2, p.top - 20, 8, 16);

            // Cuerpo inferior
            drawPixelBlock(p.x, canvas.height - p.bottom, 60, p.bottom, color);
            ctx.fillStyle = highlight; ctx.fillRect(p.x + 6, canvas.height - p.bottom + 4, 8, p.bottom);

            // Tapa inferior
            drawPixelBlock(p.x - 4, canvas.height - p.bottom, 68, 24, color);
            ctx.fillStyle = highlight; ctx.fillRect(p.x + 2, canvas.height - p.bottom + 4, 8, 16);
        });

        drawEndScene();

        // CARTA EN EL SUELO (Antes de empezar)
        if (!gameActive && finalPhase === 0 && pipes.length === 0) {
            drawLetter(bird.x + 35, bird.y + 12);
        }

        // DIBUJAR PAJARITO PIXEL ART
        ctx.save();
        ctx.translate(bird.x, bird.y);
        
        let rot = 0;
        if (gameActive) rot = Math.min(Math.PI / 6, Math.max(-Math.PI / 6, (bird.v * 0.1)));
        ctx.rotate(rot);

        let s = 3; // Escala del pixel art del ave
        
        // Cuerpo (Caja amarilla con borde negro)
        drawPixelBlock(-4*s, -3*s, 8*s, 7*s, "#fde047");
        
        // Ojo
        ctx.fillStyle = "#222"; ctx.fillRect(1*s, -1.5*s, 1.5*s, 2*s);
        
        // Pico
        drawPixelBlock(4*s, 0, 3*s, 2.5*s, "#f97316");
        
        // Ala (Movimiento según si sube o baja)
        let wingY = (bird.v < 0) ? -1*s : 1*s;
        drawPixelBlock(-3*s, wingY, 4*s, 3*s, "#ffffff");

        // CARTA VOLADORA (Agarrada en el aire, excepto en fase 3 y 4)
        if ((gameActive || finalPhase === 1 || finalPhase === 2) && pipes.length > 0 || (finalPhase>0 && finalPhase<3)) {
            ctx.translate(2*s, 4*s); 
            ctx.rotate(Math.PI / 6);
            drawLetter(0, 0);
        }
        ctx.restore(); 
        
        // MARCADOR PIXEL
        if (finalPhase < 4) {
            ctx.fillStyle = "#fff";
            ctx.font = "bold 24px 'Courier New', monospace";
            ctx.shadowBlur = 0;
            // Borde del texto estilo retro
            ctx.strokeStyle = "#222";
            ctx.lineWidth = 4;
            ctx.strokeText("Nivel: " + score, 15, 35);
            ctx.fillText("Nivel: " + score, 15, 35);
        }

        // TEXTO DE INICIO
        if (!gameActive && pipes.length === 0 && finalPhase === 0) {
            ctx.fillStyle = "rgba(0,0,0,0.5)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#fff";
            ctx.font = "bold 18px 'Courier New', monospace";
            ctx.textAlign = "center";
            
            // Texto con contorno retro
            ctx.strokeStyle = "#222"; ctx.lineWidth = 4;
            ctx.strokeText("Haz clic o presiona", canvas.width/2, 180);
            ctx.fillText("Haz clic o presiona", canvas.width/2, 180);
            
            ctx.strokeText("espacio para volar ❤️", canvas.width/2, 215);
            ctx.fillText("espacio para volar ❤️", canvas.width/2, 215);
            ctx.textAlign = "left"; 
        }
    }

    resetGame(false);
    update();
    </script>
</body>
</html>
"""

# Renderizar el juego
st.components.v1.html(juego_html, height=750)

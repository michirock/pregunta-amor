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
            font-family: 'Courier New', Courier, monospace; 
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
            border: 6px solid #222; 
            background: #ff9a9e; /* Color de respaldo del cielo */
            box-shadow: 8px 8px 0px rgba(219, 39, 119, 0.3); 
            image-rendering: pixelated; 
        }
        
        /* Mensajes de Nivel Mejorados (Mayor tamaño y contraste) */
        #mensaje { 
            font-size: 22px; 
            color: #111; /* Contraste oscuro máximo */
            background: #ffffff; /* Fondo blanco para legibilidad */
            border: 6px solid #222;
            font-weight: 900; 
            margin: 15px auto; 
            padding: 16px 20px;
            min-height: 35px; 
            width: 85%;
            max-width: 500px;
            box-shadow: 6px 6px 0px #f472b6; /* Sombra retro rosada */
            transition: transform 0.1s;
        }
        
        .pop { animation: popAnim 0.4s ease-out; }
        @keyframes popAnim { 
            0% { transform: scale(1); } 
            50% { transform: scale(1.05); } 
            100% { transform: scale(1); } 
        }
        
        /* Carta Final Retro */
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
    ctx.imageSmoothingEnabled = false; 

    // Variables de estado
    let bird = { x: 100, y: 440, v: 0, g: 0.12, jump: -3.8, r: 14 }; 
    let pipes = [];
    let score = 0;
    let gameActive = false;
    let bgOffsetX = 0; 
    let pipesSpawned = 0;
    let finalPhase = 0; 
    
    let endScene = { active: false, x: 0, letterDropY: 0 };

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
        bird.y = 440; 
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
        let maxH = canvas.height - gap - minH - 40; 
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

    function drawPixelBlock(x, y, w, h, fill, stroke="#222") {
        ctx.fillStyle = fill;
        ctx.fillRect(x, y, w, h);
        ctx.strokeStyle = stroke;
        ctx.lineWidth = 3;
        ctx.strokeRect(x, y, w, h);
    }

    // Dibujar Árboles de Cerezo
    function drawCherryTree(x, y) {
        // Tronco
        drawPixelBlock(x + 16, y - 40, 12, 40, "#5c4033");
        // Hojas y pétalos (capas de píxeles)
        drawPixelBlock(x - 8, y - 60, 60, 25, "#db2777"); // Sombra rosa oscura
        drawPixelBlock(x - 4, y - 75, 52, 25, "#f472b6"); // Rosa medio
        drawPixelBlock(x + 4, y - 90, 36, 25, "#fbcfe8"); // Rosa claro superior
    }

    function drawBackground() {
        // 1. Cielo Atardecer Romántico (Bandas horizontales pixeladas)
        ctx.fillStyle = "#ff9a9e"; ctx.fillRect(0, 0, canvas.width, 140);
        ctx.fillStyle = "#fecfef"; ctx.fillRect(0, 140, canvas.width, 140);
        ctx.fillStyle = "#fdfbfb"; ctx.fillRect(0, 280, canvas.width, 220);

        // Sol Atardecer Pixelado (Cruz/Diamante en bloques)
        ctx.fillStyle = "#fde047";
        ctx.fillRect(canvas.width/2 - 40, 180, 80, 80);
        ctx.fillRect(canvas.width/2 - 50, 190, 100, 60);
        ctx.fillRect(canvas.width/2 - 60, 200, 120, 40);

        let scrollSpeed = (gameActive || finalPhase === 1) ? 1.4 : 0;
        bgOffsetX -= scrollSpeed * 0.2; 
        if (bgOffsetX <= -canvas.width) bgOffsetX = 0;

        // 2. Nubes Pixel Art (Moviéndose lento)
        ctx.fillStyle = "#ffffff";
        for (let i = 0; i < 2; i++) {
            let offset = bgOffsetX + (i * canvas.width);
            ctx.fillRect(offset + 60, 80, 80, 30);
            ctx.fillRect(offset + 80, 60, 40, 70);
            ctx.fillRect(offset + 260, 120, 60, 20);
            ctx.fillRect(offset + 270, 110, 40, 40);
        }

        // 3. Árboles de Cerezo en el fondo (Moviéndose velocidad media)
        let groundY = canvas.height - 40;
        let treeOffset = (bgOffsetX * 2.5) % 150; 
        for (let x = treeOffset - 150; x < canvas.width; x += 150) {
            drawCherryTree(x + 30, groundY);
        }
        
        // 4. Suelo Pixel Art (Moviéndose rápido)
        ctx.fillStyle = "#d8a038"; ctx.fillRect(0, groundY + 12, canvas.width, 28);
        ctx.fillStyle = "#54ca2f"; ctx.fillRect(0, groundY, canvas.width, 12);
        ctx.fillStyle = "#222"; ctx.fillRect(0, groundY, canvas.width, 4);

        let grassOffset = (bgOffsetX * 5) % 30;
        ctx.fillStyle = "#3da11d";
        for (let x = grassOffset - 30; x < canvas.width; x += 30) {
            ctx.fillRect(x, groundY + 4, 8, 8);
        }
        ctx.fillStyle = "#c08020";
        for (let x = grassOffset - 30; x < canvas.width; x += 40) {
            ctx.fillRect(x + 10, groundY + 20, 12, 8);
            ctx.fillRect(x + 25, groundY + 30, 8, 8);
        }
    }

    function drawEndScene() {
        if (!endScene.active) return;
        
        let x = endScene.x;
        let groundY = canvas.height - 40;

        // CASITA
        drawPixelBlock(x + 60, groundY - 70, 80, 70, "#fffafa");
        ctx.fillStyle = "#e11d48";
        ctx.beginPath();
        ctx.moveTo(x + 50, groundY - 70);
        ctx.lineTo(x + 100, groundY - 110);
        ctx.lineTo(x + 150, groundY - 70);
        ctx.fill();
        ctx.strokeStyle = "#222"; ctx.lineWidth = 4;
        ctx.stroke();
        
        drawPixelBlock(x + 85, groundY - 35, 20, 35, "#a16207");
        ctx.fillStyle = "#fbbf24"; ctx.fillRect(x + 90, groundY - 20, 4, 4); 
        
        drawPixelBlock(x + 115, groundY - 50, 16, 16, "#38bdf8");
        ctx.fillStyle = "#222"; ctx.fillRect(x + 122, groundY - 50, 2, 16); 
        ctx.fillRect(x + 115, groundY - 43, 16, 2);

        // BUZÓN
        let mailX = x + 10;
        drawPixelBlock(mailX + 6, groundY - 30, 8, 30, "#737373");
        drawPixelBlock(mailX, groundY - 45, 20, 15, "#3b82f6");
        drawPixelBlock(mailX + 18, groundY - 55, 4, 10, "#ef4444");

        // CARTA CAYENDO
        if (finalPhase === 3) {
            drawLetter(bird.x + 10, endScene.letterDropY);
        }
    }

    function drawLetter(x, y) {
        ctx.save();
        ctx.translate(x, y);
        drawPixelBlock(-8, -6, 16, 12, "#ffffff");
        ctx.strokeStyle = "#222"; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(-8, -6); ctx.lineTo(0, 0); ctx.lineTo(8, -6); ctx.stroke();
        ctx.fillStyle = "#e11d48";
        ctx.fillRect(-2, -1, 4, 4);
        ctx.restore();
    }

    function update() {
        let scrollSpeed = 1.4;

        if (gameActive) {
            bird.v += bird.g;
            bird.y += bird.v;

            if (bird.y + bird.r > canvas.height - 40 || bird.y - bird.r < 0) {
                gameActive = false;
                mostrarMensaje("💥 ¡Ups! Chocaste. Haz clic para reiniciar.");
            }

            if (pipes.length === 0 || pipes[pipes.length - 1].x < canvas.width - 200) {
                spawnPipe();
            }

            for (let i = pipes.length - 1; i >= 0; i--) {
                pipes[i].x -= scrollSpeed; 

                // Hitbox cuadrada para Pixel Art (Mejorada para el nuevo pájaro)
                let hx = bird.x - 12;
                let hy = bird.y - 10;
                let hw = 24; let hh = 20;

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
                        finalPhase = 1; 
                        document.getElementById("mensaje").style.display = "none";
                        endScene.active = true;
                        endScene.x = canvas.width + 50; 
                    } else if (mensajes[score]) {
                        mostrarMensaje(mensajes[score]);
                    }
                }

                if (pipes[i].x + 60 < 0) pipes.splice(i, 1);
            }
            
        } else if (finalPhase === 1) {
            bird.v += bird.g;
            bird.y += bird.v;
            if (bird.y > canvas.height - 140) bird.v = -2; 
            
            endScene.x -= scrollSpeed;
            for (let i = pipes.length - 1; i >= 0; i--) { pipes[i].x -= scrollSpeed; }

            if (endScene.x <= canvas.width / 2 + 20) {
                finalPhase = 2; 
            }
        } else if (finalPhase === 2) {
            let targetX = endScene.x - 5; 
            let targetY = canvas.height - 40 - 55; 
            
            bird.x += (targetX - bird.x) * 0.05;
            bird.y += (targetY - bird.y) * 0.05;
            
            if (Math.abs(bird.x - targetX) < 2 && Math.abs(bird.y - targetY) < 2) {
                finalPhase = 3; 
                endScene.letterDropY = bird.y + 6;
            }
        } else if (finalPhase === 3) {
            endScene.letterDropY += 3;
            bird.y += Math.sin(Date.now() / 100) * 1.5;

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

        pipes.forEach(p => {
            let color = p.esUltima ? "#ef4444" : "#4ade80"; 
            let highlight = p.esUltima ? "#fca5a5" : "#86efac";
            
            drawPixelBlock(p.x, 0, 60, p.top, color);
            ctx.fillStyle = highlight; ctx.fillRect(p.x + 6, 0, 8, p.top - 4); 

            drawPixelBlock(p.x - 4, p.top - 24, 68, 24, color);
            ctx.fillStyle = highlight; ctx.fillRect(p.x + 2, p.top - 20, 8, 16);

            drawPixelBlock(p.x, canvas.height - p.bottom, 60, p.bottom, color);
            ctx.fillStyle = highlight; ctx.fillRect(p.x + 6, canvas.height - p.bottom + 4, 8, p.bottom);

            drawPixelBlock(p.x - 4, canvas.height - p.bottom, 68, 24, color);
            ctx.fillStyle = highlight; ctx.fillRect(p.x + 2, canvas.height - p.bottom + 4, 8, 16);
        });

        drawEndScene();

        if (!gameActive && finalPhase === 0 && pipes.length === 0) {
            drawLetter(bird.x + 38, bird.y + 12);
        }

        // --- PAJARITO REDISEÑADO ---
        ctx.save();
        ctx.translate(bird.x, bird.y);
        
        let rot = 0;
        if (gameActive) rot = Math.min(Math.PI / 6, Math.max(-Math.PI / 6, (bird.v * 0.1)));
        ctx.rotate(rot);

        let s = 2.5; // Escala del pajarito
        
        // Cola (Naranja con borde negro manual)
        ctx.fillStyle = "#222"; ctx.fillRect(-8*s, -2*s, 5*s, 4*s);
        ctx.fillStyle = "#f97316"; ctx.fillRect(-7*s, -1.5*s, 4*s, 3*s);

        // Pecho/Panza (Blanca) debajo del cuerpo
        drawPixelBlock(-4*s, 2*s, 8*s, 3*s, "#ffffff");

        // Cuerpo principal (Amarillo)
        drawPixelBlock(-5*s, -4*s, 10*s, 7*s, "#fde047");
        
        // Ojo
        ctx.fillStyle = "#ffffff"; ctx.fillRect(1*s, -2*s, 3*s, 3*s); // Blanco del ojo
        ctx.fillStyle = "#222"; ctx.fillRect(2.5*s, -1*s, 1.5*s, 1.5*s); // Pupila
        
        // Pico (Detallado)
        drawPixelBlock(4*s, 0, 4*s, 3*s, "#f97316");
        ctx.fillStyle = "#222"; ctx.fillRect(4*s, 1.5*s, 4*s, 0.5*s); // Línea del pico
        
        // Ala Animada (Blanca y detallada)
        let wingY = (bird.v < 0) ? -2*s : 1*s;
        drawPixelBlock(-3*s, wingY, 5*s, 3.5*s, "#ffffff");
        ctx.fillStyle = "#cbd5e1"; ctx.fillRect(-2*s, wingY + 2*s, 3*s, 1*s); // Sombra del ala

        // CARTA VOLADORA
        if ((gameActive || finalPhase === 1 || finalPhase === 2) && pipes.length > 0 || (finalPhase>0 && finalPhase<3)) {
            ctx.translate(2*s, 5*s); 
            ctx.rotate(Math.PI / 6);
            drawLetter(0, 0);
        }
        ctx.restore(); 
        
        // MARCADOR
        if (finalPhase < 4) {
            ctx.fillStyle = "#fff";
            ctx.font = "bold 24px 'Courier New', monospace";
            ctx.strokeStyle = "#222";
            ctx.lineWidth = 4;
            ctx.strokeText("Nivel: " + score, 15, 35);
            ctx.fillText("Nivel: " + score, 15, 35);
        }

        // TEXTO DE INICIO
        if (!gameActive && pipes.length === 0 && finalPhase === 0) {
            ctx.fillStyle = "rgba(0,0,0,0.4)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#fff";
            ctx.font = "bold 18px 'Courier New', monospace";
            ctx.textAlign = "center";
            
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

import streamlit as st

st.set_page_config(page_title="Para Ariana ❤️", page_icon="🐦", layout="centered")

# Estilos CSS y el motor del juego en JavaScript
juego_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { 
            text-align: center; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background-color: #fdf2f8; 
            margin: 0; 
            padding: 0; 
        }
        h2 { color: #db2777; margin-top: 10px; }
        
        .game-container {
            position: relative;
            width: 400px;
            margin: 15px auto;
        }
        
        canvas { 
            display: block; 
            border: 5px solid #fff; 
            border-radius: 12px;
            box-shadow: 0 8px 25px rgba(219, 39, 119, 0.3);
            background: #a6c1ee;
        }
        
        #mensaje { 
            font-size: 22px; 
            color: #fff; 
            background: linear-gradient(135deg, #ff758c, #ff7eb3);
            font-weight: bold; 
            margin: 15px auto; 
            padding: 15px 25px;
            min-height: 35px; 
            width: 80%;
            max-width: 500px;
            border-radius: 20px;
            box-shadow: 0 6px 15px rgba(255, 117, 140, 0.5);
            transition: transform 0.1s;
        }
        
        .pop { animation: popAnim 0.4s ease-out; }
        @keyframes popAnim { 
            0% { transform: scale(1); } 
            50% { transform: scale(1.08); } 
            100% { transform: scale(1); } 
        }
        
        /* Diseño de la Carta Gigante Final Mejorada */
        #carta-final {
            display: none;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0);
            background: #fffafa;
            border: 4px dashed #ff758c;
            border-radius: 15px;
            padding: 35px 25px;
            width: 320px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
            z-index: 10;
            text-align: center;
            cursor: pointer;
        }
        
        .abrir-carta {
            animation: abrirAnim 1.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        }
        @keyframes abrirAnim {
            0% { transform: translate(-50%, -50%) scale(0); opacity: 0; }
            100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
        }

        .sello { font-size: 50px; margin-bottom: 5px; line-height: 1; text-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
        .texto-te-amo { font-size: 28px; color: #e11d48; font-weight: 900; margin-bottom: 10px; }
        
        /* Estilos del Poema */
        .poema {
            font-size: 17px;
            color: #4b5563;
            margin: 15px 0;
            font-style: italic;
            font-family: 'Georgia', serif;
            line-height: 1.6;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
        }

        .reinicio { font-size: 13px; color: #888; margin-top: 15px; }
        .instrucciones { color: #6b7280; font-size: 15px; margin-bottom: 5px; }
    </style>
</head>
<body>

    <h2>🐦 Flappy Bird: Edición Amor ❤️</h2>
    <p class="instrucciones">Presiona la <b>Barra Espaciadora</b> o <b>Haz Clic</b> en el cuadro para saltar.</p>
    
    <div class="game-container">
        <canvas id="canvas" width="400" height="500"></canvas>
        
        <div id="carta-final">
            <div class="sello">💌</div>
            <div class="texto-te-amo">Para Ariana ❤️</div>
            <div class="poema">
                Eres el cielo donde aprendí a volar,<br>
                la melodía que no dejo de cantar.<br>
                En cada latido y en cada mañana,<br>
                mi nivel favorito siempre eres tú, Ariana.
            </div>
            <div class="reinicio">(Haz clic aquí para volver a empezar)</div>
        </div>
    </div>
    
    <div id="mensaje">✨ ¡Presiona espacio para empezar a volar! ✨</div>

    <script>
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    // Variables de estado
    let bird = { x: 100, y: 456, v: 0, g: 0.12, jump: -3.8, r: 14 }; 
    let pipes = [];
    let score = 0;
    let gameActive = false;
    let bgOffsetX = 0; 
    let pipesSpawned = 0;
    let finalAnimationPhase = 0; 

    const mensajes = {
        1: "❤️ ¡Cada segundo contigo es mi parte favorita del día!",
        2: "✨ Eres la personita que alegra todos mis días.",
        3: "🌹 Me encantas un poquito más cada vez que te veo.",
        4: "💫 Juntos somos el mejor equipo del mundo.",
        5: "🧸 Eres mi pensamiento favorito las 24 horas.",
        6: "🌙 Si pudiera pedir un deseo, sería estar contigo siempre.",
        7: "🎵 Mi canción favorita eres tú.",
        8: "⭐ Tienes la sonrisa más bonita de todo el universo.",
        9: "🔮 Todo es más hermoso si estás a mi lado."
    };

    function resetGame(iniciarVuelo = true) {
        bird.x = 100;
        bird.y = 456; // Ajustado para el nuevo nivel de la tierra
        bird.v = 0;
        pipes = [];
        score = 0;
        pipesSpawned = 0;
        gameActive = false;
        finalAnimationPhase = 0;
        
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

        let gap = 240; 
        let minH = 50;
        let maxH = canvas.height - gap - minH - 30; // -30 por la tierra
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
        if (finalAnimationPhase === 2) {
            resetGame(false); 
        } else if (!gameActive && finalAnimationPhase === 0) {
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

    function drawBackground() {
        // Cielo
        let sky = ctx.createLinearGradient(0, 0, 0, canvas.height);
        sky.addColorStop(0, "#fbc2eb"); 
        sky.addColorStop(1, "#a6c1ee"); 
        ctx.fillStyle = sky;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Brillo del Sol romántico
        let sunGrad = ctx.createRadialGradient(canvas.width/2, 280, 10, canvas.width/2, 280, 150);
        sunGrad.addColorStop(0, "rgba(255, 255, 255, 0.7)");
        sunGrad.addColorStop(0.4, "rgba(253, 224, 71, 0.3)");
        sunGrad.addColorStop(1, "rgba(253, 224, 71, 0)");
        ctx.fillStyle = sunGrad;
        ctx.beginPath();
        ctx.arc(canvas.width/2, 280, 150, 0, Math.PI*2);
        ctx.fill();

        bgOffsetX -= 0.2; 
        if (bgOffsetX <= -canvas.width) bgOffsetX = 0;

        // Nubes con volumen
        for (let i = 0; i < 2; i++) {
            let offset = bgOffsetX + (i * canvas.width);
            
            // Sombras de las nubes
            ctx.fillStyle = "rgba(255, 255, 255, 0.3)";
            ctx.beginPath(); ctx.arc(offset + 82, 105, 30, 0, Math.PI*2); ctx.fill();
            ctx.beginPath(); ctx.arc(offset + 122, 115, 40, 0, Math.PI*2); ctx.fill();
            ctx.beginPath(); ctx.arc(offset + 162, 105, 30, 0, Math.PI*2); ctx.fill();
            
            // Luces de las nubes
            ctx.fillStyle = "rgba(255, 255, 255, 0.8)";
            ctx.beginPath(); ctx.arc(offset + 80, 100, 30, 0, Math.PI*2); ctx.fill();
            ctx.beginPath(); ctx.arc(offset + 120, 110, 40, 0, Math.PI*2); ctx.fill();
            ctx.beginPath(); ctx.arc(offset + 160, 100, 30, 0, Math.PI*2); ctx.fill();
            
            // Segundo grupo de nubes
            ctx.fillStyle = "rgba(255, 255, 255, 0.8)";
            ctx.beginPath(); ctx.arc(offset + 280, 200, 25, 0, Math.PI*2); ctx.fill();
            ctx.beginPath(); ctx.arc(offset + 310, 210, 35, 0, Math.PI*2); ctx.fill();
            ctx.beginPath(); ctx.arc(offset + 340, 200, 25, 0, Math.PI*2); ctx.fill();
        }
        
        // Suelo texturizado y en movimiento
        let groundY = canvas.height - 30;
        
        // Tierra
        ctx.fillStyle = "#8b5a2b"; 
        ctx.fillRect(0, groundY + 10, canvas.width, 20);
        
        // Pasto base
        ctx.fillStyle = "#4ade80"; 
        ctx.fillRect(0, groundY, canvas.width, 10);
        
        // Briznas de pasto moviéndose (Parallax más rápido)
        ctx.strokeStyle = "#16a34a";
        ctx.lineWidth = 2;
        ctx.beginPath();
        let scrollGrass = (bgOffsetX * 6) % 20; // Se mueve más rápido que las nubes
        for (let x = scrollGrass; x < canvas.width + 20; x += 20) {
            ctx.moveTo(x, groundY + 10);
            ctx.lineTo(x + 5, groundY + 2);
        }
        ctx.stroke();
    }

    function update() {
        if (gameActive) {
            bird.v += bird.g;
            bird.y += bird.v;

            // Chocar con el suelo de textura (-30 de altura)
            if (bird.y + bird.r > canvas.height - 30 || bird.y - bird.r < 0) {
                gameActive = false;
                mostrarMensaje("💥 ¡Ups! Chocaste. Haz clic para reiniciar, mi amor.");
            }

            if (pipes.length === 0 || pipes[pipes.length - 1].x < canvas.width - 250) {
                spawnPipe();
            }

            for (let i = pipes.length - 1; i >= 0; i--) {
                pipes[i].x -= 1.4; 

                let birdHitboxR = bird.r - 3; 
                if (bird.x + birdHitboxR > pipes[i].x && bird.x - birdHitboxR < pipes[i].x + 60) {
                    if (bird.y - birdHitboxR < pipes[i].top || bird.y + birdHitboxR > canvas.height - pipes[i].bottom) {
                        gameActive = false;
                        mostrarMensaje("💥 ¡Casi! Inténtalo de nuevo, mi vida.");
                    }
                }

                if (!pipes[i].passed && pipes[i].x + 60 < bird.x) {
                    pipes[i].passed = true;
                    score++;
                    
                    if (score >= 10) {
                        gameActive = false; 
                        finalAnimationPhase = 1; 
                        document.getElementById("mensaje").style.display = "none";
                    } else if (mensajes[score]) {
                        mostrarMensaje(mensajes[score]);
                    }
                }

                if (pipes[i].x + 60 < 0) pipes.splice(i, 1);
            }
            
        } else if (finalAnimationPhase === 1) {
            let targetX = canvas.width / 2;
            let targetY = canvas.height / 2;
            
            bird.x += (targetX - bird.x) * 0.04;
            bird.y += (targetY - bird.y) * 0.04;
            bird.v = 0; 
            
            for (let i = pipes.length - 1; i >= 0; i--) {
                pipes[i].x -= 1.4;
            }

            if (Math.abs(bird.x - targetX) < 1 && Math.abs(bird.y - targetY) < 1) {
                finalAnimationPhase = 2;
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

        // DIBUJAR TUBERÍAS CON TEXTURAS 3D
        pipes.forEach(p => {
            let pipeGrad = ctx.createLinearGradient(p.x, 0, p.x + 60, 0);
            if (p.esUltima) {
                pipeGrad.addColorStop(0, "#ef4444"); 
                pipeGrad.addColorStop(0.7, "#dc2626"); 
                pipeGrad.addColorStop(1, "#991b1b");
            } else {
                pipeGrad.addColorStop(0, "#22c55e"); 
                pipeGrad.addColorStop(0.7, "#16a34a"); 
                pipeGrad.addColorStop(1, "#14532d"); 
            }
            ctx.fillStyle = pipeGrad;
            
            // Cuerpo del tubo
            ctx.fillRect(p.x, 0, 60, p.top);
            ctx.fillRect(p.x, canvas.height - p.bottom, 60, p.bottom);
            
            // Brillo izquierdo para efecto 3D
            ctx.fillStyle = "rgba(255, 255, 255, 0.25)";
            ctx.fillRect(p.x + 4, 0, 8, p.top);
            ctx.fillRect(p.x + 4, canvas.height - p.bottom, 8, p.bottom);

            // Tapas del tubo
            ctx.fillStyle = pipeGrad;
            ctx.fillRect(p.x - 5, p.top - 25, 70, 25);
            ctx.strokeRect(p.x - 5, p.top - 25, 70, 25);
            ctx.fillRect(p.x - 5, canvas.height - p.bottom, 70, 25);
            ctx.strokeRect(p.x - 5, canvas.height - p.bottom, 70, 25);
            
            // Brillos en las tapas
            ctx.fillStyle = "rgba(255, 255, 255, 0.25)";
            ctx.fillRect(p.x - 1, p.top - 25, 8, 25);
            ctx.fillRect(p.x - 1, canvas.height - p.bottom, 8, 25);
        });

        // CARTA EN EL SUELO (Antes de empezar)
        if (!gameActive && finalAnimationPhase === 0 && pipes.length === 0) {
            ctx.save();
            ctx.translate(bird.x + 28, bird.y + 6); 
            
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(-7, -5, 14, 10);
            ctx.strokeStyle = "#db2777";
            ctx.lineWidth = 1;
            ctx.strokeRect(-7, -5, 14, 10);
            
            ctx.beginPath(); ctx.moveTo(-7, -5); ctx.lineTo(0, 0); ctx.lineTo(7, -5); ctx.stroke();
            
            ctx.fillStyle = "#ef4444"; ctx.font = "8px sans-serif"; ctx.fillText("❤", -3, 3);
            ctx.restore();
        }

        // DIBUJAR PAJARITO 
        if (finalAnimationPhase < 2) {
            ctx.save();
            ctx.translate(bird.x, bird.y);
            let rotation = 0;
            if (gameActive) {
                rotation = Math.min(Math.PI / 4, Math.max(-Math.PI / 4, (bird.v * 0.1)));
            }
            ctx.rotate(rotation);

            // Cuerpo con sombra
            ctx.shadowBlur = 4;
            ctx.shadowColor = "rgba(0,0,0,0.3)";
            let birdGrad = ctx.createRadialGradient(-3, -3, 2, 0, 0, bird.r);
            birdGrad.addColorStop(0, "#fffbe1");
            birdGrad.addColorStop(1, "#fde047");
            ctx.fillStyle = birdGrad;
            ctx.beginPath();
            ctx.arc(0, 0, bird.r, 0, Math.PI * 2);
            ctx.fill();
            ctx.shadowBlur = 0; // Quitar sombra para los detalles
            
            ctx.strokeStyle = "#ca8a04";
            ctx.lineWidth = 1.5;
            ctx.stroke();

            // Ojo
            ctx.fillStyle = "#333";
            ctx.beginPath();
            ctx.arc(4, -4, 3, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = "#fff";
            ctx.beginPath();
            ctx.arc(5, -5, 1, 0, Math.PI * 2);
            ctx.fill();

            // Pico
            ctx.fillStyle = "#f97316";
            ctx.beginPath();
            ctx.moveTo(10, -2);
            ctx.lineTo(18, 1);
            ctx.lineTo(10, 4);
            ctx.fill();
            ctx.stroke();

            // Ala
            ctx.fillStyle = "#fef08a";
            ctx.beginPath();
            ctx.ellipse(-4, 2, 7, 4, -0.2, 0, Math.PI * 2);
            ctx.fill();
            ctx.stroke();

            // CARTA VOLADORA 
            if (gameActive || finalAnimationPhase === 1) {
                ctx.save();
                ctx.translate(6, 6); 
                ctx.rotate(Math.PI / 8);
                
                ctx.fillStyle = "#ffffff";
                ctx.fillRect(0, 0, 14, 10);
                ctx.strokeStyle = "#db2777";
                ctx.lineWidth = 1;
                ctx.strokeRect(0, 0, 14, 10);
                
                ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(7, 5); ctx.lineTo(14, 0); ctx.stroke();
                
                ctx.fillStyle = "#ef4444"; ctx.font = "8px sans-serif"; ctx.fillText("❤", 4, 8);
                ctx.restore(); 
            }
            
            ctx.restore(); 
            
            // MARCADOR 
            ctx.fillStyle = "#fff";
            ctx.font = "bold 28px 'Segoe UI', sans-serif";
            ctx.shadowBlur = 5;
            ctx.shadowColor = "rgba(0,0,0,0.5)";
            ctx.fillText("Nivel: " + score, 15, 40);
            ctx.shadowBlur = 0; 
        }

        // TEXTO DE INICIO
        if (!gameActive && pipes.length === 0 && finalAnimationPhase === 0) {
            ctx.fillStyle = "rgba(0,0,0,0.2)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#fff";
            ctx.font = "bold 24px 'Segoe UI', sans-serif";
            ctx.textAlign = "center";
            ctx.shadowBlur = 8;
            ctx.shadowColor = "#000";
            
            ctx.fillText("Haz clic o presiona espacio", canvas.width/2, 180);
            ctx.fillText("para recoger la carta ❤️", canvas.width/2, 215);
            ctx.textAlign = "left"; 
            ctx.shadowBlur = 0;
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

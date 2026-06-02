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
        
        canvas { 
            display: block; 
            margin: 15px auto; 
            border: 5px solid #fff; 
            border-radius: 12px;
            box-shadow: 0 8px 25px rgba(219, 39, 119, 0.3);
        }
        
        /* Contenedor de mensajes súper llamativo */
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
        
        /* Animación para cuando el mensaje cambia */
        .pop { animation: popAnim 0.4s ease-out; }
        @keyframes popAnim { 
            0% { transform: scale(1); } 
            50% { transform: scale(1.08); } 
            100% { transform: scale(1); } 
        }
        
        #final { 
            display: none; 
            font-size: 38px; 
            color: #e11d48; 
            font-weight: 900; 
            margin-top: 20px; 
            text-shadow: 2px 2px 5px rgba(0,0,0,0.2);
            animation: pulse 1s infinite; 
        }
        
        @keyframes pulse { 
            0% { transform: scale(1); } 
            50% { transform: scale(1.05); } 
            100% { transform: scale(1); } 
        }
        
        .instrucciones { color: #6b7280; font-size: 15px; margin-bottom: 5px; }
    </style>
</head>
<body>

    <h2>🐦 Flappy Bird: Edición Ariana ❤️</h2>
    <p class="instrucciones">Presiona la <b>Barra Espaciadora</b> o <b>Haz Clic</b> en el cuadro para saltar.</p>
    
    <canvas id="canvas" width="400" height="500"></canvas>
    
    <div id="mensaje">✨ ¡Presiona espacio para empezar a volar! ✨</div>
    <div id="final">💖 ¡TE AMO, ARIANA! 👑❤️</div>

    <script>
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    // Variables del juego (Físicas más suaves para hacerlo más fácil)
    let bird = { x: 60, y: 150, v: 0, g: 0.18, jump: -4.8, r: 14 };
    let pipes = [];
    let score = 0;
    let gameActive = false;
    let nivel10Alcanzado = false;
    let bgOffsetX = 0; // Para mover las nubes

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

    function resetGame() {
        bird.y = 150;
        bird.v = 0;
        pipes = [];
        score = 0;
        gameActive = true;
        nivel10Alcanzado = false;
        document.getElementById("final").style.display = "none";
        mostrarMensaje("¡Vamos Ariana, tú puedes! 🚀");
    }

    function mostrarMensaje(texto) {
        let msgDiv = document.getElementById("mensaje");
        msgDiv.innerText = texto;
        // Reiniciar la animación
        msgDiv.classList.remove("pop");
        void msgDiv.offsetWidth; // Trigger reflow
        msgDiv.classList.add("pop");
    }

    function spawnPipe() {
        let gap = 200; // ESPACIO MÁS AMPLIO (Antes era 130)
        let minH = 60;
        let maxH = canvas.height - gap - minH;
        let h = Math.floor(Math.random() * (maxH - minH + 1)) + minH;
        pipes.push({ x: canvas.width, top: h, bottom: canvas.height - h - gap, passed: false });
    }

    // Controles
    function bJump() {
        if (!gameActive && !nivel10Alcanzado) {
            resetGame();
        } else if (gameActive) {
            bird.v = bird.jump;
        }
    }
    window.addEventListener("keydown", (e) => { if(e.code === "Space") { bJump(); e.preventDefault(); } });
    canvas.addEventListener("click", bJump);

    function drawBackground() {
        // Cielo romántico degradado
        let sky = ctx.createLinearGradient(0, 0, 0, canvas.height);
        sky.addColorStop(0, "#fbc2eb"); // Rosa pastel
        sky.addColorStop(1, "#a6c1ee"); // Azul pastel
        ctx.fillStyle = sky;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Nubes en movimiento parallax
        bgOffsetX -= 0.3;
        if (bgOffsetX <= -canvas.width) bgOffsetX = 0;

        ctx.fillStyle = "rgba(255, 255, 255, 0.5)";
        for (let i = 0; i < 2; i++) {
            let offset = bgOffsetX + (i * canvas.width);
            // Nube 1
            ctx.beginPath(); ctx.arc(offset + 80, 100, 30, 0, Math.PI*2); ctx.fill();
            ctx.beginPath(); ctx.arc(offset + 120, 110, 40, 0, Math.PI*2); ctx.fill();
            ctx.beginPath(); ctx.arc(offset + 160, 100, 30, 0, Math.PI*2); ctx.fill();
            // Nube 2
            ctx.beginPath(); ctx.arc(offset + 280, 200, 25, 0, Math.PI*2); ctx.fill();
            ctx.beginPath(); ctx.arc(offset + 310, 210, 35, 0, Math.PI*2); ctx.fill();
            ctx.beginPath(); ctx.arc(offset + 340, 200, 25, 0, Math.PI*2); ctx.fill();
        }
        
        // Suelo estilizado
        ctx.fillStyle = "#86efac";
        ctx.fillRect(0, canvas.height - 20, canvas.width, 20);
        ctx.fillStyle = "#4ade80";
        ctx.fillRect(0, canvas.height - 10, canvas.width, 10);
    }

    function update() {
        if (gameActive) {
            bird.v += bird.g;
            bird.y += bird.v;

            // Colisión suelo/techo (dejamos un margen para el piso nuevo)
            if (bird.y + bird.r > canvas.height - 20 || bird.y - bird.r < 0) {
                gameActive = false;
                mostrarMensaje("💥 ¡Ups! Chocaste. Haz clic para reiniciar, mi amor.");
            }

            // Generar tuberías
            if (pipes.length === 0 || pipes[pipes.length - 1].x < canvas.width - 250) {
                spawnPipe();
            }

            for (let i = pipes.length - 1; i >= 0; i--) {
                pipes[i].x -= 1.8; // Velocidad ligeramente más lenta

                // Colisiones con tuberías (Hitbox ajustada para ser más permisiva)
                let birdHitboxR = bird.r - 2; 
                if (bird.x + birdHitboxR > pipes[i].x && bird.x - birdHitboxR < pipes[i].x + 60) {
                    if (bird.y - birdHitboxR < pipes[i].top || bird.y + birdHitboxR > canvas.height - pipes[i].bottom) {
                        gameActive = false;
                        mostrarMensaje("💥 ¡Casi! Inténtalo de nuevo, Ariana.");
                    }
                }

                // Sumar puntos
                if (!pipes[i].passed && pipes[i].x + 60 < bird.x) {
                    pipes[i].passed = true;
                    score++;
                    
                    if (score >= 10) {
                        gameActive = false;
                        nivel10Alcanzado = true;
                        document.getElementById("mensaje").style.display = "none";
                        document.getElementById("final").style.display = "block";
                    } else if (mensajes[score]) {
                        mostrarMensaje(mensajes[score]);
                    }
                }

                if (pipes[i].x + 60 < 0) pipes.splice(i, 1);
            }
        }

        draw();
        requestAnimationFrame(update);
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        drawBackground();

        // Dibujar Tuberías con texturas (Degradados)
        pipes.forEach(p => {
            let pipeGrad = ctx.createLinearGradient(p.x, 0, p.x + 60, 0);
            pipeGrad.addColorStop(0, "#4ade80"); // Verde brillante
            pipeGrad.addColorStop(0.5, "#22c55e"); 
            pipeGrad.addColorStop(1, "#16a34a"); // Verde oscuro sombra
            
            ctx.fillStyle = pipeGrad;
            
            // Tubo Superior
            ctx.fillRect(p.x, 0, 60, p.top);
            // Borde superior (Cap)
            ctx.fillRect(p.x - 5, p.top - 25, 70, 25);
            ctx.strokeRect(p.x - 5, p.top - 25, 70, 25);

            // Tubo Inferior
            ctx.fillRect(p.x, canvas.height - p.bottom, 60, p.bottom);
            // Borde inferior (Cap)
            ctx.fillRect(p.x - 5, canvas.height - p.bottom, 70, 25);
            ctx.strokeRect(p.x - 5, canvas.height - p.bottom, 70, 25);
        });

        // Dibujar Pájaro
        ctx.save();
        ctx.translate(bird.x, bird.y);
        
        // Inclinación del pájaro según su velocidad
        let rotation = Math.min(Math.PI / 4, Math.max(-Math.PI / 4, (bird.v * 0.1)));
        ctx.rotate(rotation);

        if (nivel10Alcanzado) {
            // Forma de Corazón rojo brillante
            ctx.fillStyle = "#ef4444";
            ctx.shadowBlur = 15;
            ctx.shadowColor = "#ef4444";
            ctx.beginPath();
            ctx.arc(0, 0, bird.r + 2, 0, Math.PI * 2);
            ctx.fill();
        } else {
            // Pajarito con degradado amarillo/naranja
            let birdGrad = ctx.createRadialGradient(-3, -3, 2, 0, 0, bird.r);
            birdGrad.addColorStop(0, "#fde047");
            birdGrad.addColorStop(1, "#eab308");
            
            ctx.fillStyle = birdGrad;
            ctx.beginPath();
            ctx.arc(0, 0, bird.r, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = "#ca8a04";
            ctx.lineWidth = 2;
            ctx.stroke();

            // Ojo
            ctx.fillStyle = "#000";
            ctx.beginPath();
            ctx.arc(5, -4, 2.5, 0, Math.PI * 2);
            ctx.fill();
            
            // Brillo del ojo
            ctx.fillStyle = "#fff";
            ctx.beginPath();
            ctx.arc(6, -5, 1, 0, Math.PI * 2);
            ctx.fill();

            // Alita
            ctx.fillStyle = "#fef08a";
            ctx.beginPath();
            ctx.ellipse(-4, 2, 6, 4, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.stroke();
        }
        ctx.restore();

        // Marcador de Score
        ctx.fillStyle = "#fff";
        ctx.font = "bold 28px 'Segoe UI', sans-serif";
        ctx.shadowBlur = 5;
        ctx.shadowColor = "rgba(0,0,0,0.5)";
        ctx.fillText("Nivel: " + score, 15, 40);
        ctx.shadowBlur = 0; // Resetear sombra

        // Pantalla de inicio
        if (!gameActive && pipes.length === 0 && !nivel10Alcanzado) {
            ctx.fillStyle = "rgba(0,0,0,0.4)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#fff";
            ctx.font = "bold 24px 'Segoe UI', sans-serif";
            ctx.textAlign = "center";
            ctx.shadowBlur = 8;
            ctx.shadowColor = "#000";
            ctx.fillText("Haz clic o presiona espacio", canvas.width/2, canvas.height/2 - 10);
            ctx.fillText("para volar ❤️", canvas.width/2, canvas.height/2 + 20);
            ctx.textAlign = "left"; 
            ctx.shadowBlur = 0;
        }
    }

    update();
    </script>
</body>
</html>
"""

# Renderizar el juego real dentro de Streamlit usando componentes HTML
st.components.v1.html(juego_html, height=750)

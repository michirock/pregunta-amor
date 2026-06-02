import streamlit as st

st.set_page_config(page_title="Para Ariana ❤️", page_icon="🐦", layout="centered")

# Estilos CSS y el motor del juego en JavaScript
juego_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { text-align: center; font-family: sans-serif; background-color: #f0f0f0; margin: 0; padding: 0; }
        canvas { background: #70c5ce; display: block; margin: 20px auto; border: 4px solid #333; border-radius: 8px; }
        #mensaje { font-size: 20px; color: #ff4b4b; font-weight: bold; margin-top: 15px; min-height: 30px; }
        #final { display: none; font-size: 35px; color: #ff4b4b; font-weight: bold; margin-top: 20px; animation: pulse 1s infinite; }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.1); } 100% { transform: scale(1); } }
        .instrucciones { color: #555; font-size: 14px; }
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

    // Variables del juego
    let bird = { x: 50, y: 150, v: 0, g: 0.25, jump: -5.5, r: 12 };
    let pipes = [];
    let score = 0;
    let gameActive = false;
    let nivel10Alcanzado = false;

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
        document.getElementById("mensaje").innerText = "¡Vamos Ariana, tú puedes! 🚀";
    }

    function spawnPipe() {
        let gap = 130;
        let minH = 50;
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

    function update() {
        if (gameActive) {
            bird.v += bird.g;
            bird.y += bird.v;

            // Colisión suelo/techo
            if (bird.y + bird.r > canvas.height || bird.y - bird.r < 0) {
                gameActive = false;
                document.getElementById("mensaje").innerText = "💥 ¡Ups! Chocaste. Haz clic para reiniciar, Ariana.";
            }

            // Tuberías
            if (pipes.length === 0 || pipes[pipes.length - 1].x < canvas.width - 200) {
                spawnPipe();
            }

            for (let i = pipes.length - 1; i >= 0; i--) {
                pipes[i].x -= 2;

                // Colisiones con tuberías
                if (bird.x + bird.r > pipes[i].x && bird.x - bird.r < pipes[i].x + 50) {
                    if (bird.y - bird.r < pipes[i].top || bird.y + bird.r > canvas.height - pipes[i].bottom) {
                        gameActive = false;
                        document.getElementById("mensaje").innerText = "💥 ¡Casi! Inténtalo de nuevo, Ariana.";
                    }
                }

                // Sumar puntos
                if (!pipes[i].passed && pipes[i].x + 50 < bird.x) {
                    pipes[i].passed = true;
                    score++;
                    
                    if (score >= 10) {
                        gameActive = false;
                        nivel10Alcanzado = true;
                        document.getElementById("mensaje").innerText = "";
                        document.getElementById("final").style.display = "block";
                    } else if (mensajes[score]) {
                        document.getElementById("mensaje").innerText = mensajes[score];
                    }
                }

                if (pipes[i].x + 50 < 0) pipes.splice(i, 1);
            }
        }

        draw();
        requestAnimationFrame(update);
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Dibujar Tuberías
        ctx.fillStyle = "#73bf2e";
        pipes.forEach(p => {
            ctx.fillRect(p.x, 0, 50, p.top);
            ctx.fillRect(p.x, canvas.height - p.bottom, 50, p.bottom);
        });

        // Dibujar Pájaro (Forma de corazón o ave amarilla)
        ctx.fillStyle = nivel10Alcanzado ? "#ff4b4b" : "#f1c40f";
        ctx.beginPath();
        ctx.arc(bird.x, bird.y, bird.r, 0, Math.PI * 2);
        ctx.fill();

        // Ojo del pájaro
        if (!nivel10Alcanzado) {
            ctx.fillStyle = "#000";
            ctx.beginPath();
            ctx.arc(bird.x + 4, bird.y - 4, 2, 0, Math.PI * 2);
            ctx.fill();
        }

        // Marcador de Score
        ctx.fillStyle = "#333";
        ctx.font = "bold 24px sans-serif";
        ctx.fillText("Nivel: " + score, 20, 40);

        // Pantalla de inicio
        if (!gameActive && pipes.length === 0 && !nivel10Alcanzado) {
            ctx.fillStyle = "rgba(0,0,0,0.3)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#fff";
            ctx.font = "20px sans-serif";
            ctx.textAlign = "center";
            ctx.fillText("Haz clic aquí para Jugar", canvas.width/2, canvas.height/2);
            ctx.textAlign = "left"; // reset
        }
    }

    update();
    </script>
</body>
</html>
"""

# Renderizar el juego real dentro de Streamlit usando componentes HTML
st.components.v1.html(juego_html, height=650)

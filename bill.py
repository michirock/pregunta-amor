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
        //

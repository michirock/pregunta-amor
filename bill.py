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
        
        /* Contenedor relativo para posicionar la carta final encima del canvas */
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
            background: #a6c1ee; /* Color de respaldo */
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
        
        /* Diseño de la Carta Gigante Final */
        #carta-final {
            display: none;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0);
            background: #fffafa;
            border: 4px dashed #ff758c;
            border-radius: 15px;
            padding: 40px 20px;
            width: 280px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
            z-index: 10;
            text-align: center;
            cursor: pointer;
        }
        
        /* Animación para que la carta se agrande */
        .abrir-carta {
            animation: abrirAnim 1s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        }
        @keyframes abrirAnim {
            0% { transform: translate(-50%, -50%) scale(0); opacity: 0; }
            100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
        }

        .sello { font-size: 55px; margin-bottom: 10px; line-height: 1; }
        .texto-te-amo { font-size: 32px; color: #e11d48; font-weight: 900; }
        .reinicio { font-size: 13px; color: #888; margin-top: 20px; }

        .instrucciones { color: #6b7280; font-size: 15px; margin-bottom: 5px; }
    </style>
</head>
<body>

    <h2>🐦 Flappy Bird: Edición Ariana ❤️</h2>
    <p class="instrucciones">Presiona la <b>Barra Espaciadora</b> o <b>Haz Clic</b> en el cuadro para saltar.</p>
    
    <div class="game-container">
        <canvas id="canvas" width="400" height="500"></canvas>
        
        <div id="carta-final">
            <div class="sello">💌</div>
            <div class="texto-te-amo">¡Te amo Ariana! ❤️</div>
            <div class="reinicio">(Haz clic aquí para volver a volar)</div>
        </div>
    </div>
    
    <div id="mensaje">✨ ¡Presiona espacio para empezar a volar! ✨</div>

    <script>
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    // FÍSICAS MUCHO MÁS FÁCILES
    let bird = { x: 60, y: 150, v: 0, g: 0.12, jump: -3.8, r: 14 }; // g más baja = cae más lento
    let pipes = [];
    let score = 0;
    let gameActive = false;
    let nivel10Alcanzado = false;
    let bgOffsetX = 0; 

    const mensajes = {
        1: "❤️ ¡Cada segundo contigo es mi parte favorita del día!",
        2: "✨ E

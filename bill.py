import streamlit as st
import time

# Configuración de la página
st.set_page_config(page_title="Para Ariana ❤️", page_icon="🐦", layout="centered")

# Inicializar el estado del juego si no existe
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# Mensajes de amor para cada nivel (del 1 al 9)
mensajes = {
    1: "❤️ ¡Cada segundo contigo es mi parte favorita del día!",
    2: "✨ Eres la personita que alegra todos mis días.",
    3: "🌹 Me encantas un poquito más cada vez que te veo.",
    4: "💫 Juntos somos el mejor equipo del mundo.",
    5: "🧸 Eres mi pensamiento favorito las 24 horas.",
    6: "🌙 Si pudiera pedir un deseo, sería estar contigo siempre.",
    7: "🎵 Mi canción favorita eres tú.",
    8: "⭐ Tienes la sonrisa más bonita de todo el universo.",
    9: "🔮 Todo es más hermoso si estás a mi lado."
}

st.title("🐦 Flappy Bird: Edición Ariana")
st.write("¡Esquiva los obstáculos clonados en la pantalla y llega al nivel 10!")

# Estilo CSS para la animación del corazón del Nivel 10
st.markdown("""
<style>
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.3); }
    100% { transform: scale(1); }
}
.corazon-abierto {
    font-size: 100px;
    text-align: center;
    animation: pulse 1.5s infinite;
    cursor: default;
}
.mensaje-final {
    font-size: 40px;
    color: #ff4b4b;
    font-weight: bold;
    text-align: center;
    font-family: 'Courier New', Courier, monospace;
}
</style>
""", unsafe_allow_html=True)

# Lógica del Juego
if st.session_state.score < 10:
    st.subheader(f"Nivel Actual: {st.session_state.score}")
    
    # Barra de progreso hacia el nivel 10
    st.progress(st.session_state.score * 10)
    
    # Simulación del salto de Flappy Bird con botones interactivos
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 ¡SALTAR OBSTÁCULO!", use_container_width=True):
            st.session_state.score += 1
            st.rerun()
            
    with col2:
        if st.button("💥 Chocar (Reiniciar)", use_container_width=True):
            st.session_state.score = 0
            st.toast("¡Ups! Volvamos a intentar, Ariana 🐧")
            st.rerun()

    # Mostrar mensajito de amor según el nivel actual
    if st.session_state.score in mensajes:
        st.info(mensajes[st.session_state.score])

else:
    # --- NIVEL 10: PANTALLA DE VICTORIA Y ANIMACIÓN ---
    st.balloons() # Animación nativa de globos celebrando
    
    # Animación del corazón latiendo/abriéndose
    st.markdown('<div class="corazon-abierto">💖</div>', unsafe_allow_html=True)
    st.markdown('<div class="mensaje-final">¡TE AMO, ARIANA! 👑❤️</div>', unsafe_allow_html=True)
    
    st.write("---")
    if st.button("🔄 Jugar de nuevo"):
        st.session_state.score = 0
        st.rerun()

import streamlit as st

# 1. Configuración de la página
st.set_page_config(page_title="Pregunta seria...", page_icon="❤️", layout="centered")

# CSS personalizado para mantener el alto contraste y los estilos estables
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffe6e6;
    }
    h1, h2, h3, p, span, label {
        color: #1a1a1a !important;
        font-family: 'Arial', sans-serif;
    }
    h1 {
        text-align: center;
        font-weight: bold;
    }
    /* Estilo gigante personalizado para el nombre */
    .texto-gigante {
        font-size: 55px !important;
        color: #ff1a1a !important;
        text-align: center;
        font-weight: 900;
        letter-spacing: 2px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    /* Estilo del corazón de dibujo grande */
    .corazon-grande {
        font-size: 100px;
        text-align: center;
        line-height: 1;
        margin: 20px 0;
    }
    /* Estilo de los botones */
    div.stButton > button {
        background-color: #ff4d4d;
        color: white !important;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
        border: none;
        padding: 10px;
    }
    div.stButton > button:hover {
        background-color: #ff1a1a;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializar los estados en la sesión de Streamlit
if "intentos_no" not in st.session_state:
    st.session_state.intentos_no = 0
if "acepto" not in st.session_state:
    st.session_state.acepto = False

# Mensaje inicial
st.write("### ❤️ Hola mi amor... Tengo una pregunta muy importante para ti:")
st.title("¿Me amas? 🥰")
st.write("")

# Lógica si aún no ha aceptado
if not st.session_state.acepto:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("¡SÍ! ❤️"):
            st.session_state.acepto = True
            st.rerun()

    with col2:
        # Interacciones extendidas para el botón "NO"
        if st.session_state.intentos_no == 0:
            if st.button("No 💔"):
                st.session_state.intentos_no += 1
                st.rerun()
                
        elif st.session_state.intentos_no == 1:
            st.warning("¿Cómo que no? 🤔 ¡Inténtalo de nuevo!")
            if st.button("¿Segura? 🥺"):
                st.session_state.intentos_no += 1
                st.rerun()
                
        elif st.session_state.intentos_no == 2:
            st.error("Respuesta incorrecta... piénsalo bien. 😜")
            if st.button("Claro que no... 😭"):
                st.session_state.intentos_no += 1
                st.rerun()
                
        elif st.session_state.intentos_no == 3:
            st.error("Es físicamente imposible que no me ames. 🔬")
            if st.button("Que noooo 😡"):
                st.session_state.intentos_no += 1
                st.rerun()
                
        elif st.session_state.intentos_no == 4:
            st.info("Ya gastaste todos tus intentos de 'No'. Tu única opción es ser feliz a mi lado. 😏")
            if st.button("Oblígame 👁️👄👁️"):
                st.session_state.intentos_no += 1
                st.rerun()
                
        else:
            st.error("🚨 Error 404: Botón 'NO' deshabilitado por exceso de terquedad.")
            st.info("Por favor, presiona el gran botón de la izquierda. 👉❤️")

# Lógica cuando presiona "SÍ"
else:
    st.balloons()  # Lluvia de globos interactivas
    st.success("¡Siiii! Sabía que la respuesta correcta era esa. 😍")
    
    # Dibujo de corazón limpio, grande y sin caja negra
    st.markdown('<div class="corazon-grande">❤️</div>', unsafe_allow_html=True)
    
    # Texto en mayúsculas y gigante solicitado
    st.markdown('<div class="texto-gigante">TE AMO ARIANA</div>', unsafe_allow_html=True)
    
    st.write("### ¡Yo también te amo con todo mi corazón! ❤️")
    st.write("Gracias por ser la mejor novia del mundo mundial. 🥰")
    st.write("")
    
    if st.button("Empezar de nuevo 🔄"):
        st.session_state.intentos_no = 0
        st.session_state.acepto = False
        st.rerun()

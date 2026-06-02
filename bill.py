import streamlit as st

# Configuración de la página (Título e Icono en la pestaña del navegador)
st.set_page_config(page_title="Pregunta seria...", page_icon="❤️", layout="centered")

# Estilos personalizados para poner fondo rosa y ocultar menús aburridos
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffe6e6;
    }
    h1 {
        color: #ff4d4d;
        text-align: center;
        font-family: 'Arial', sans-serif;
    }
    div.stButton > button {
        background-color: #ff4d4d;
        color: white;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
        border: none;
        padding: 10px;
    }
    div.stButton > button:hover {
        background-color: #ff1a1a;
        color: white;
    }
    </style>
   """,
    unsafe_allow_html=True
)

# Inicializar estados para saber si intentó decir que NO o si ya dijo que SÍ
if "intentos_no" not in st.session_state:
    st.session_state.intentos_no = 0
if "acepto" not in st.session_state:
    st.session_state.acepto = False

# Título principal
st.write("### ❤️ Hola mi amor... Tengo una pregunta para ti:")
st.title("¿Me amas? 🥰")

# Si todavía no acepta, mostramos los botones
if not st.session_state.acepto:
    col1, col2 = st.columns(2)

    with col1:
        # El botón de SÍ cambia el estado a True
        if st.button("¡SÍ! ❤️"):
            st.session_state.acepto = True
            st.rerun()

    with col2:
        # Lógica del botón NO según los intentos
        if st.session_state.intentos_no == 0:
            if st.button("No 💔"):
                st.session_state.intentos_no += 1
                st.rerun()
        elif st.session_state.intentos_no == 1:
            st.warning("¡Respuesta incorrecta! Inténtalo de nuevo. 😜")
            if st.button("No... de verdad no 🥺"):
                st.session_state.intentos_no += 1
                st.rerun()
        elif st.session_state.intentos_no == 2:
            st.error("Esa opción está deshabilitada por exceso de terquedad. 😏")
            st.info("Por favor, presiona el botón de la izquierda.")

# Si ya aceptó, mostramos el gran final romántico
else:
    st.balloons() # Lluvia de globos en la pantalla
    st.success("¡Siiii! Sabía que me amabas. 😍")
    
    # Dibujo del corazón en texto gigante y centrado
    corazon = """
         ****** ******
       ** ******** **
     ** ************ **
    ** ************** **
    ** ************** **
     ** ************ **
       ** ********** **
         ** ****** **
           ** **** **
             ** ** **
               ****
                **
    """
    st.code(corazon, language="text")
    
    st.write("### ¡Yo también te amo con todo mi corazón! ❤️")
    st.write("Gracias por ser la mejor novia del mundo mundial. 🥰")
    st.write("_¡Eres mi bug favorito en este código llamado vida!_ 💻✨")
    
    # Botón para reiniciar por si quiere jugar otra vez
    if st.button("Empezar de nuevo 🔄"):
        st.session_state.intentos_no = 0
        st.session_state.acepto = False
        st.rerun()

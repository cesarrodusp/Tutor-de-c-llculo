import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE SEGURIDAD ---
# Opción A: Pegar la llave aquí (Rápido pero menos seguro)
# Opción B: Usar st.secrets (Ideal para producción)
API_KEY = "TU_API_KEY_AQUÍ" 

genai.configure(api_key=API_KEY)

# Instrucciones detalladas para el comportamiento de la IA
INSTRUCCIONES = """
Eres un Tutor Socrático de Cálculo Diferencial. 
Tu misión es guiar al estudiante sin resolver los ejercicios por él.

HABILIDAD ESPECIAL: 
Si el usuario pide un ejercicio o reto, propón uno sobre: límites, derivadas, o optimización. 
Clasifícalo como 'Básico', 'Intermedio' o 'Reto' y usa LaTeX. 
No des la solución, espera a que el alumno muestre su avance.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=INSTRUCCIONES
)

# --- INTERFAZ ---
st.set_page_config(page_title="Tutor IA - Cálculo", page_icon="📐")

with st.sidebar:
    st.title("Panel de Control")
    st.info("Este tutor usa el método socrático para enseñarte cálculo.")
    if st.button("🎲 Proponer un ejercicio"):
        # Esto añade un mensaje automático al chat
        if "messages" not in st.session_state:
            st.session_state.messages = []
        st.session_state.messages.append({"role": "user", "content": "Por favor, propónme un ejercicio para practicar ahora mismo."})

st.title("🎓 Mi Tutor de Cálculo")

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("Escribe tu duda o procedimiento aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Creamos la respuesta enviando el historial completo para que tenga memoria
        chat = model.start_chat(history=[
            {"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages[:-1]
        ])
        response = chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

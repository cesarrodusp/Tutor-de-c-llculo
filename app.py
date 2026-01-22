import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE LA IA ---
# Pega aquí tu API Key
genai.configure(api_key="TU_API_KEY_AQUÍ")

# Instrucciones del sistema (Tu prompt de tutor)
SYSTEM_PROMPT = """
Eres un Tutor Socrático de Cálculo Diferencial. 
REGLA DE ORO: NUNCA des la respuesta final. 
Si el alumno pregunta por una derivada o límite, responde con una pregunta guía.
Usa LaTeX para las fórmulas. 
Si el alumno se frustra, sé empático pero no resuelvas el ejercicio.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# --- INTERFAZ DE LA WEB ---
st.title("🎓 Tutor IA: Cálculo Diferencial")
st.markdown("Bienvenido. Cuéntame en qué ejercicio estás trabajando y lo resolveremos juntos paso a paso.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("¿En qué puedo ayudarte?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Enviar historial al modelo
        chat = model.start_chat(history=[
            {"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages[:-1]
        ])
        response = chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

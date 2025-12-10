import streamlit as st
import random
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Línea del Día", layout="wide")
st.title("Línea del Día de Loterías (Ritmo Algorítmico)")

# --- Lista de loterías ---
loterias = [
    "Gana Más",
    "Lotería Nacional",
    "Quiniela Leidsa",
    "Quiniela Real",
    "Quiniela Loteka",
    "New York 3:30",
    "New York 11:30",
    "Florida Día",
    "Florida Noche",
    "La Primera Día",
    "Primera Noche",
    "La Suerte MD",
    "La Suerte 6PM"
]

# --- Inicializar estado y línea única si no existe ---
if 'estado' not in st.session_state:
    st.session_state.estado = {}
    st.session_state.lineas = {}  # línea única por lotería
    for lot in loterias:
        st.session_state.estado[lot] = {
            "ultimo_num": random.randint(0, 99),  # número inicial 2 dígitos
            "incremento": random.choice([1,3,5,7])
        }
        # Generar línea única al inicio
        info = st.session_state.estado[lot]
        ultimo = info["ultimo_num"]
        d1 = ultimo // 10
        d2 = ultimo % 10
        if d1 == d2:
            representacion = f"{d1}{d2}"  # AA
        else:
            representacion = f"{d1}{d2}{d1}"  # ABA
        st.session_state.lineas[lot] = representacion

# --- Menú para seleccionar lotería ---
loteria_seleccionada = st.selectbox("Selecciona la lotería", loterias)

# --- Mostrar la línea del día ---
st.subheader(f"Línea del Día para {loteria_seleccionada}")
st.markdown(f"**{st.session_state.lineas[loteria_seleccionada]}**")

















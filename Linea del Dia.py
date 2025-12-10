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

# --- Estado interno (para mantener coherencia entre clicks) ---
if 'estado' not in st.session_state:
    st.session_state.estado = {}
    for lot in loterias:
        st.session_state.estado[lot] = {
            "ultimo_num": random.randint(0, 99),  # número inicial 2 dígitos
            "incremento": random.choice([1,3,5,7])  # ritmo algorítmico
        }

# --- Función para generar número tipo span ---
def generar_numero_dos_digitos(loteria):
    info = st.session_state.estado[loteria]
    ultimo = info["ultimo_num"]
    inc = info["incremento"]

    # Generar el nuevo número siguiendo el ritmo
    nuevo = (ultimo + inc) % 100
    st.session_state.estado[loteria]["ultimo_num"] = nuevo

    # Representación tipo span
    d1 = nuevo // 10
    d2 = nuevo % 10
    if d1 == d2:
        return f"{d1}{d2}"  # AA
    else:
        return f"{d1}{d2}{d1}"  # ABA

# --- Botón para generar la línea del día ---
if st.button("Generar Línea del Día"):
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    linea_dia = {"Fecha": fecha_hoy}

    for lot in loterias:
        linea_dia[lot] = generar_numero_dos_digitos(lot)

    st.session_state.linea_dia = linea_dia

# --- Mostrar la línea del día ---
if 'linea_dia' in st.session_state:
    st.subheader(f"Línea del Día: {st.session_state.linea_dia['Fecha']}")
    
    for lot in loterias:
        st.markdown(f"**{lot}:** {st.session_state.linea_dia[lot]}")
















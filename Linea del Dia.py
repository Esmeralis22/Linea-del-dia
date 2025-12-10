# linea_del_dia_unica.py
import streamlit as st
import pandas as pd
from datetime import date, timedelta
import os
import random

# ---------------- CONFIG ----------------
LOTERIAS = [
    "Loteria Nacional- Gana Más",
    "Loteria Nacional- Noche",
    "Quiniela Palé",
    "Quiniela Real",
    "Quiniela Loteka",
    "Quiniela La Primera",
    "Quiniela La Primera Noche",
    "Quiniela La Suerte",
    "Quiniela La Suerte 6PM",
    "New York Tarde",
    "New York Noche",
    "Florida Tarde",
    "Florida Noche",
    "Anguila 10AM",
    "Anguila 1PM",
    "Anguila 6PM",
    "Anguila 9PM",
]

HISTORIAL_DIR = "historial_loterias"
os.makedirs(HISTORIAL_DIR, exist_ok=True)

# ---------------- UTILIDADES ----------------
def vibracion_del_dia(fecha: date) -> int:
    """Calcula la vibración del día (00-99) a partir de la fecha"""
    return (fecha.day + fecha.month + fecha.year) % 100

def load_historial(loteria):
    """Carga historial de la lotería (CSV)"""
    path = os.path.join(HISTORIAL_DIR, f"{loteria.replace(' ','_')}.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return pd.DataFrame(columns=["fecha", "numero"])

def save_historial(loteria, numero):
    """Guarda un número en el historial de la lotería"""
    path = os.path.join(HISTORIAL_DIR, f"{loteria.replace(' ','_')}.csv")
    df = load_historial(loteria)
    today = date.today().isoformat()
    df = pd.concat([df, pd.DataFrame([{"fecha": today, "numero": numero}])], ignore_index=True)
    df.to_csv(path, index=False)

def generar_linea_unica(loteria):
    """Genera la línea del día para una lotería"""
    historial = load_historial(loteria)
    hoy = date.today().isoformat()
    numero_base = vibracion_del_dia(date.today())
    
    # Revisar si el número ya salió hoy
    numeros_hoy = historial[historial["fecha"]==hoy]["numero"].astype(int).tolist()
    intento = numero_base
    intentos = 0
    while intento in numeros_hoy and intentos < 10:
        intento = (intento + 1) % 100
        intentos += 1

    num_str = f"{intento:02d}"
    # Aplicar reglas ABA o AA
    if num_str[0] == num_str[1]:
        linea = num_str*1  # AA → AA
    else:
        linea = num_str[0] + num_str[1] + num_str[0]  # AB → ABA

    # Guardar el número base como salida del día
    save_historial(loteria, intento)
    return linea, intento

# ---------------- STREAMLIT ----------------
st.title("Línea del Día - Todas las Loterías")

st.write("Genera una línea del día única para cada lotería según ritmo algorítmico y números calientes.")

lineas = {}
for loteria in LOTERIAS:
    linea, numero_base = generar_linea_unica(loteria)
    lineas[loteria] = linea
    st.markdown(f"**{loteria}:** <span style='font-size:50px; color:green'>{linea}</span> (Base: {numero_base:02d})", unsafe_allow_html=True)












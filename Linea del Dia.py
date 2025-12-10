import streamlit as st
import pandas as pd
import os
import datetime

st.set_page_config(layout="centered")
st.title("📊 Línea del Día según Vibración y Historial (AB → ABA)")

# Carpeta historial
HIST_DIR = "historial_loterias"
os.makedirs(HIST_DIR, exist_ok=True)

# Nombres exactos de las loterías
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

# ----------------- Funciones -----------------

def registrar_numero(loteria, numero, vibracion_dia):
    """Registra el número diario y retorna línea del día según AB → ABA"""
    archivo = os.path.join(HIST_DIR, f"{loteria.replace(' ','_')}.csv")
    df = pd.read_csv(archivo) if os.path.exists(archivo) else pd.DataFrame(columns=["fecha","numero","vibracion"])
    
    fecha = datetime.date.today().isoformat()
    df = pd.concat([df, pd.DataFrame([{"fecha": fecha, "numero": numero, "vibracion": vibracion_dia}])], ignore_index=True)
    df.to_csv(archivo, index=False)
    
    # Generar Línea del Día AB → ABA
    numero = str(numero).zfill(2)
    if numero[0] == numero[1]:
        linea = numero  # AA → AA
    else:
        linea = numero[0] + numero[1] + numero[0]  # AB → ABA
    return linea

def leer_historial(loteria):
    archivo = os.path.join(HIST_DIR, f"{loteria.replace(' ','_')}.csv")
    if os.path.exists(archivo):
        return pd.read_csv(archivo)
    else:
        return pd.DataFrame(columns=["fecha","numero","vibracion"])

# ----------------- Interfaz -----------------

st.subheader("Selecciona la Lotería")
loteria_sel = st.selectbox("Lotería", LOTERIAS)

st.subheader("Registrar Número y Vibración del Día")
numero_input = st.text_input("Número del día (00-99)", value="00")
vibracion_input = st.text_input("Vibración del día (0-99)", value="17")

if st.button("Registrar y Generar Línea"):
    try:
        linea = registrar_numero(loteria_sel, numero_input, vibracion_input)
        st.markdown(f"**Línea del Día:** <span style='font-size:28px;color:green'>{linea}</span>", unsafe_allow_html=True)
        st.success("Número registrado y Línea del Día calculada.")
    except Exception as e:
        st.error(f"Error: {e}")

st.subheader("Historial de la Lotería")
df_hist = leer_historial(loteria_sel)
st.dataframe(df_hist.tail(10))  # últimos 10 registros










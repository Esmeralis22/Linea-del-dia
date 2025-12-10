import streamlit as st
import pandas as pd
import os
import datetime
import requests
from bs4 import BeautifulSoup
import unicodedata

st.set_page_config(layout="centered")
st.title("📊 Línea del Día — Lotería Dominicana")

# Carpeta historial
HIST_DIR = "historial_loterias"
os.makedirs(HIST_DIR, exist_ok=True)

# Lista de loterías
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

BASE_URL = "https://www.loteriadominicana.com.do/"

# ---------- Funciones ----------

def normalize_text(s):
    """Quita acentos y espacios, pasa a minúsculas"""
    s = unicodedata.normalize('NFKD', s).encode('ASCII','ignore').decode()
    s = s.lower().strip()
    return s

def scrape_resultados():
    """Extrae el número 1ro de cada lotería."""
    resultados = {}
    resp = requests.get(BASE_URL, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    for lot in LOTERIAS:
        lot_norm = normalize_text(lot)
        # Buscar encabezados que contengan la lotería
        header = soup.find(lambda tag: tag.name in ["h2","h3","h4","strong","b"] 
                           and lot_norm in normalize_text(tag.get_text()))
        if header:
            # Buscar siguiente número que sea 1 o 2 dígitos
            text = header.find_next(string=True)
            while text:
                s = text.strip()
                if s.isdigit() and len(s) <= 2:
                    resultados[lot] = s.zfill(2)
                    break
                text = text.find_next(string=True)
    return resultados

def cargar_historial(loteria):
    archivo = os.path.join(HIST_DIR, f"{loteria.replace(' ','_')}.csv")
    if os.path.exists(archivo):
        df = pd.read_csv(archivo, dtype={"numero":str})
    else:
        df = pd.DataFrame(columns=["fecha","numero"])
    return df, archivo

def guardar_historial(loteria, numero):
    df, archivo = cargar_historial(loteria)
    fecha = datetime.date.today().isoformat()
    if not ((df["fecha"] == fecha) & (df["numero"] == numero)).any():
        df = pd.concat([df, pd.DataFrame([{"fecha": fecha, "numero": numero}])], ignore_index=True)
        df.to_csv(archivo, index=False)
    return df

def calcular_vibracion(fecha=None):
    if fecha is None:
        fecha = datetime.date.today()
    return (fecha.year + fecha.month + fecha.day) % 100

def generar_linea_dia(numero):
    numero = str(numero).zfill(2)
    if numero[0] == numero[1]:
        return numero  # AA → AA
    else:
        return numero[0] + numero[1] + numero[0]  # AB → ABA

# ---------- Interfaz ----------

st.subheader("Selecciona la lotería")
loteria_sel = st.selectbox("Lotería", LOTERIAS)

if st.button("Actualizar resultados + generar Línea del Día"):
    try:
        resultados = scrape_resultados()
        numero_base = resultados.get(loteria_sel)
        if numero_base is None:
            st.warning("No se encontró resultado para esa lotería — revisa la página.")
        else:
            guardar_historial(loteria_sel, numero_base)
            vibr = calcular_vibracion()
            linea = generar_linea_dia(numero_base)
            st.markdown(f"**Fecha:** {datetime.date.today().isoformat()}")
            st.markdown(f"**Vibración del día:** {vibr}")
            st.markdown(f"**Número base (1ro):** <span style='font-size:24px;color:blue'>{numero_base}</span>", unsafe_allow_html=True)
            st.markdown(f"**Línea del Día:** <span style='font-size:32px;color:green'>{linea}</span>", unsafe_allow_html=True)
    except Exception as e:
        st.error("Error al obtener resultados: " + str(e))

st.subheader("Historial de la lotería")
df_hist, _ = cargar_historial(loteria_sel)
if not df_hist.empty:
    st.dataframe(df_hist.sort_values("fecha", ascending=False).head(20))
else:
    st.write("No hay historial aún para esta lotería.")











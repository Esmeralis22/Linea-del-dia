# linea_del_dia_app.py
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import os

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
BASE_URL = "https://www.loteriadominicana.com.do/"

# ---------------- FUNCIONES ----------------
def normalize(s):
    return s.strip().lower()

def fetch_results_page():
    resp = requests.get(BASE_URL, timeout=10)
    resp.raise_for_status()
    return resp.text

def parse_results(html):
    soup = BeautifulSoup(html, "html.parser")
    results = []
    date = datetime.date.today().isoformat()
    for lot in LOTERIAS:
        header = soup.find(lambda tag: tag.name in ["h2","h3","h4","strong","b"] and normalize(lot) in normalize(tag.get_text()))
        if header:
            text = header.find_next(string=True)
            while text:
                s = text.strip()
                if s.isdigit() and len(s) <= 2:
                    results.append({"fecha": date, "loteria": lot, "numero_1ro": s.zfill(2)})
                    break
                text = text.find_next(string=True)
    return results

def save_historial(df):
    for lot in LOTERIAS:
        df_lot = df[df["loteria"]==lot]
        if df_lot.empty:
            continue
        file_path = os.path.join(HISTORIAL_DIR, f"{lot.replace(' ','_')}.csv")
        if os.path.exists(file_path):
            df_exist = pd.read_csv(file_path)
            df_lot = pd.concat([df_exist, df_lot]).drop_duplicates(subset=["fecha","numero_1ro"])
        df_lot.to_csv(file_path, index=False)

def load_historial(loteria):
    file_path = os.path.join(HISTORIAL_DIR, f"{loteria.replace(' ','_')}.csv")
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=["fecha","loteria","numero_1ro"])

def generar_linea_del_dia(numero_base):
    """Genera el AB -> ABA automáticamente"""
    a, b = numero_base[0], numero_base[1]
    return f"{a}{b}{a}"

# ---------------- STREAMLIT ----------------
st.title("Línea del Día - Loterías Dominicanas y Americanas")

# Selección de lotería
loteria_sel = st.selectbox("Selecciona la lotería:", LOTERIAS)

# Botón de actualizar resultados
if st.button("Actualizar resultados"):
    st.info("Actualizando resultados desde la página...")
    try:
        html = fetch_results_page()
        res = parse_results(html)
        df = pd.DataFrame(res)
        save_historial(df)
        st.success("Resultados actualizados y guardados en historial.")
    except Exception as e:
        st.error(f"Error al actualizar: {e}")

# Mostrar historial
if st.button("Mostrar historial"):
    df_hist = load_historial(loteria_sel)
    if df_hist.empty:
        st.warning("No hay historial para esta lotería.")
    else:
        st.dataframe(df_hist)

# Generar Línea del Día
st.subheader("Generar Línea del Día")
numero_input = st.text_input("Número base (dos dígitos) para la línea del día:", max_chars=2)

if st.button("Generar línea"):
    if len(numero_input)==2 and numero_input.isdigit():
        linea = generar_linea_del_dia(numero_input)
        st.markdown(f"<span style='font-size:40px; color:blue;'>{linea}</span>", unsafe_allow_html=True)
    else:
        st.error("Introduce un número válido de dos dígitos.")












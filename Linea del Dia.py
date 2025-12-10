# linea_del_dia_historial.py
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
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

# ---------------- UTILIDADES ----------------
def normalize(s):
    return s.strip().lower()

def fetch_results_page(fecha=None):
    """Devuelve HTML de la página de resultados. Si fecha=None toma hoy."""
    if fecha:
        url = f"{BASE_URL}resultados?fecha={fecha}"
    else:
        url = BASE_URL
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.text

def parse_results(html):
    """Extrae resultados de la página y devuelve lista de dicts."""
    soup = BeautifulSoup(html, "html.parser")
    results = []
    today = date.today().isoformat()
    for lot in LOTERIAS:
        header = soup.find(lambda tag: tag.name in ["h2","h3","h4","strong","b"] and normalize(lot) in normalize(tag.get_text()))
        if header:
            text = header.find_next(string=True)
            while text:
                s = text.strip()
                if s.isdigit() and len(s) <= 2:
                    results.append({"fecha": today, "loteria": lot, "numero_1ro": s.zfill(2)})
                    break
                text = text.find_next(string=True)
    return results

def save_historial(df):
    """Guarda historial por lotería evitando duplicados."""
    for col in ["fecha", "loteria", "numero_1ro"]:
        if col not in df.columns:
            df[col] = []

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

def obtener_historico_90dias():
    """Extrae resultados últimos 90 días (simulación)."""
    historico = []
    for dias_atras in range(0, 90):
        f = (date.today() - timedelta(days=dias_atras)).isoformat()
        try:
            html = fetch_results_page(fecha=f)
            resultados_dia = parse_results(html)
            historico.extend(resultados_dia)
        except Exception as e:
            print(f"No se pudo obtener {f}: {e}")
    df = pd.DataFrame(historico)
    for col in ["fecha","loteria","numero_1ro"]:
        if col not in df.columns:
            df[col] = []
    return df

def calcular_vibracion(fecha):
    """Calcula vibración del día a partir de la fecha, valor 00-99."""
    s = fecha.day + fecha.month + fecha.year
    return f"{s%100:02d}"

def generar_linea_del_dia(numero_base, df_hist, loteria):
    """Genera AB -> ABA tomando en cuenta historial reciente."""
    base_num = int(numero_base)
    # Revisa si ya salió hoy
    hoy = date.today().isoformat()
    df_lot = df_hist[df_hist["loteria"]==loteria]
    numeros_hoy = df_lot[df_lot["fecha"]==hoy]["numero_1ro"].astype(int).tolist()
    intento = base_num
    intentos = 0
    while intento in numeros_hoy and intentos<10:
        intento = (intento + 1) % 100
        intentos +=1
    num_str = f"{intento:02d}"
    # Formato ABA
    a, b = num_str[0], num_str[1]
    return f"{a}{b}{a}", intento in numeros_hoy

# ---------------- STREAMLIT ----------------
st.title("Línea del Día Inteligente - Loterías Dominicanas y Americanas")

# Selector de lotería
loteria_sel = st.selectbox("Selecciona la lotería:", LOTERIAS)

# Inicializar historial 90 días
if st.button("Inicializar historial 90 días"):
    with st.spinner("Obteniendo resultados últimos 90 días..."):
        df_hist = obtener_historico_90dias()
        save_historial(df_hist)
    st.success("Historial de 90 días actualizado.")

# Actualizar resultados del día
if st.button("Actualizar resultados hoy"):
    with st.spinner("Obteniendo resultados de hoy..."):
        try:
            html = fetch_results_page()
            res = parse_results(html)
            df = pd.DataFrame(res)
            for col in ["fecha","loteria","numero_1ro"]:
                if col not in df.columns:
                    df[col] = []
            save_historial(df)
            st.success("Resultados de hoy agregados al historial.")
        except Exception as e:
            st.error(f"Error al actualizar: {e}")

# Mostrar historial
if st.button("Mostrar historial"):
    df_hist = load_historial(loteria_sel)
    if df_hist.empty:
        st.warning("No hay historial para esta lotería.")
    else:
        st.dataframe(df_hist)

# Línea del Día inteligente
st.subheader("Línea del Día Automática")
df_hist = load_historial(loteria_sel)
hoy = date.today()
numero_base = calcular_vibracion(hoy)
linea, ya_salio = generar_linea_del_dia(numero_base, df_hist, loteria_sel)

if ya_salio:
    st.warning(f"Número base {numero_base} ya salió hoy, ajustado a {linea[:2]}")
st.markdown(f"<span style='font-size:60px; color:green;'>{linea}</span>", unsafe_allow_html=True)
st.caption(f"Número base del día según vibración: {numero_base}")













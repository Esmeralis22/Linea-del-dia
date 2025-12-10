# linea_del_dia.py
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timedelta

# ---------- Configuración ----------
LOTTERIES = [
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

HIST_DIR = "historial_loterias"
if not os.path.exists(HIST_DIR):
    os.makedirs(HIST_DIR)

# ---------- Funciones ----------
def scrap_ultimo_numero(loteria):
    """
    Scrap del último resultado publicado de la lotería desde la web pública.
    """
    # URL de la página con resultados (ejemplo: Lotería Dominicana)
    URL = "https://www.loteriadominicana.com.do/"  # modificar según estructura real
    try:
        r = requests.get(URL, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        # Buscar la sección que corresponda a la lotería
        # Ajusta este selector según la estructura real de la página
        # Ejemplo: <div class="loteria" data-name="Loteria Nacional- Gana Más">66</div>
        lot_div = soup.find("div", {"data-name": loteria})
        if lot_div:
            numero = lot_div.text.strip()
            if numero.isdigit() and len(numero) == 2:
                return numero
    except Exception as e:
        st.warning(f"No se pudo obtener el número de {loteria}: {e}")
    return None

def load_historial(loteria):
    archivo = os.path.join(HIST_DIR, f"{loteria}.csv")
    if os.path.exists(archivo):
        df = pd.read_csv(archivo)
        df["fecha"] = pd.to_datetime(df["fecha"])
        return df
    else:
        return pd.DataFrame(columns=["fecha","numero"])

def save_historial(loteria, numero):
    df = load_historial(loteria)
    hoy = datetime.now().date()
    df = pd.concat([df, pd.DataFrame([{"fecha": hoy, "numero": numero}])], ignore_index=True)
    archivo = os.path.join(HIST_DIR, f"{loteria}.csv")
    df.to_csv(archivo, index=False)

def generar_linea_del_dia(numero_anterior):
    """
    Genera la Línea del Día según el número anterior.
    AB -> ABA
    AA -> AA
    """
    if not numero_anterior or len(numero_anterior) != 2 or not numero_anterior.isdigit():
        return "??"
    a, b = numero_anterior[0], numero_anterior[1]
    if a == b:
        return a + a
    else:
        return a + b + a

# ---------- Interfaz Streamlit ----------
st.set_page_config(page_title="Línea del Día", layout="wide")
st.title("Línea del Día - Vibración y Ritmo Algorítmico")

loteria_seleccionada = st.selectbox("Selecciona la Lotería", LOTTERIES)

# Botón para actualizar y calcular línea
if st.button("Generar Línea del Día"):
    numero_anterior = scrap_ultimo_numero(loteria_seleccionada)
    if numero_anterior:
        linea = generar_linea_del_dia(numero_anterior)
        save_historial(loteria_seleccionada, numero_anterior)
        st.markdown(f"<span style='font-size:40px;color:blue'>{linea}</span>", unsafe_allow_html=True)
        st.info(f"Número anterior: {numero_anterior}")
    else:
        st.error(f"No se pudo obtener el último número de {loteria_seleccionada}")

# Mostrar historial
if st.checkbox("Mostrar Historial"):
    df_hist = load_historial(loteria_seleccionada)
    if df_hist.empty:
        st.write("No hay historial para esta lotería.")
    else:
        st.dataframe(df_hist.sort_values(by="fecha", ascending=False))













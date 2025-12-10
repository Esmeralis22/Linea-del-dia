import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import datetime

st.set_page_config(layout="centered")
st.title("📥 Resultados automáticos desde LoteriaDominicana.com.do")

HIST_DIR = "historial_scraping"
os.makedirs(HIST_DIR, exist_ok=True)

LOTERIAS = [
    "Lotería Nacional", "La Suerte", "Loteka", "Leidsa", "Lotería Real",
    "La Primera", "Gana Más",  # etc según los nombres en la web
]

def descargar_resultados():
    url = "https://www.loteriadominicana.com.do/"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.text

def parsear_resultados(html):
    soup = BeautifulSoup(html, "html.parser")
    resultados = {}
    # Ejemplo genérico: buscar etiquetas que indiquen loteria + número ganador
    # Este bloque debes adaptar según la estructura real del HTML
    for lot in LOTERIAS:
        tag = soup.find("div", text=lambda t: t and lot in t)
        if tag:
            # Supongamos que junto está el número ganador en un <span>
            num = tag.find_next("span").get_text(strip=True)
            resultados[lot] = num
    hoy = datetime.date.today().isoformat()
    return hoy, resultados

def actualizar_historial():
    html = descargar_resultados()
    fecha, res = parsear_resultados(html)
    for lot, num in res.items():
        archivo = os.path.join(HIST_DIR, f"{lot.replace(' ','_')}.csv")
        df = pd.read_csv(archivo) if os.path.exists(archivo) else pd.DataFrame(columns=["fecha","numero"])
        if not ((df["fecha"]==fecha) & (df["numero"]==num)).any():
            df = pd.concat([df, pd.DataFrame([{"fecha":fecha,"numero":num}])], ignore_index=True)
            df.to_csv(archivo, index=False)
    return res

if st.button("Actualizar resultados"):
    try:
        res = actualizar_historial()
        st.success("Historial actualizado.")
        st.write(res)
    except Exception as e:
        st.error("Error al actualizar: " + str(e))

st.header("Historial por lotería")
loteria_sel = st.selectbox("Elige lotería", LOTERIAS)
archivo = os.path.join(HIST_DIR, f"{loteria_sel.replace(' ','_')}.csv")
if os.path.exists(archivo):
    df = pd.read_csv(archivo)
    st.dataframe(df)
else:
    st.write("No hay historial aún para esa lotería.")









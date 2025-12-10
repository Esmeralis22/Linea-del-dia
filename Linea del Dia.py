# app_linea_conectate.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
import unicodedata

st.set_page_config(page_title="Línea del Día - Conectate", layout="centered")

LOTERIAS = [
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
    "La Suerte 6PM",
    "Anguila 10:00 AM",
    "Anguila 1:00 PM",
    "Anguila 6:00 PM",
    "Anguila 9:00 PM",
]

BASE_URL = "https://www.conectate.com.do/loterias/pagina/ultimos-resultados"

def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII','ignore').decode().lower().strip()

def get_last_draw_number(loteria_name):
    """
    Intenta extraer el último número de 2 dígitos para la lotería indicada.
    Retorna 'NN' string o None si no encuentra.
    """
    resp = requests.get(BASE_URL, timeout=10)
    if resp.status_code != 200:
        return None
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Buscar una línea donde aparezca el nombre de la lotería
    lot_norm = normalize(loteria_name)
    # cada resultado suele estar en un row; buscar cualquier texto que contenga la lotería
    for tag in soup.find_all(text=True):
        txt = normalize(tag)
        if lot_norm in txt:
            # después del nombre usualmente vienen los números
            parent = tag.parent
            # buscar en sus hermanos o descendientes algo que parezca dos dígitos
            for sib in parent.find_all(text=True):
                s = sib.strip()
                if s.isdigit() and len(s)==2:
                    return s
    return None

def generar_linea(numero_anterior):
    """Si numero_anterior es 'AB' → devuelve ABA; si AA → AA."""
    if not numero_anterior or len(numero_anterior)!=2:
        return None
    a, b = numero_anterior[0], numero_anterior[1]
    if a == b:
        return a + b
    else:
        return a + b + a

st.title("Línea del Día - Según Conectate")

loteria = st.selectbox("Selecciona la lotería", LOTERIAS)

if st.button("Generar línea del día"):
    num = get_last_draw_number(loteria)
    if num is None:
        st.error("No se encontró resultado reciente para esa lotería.")
    else:
        linea = generar_linea(num)
        st.markdown(f"**Lotería:** {loteria}")
        st.markdown(f"**Último resultado:** {num}")
        st.markdown(f"**Línea del Día sugerida:** <span style='font-size:48px;color:green'>{linea}</span>", unsafe_allow_html=True)













import streamlit as st
import random
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Línea del Día Exacta", layout="wide")
st.title("Línea del Día Exacta de Loterías (Ritmo Algorítmico)")

# Lista de loterías
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

# Función determinista para generar número tipo span según fecha y lotería
def generar_linea_dia(loteria, fecha):
    # Crear semilla única a partir de la fecha y el nombre de la lotería
    semilla = sum([ord(c) for c in loteria]) + int(fecha.replace('-', ''))
    random.seed(semilla)
    
    # Patrones por tipo de lotería
    if "Quiniela" in loteria or "New York" in loteria or "Gana Más" in loteria or "Florida" in loteria:
        decena = random.choice([0,2,4,6,8])
        unidad = random.choice([1,3,5,7,9])
    elif "Lotería Nacional" in loteria:
        decena = random.randint(0,9)
        unidad = random.randint(0,9)
    elif "La Suerte" in loteria or "Primera" in loteria:
        decena = random.randint(0,9)
        unidad = random.randint(0,9)
    else:
        decena = random.randint(0,9)
        unidad = random.randint(0,9)
    
    # Representación tipo span
    if decena == unidad:
        return f"{decena}{unidad}"  # AA
    else:
        return f"{decena}{unidad}{decena}"  # ABA

# Selección de la lotería
loteria_seleccionada = st.selectbox("Selecciona la lotería", loterias)

# Fecha de hoy
fecha_hoy = datetime.now().strftime("%Y-%m-%d")

# Generar línea del día exacta
linea_dia = generar_linea_dia(loteria_seleccionada, fecha_hoy)

# Mostrar resultado
st.subheader(f"Línea del Día para {loteria_seleccionada} ({fecha_hoy})")
st.markdown(f"**{linea_dia}**")
















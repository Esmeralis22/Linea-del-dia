import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import datetime
import random
import os

st.set_page_config(page_title="Ritmo Algorítmico de Loterías", layout="centered")
st.title("🎲 Línea del Día - Ritmo Algorítmico")

# ----- Loterías -----
lot_dominicanas = [
    "Primera Día", "Primera Noche", "Gana Más", "Lotería Nacional",
    "La Suerte MD", "La Suerte Noche", "Lotería Real", "Loteka", "Leidsa"
]
lot_americanas = [
    "Anguilla 10:00 AM", "Anguilla 1:00 PM", "Anguilla 6:00 PM", "Anguilla 9:00 PM",
    "Florida Día", "Florida Noche", "New York Tarde", "New York Noche"
]
todas_loterias = lot_dominicanas + lot_americanas

# ----- Selector de lotería -----
loteria = st.selectbox("Selecciona la lotería", todas_loterias)

# ----- Archivo de historial -----
HISTORIAL_DIR = "historial_loterias"
os.makedirs(HISTORIAL_DIR, exist_ok=True)
archivo_hist = os.path.join(HISTORIAL_DIR, f"{loteria.replace(' ', '_')}_historial.csv")

# ----- Cargar historial -----
if os.path.exists(archivo_hist):
    df_hist = pd.read_csv(archivo_hist)
else:
    df_hist = pd.DataFrame(columns=["fecha", "numero_base", "numero_jugar"])

# ----- Función número del día según ritmo algorítmico -----
def numero_base_dia(lot):
    today = datetime.datetime.now()
    seed = today.strftime("%Y-%m-%d") + lot
    random.seed(seed)
    return random.randint(0, 99)

def numero_a_jugar(n):
    str_n = str(n).zfill(2)
    if str_n[0] == str_n[1]:
        return str_n  # AA exacto
    else:
        return str_n[0] + str_n[1] + str_n[0]  # ABA

# ----- Estado del número -----
def estado_numero(n, df_hist):
    str_n = str(n).zfill(2)
    # Filtrar por mes actual
    hoy = datetime.datetime.now()
    mes_actual = hoy.month
    año_actual = hoy.year
    df_hist["fecha"] = pd.to_datetime(df_hist["fecha"])
    df_mes = df_hist[(df_hist["fecha"].dt.month == mes_actual) &
                     (df_hist["fecha"].dt.year == año_actual)]
    salidas = (df_mes["numero_base"] == str_n).sum()
    if salidas == 0:
        return f"Número Frío — Salidas este mes: {salidas}"
    elif salidas == 1:
        return f"Número en Ascenso — Salidas este mes: {salidas}"
    elif salidas == 2:
        return f"Número Caliente — Salidas este mes: {salidas}"
    else:
        return f"Número Quemado — Salidas este mes: {salidas}"

# ----- Span animado -----
def generar_span(numero):
    html_code = f"""
    <div style="text-align:center; margin-top:30px;">
        <span style="
            font-size:6rem;
            font-weight:bold;
            color:white;
            padding:20px 40px;
            border-radius:20px;
            background: linear-gradient(135deg, #ff416c, #ff4b2b);
            display:inline-block;
            animation: bounce 0.6s ease-out;
        ">{numero}</span>
    </div>
    <style>
    @keyframes bounce {{
        0% {{ transform: translateY(-50px); opacity:0; }}
        50% {{ transform: translateY(10px); opacity:1; }}
        100% {{ transform: translateY(0); opacity:1; }}
    }}
    </style>
    """
    return html_code

# ----- Botón generar número -----
if st.button("Generar Número del Día"):
    num_base = numero_base_dia(loteria)
    num_jugar = numero_a_jugar(num_base)
    
    # Guardar en historial
    hoy_str = datetime.datetime.now().strftime("%Y-%m-%d")
    df_hist = pd.concat([df_hist, pd.DataFrame([{
        "fecha": hoy_str,
        "numero_base": str(num_base).zfill(2),
        "numero_jugar": num_jugar
    }])], ignore_index=True)
    df_hist.to_csv(archivo_hist, index=False)
    
    # Mostrar número en span
    st.subheader(f"🎯 Número para {loteria}")
    components.html(generar_span(num_jugar), height=200)
    
    # Estado
    estado = estado_numero(num_base, df_hist)
    st.write(f"**Número base:** {num_base} → **Número a jugar:** {num_jugar}")
    st.info(estado)

# ----- Mostrar historial -----
if st.button("Mostrar Historial"):
    if df_hist.empty:
        st.warning("No hay historial registrado aún para esta lotería.")
    else:
        st.subheader(f"📜 Historial de {loteria}")
        st.dataframe(df_hist.sort_values("fecha", ascending=False))










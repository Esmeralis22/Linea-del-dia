import streamlit as st
import streamlit.components.v1 as components
import datetime
import random

st.set_page_config(page_title="Número Vibración del Día", layout="centered")
st.title("🎲 Número Vibración del Día por Lotería")

st.write("Selecciona la lotería y genera tu número según la vibración del día.")

# Listas de loterías
lot_americanas = [
    "Anguilla 10:00 AM", "Anguilla 1:00 PM", "Anguilla 6:00 PM", "Anguilla 9:00 PM",
    "Florida Día", "Florida Noche", "New York Tarde", "New York Noche"
]
lot_dominicanas = ["Primera Día", "Primera Noche", "Lotería Nacional", "La Suerte MD", "Gana Mas", "Loteria Real", "La Suerte Noche", "Loteka", "Leidsa"]
todas_loterias = lot_dominicanas + lot_americanas

# Selector de lotería
loteria = st.selectbox("Selecciona la lotería", todas_loterias)

# Función vibración del día
def vibracion_del_dia(lot):
    today = datetime.datetime.now()
    # semilla basada en fecha + lotería → mismo número por día y lotería
    random.seed(today.strftime("%Y-%m-%d") + lot)
    return random.randint(0, 99)

# Función número a jugar con regla final:
# AB -> ABA, AA -> AA
def numero_a_jugar(n):
    str_n = str(n).zfill(2)
    if str_n[0] == str_n[1]:
        return str_n  # AA
    else:
        return str_n[0] + str_n[1] + str_n[0]  # ABA

# HTML span animado
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

# Botón para generar número
if st.button("Generar Número del Día"):
    num_base = vibracion_del_dia(loteria)
    numero_final = numero_a_jugar(num_base)
    
    st.subheader(f"🎯 Número para {loteria}")
    components.html(generar_span(numero_final), height=200)
    st.write(f"**Número base:** {num_base} → **Número a jugar:** {numero_final}")








import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="ODS Master", layout="centered")

# --- BASE DE DATOS COMPLETA ---
ODS_DATA = [
    {"id": 1, "titulo": "Fin de la Pobreza", "bien": "Pobreza Extrema", "mal": "Ruido Urbano"},
    {"id": 2, "titulo": "Hambre Cero", "bien": "Desnutrición", "mal": "Mala conexión WiFi"},
    {"id": 6, "titulo": "Agua Limpia", "bien": "Falta de Grifos", "mal": "Mucho Tráfico"},
    {"id": 7, "titulo": "Energía Asequible", "bien": "Uso de Carbón", "mal": "Poca Lectura"},
    {"id": 13, "titulo": "Acción por el Clima", "bien": "Glaciares derretidos", "mal": "Precios altos"},
    {"id": 14, "titulo": "Vida Submarina", "bien": "Plásticos en mar", "mal": "Luz azul"},
    {"id": 15, "titulo": "Vida de Ecosistemas", "bien": "Deforestación", "mal": "Batería baja"},
]

# --- ESTADO ---
if 'nivel' not in st.session_state:
    st.session_state.nivel = 1
if 'jugando' not in st.session_state:
    st.session_state.jugando = False
if 'victoria' not in st.session_state:
    st.session_state.victoria = False

def avanzar():
    if st.session_state.nivel >= len(ODS_DATA):
        st.session_state.victoria = True
        st.session_state.jugando = False
    else:
        st.session_state.nivel += 1
        st.session_state.jugando = False

def reset():
    st.session_state.nivel = 1
    st.session_state.jugando = False
    st.session_state.victoria = False

# --- PANTALLA DE GANADOR FINAL ---
if st.session_state.victoria:
    st.balloons()
    st.title("🏆 ¡GANASTE!")
    st.success("Has superado todos los niveles y conoces los desafíos de los ODS.")
    if st.button("Jugar de nuevo", on_click=reset):
        st.rerun()
    st.stop()

st.title("🎈 ODS Balloon Challenge")

# --- PANTALLA DE INICIO O JUEGO ---
if not st.session_state.jugando:
    st.header(f"Nivel {st.session_state.nivel} de {len(ODS_DATA)}")
    if st.button("¡LANZAR GLOBOS!", type="primary"):
        st.session_state.jugando = True
        st.rerun()
else:
    # 1. Seleccionar ODS actual
    ods = ODS_DATA[st.session_state.nivel - 1]
    
    # 2. Crear lista de opciones de forma segura
    males_disponibles = [o['mal'] for o in ODS_DATA if o['id'] != ods['id']]
    random.shuffle(males_disponibles)
    
    # num_globos es nivel+1, pero nunca más que los males disponibles + 1
    max_posible = len(males_disponibles) + 1
    num_globos = min(st.session_state.nivel + 1, max_posible) 
    
    opciones = [{"text": ods['bien'], "tipo": "GANAR"}]
    for i in range(num_globos - 1):
        opciones.append({"text": males_disponibles[i], "tipo": "PERDER"})
    
    random.shuffle(opciones)

    st.subheader(f"Encuentra el problema de: {ods['titulo']}")

    # 3. Generar HTML
    globos_html = ""
    colores = ["#FF4B4B", "#1C83E1", "#FFD700", "#28A745", "#6F42C1", "#FD7E14"]
    
    for i, opt in enumerate(opciones):
        left_pos = (i * (85 / num_globos)) + 7
        color = colores[i % len(colores)]
        globos_html += f'<div id="ball_{i}" class="balloon" style="left:{left_pos}%; background:{color}; bottom:-150px;" onclick="clickBalloon({i})">{opt["text"]}</div>'

    velocidad = 1.0 + (st.session_state.nivel * 0.4)

    game_code = f"""
    <div id="canvas" style="width:100%; height:450px; background:#f8f9fa; position:relative; overflow:hidden; border:2px solid #ddd; border-radius:15px;">
        {globos_html}
    </div>
    <style>
        .balloon {{
            position: absolute; width: 85px; height: 110px; color: white; border-radius: 50% 50% 50% 50% / 40% 40% 60% 60%;
            display: flex; align-items: center; justify-content: center; text-align: center; font-family: sans-serif; 
            font-size: 11px; font-weight: bold; cursor: pointer; padding: 10px; box-shadow: inset -5px -10px 15px rgba(0,0,0,0.2);
        }}
    </style>
    <script>
        const total = {num_globos};
        const opciones = {opciones};
        let positions = Array(total).fill(-150);
        let active = true;

        function step() {{
            if(!active) return;
            let lost = false;
            for(let i=0; i<total; i++) {{
                positions[i] += {velocidad};
                const el = document.getElementById('ball_' + i);
                if(el) {{
                    el.style.bottom = positions[i] + 'px';
                    if(positions[i] > 450) lost = true;
                }}
            }}
            if(lost) {{
                active = false;
                alert("¡Se escaparon!");
                window.parent.document.querySelector('button[kind="secondary"]').click();
            }} else {{ requestAnimationFrame(step); }}
        }}

        window.clickBalloon = (i) => {{
            if(!active) return;
            active = false;
            if(opciones[i].tipo === "GANAR") {{
                alert("¡Correcto!");
                window.parent.document.querySelector('button[kind="primary"]').click();
            }} else {{
                alert("¡Incorrecto!");
                window.parent.document.querySelector('button[kind="secondary"]').click();
            }}
        }}
        setTimeout(step, 300);
    </script>
    """

    components.html(game_code, height=470)

    # Botones de control
    col1, col2 = st.columns(2)
    with col1:
        st.button("Continuar", on_click=avanzar, type="primary", use_container_width=True)
    with col2:
        st.button("Reiniciar", on_click=reset, type="secondary", use_container_width=True)

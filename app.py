import streamlit as st
import math
import pandas as pd
import altair as alt

st.markdown("""
<style>

/* ====== FONDO GENERAL ====== */
.stApp {
    background-color: #121212;
}

/* ====== LABELS (subtítulos pequeños) ====== */
label {
    color: #FFD600 !important;
    font-weight: bold;
}

/* ====== INPUTS (cajas donde escribes) ====== */
div[data-baseweb="input"] > div {
    background-color: #102a1c !important;
    border-radius: 10px;
    border: 1px solid #00c853;
}

/* Texto dentro del input */
input {
    color: #ffffff !important;
}

/* Efecto al hacer clic */
div[data-baseweb="input"]:focus-within {
    border: 10px solid #FFD600 !important;
    box-shadow: 0 0 8px #FFD600;
}

/* ====== MÉTRICAS ====== */
[data-testid="stMetricValue"] {
    color: #00c853;
    font-weight: bold;
    font-size: 28px;
}

[data-testid="stMetricLabel"] {
    color: #FFD600;
}

/* Títulos */
h1, h2, h3 {
    color: #f1f1f1;
}

/* Texto */
p, label {
    color: #d1d1d1;
}

/* Inputs */
.stNumberInput, .stSelectbox {
    background-color: #1c1f26;
    border-radius: 10px;
}

/* Botones */
.stButton>button {
    background-color: #00c853;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
}

/* Tarjetas tipo dashboard */
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.5);
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align: center; color: #00c853;'>
☀️ Calculadora Solar Fotovoltaica
</h1>
<p style='text-align: center; color: white;'>
Dimensionamiento, inversión y retorno en un solo lugar
</p>
""", unsafe_allow_html=True)

# 🔹 Catálogo de paneles
paneles_disponibles = {
    "Jinko": [535, 540, 545, 550, 555, 560, 565, 570, 580, 585, 590, 595, 600, 605, 610, 615, 620, 625, 630, 635, 640, 645, 650, 720],
    
    "Longi": [440, 445, 450, 470, 475, 540, 545, 550, 555, 560, 565, 570, 580, 585, 590, 595, 600, 605, 610, 625, 630, 635, 640, 645, 650, 655, 660],
    
    "Trina": [480, 485, 490, 495, 500, 505, 535, 540, 545, 550, 555, 590, 595, 600, 605, 610, 645, 650, 655, 660],
    
    "Canadian": [530, 535, 540, 545, 550, 555, 560, 590, 595, 600, 605, 610, 615, 620, 625, 630, 635, 640, 645, 650, 655, 660, 665, 670]
}


inversores = {
    "HUAWEI SUN2000-2KTL-L1": 2,
    "HUAWEI SUN2000-3KTL-L1": 3,
    "HUAWEI SUN2000-4KTL-L1": 4,
    "HUAWEI SUN2000-5KTL-L1": 5,
    "HUAWEI SUN2000-6KTL-L1": 6,
    "HUAWEI SUN2000-8K-LC0": 8,
    "HUAWEI SUN2000-10K-LC0": 10,
    "HUAWEI SUN2000-20KTL-M3": 20,
    "HUAWEI SUN2000-30KTL-M3": 30,
    "HUAWEI SUN2000-36KTL-M3": 36,
    "HUAWEI SUN2000-40KTL-M3": 40,
    "HUAWEI SUN2000-50KTL-M3": 50,
    "HUAWEI SUN2000-50KTL-MG0-220V": 50,
    "HUAWEI SUN2000-80KTL-MG0-220V": 80,
    "HUAWEI SUN2000-100KTL-M2": 100,
    "HUAWEI SUN2000-150KTL-MG0": 150,
    "HUAWEI SUN2000-215KTL-H0": 215,
    "HUAWEI SUN2000-330KTL-H1": 330
}
st.set_page_config(page_title="Calculadora Solar", layout="centered")

tab1, tab2, tab3 = st.tabs(["🔆 DIMENSIONAMIENTO", "💰 CAPEX", "📈 ROI"])

with tab1:

    st.title("🔆 Calculadora de Sistemas Fotovoltaicos")

    # ===============================
    # PARÁMETROS DEL SISTEMA
    # ===============================
    st.sidebar.header("⚙️ Parámetros del sistema")

    HSP = st.sidebar.number_input("Horas Sol Pico (HSP)",min_value=0.0,value=3.5)
    eficiencia = st.sidebar.number_input(
        "Eficiencia del sistema (%)",
        min_value=0.0,
        max_value=100.0,
        value=80.0
    ) / 100

    # 🔹 AQUÍ VA EL SELECTOR
    marca = st.sidebar.selectbox(
        "Seleccione la marca",
        list(paneles_disponibles.keys())
    )


    potencia_w = st.sidebar.selectbox(
        "Seleccione la potencia del panel (W)",
        paneles_disponibles[marca]
    )

    potencia_panel = potencia_w / 1000
    # ===============================
    # SELECCIÓN DE MÉTODO
    # ===============================
    modo = st.radio(
        "Seleccione el método de cálculo:",
        ("Por consumo del recibo", "Por cargas eléctricas")
    )

    # ===============================
    # OPCIÓN 1: CONSUMO
    # ===============================
    if modo == "Por consumo del recibo":

        st.header("📊 Cálculo por consumo mensual")

        consumo_mensual = st.number_input(
            "Consumo mensual (kWh)",
            min_value=0.0
        )

        if consumo_mensual > 0:

            consumo_diario = consumo_mensual / 30
            potencia_requerida = consumo_diario / (HSP * eficiencia)

            paneles = math.ceil(potencia_requerida / potencia_panel)

            potencia_dc = paneles * potencia_panel
            potencia_min_inversor = potencia_dc / 1.3

            st.session_state.paneles = paneles
            st.session_state.potencia_dc = potencia_dc
            

            inversor_seleccionado = None
            for modelo, potencia in sorted(inversores.items(), key=lambda x: x[1]):
                if potencia >= potencia_min_inversor:
                    inversor_seleccionado = (modelo, potencia)
                    break
            st.session_state.inversor = inversor_seleccionado
            
            st.subheader("Resultados")
            st.write(f"Consumo diario: {consumo_diario:.2f} kWh/día")
            st.write(f"Potencia requerida: {potencia_requerida:.2f} kW")
            st.write(f"Número de paneles: {paneles}")

            # 🔌 INVERSOR
            if inversor_seleccionado:
                modelo, potencia_inv = inversor_seleccionado

                st.subheader("🔌 Inversor recomendado")
                st.write(f"Modelo: {modelo}")
                st.write(f"Potencia del inversor: {potencia_inv} kW")
                st.write(f"Potencia del sistema: {potencia_dc:.2f} kW")

                st.write(
                    "Selección basada en una sobrecarga máxima del 30% "
                    "(relación DC/AC ≤ 1.3)."
                )

                st.markdown("### 💡 Recomendación para el cliente")
                st.write(
                    f"Se recomienda el inversor **{modelo}**, ya que tiene la capacidad "
                    f"adecuada para manejar la energía generada por su sistema solar, "
                    f"permitiendo un funcionamiento seguro y eficiente sin desperdiciar energía."
                )
    # ===============================
    # OPCIÓN 2: CARGAS
    # ===============================
    elif modo == "Por cargas eléctricas":

        st.header("⚡ Cálculo por cargas")

        num_equipos = st.number_input(
            "Número de equipos",
            min_value=1,
            step=1
        )

        consumo_total = 0

        for i in range(int(num_equipos)):

            st.subheader(f"Equipo {i+1}")

            potencia = st.number_input(
                f"Potencia (W) equipo {i+1}",
                min_value=0.0,
                key=f"pot_{i}"
            )

            horas = st.number_input(
                f"Horas de uso al día equipo {i+1}",
                min_value=0.0,
                key=f"horas_{i}"
            )

            consumo_equipo = (potencia * horas) / 1000
            consumo_total += consumo_equipo

        if consumo_total > 0:

            potencia_requerida = consumo_total / (HSP * eficiencia)

            paneles = math.ceil(potencia_requerida / potencia_panel)

            potencia_dc = paneles * potencia_panel
            potencia_min_inversor = potencia_dc / 1.3


            st.session_state.paneles = paneles
            st.session_state.potencia_dc = potencia_dc
            
            
            inversor_seleccionado = None
            for modelo, potencia in sorted(inversores.items(), key=lambda x: x[1]):
                if potencia >= potencia_min_inversor:
                    inversor_seleccionado = (modelo, potencia)
                    break
            st.session_state.inversor = inversor_seleccionado
            
            st.subheader("Resultados")
            st.write(f"Consumo diario total: {consumo_total:.2f} kWh/día")
            st.write(f"Potencia requerida: {potencia_requerida:.2f} kW")
            st.write(f"Número de paneles: {paneles}")

            # 🔌 INVERSOR
            if inversor_seleccionado:
                modelo, potencia_inv = inversor_seleccionado

                st.subheader("🔌 Inversor recomendado")
                st.write(f"Modelo: {modelo}")
                st.write(f"Potencia del inversor: {potencia_inv} kW")
                st.write(f"Potencia del sistema: {potencia_dc:.2f} kW")

                st.write(
                    "Selección basada en una sobrecarga máxima del 30% "
                    "(relación DC/AC ≤ 1.3)."
                )

                st.markdown("### 💡 Recomendación para el cliente")
                st.write(
                    f"Se recomienda el inversor **{modelo}**, ya que permite "
                    f"aprovechar al máximo la energía generada por los paneles "
                    f"de forma segura y eficiente."
                )

with tab2:

    st.header("💰 Análisis de Inversión (CAPEX)")

    paneles = st.session_state.get("paneles", None)
    potencia_dc = st.session_state.get("potencia_dc", None)

    if paneles is None or potencia_dc is None:
        st.warning("Primero realiza el dimensionamiento en la pestaña anterior.")
    else:

        st.subheader("Parámetros económicos")

        # 🔹 Selección operador de red
        chec = st.selectbox(
            "¿Proyecto con CHEC (Operador de Red)?",
            ["No", "Sí"]
        )

        # 🔹 Precio base
        costo_kw = 3_200_000  # COP/kW

        # 🔹 Ajuste por CHEC
        if chec == "Sí":
            costo_kw *= 1.06

        st.write(f"Valor aplicado: ${costo_kw:,.0f} COP/kW")

        # 🔹 CAPEX total
        capex_total = potencia_dc * costo_kw
        st.session_state.capex = capex_total

        st.subheader("📊 Resumen del sistema")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🔆 Paneles", paneles)

        with col2:
            st.metric("⚡ Potencia", f"{potencia_dc:.2f} kWp")

        with col3:
            st.metric("💰 CAPEX", f"${capex_total:,.0f}")

with tab3:

    st.header("📈 Retorno de Inversión (ROI)")

    potencia_dc = st.session_state.get("potencia_dc", None)
    capex = st.session_state.get("capex", None)
    HSP = st.session_state.get("HSP", 3.5)
    eficiencia = st.session_state.get("eficiencia", 0.8)

    if potencia_dc is None or capex is None:
        st.warning("Primero completa el dimensionamiento y CAPEX.")
    else:

        st.subheader("Parámetros económicos")

        # Crear 3 columnas
        col1, col2, col3 = st.columns(3)

        # Colocar cada input en su columna correspondiente
        with col1:
            precio_kwh = st.number_input("Precio energía ($/kWh)", value=800.0)

        with col2:
            costo_excedente = st.number_input("Precio excedentes ($/kWh)", value=300.0)

        with col3:
            porcentaje_autoconsumo = st.number_input("Autoconsumo (%)", min_value=0.0, max_value=100.0, value=75.0) / 100

        st.session_state.precio_kwh = precio_kwh
        st.session_state.precio_excedente = costo_excedente
        st.session_state.porcentaje_autoconsumo = porcentaje_autoconsumo
        # 🔹 Generación mensual

        generacion_mensual = potencia_dc * HSP * 30 * eficiencia

        energia_autoconsumo = generacion_mensual * porcentaje_autoconsumo
        energia_excedente = generacion_mensual * (1 - porcentaje_autoconsumo)

        ahorro_mensual = (energia_autoconsumo * precio_kwh) + (energia_excedente * costo_excedente)

        ahorro_anual = ahorro_mensual * 12

        payback = capex / ahorro_anual if ahorro_anual > 0 else 0

        st.subheader("📊 Indicadores financieros")

        col1, col2, = st.columns(2)

        with col1:
            st.metric("⚡ Generación mensual", f"{generacion_mensual:.0f} kWh")
            

        with col2:
            st.metric("💰 Ahorro mensual", f"${ahorro_mensual:,.0f}")

        col3, col4 = st.columns(2)

        with col3:
            st.metric("📈 Ahorro anual", f"${ahorro_anual:,.0f}")

        with col4:
            st.metric("⏳ Payback", f"{payback:.1f} años")

        st.markdown("### 💡 Interpretación")

        st.write(
            f"Con estas condiciones, tu inversión se recupera en aproximadamente "
            f"**{payback:.1f} años**, generando ahorros desde el primer mes."
        )
        # Inputs del usuario (ejemplo, reemplazar con st.number_input si quieres que sea dinámico)
        potencia_dc = st.session_state.get("potencia_dc", 50)  # kW del sistema
        capex = st.session_state.get("capex", 38596896)        # inversión inicial
        precio_kwh = st.session_state.get("precio_kwh", 800)  # $/kWh
        precio_excedente = st.session_state.get("precio_excedente", 300)  # $/kWh
        HSP = st.session_state.get("HSP", 3.5)                 # horas sol pico
        eficiencia = st.session_state.get("eficiencia", 0.8)   # eficiencia sistema
        porcentaje_autoconsumo = st.session_state.get("porcentaje_autoconsumo", 0.75)  # 0-1

        n_años = st.number_input("Años", value=25)
        incremento_tarifa = 0.10  # 10% anual
        mantenimiento_base = potencia_dc * 70000
        mantenimiento_incremento_1 = 0.05
        mantenimiento_incremento_rest = 0.02

        # Generación mensual y anual
        generacion_anual = potencia_dc * HSP * 365 * eficiencia

        # Inicializar listas
        flujo = []
        flujo_acumulado = 0
        flujo_recuperacion = -capex

        for año in range(1, n_años + 1):
            # Ajuste de precios con incremento anual
            factor_precio = (1 + incremento_tarifa) ** (año - 1)
            ingresos_netos = generacion_anual * precio_kwh * porcentaje_autoconsumo * factor_precio
            generacion_excedente_valor = generacion_anual * precio_excedente * (1 - porcentaje_autoconsumo) * factor_precio
            
            # Mantenimiento anual
            if año == 1:
                mantenimiento = mantenimiento_base * (1 + mantenimiento_incremento_1)
            else:
                mantenimiento = mantenimiento_base * (1 + mantenimiento_incremento_1) * ((1 + mantenimiento_incremento_rest) ** (año - 2))
            
            # Flujo de caja del año
            flujo_caja = ingresos_netos + generacion_excedente_valor - mantenimiento
            
            # Flujo acumulado para recuperación
            flujo_recuperacion += flujo_caja
            
            flujo.append({
                "AÑO": año,
                "INVERSION": capex if año == 1 else "",
                "INGRESOS NETOS": round(ingresos_netos, 0),
                "GENERACION EXCEDENTE": round(generacion_excedente_valor, 0),
                "MANTENIMIENTO ANUAL": round(mantenimiento, 0),
                "FLUJO DE CAJA": round(flujo_caja, 0),
                "FLUJO ACUMULADO": round(flujo_recuperacion, 0),
                "AÑO RECUPERACION": año if flujo_recuperacion >= 0 and año > 0 and all(f["FLUJO ACUMULADO"] < 0 for f in flujo[:-1]) else ""
            })

        df_flujo = pd.DataFrame(flujo)

        st.subheader("📊 Flujo de caja anual")
        st.dataframe(df_flujo, use_container_width=True)

        # Gráfico de barras del flujo acumulado
        chart = alt.Chart(df_flujo).mark_bar().encode(
            x=alt.X("AÑO:O", title="Año"),
            y=alt.Y("FLUJO ACUMULADO:Q", title="Pesos"),
            color=alt.condition(
                alt.datum.FLUJO_ACUMULADO >= 0,
                alt.value("#00c853"), alt.value("#ff5252")
            ),
            tooltip=["AÑO", "FLUJO DE CAJA", "FLUJO ACUMULADO", "AÑO RECUPERACION"]
        ).properties(
            width=800,
            height=400,
            title="📈 Retorno de inversión acumulado"
        )

        st.altair_chart(chart, use_container_width=True)


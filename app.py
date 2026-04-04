import streamlit as st
import math
import pandas as pd
import altair as alt
import numpy as np
import numpy_financial as npf
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

st.set_page_config(page_title="Calculadora Solar", layout="centered")

st.markdown("""
<style>

/* ====== FONDO PRINCIPAL (AJUSTADO A LA IMAGEN) ====== */
.stApp {
    background: linear-gradient(
        115deg,
        #fffdf8 0%,
        #f1f8f4 25%,
        #d7f0df 50%,
        #a5d6a7 70%,
        #66bb6a 85%,
        #2e7d32 100%
    );
}
/* ====== TABS CONTENEDOR ====== */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 2px solid #1f3d2b;
    margin-bottom: 20px;
}

/* ====== TABS INDIVIDUALES (MODO CLARO) ====== */
.stTabs [data-baseweb="tab"] {
    background-color: rgba(255,255,255,0.6);
    color: #2e7d32;
    border-radius: 10px 10px 0 0;
    padding: 10px 18px;
    font-weight: 500;
    transition: all 0.3s ease;
}

/* ====== HOVER ====== */
.stTabs [data-baseweb="tab"]:hover {
    background-color: rgba(76, 175, 80, 0.15);
    color: #1b5e20;
}

/* ====== TAB ACTIVA ====== */
.stTabs [aria-selected="true"] {
    color: #1b5e20 !important;
    background: #ffffff !important;
    border-bottom: 3px solid #43a047;
    font-weight: 600;
}

/* ====== CONTENIDO DE TABS ====== */
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 10px;
}

/* ====== SIDEBAR BASE ====== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f4f7f5 0%, #eef3f0 100%);
    padding: 20px 10px;
    border-right: 2px solid #e0e0e0;
}

/* ====== CONTENEDOR INTERNO ====== */
section[data-testid="stSidebar"] .block-container {
    padding-top: 10px;
}

/* ====== LOGO ESPACIADO ====== */
section[data-testid="stSidebar"] img {
    display: block;
    margin: 0 auto 20px auto;
}

/* ====== TITULO SIDEBAR ====== */
section[data-testid="stSidebar"] h2 {
    color: #1b5e20;
    text-align: center;
    margin-bottom: 20px;
}

/* ====== LABELS ====== */
section[data-testid="stSidebar"] label {
    color: #6c757d !important;
    font-size: 13px;
    font-weight: 500;
}

/* ====== INPUT BOX (ESTILO TARJETA) ====== */
section[data-testid="stSidebar"] div[data-baseweb="input"] > div {
    background-color: #ffffff !important;
    border-radius: 12px;
    border: 1px solid #dfe6e2;
    padding: 5px;
}

/* TEXTO INPUT */
section[data-testid="stSidebar"] input {
    color: #1c1f26 !important;
}

/* FOCUS INPUT */
section[data-testid="stSidebar"] div[data-baseweb="input"]:focus-within {
    border: 1px solid #00c853 !important;
    box-shadow: 0 0 6px rgba(0,200,83,0.25);
}

/* ====== SELECTBOX ====== */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border-radius: 12px;
    border: 1px solid #dfe6e2;
    color: #1c1f26 !important;
}

/* ====== HOVER SUAVE ====== */
section[data-testid="stSidebar"] div[data-baseweb="select"]:hover,
section[data-testid="stSidebar"] div[data-baseweb="input"]:hover {
    background-color: #e8f5e9 !important;
}

/* ====== BOTONES +/- ====== */
section[data-testid="stSidebar"] button {
    background-color: transparent !important;
    color: #00c853 !important;
    border: none !important;
    font-weight: bold;
}

/* ====== SEPARADORES (opcional visual PRO) ====== */
.sidebar-separator {
    height: 1px;
    background: #dfe6e2;
    margin: 15px 0;
}

/* ====== TARJETAS VISUALES (opcional) ====== */
.sidebar-card {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #dfe6e2;
    margin-bottom: 15px;
}

/* ====== TEXTO GENERAL (SOLO CONTENIDO PRINCIPAL) ====== */
.block-container {
    color: #1b3a2a; /* verde oscuro elegante */
}


/* TITULOS */
.block-container h1 {
    color: #1b5e20 !important;
}

.block-container h2, 
.block-container h3 {
    color: #2e7d32 !important;
}


/* TEXTO NORMAL */
.block-container p,
.block-container label,
.block-container span,
.block-container div {
    color: #2f3e34 !important;
}

/* ====== MEJORA VISUAL: TARJETA SUAVE ====== */
.block-container {
    background: rgba(255, 255, 255, 0.65);
    padding: 2rem;
    border-radius: 18px;
    backdrop-filter: blur(6px);
}

/* ====== DATAFRAME MODO CLARO ====== */
.stDataFrame {
    background-color: #ffffff !important;
    border-radius: 12px;
    border: 1px solid #dfe6e2;
}

/* Texto tabla */
.stDataFrame div {
    color: #1c1f26 !important;
}

/* Header tabla */
.stDataFrame thead {
    background-color: #e8f5e9 !important;
}

.stDataFrame th {
    color: #1b5e20 !important;
    font-weight: 600;
}


.stDataFrame {
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)



st.markdown("""
<h1 style='text-align: center; color: #00c853;'>
☀️ Calculadora Solar Fotovoltaica
</h1>

<p style='text-align: center; color: #6c757d;'>
Dimensionamiento, inversión y retorno en un solo lugar
</p>
""", unsafe_allow_html=True)

st.sidebar.image("logo.png", width=5000)

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

tab1, tab2, tab3, tab4 = st.tabs(["🔆 DIMENSIONAMIENTO", "💰 CAPEX", "📈 ROI", "📄 REPORTE" ])

with tab1:

    st.sidebar.header("⚙️ Parámetros del sistema")

    HSP = st.sidebar.number_input("Horas Sol Pico (HSP)", min_value=0.0, value=3.5)

    eficiencia = st.sidebar.number_input(
        "Eficiencia del sistema (%)",
        min_value=0.0,
        max_value=100.0,
        value=80.0
    ) / 100

    st.session_state.HSP = HSP
    st.session_state.eficiencia = eficiencia
    
    # 🔹 AQUÍ VA EL SELECTOR
    marca = st.sidebar.selectbox(
        "Seleccione la marca",
        list(paneles_disponibles.keys())
    )


    potencia_w = st.sidebar.selectbox(
        "Seleccione la potencia del panel (W)",
        paneles_disponibles[marca]
    )

    
    def carrusel_sidebar(imagenes, altura=80, velocidad=3):
        import base64
        import mimetypes


        n = len(imagenes)
        imgs_html = ""

        for img in imagenes:
            try:
                if img.startswith("http"):
                    src = img
                else:
                    with open(img, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode()
                        src = f"data:image/png;base64,{b64}"
            except:
                continue

            imgs_html += f'<img src="{src}">'

        if imgs_html == "":
            st.sidebar.warning("No se pudieron cargar imágenes")
            return

        st.sidebar.markdown(f"""
        <style>
        .carousel {{
            overflow: hidden;
            width: 100%;
            height: {altura}px;
            margin-top: 20px;
        }}

        .carousel-track {{
            display: flex;
            gap: 6px;
            width: max-content;
            animation: scroll {velocidad}s linear infinite;
        }}

        .carousel img {{
            height: {altura}px;
            border-radius: 8px;
        }}

        @keyframes scroll {{
            0% {{ transform: translateX(0); }}
            100% {{ transform: translateX(-50%); }}
        }}

        
        </style>

        <div class="carousel">
            <div class="carousel-track">
                {imgs_html + imgs_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
    imagenes = [
        "images/epm.png",
        "images/cens.png",
        "images/edeq.png",
        "images/chec.png",
        "images/celsia.png",
        "images/SomosEPM.png",
        "images/essa.png",
        "images/erco.jpg"
    ]

    carrusel_sidebar(imagenes)
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
        st.session_state.consumo_mensual = consumo_mensual
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

        chec = st.sidebar.selectbox(
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

    potencia_dc = st.session_state.get("potencia_dc", None)
    capex = st.session_state.get("capex", None)
    HSP = st.session_state.get("HSP", 3.5)
    eficiencia = st.session_state.get("eficiencia", 0.8)

    if potencia_dc is None or capex is None:
        st.warning("Primero completa el dimensionamiento y CAPEX.")
    else:

        # ===============================
        # INPUTS FINANCIEROS
        # ===============================
        precio_kwh = st.sidebar.number_input(
            "Precio energía ($/kWh)", value=800.0
        )

        costo_excedente = st.sidebar.number_input(
            "Precio excedentes ($/kWh)", value=300.0
        )

        porcentaje_autoconsumo = st.sidebar.number_input(
            "Autoconsumo (%)",
            min_value=0.0,
            max_value=100.0,
            value=75.0
        ) / 100

        n_años = st.sidebar.number_input("Años del proyecto", value=15)
        tasa_descuento = st.sidebar.number_input("Tasa de descuento (%)", value=10.0) / 100

        st.session_state.precio_kwh = precio_kwh
        st.session_state.precio_excedente = costo_excedente
        st.session_state.porcentaje_autoconsumo = porcentaje_autoconsumo
        st.session_state.n_años = n_años

        # ===============================
        # CÁLCULOS ENERGÉTICOS BASE
        # ===============================
        generacion_mensual = potencia_dc * HSP * 30 * eficiencia
        generacion_anual = potencia_dc * HSP * 365 * eficiencia

        energia_autoconsumo = generacion_mensual * porcentaje_autoconsumo
        energia_excedente = generacion_mensual * (1 - porcentaje_autoconsumo)

        ahorro_mensual = (energia_autoconsumo * precio_kwh) + (energia_excedente * costo_excedente)
        ahorro_anual = ahorro_mensual * 12

        payback = capex / ahorro_anual if ahorro_anual > 0 else 0

        # ===============================
        # VARIABLES FINANCIERAS COMPLEMENTARIAS
        # ===============================
        consumo_mensual = st.session_state.get("consumo_mensual", None)

        if consumo_mensual is None:
            consumo_mensual = generacion_mensual / porcentaje_autoconsumo if porcentaje_autoconsumo > 0 else generacion_mensual

        pago_actual = consumo_mensual * precio_kwh
        cobertura = (generacion_mensual / consumo_mensual) * 100 if consumo_mensual > 0 else 0

        paneles = st.session_state.get("paneles", 0)
        area_total = paneles * 2.2

        om_anual = potencia_dc * 70000
        ahorro_total = ahorro_anual * n_años

        tarifa_ssfv = (capex + (om_anual * n_años)) / (generacion_anual * n_años) if generacion_anual > 0 else 0

        # Guardar en sesión
        st.session_state.consumo_mensual = consumo_mensual
        st.session_state.area_total = area_total
        st.session_state.om_anual = om_anual
        st.session_state.ahorro_total = ahorro_total
        st.session_state.tarifa_ssfv = tarifa_ssfv
        st.session_state.generacion_anual = generacion_anual
        st.session_state.ahorro_anual = ahorro_anual
        st.session_state.payback = payback

        # ===============================
        # INDICADORES FINANCIEROS BÁSICOS
        # ===============================
        st.subheader("📊 Indicadores financieros")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("⚡ Generación mensual", f"{generacion_mensual:.0f} kWh")

        with col2:
            st.metric("💰 Ahorro mensual", f"${ahorro_mensual:,.0f}")

        col3, col4 = st.columns(2)

        with col3:
            st.metric("📈 Ahorro anual", f"${ahorro_anual:,.0f}")

        with col4:
            st.metric("⏳ Payback", f"{payback:.1f} años")

        # ===============================
        # FLUJO DE CAJA PROYECTADO
        # ===============================
        incremento_tarifa = 0.10  # 10% anual
        mantenimiento_base = potencia_dc * 70000
        mantenimiento_incremento_1 = 0.05
        mantenimiento_incremento_rest = 0.02

        flujo = []
        flujo_recuperacion = -capex

        for año in range(1, n_años + 1):
            factor_precio = (1 + incremento_tarifa) ** (año - 1)

            ingresos_netos = generacion_anual * precio_kwh * porcentaje_autoconsumo * factor_precio
            generacion_excedente_valor = generacion_anual * costo_excedente * (1 - porcentaje_autoconsumo) * factor_precio

            if año == 1:
                mantenimiento = mantenimiento_base * (1 + mantenimiento_incremento_1)
            else:
                mantenimiento = mantenimiento_base * (1 + mantenimiento_incremento_1) * ((1 + mantenimiento_incremento_rest) ** (año - 2))

            flujo_caja = ingresos_netos + generacion_excedente_valor - mantenimiento
            flujo_recuperacion += flujo_caja

            flujo.append({
                "AÑO": año,
                "INVERSION": int(capex) if año == 1 else None,
                "INGRESOS NETOS": int(round(ingresos_netos, 0)),
                "EXCEDENTE": int(round(generacion_excedente_valor, 0)),
                "MANT. ANUAL": int(round(mantenimiento, 0)),
                "FLUJO DE CAJA": int(round(flujo_caja, 0)),
                "FLUJO ACUMULADO": int(round(flujo_recuperacion, 0)),
                "AÑO RECUPERACION": año if flujo_recuperacion >= 0 and año > 0 and all(f["FLUJO ACUMULADO"] < 0 for f in flujo[:-1]) else ""
            })

        df_flujo = pd.DataFrame(flujo)

        # ===============================
        # INDICADORES AVANZADOS
        # ===============================
        flujos = [-capex] + [f["FLUJO DE CAJA"] for f in flujo]

        vpn = npf.npv(tasa_descuento, flujos)
        tir = npf.irr(flujos)
        precio_wp = capex / (potencia_dc * 1000)

        energia_total = sum([
            generacion_anual / ((1 + tasa_descuento) ** i)
            for i in range(1, n_años + 1)
        ])

        costos_total = capex + sum([
            (potencia_dc * 70000) / ((1 + tasa_descuento) ** i)
            for i in range(1, n_años + 1)
        ])

        lcoe = costos_total / energia_total if energia_total > 0 else 0

        st.session_state.vpn = vpn
        st.session_state.tir = tir
        st.session_state.precio_wp = precio_wp
        st.session_state.lcoe = lcoe

        col1, col2 = st.columns(2)

        with col1:
            st.metric("📊 VPN", f"$ {int(vpn):,}".replace(",", "."))

        with col2:
            st.metric("📈 TIR", f"{tir*100:.1f} %")

        col3, col4 = st.columns(2)

        with col3:
            st.metric("💲 $/Wp", f"$ {precio_wp:,.0f}".replace(",", "."))

        with col4:
            st.metric("⚡ LCOE", f"$ {lcoe:,.0f} /kWh".replace(",", "."))

        # ===============================
        # TABLA FINANCIERA EJECUTIVA
        # ===============================
        st.subheader("📋 Análisis financiero ejecutivo")

        tabla_financiera = pd.DataFrame({
            "Concepto": [
                "Consumo actual promedio (kWh/mes)",
                "Tarifa actual promedio ($/kWh)",
                "Pago actual mensual ($)",
                "Inversión inicial ($)",
                "Potencia del sistema (kWp)",
                "Energía generada (kWh/mes)",
                "Cobertura energética (%)",
                "Área requerida (m²)",
                "Ahorro mensual ($)",
                "Operación y mantenimiento anual ($)",
                "Tiempo de retorno (años)",
                f"Ahorro acumulado {n_años} años ($)",
                "TIR (%)",
                "Tarifa equivalente con SSFV ($/kWh)"
            ],
            "Valor": [
                round(consumo_mensual, 0),
                round(precio_kwh, 2),
                round(pago_actual, 0),
                round(capex, 0),
                round(potencia_dc, 2),
                round(generacion_mensual, 0),
                f"{cobertura:.1f}%",
                round(area_total, 0),
                round(ahorro_mensual, 0),
                round(om_anual, 0),
                round(payback, 2),
                round(ahorro_total, 0),
                f"{tir*100:.1f}%",
                round(tarifa_ssfv, 2)
            ]
        })

        st.dataframe(
            tabla_financiera.style
            .set_properties(**{
                'background-color': '#ffffff',
                'color': '#1c1f26',
                'border-color': '#dfe6e2',
                'text-align': 'right'
            })
            .set_table_styles([
                {
                    'selector': 'th',
                    'props': [
                        ('background-color', '#e8f5e9'),
                        ('color', '#1b5e20'),
                        ('font-weight', '600'),
                        ('text-align', 'center')
                    ]
                }
            ]),
            use_container_width=True
        )

        # ===============================
        # INTERPRETACIÓN
        # ===============================
        st.markdown("### 💡 Interpretación avanzada")

        st.write(
            f"""
        - El proyecto genera un **VPN de $ {int(vpn):,}**, indicando valor económico positivo.
        - Presenta una **TIR de {tir*100:.1f}%**, superior a la tasa de descuento.
        - El costo de energía (**LCOE**) es de **$ {lcoe:,.0f}/kWh**.
        - El sistema tiene un costo de **$ {precio_wp:,.0f} por Wp instalado**.
        """.replace(",", ".")
        )

        # ===============================
        # FLUJO DE CAJA
        # ===============================
        st.subheader("📊 Flujo de caja anual")

        st.dataframe(
            df_flujo.style
            .format({
                "INVERSION": lambda x: f"$ {int(x):,}".replace(",", ".") if pd.notnull(x) else "",
                "INGRESOS NETOS": lambda x: f"$ {int(x):,}".replace(",", "."),
                "EXCEDENTE": lambda x: f"$ {int(x):,}".replace(",", "."),
                "MANT. ANUAL": lambda x: f"$ {int(x):,}".replace(",", "."),
                "FLUJO DE CAJA": lambda x: f"$ {int(x):,}".replace(",", "."),
                "FLUJO ACUMULADO": lambda x: f"$ {int(x):,}".replace(",", "."),
            })
            .set_properties(**{
                'background-color': '#ffffff',
                'color': '#1c1f26',
                'border-color': '#dfe6e2',
                'text-align': 'right'
            })
            .set_table_styles([
                {
                    'selector': 'th',
                    'props': [
                        ('background-color', '#e8f5e9'),
                        ('color', '#1b5e20'),
                        ('font-weight', '600'),
                        ('text-align', 'center')
                    ]
                }
            ]),
            use_container_width=True
        )

        # ===============================
        # GRÁFICO ROI ACUMULADO
        # ===============================
        st.subheader("📈 Retorno de inversión acumulado")

        chart = alt.Chart(df_flujo).mark_bar().encode(
            x=alt.X("AÑO:O", title="Año"),
            y=alt.Y("FLUJO ACUMULADO:Q", title="Pesos"),
            color=alt.condition(
                alt.datum.FLUJO_ACUMULADO >= 0,
                alt.value("#2e7d32"),
                alt.value("#a5d6a7")
            ),
            tooltip=["AÑO", "FLUJO DE CAJA", "FLUJO ACUMULADO", "AÑO RECUPERACION"]
        ).properties(
            width=800,
            height=400,
            title=alt.TitleParams(text="", anchor="middle")
        ).configure_view(
            fill="#ffffff"
        ).configure(
            background="#ffffff"
        ).configure_axis(
            labelColor="#2f3e34",
            titleColor="#1b5e20",
            gridColor="#e0e0e0"
        ).configure_title(
            color="#1b5e20"
        )

        st.altair_chart(chart, use_container_width=True)
############################################################################################
with tab4:

    st.header("📄 Datos del cliente para el reporte")

    cliente_nombre = st.text_input("Nombre del cliente")
    cliente_telefono = st.text_input("Teléfono")
    cliente_direccion = st.text_input("Dirección")
    cliente_ciudad = st.text_input("Ciudad")
    cliente_fecha = st.date_input("Fecha")

    st.session_state.cliente_nombre = cliente_nombre
    st.session_state.cliente_telefono = cliente_telefono
    st.session_state.cliente_direccion = cliente_direccion
    st.session_state.cliente_ciudad = cliente_ciudad
    st.session_state.cliente_fecha = cliente_fecha

    st.success("Datos del cliente listos para generar el PDF.")


# =====================================================
# ENCABEZADO Y PIE
# =====================================================
def encabezado_y_pie(canvas, doc):
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.lib.utils import ImageReader
    import os

    canvas.saveState()

    width, height = doc.pagesize

    # TÍTULO IZQUIERDA
    canvas.setFont("Helvetica-Bold", 13)
    canvas.setFillColor(colors.HexColor("#1b5e20"))
    canvas.drawString(2*cm, height - 1.6*cm, "PROPUESTA SOLAR FOTOVOLTAICA")

    # Subtítulo
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#4e5d52"))
    canvas.drawString(2*cm, height - 2.0*cm, "Análisis técnico y financiero")

    # LOGO DERECHA
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        canvas.drawImage(
            logo,
            width - 5*cm,
            height - 2.5*cm,
            width=3.0*cm,
            height=1.4*cm,
            preserveAspectRatio=True,
            mask='auto'
        )

    # LÍNEA DIVISORIA
    canvas.setStrokeColor(colors.HexColor("#2e7d32"))
    canvas.setLineWidth(1.5)
    canvas.line(2*cm, height - 2.8*cm, width - 2*cm, height - 2.8*cm)

    # PIE DE PÁGINA
    canvas.setStrokeColor(colors.HexColor("#a5d6a7"))
    canvas.setLineWidth(1)
    canvas.line(2*cm, 2*cm, width - 2*cm, 2*cm)

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2*cm, 1.5*cm, "Generado por Calculadora Solar Fotovoltaica")
    canvas.drawRightString(width - 2*cm, 1.5*cm, f"Página {doc.page}")

    canvas.restoreState()


# =====================================================
# PORTADA PDF
# =====================================================
def portada_pdf(canvas, doc, datos):
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.lib.utils import ImageReader
    import os

    canvas.saveState()

    width, height = doc.pagesize

    # FONDO
    canvas.setFillColor(colors.HexColor("#f7f7f5"))
    canvas.rect(0, 0, width, height, fill=1, stroke=0)

    # FRANJAS DECORATIVAS
    canvas.setFillColor(colors.HexColor("#a5d6a7"))
    canvas.rect(0, height - 0.8*cm, width, 0.8*cm, fill=1, stroke=0)

    canvas.setFillColor(colors.HexColor("#2e7d32"))
    canvas.rect(0, 0, width, 0.6*cm, fill=1, stroke=0)

    # IMÁGENES IZQUIERDA (3)
    imagenes = ["images/p1.png", "images/p2.jpg", "images/p3.png"]
    x_img = 0
    ancho_img = 8.2*cm
    margen = 1*cm
    alto_util = height - (2 * margen)
    separacion = 0.3*cm
    alto_img = (alto_util - 2*separacion) / 3

    y_actual = height - margen

    for img_path in imagenes:
        if os.path.exists(img_path):
            imagen = ImageReader(img_path)
            y_actual -= alto_img
            canvas.drawImage(
                imagen,
                x_img,
                y_actual,
                width=ancho_img,
                height=alto_img,
                preserveAspectRatio=False,
                mask='auto'
            )
            y_actual -= separacion

    # Línea divisoria
    canvas.setStrokeColor(colors.HexColor("#66bb6a"))
    canvas.setLineWidth(1.5)
    canvas.line(8.2*cm, margen, 8.2*cm, height - margen)

    # LOGO DERECHA
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        canvas.drawImage(
            logo,
            11*cm,
            height - 8*cm,
            width=8*cm,
            height=6*cm,
            preserveAspectRatio=True,
            mask='auto'
        )

    # TEXTO INTRODUCTORIO
    canvas.setFillColor(colors.HexColor("#1c1f26"))
    canvas.setFont("Helvetica", 11)

    texto_y = height - 8*cm
    intro = [
        "Te presentamos una propuesta pensada para ti,",
        "para que tomes la decisión de cambiar tu forma",
        "de consumir energía y empieces a ahorrar desde ahora.",
        "",
        "Con nosotros, no tienes que preocuparte por nada:",
        "Diseñamos, instalamos y legalizamos todo el sistema por ti.",
        "",
        "Lo único que te queda es disfrutar los beneficios",
        "de una energía limpia, reducir tus gastos y asegurar tu futuro."
    ]

    for linea in intro:
        canvas.drawString(9.5*cm, texto_y, linea)
        texto_y -= 0.55*cm

    # DATOS DEL CLIENTE
    canvas.setFont("Helvetica-Bold", 11)
    y = texto_y - 1*cm

    datos_cliente = [
        ("Nombre:", datos["cliente_nombre"]),
        ("Teléfono:", datos["cliente_telefono"]),
        ("Dirección:", datos["cliente_direccion"]),
        ("Ciudad:", datos["cliente_ciudad"]),
        ("Fecha:", str(datos["cliente_fecha"]))
    ]

    for etiqueta, valor in datos_cliente:
        canvas.setFillColor(colors.black)
        canvas.drawString(9.5*cm, y, etiqueta)
        canvas.setFont("Helvetica", 11)
        canvas.setFillColor(colors.HexColor("#1b5e20"))
        canvas.drawString(12.2*cm, y, str(valor))
        y -= 0.8*cm
        canvas.setFont("Helvetica-Bold", 11)

    # POTENCIA
    canvas.setFont("Helvetica-Bold", 12)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(14*cm, 4.2*cm, "POTENCIA DEL SISTEMA")

    canvas.setFont("Helvetica-Bold", 20)
    canvas.setFillColor(colors.HexColor("#1b5e20"))
    canvas.drawCentredString(14*cm, 3.1*cm, f"{datos['potencia']:.2f} kWp")

    canvas.setFont("Helvetica-Bold", 18)
    canvas.drawCentredString(14*cm, 2.1*cm, "On Grid")

    canvas.restoreState()


# =====================================================
# PÁGINA 2 - BENEFICIOS (FLOWABLES)
# =====================================================
def pagina_beneficios(styles):
    import os
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib import colors
    from reportlab.lib.units import cm

    VERDE_OSCURO = colors.HexColor("#1B5E20")
    VERDE_MEDIO  = colors.HexColor("#2E7D32")
    VERDE_SUAVE  = colors.HexColor("#A5D6A7")
    GRIS         = colors.HexColor("#5F6B63")

    estilo_titulo = ParagraphStyle(
        "benef_titulo",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=12,
        alignment=TA_CENTER,
        textColor=VERDE_OSCURO,
        spaceAfter=4,
    )

    estilo_titulo_superior = ParagraphStyle(
        "obs_titulo",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=16,
        alignment=TA_CENTER,
        textColor=VERDE_OSCURO,
        spaceAfter=4,
    )

    estilo_desc = ParagraphStyle(
        "benef_desc",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=GRIS,
    )

    estilo_frase = ParagraphStyle(
        "frase_central",
        parent=styles["Normal"],
        fontName="Helvetica-BoldOblique",
        fontSize=15,
        leading=15,
        alignment=TA_CENTER,
        textColor=VERDE_MEDIO,
        spaceBefore=6,
        spaceAfter=6,
    )

    estilo_subtitulo = ParagraphStyle(
        "subtitulo_1715",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=16,
        alignment=TA_CENTER,
        textColor=VERDE_OSCURO,
        spaceAfter=4,
    )

    estilo_subinfo = ParagraphStyle(
        "subinfo_1715",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=12,
        alignment=TA_CENTER,
        textColor=GRIS,
        spaceAfter=8,
    )

    estilo_benef_t = ParagraphStyle(
        "tributario_titulo",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=12,
        textColor=VERDE_OSCURO,
    )

    estilo_benef_d = ParagraphStyle(
        "tributario_desc",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=11,
        textColor=GRIS,
    )

    imagenes = [
        "images/costos.png",
        "images/tarifa.jpg",
        "images/valorizacion.png",
    ]

    titulos = [
        "Ahorro en tu factura",
        "Protección ante tarifas",
        "Mayor valor del inmueble",
    ]

    descripciones = [
        "Reduce significativamente el costo de tu energía mensual mediante la generación propia.",
        "Evita el impacto de los incrementos en tarifas eléctricas a lo largo del tiempo.",
        "Incrementa el valor comercial de tu propiedad con energía limpia instalada.",
    ]

    def imagen_o_placeholder(ruta, w=4.6*cm, h=3.2*cm):
        if os.path.exists(ruta):
            return Image(ruta, width=w, height=h)
        else:
            ph = Table(
                [[Paragraph("Imagen aquí", estilo_titulo)]],
                colWidths=[w],
                rowHeights=[h],
            )
            ph.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E8F5E9")),
                ("BOX", (0, 0), (-1, -1), 1, VERDE_SUAVE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]))
            return ph

    columnas = []
    for i in range(3):
        bloque = [
            imagen_o_placeholder(imagenes[i]),
            Spacer(1, 0.25*cm),
            Paragraph(titulos[i], estilo_titulo),
            Spacer(1, 0.1*cm),
            Paragraph(descripciones[i], estilo_desc),
        ]
        card = Table([[bloque]], colWidths=[5.5*cm])
        card.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.white),
            ("BOX", (0, 0), (-1, -1), 1, VERDE_SUAVE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        columnas.append(card)

    tabla_superior = Table([columnas], colWidths=[5.8*cm, 5.8*cm, 5.8*cm])
    tabla_superior.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))

    frase = Paragraph(
        "LA ENERRGÍA SOLAR NO SOLO NOS BRINDA LUZ, SINO QUE TAMBIÉN ILUMINA EL CAMINO HACIA UN MUNDO MÁS LIMPIO Y SALUDABLE",
        estilo_frase
    )

    beneficios_tributarios = [
        ("Deducción de renta", "Permite deducir hasta el 50% de la inversión realizada del impuesto sobre la renta."),
        ("Exclusión de IVA", "Los equipos y servicios asociados al sistema pueden quedar excluidos del IVA."),
        ("Exención de aranceles", "Posibilidad de importar equipos y componentes sin pago de arancel."),
        ("Depreciación acelerada", "Permite depreciar los activos en un menor tiempo, mejorando la estructura financiera del proyecto."),
    ]

    filas_tributarias = []
    for i, (titulo, texto) in enumerate(beneficios_tributarios, start=1):
        num = Table([[str(i)]], colWidths=[0.7*cm], rowHeights=[0.7*cm])
        num.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), VERDE_MEDIO),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
        ]))

        texto_benef = [
            Paragraph(titulo, estilo_benef_t),
            Spacer(1, 0.05*cm),
            Paragraph(texto, estilo_benef_d),
        ]

        fila = Table([[num, texto_benef]], colWidths=[1.1*cm, 15.8*cm])
        fila.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.white),
            ("BOX", (0, 0), (-1, -1), 1, VERDE_SUAVE),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        filas_tributarias.append(fila)
        filas_tributarias.append(Spacer(1, 0.25*cm))

    flowables = [
        Spacer(1, 0.5*cm),

        Paragraph("BENEFICIOS DE LA ENERGÍA SOLAR", estilo_titulo_superior),
        Spacer(1, 0.4*cm),
        tabla_superior,
        Spacer(1, 0.8*cm),
        frase,
        Spacer(1, 0.7*cm),
        Paragraph("Beneficios Tributarios - Ley 1715", estilo_titulo_superior),
        Paragraph("Incentivos aplicables a proyectos de energías renovables en Colombia", estilo_subinfo),
        Spacer(1, 0.2*cm),
    ]

    flowables.extend(filas_tributarias)
    return flowables
###########################################################################################
def pagina_observaciones_estilo(styles):
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    import os

    VERDE_OSCURO = colors.HexColor("#1B5E20")
    VERDE_MEDIO  = colors.HexColor("#2E7D32")
    VERDE_SUAVE  = colors.HexColor("#A5D6A7")
    GRIS         = colors.HexColor("#5F6B63")

    # =========================
    # ESTILOS
    # =========================
    estilo_titulo = ParagraphStyle(
        "obs_titulo",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=16,
        alignment=TA_CENTER,
        textColor=VERDE_OSCURO,
        spaceAfter=4,
    )

    estilo_sub = ParagraphStyle(
        "obs_sub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=11,
        alignment=TA_CENTER,
        textColor=GRIS,
        spaceAfter=8,
    )

    estilo_benef_t = ParagraphStyle(
        "tributario_titulo",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=12,
        textColor=VERDE_OSCURO,
    )

    estilo_benef_d = ParagraphStyle(
        "tributario_desc",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=11,
        textColor=GRIS,
    )

    estilo_desc_img = ParagraphStyle(
        "desc_img",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=10.5,
        alignment=TA_CENTER,
        textColor=GRIS,
    )

    # =========================
    # CONTENIDO
    # =========================
    observaciones = [
        "La propuesta incluye transporte de carga y viáticos del personal técnico.",
        "El cliente debe garantizar que el área de instalación se encuentre disponible.",
        "Se deberá realizar un levantamiento detallado de la infraestructura existente para validar el punto de conexión.",
        "Será necesario efectuar la adecuación de la cubierta asegurando su capacidad estructural.",
        "Se recomienda realizar dos mantenimientos preventivos al año para garantizar el rendimiento del sistema.",
        "Se requiere validación con el operador de red sobre la disponibilidad del transformador principal."
    ]

    

    flowables = []

    # =========================
    # OBSERVACIONES
    # =========================
    flowables.append(Paragraph("OBSERVACIONES", estilo_titulo))
    flowables.append(Spacer(1, 0.1*cm))

    for i, texto in enumerate(observaciones, start=1):
        num = Table([[str(i)]], colWidths=[0.7*cm], rowHeights=[0.7*cm])
        num.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), VERDE_MEDIO),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
        ]))

        texto_benef = [
            Paragraph(texto, estilo_benef_d),
        ]

        fila = Table([[num, texto_benef]], colWidths=[1.1*cm, 15.8*cm])
        fila.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.white),
            ("BOX", (0, 0), (-1, -1), 1, VERDE_SUAVE),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))

        flowables.append(fila)
        flowables.append(Spacer(1, 0.18*cm))
    
    # =========================
    # TIEMPOS DE CONSTRUCCIÓN Y OBRA
    # =========================
    flowables.append(Spacer(1, 0.3*cm))
    flowables.append(Paragraph("TIEMPOS DE CONSTRUCCIÓN Y OBRA", estilo_titulo))
    flowables.append(Spacer(1, 0.2*cm))

    imagenes_tiempos = [
        "images/entrega.png",
        "images/obra.jpg",
        "images/retie.png",
        "images/OR.png"
    ]

    descripciones_tiempos = [
        "30 DíAS: Entrega de equipos y logística de materiales requeridos para la ejecución del proyecto.",
        "20 DÍAS: Instalación, adecuaciones y montaje técnico del sistema solar fotovoltaico.",
        "30 DÍAS: Pruebas operativas, validación técnica y proceso de certificación RETIE.",
        "30 DÍAS: Gestión documental y legalización del sistema ante el operador de red correspondiente."
    ]

    bloques_tiempos = []

    for i in range(4):
        if os.path.exists(imagenes_tiempos[i]):
            img = Image(imagenes_tiempos[i], width=6.0*cm, height=3.4*cm)
        else:
            img = Table(
                [[Paragraph("Imagen aquí", estilo_benef_t)]],
                colWidths=[6.0*cm],
                rowHeights=[3.4*cm]
            )
            img.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E8F5E9")),
                ("BOX", (0, 0), (-1, -1), 1, VERDE_SUAVE),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]))

        bloque = [
            img,
            Spacer(1, 0.18*cm),
            Paragraph(descripciones_tiempos[i], estilo_desc_img)
        ]

        card = Table([[bloque]], colWidths=[6.4*cm])
        card.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.white),
            ("BOX", (0, 0), (-1, -1), 1, VERDE_SUAVE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))

        bloques_tiempos.append(card)

    # 2 filas x 2 columnas
    tabla_tiempos_imgs = Table(
        [
            [bloques_tiempos[0], bloques_tiempos[1]],
            [bloques_tiempos[2], bloques_tiempos[3]]
        ],
        colWidths=[8.1*cm, 8.1*cm],
        rowHeights=[5.5*cm, 5.5*cm]
    )

    tabla_tiempos_imgs.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    flowables.append(tabla_tiempos_imgs)
    return flowables
###########################################################################################
###########################################################################################

def pagina_capex_y_pago(styles):
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    import os

    VERDE_OSCURO = colors.HexColor("#1B5E20")
    VERDE_MEDIO  = colors.HexColor("#2E7D32")
    VERDE_SUAVE  = colors.HexColor("#A5D6A7")
    GRIS         = colors.HexColor("#5F6B63")
    FONDO        = colors.HexColor("#F7FBF8")

    # =========================
    # ESTILOS
    # =========================
    titulo = ParagraphStyle(
        "titulo_pago",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        textColor=VERDE_OSCURO,
        fontSize=14,
        spaceAfter=6
    )

    subtitulo = ParagraphStyle(
        "sub_pago",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        textColor=GRIS,
        fontSize=9,
        spaceAfter=10
    )

    estilo_titulo_card = ParagraphStyle(
        "titulo_card",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=VERDE_OSCURO,
    )

    estilo_desc = ParagraphStyle(
        "desc_card",
        parent=styles["Normal"],
        fontSize=10,
        textColor=GRIS,
    )

    estilo_porcentaje = ParagraphStyle(
        "porcentaje",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        alignment=TA_CENTER,
        textColor=VERDE_MEDIO,
    )

    estilo_validez = ParagraphStyle(
        "validez_propuesta",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=12,
        alignment=TA_CENTER,
        textColor=VERDE_OSCURO,
        spaceBefore=8,
    )

    estilo_validez_sub = ParagraphStyle(
        "validez_sub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=10,
        alignment=TA_CENTER,
        textColor=GRIS,
    )

    # =========================
    # DATA
    # =========================
    pagos = [
        {
            "titulo": "Firma del contrato",
            "desc": "Anticipo",
            "porcentaje": "30%",
            "img": "images/contrato.png"
        },
        {
            "titulo": "Inicio de obra",
            "desc": "Al iniciar los trabajos",
            "porcentaje": "30%",
            "img": "images/inicio.png"
        },
        {
            "titulo": "Pruebas y puesta en marcha",
            "desc": "Finalización del sistema",
            "porcentaje": "20%",
            "img": "images/pruebas.png"
        },
        {
            "titulo": "Legalización",
            "desc": "Sistema operando correctamente",
            "porcentaje": "20%",
            "img": "images/legal.png"
        }
    ]

    # =========================
    # FUNCION TARJETA
    # =========================
    def card_pago(item):

        # Imagen
        if os.path.exists(item["img"]):
            icono = Image(item["img"], width=2.2*cm, height=2.2*cm)
        else:
            icono = Table(
                [["ICONO"]],
                colWidths=[2.2*cm],
                rowHeights=[2.2*cm]
            )
            icono.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#E8F5E9")),
                ("BOX", (0,0), (-1,-1), 1, VERDE_SUAVE),
                ("ALIGN", (0,0), (-1,-1), "CENTER"),
                ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ]))

        texto = [
            Paragraph(item["titulo"], estilo_titulo_card),
            Spacer(1, 2),
            Paragraph(item["desc"], estilo_desc),
            Spacer(1, 6),
            Paragraph(item["porcentaje"], estilo_porcentaje)
        ]

        contenido = Table(
            [[icono, texto]],
            colWidths=[2.5*cm, 5.5*cm]
        )

        contenido.setStyle(TableStyle([
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ]))

        card = Table([[contenido]], colWidths=[8.2*cm], rowHeights=[3.2*cm])

        card.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), colors.white),
            ("BOX", (0,0), (-1,-1), 1, VERDE_SUAVE),
            ("ROUNDEDCORNERS", [10,10,10,10]),
            ("LEFTPADDING", (0,0), (-1,-1), 10),
            ("RIGHTPADDING", (0,0), (-1,-1), 10),
            ("TOPPADDING", (0,0), (-1,-1), 10),
            ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ]))

        return card

    # =========================
    # LAYOUT
    # =========================
    flowables = []

    # espacio superior CAPEX
    flowables.append(Spacer(1, 7.5*cm))

    flowables.append(Paragraph("MÉTODO DE PAGO", titulo))
    flowables.append(Paragraph("Distribución de pagos del proyecto", subtitulo))
    flowables.append(Spacer(1, 6))

    fila1 = [card_pago(pagos[0]), card_pago(pagos[1])]
    fila2 = [card_pago(pagos[2]), card_pago(pagos[3])]

    tabla = Table(
        [fila1, fila2],
        colWidths=[8.2*cm, 8.2*cm],
        rowHeights=[3.4*cm, 3.4*cm]
    )

    tabla.setStyle(TableStyle([
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))

    flowables.append(tabla)
    flowables.append(Spacer(1, 0.35*cm))

    flowables.append(Paragraph(
        "La presente propuesta económica tiene una validez de 30 días calendario",
        estilo_validez
    ))

    flowables.append(Paragraph(
        "a partir de su fecha de emisión.",
        estilo_validez_sub
    ))

    
    return flowables
###########################################################################################
###########################################################################################
def pagina_analisis_financiero_pdf(styles, datos):
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.lib import colors
    from reportlab.lib.units import cm

    VERDE_OSCURO = colors.HexColor("#1B5E20")
    VERDE_MEDIO  = colors.HexColor("#2E7D32")
    VERDE_SUAVE  = colors.HexColor("#A5D6A7")
    GRIS         = colors.HexColor("#5F6B63")
    FONDO_CLARO  = colors.HexColor("#F7FBF8")

    # =========================
    # ESTILOS
    # =========================
    estilo_titulo = ParagraphStyle(
        "titulo_financiero_pdf",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        alignment=TA_CENTER,
        textColor=VERDE_OSCURO,
        spaceAfter=4,
    )

    estilo_subtitulo = ParagraphStyle(
        "subtitulo_financiero_pdf",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=GRIS,
        spaceAfter=10,
    )

    estilo_concepto = ParagraphStyle(
        "concepto_financiero_pdf",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        alignment=TA_LEFT,
        textColor=VERDE_OSCURO,
    )

    estilo_valor = ParagraphStyle(
        "valor_financiero_pdf",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.black,
    )

    estilo_nota = ParagraphStyle(
        "nota_financiera_pdf",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        alignment=TA_CENTER,
        textColor=GRIS,
        spaceBefore=10,
    )

    # =========================
    # TABLA FINANCIERA
    # =========================
    filas = [
        ["Consumo actual promedio (kWh/mes)", f"{datos['consumo_mensual']:,.0f}".replace(",", ".")],
        ["Tarifa actual promedio ($/kWh)", f"$ {datos['precio_kwh']:,.0f}".replace(",", ".")],
        ["Pago actual mensual promedio", f"$ {datos['pago_actual']:,.0f}".replace(",", ".")],
        ["Inversión inicial del proyecto", f"$ {datos['capex']:,.0f}".replace(",", ".")],
        ["Potencia del sistema", f"{datos['potencia']:.2f} kWp"],
        ["Energía generada (kWh/mes)", f"{datos['generacion_mensual']:,.0f}".replace(",", ".")],
        ["Cobertura energética", f"{datos['cobertura']:.1f}%"],
        ["Área requerida", f"{datos['area_total']:,.0f} m²".replace(",", ".")],
        ["Ahorro mensual estimado", f"$ {datos['ahorro_mensual']:,.0f}".replace(",", ".")],
        ["Operación y mantenimiento anual", f"$ {datos['om_anual']:,.0f}".replace(",", ".")],
        ["Tiempo estimado de retorno", f"{datos['payback']:.1f} años"],
        [f"Ahorro acumulado a {datos['n_años']} años", f"$ {datos['ahorro_total']:,.0f}".replace(",", ".")],
        ["Tasa Interna de Retorno (TIR)", f"{datos['tir']*100:.1f}%"],
        ["Tarifa equivalente con SSFV", f"$ {datos['tarifa_ssfv']:,.0f}/kWh".replace(",", ".")]
    ]

    tabla = Table(
        [["Concepto", "Valor"]] + filas,
        colWidths=[10.8*cm, 5.2*cm]
    )

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8F5E9")),
        ("TEXTCOLOR", (0, 0), (-1, 0), VERDE_OSCURO),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),

        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, FONDO_CLARO]),

        ("GRID", (0, 0), (-1, -1), 0.6, VERDE_SUAVE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    # =========================
    # CONTENIDO
    # =========================
    flowables = []

    flowables.append(Spacer(1, 0.4*cm))
    flowables.append(Paragraph("ANÁLISIS FINANCIERO DEL PROYECTO", estilo_titulo))
    flowables.append(Paragraph("Resumen ejecutivo de desempeño económico y retorno de inversión", estilo_subtitulo))
    flowables.append(Spacer(1, 0.2*cm))
    flowables.append(tabla)
    flowables.append(Spacer(1, 0.5*cm))

    nota = f"""
    El sistema fotovoltaico propuesto permite reducir de manera significativa el costo de la energía,
    mejorar la estabilidad tarifaria y generar un retorno atractivo sobre la inversión,
    con una proyección financiera positiva durante el horizonte de evaluación del proyecto.
    """

    flowables.append(Paragraph(nota, estilo_nota))

    return flowables
###########################################################################################
###########################################################################################

def generar_graficos_financieros(df_flujo):
    import matplotlib.pyplot as plt

    # ==========================
    # GRÁFICO 1: FLUJO ACUMULADO
    # ==========================
    plt.figure(figsize=(8, 4.5))
    plt.bar(df_flujo["AÑO"], df_flujo["FLUJO ACUMULADO"])
    plt.xlabel("Año")
    plt.ylabel("Flujo acumulado ($)")
    plt.xticks(df_flujo["AÑO"])
    plt.axhline(0, linewidth=1)
    plt.tight_layout()
    plt.savefig("flujo_acumulado.png", dpi=200, bbox_inches="tight")
    plt.close()

    # ==========================
    # GRÁFICO 2: ROI ACUMULADO
    # ==========================
    plt.figure(figsize=(8, 4.5))
    plt.bar(df_flujo["AÑO"], df_flujo["FLUJO ACUMULADO"])
    plt.axhline(0, linewidth=1.5, linestyle="--")

    # Buscar año de recuperación
    año_rec = None
    for _, row in df_flujo.iterrows():
        if row["FLUJO ACUMULADO"] >= 0:
            año_rec = row["AÑO"]
            break

    if año_rec is not None:
        plt.axvline(año_rec, linewidth=1.5, linestyle="--")
        plt.text(año_rec, max(df_flujo["FLUJO ACUMULADO"]) * 0.9, f"Payback: Año {año_rec}")

    plt.xlabel("Año")
    plt.ylabel("Retorno acumulado ($)")
    plt.xticks(df_flujo["AÑO"])
    plt.tight_layout()
    plt.savefig("roi_acumulado.png", dpi=200, bbox_inches="tight")
    plt.close()

def pagina_graficos_financieros_pdf(styles, df_flujo):
    from reportlab.platypus import Paragraph, Spacer, Image
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib import colors
    from reportlab.lib.units import cm

    generar_graficos_financieros(df_flujo)

    estilo_titulo = ParagraphStyle(
        "titulo_graficos_pdf",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1B5E20"),
        spaceAfter=4,
    )

    estilo_subtitulo = ParagraphStyle(
        "subtitulo_graficos_pdf",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#5F6B63"),
        spaceAfter=10,
    )

    estilo_seccion = ParagraphStyle(
        "seccion_grafico_pdf",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1B5E20"),
        spaceAfter=5,
    )

    flowables = []

    flowables.append(Spacer(1, 0.4*cm))
    flowables.append(Paragraph("COMPORTAMIENTO FINANCIERO DEL PROYECTO", estilo_titulo))
    flowables.append(Paragraph("Evolución acumulada del flujo de caja y recuperación de la inversión", estilo_subtitulo))
    flowables.append(Spacer(1, 0.2*cm))

    # Gráfico superior
    flowables.append(Paragraph("Flujo de caja acumulado", estilo_seccion))
    flowables.append(Image("flujo_acumulado.png", width=15.8*cm, height=7.0*cm))
    flowables.append(Spacer(1, 0.35*cm))

    # Gráfico inferior
    flowables.append(Paragraph("Retorno de inversión acumulado", estilo_seccion))
    flowables.append(Image("roi_acumulado.png", width=15.8*cm, height=7.0*cm))

    return flowables
###########################################################################################
###########################################################################################

# =====================================================
# GENERADOR PDF
# =====================================================
def generar_pdf_empresa(datos):
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    )
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import cm

    doc = SimpleDocTemplate(
        "reporte_empresa.pdf",
        pagesize=letter,
        topMargin=3.5*cm,
        bottomMargin=2.5*cm,
        leftMargin=2*cm,
        rightMargin=2*cm
    )

    styles = getSampleStyleSheet()
    content = []

    # =============================
    # PÁGINA 1 → PORTADA
    # =============================
    content.append(Paragraph(" ", styles["Normal"]))
    # =============================
    # PÁGINA 2 → BENEFICIOS
    # =============================
    content.append(PageBreak())
    content.extend(pagina_beneficios(styles))

    # =============================
    # PÁGINA 3 → OBSERVACIONES
    # =============================
    content.append(PageBreak())
    content.extend(pagina_observaciones_estilo(styles))

    # =============================
    # PÁGINA 4 → CAPEX + MÉTODO DE PAGO
    # =============================
    content.append(PageBreak())
    content.extend(pagina_capex_y_pago(styles))

    # =============================
    # PÁGINA 5 → ANÁLISIS FINANCIERO
    # =============================
    content.append(PageBreak())
    content.extend(pagina_analisis_financiero_pdf(styles, datos))

    # =============================
    # PÁGINA 6 → GRÁFICOS FINANCIEROS
    # =============================
    content.append(PageBreak())
    content.extend(pagina_graficos_financieros_pdf(styles, datos["df_flujo"]))  

    # CALLBACK DE PÁGINAS
    def todas_las_paginas(canvas, doc):

        if doc.page == 1:
            portada_pdf(canvas, doc, datos)
        else:
            encabezado_y_pie(canvas, doc)

    doc.build(
        content,
        onFirstPage=todas_las_paginas,
        onLaterPages=todas_las_paginas
    )

    return "reporte_empresa.pdf"


# =====================================================
# BOTÓN DESCARGA
# =====================================================
if st.button("📄 Generar reporte PRO"):

    datos = {
        "cliente_nombre": st.session_state.get("cliente_nombre", ""),
        "cliente_telefono": st.session_state.get("cliente_telefono", ""),
        "cliente_direccion": st.session_state.get("cliente_direccion", ""),
        "cliente_ciudad": st.session_state.get("cliente_ciudad", ""),
        "cliente_fecha": st.session_state.get("cliente_fecha", ""),

        "potencia": st.session_state.get("potencia_dc", 0),
        "paneles": st.session_state.get("paneles", 0),
        "produccion": st.session_state.get("generacion_anual", 0),

        "capex": st.session_state.get("capex", 0),
        "ahorro": st.session_state.get("ahorro_anual", 0),
        "payback": st.session_state.get("payback", 0),
        "vpn": st.session_state.get("vpn", 0),
        "tir": st.session_state.get("tir", 0),
        "lcoe": st.session_state.get("lcoe", 0),
        "df_flujo": df_flujo,

        "consumo_mensual": st.session_state.get("consumo_mensual", 0),
        "precio_kwh": st.session_state.get("precio_kwh", 0),
        "pago_actual": st.session_state.get("consumo_mensual", 0) * st.session_state.get("precio_kwh", 0),
        "generacion_mensual": st.session_state.get("potencia_dc", 0) * st.session_state.get("HSP", 3.5) * 30 * st.session_state.get("eficiencia", 0.8),
        "cobertura": (
            (st.session_state.get("potencia_dc", 0) * st.session_state.get("HSP", 3.5) * 30 * st.session_state.get("eficiencia", 0.8))
            / st.session_state.get("consumo_mensual", 1)
        ) * 100 if st.session_state.get("consumo_mensual", 0) > 0 else 0,
        "area_total": st.session_state.get("area_total", 0),
        "ahorro_mensual": st.session_state.get("ahorro_anual", 0) / 12 if st.session_state.get("ahorro_anual", 0) > 0 else 0,
        "om_anual": st.session_state.get("om_anual", 0),
        "ahorro_total": st.session_state.get("ahorro_total", 0),
        "n_años": st.session_state.get("n_años", 15),
        "tarifa_ssfv": st.session_state.get("tarifa_ssfv", 0),
    }

    pdf = generar_pdf_empresa(datos)

    with open(pdf, "rb") as f:
        st.download_button(
            label="⬇️ Descargar PDF",
            data=f,
            file_name=pdf,
            mime="application/pdf"
        )


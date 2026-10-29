
import sys
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "monitor"))

from monitor import procesar

st.set_page_config(
    page_title="Monitor Cine | Autómatas",
    page_icon="🎬",
    layout="wide",
)

st.markdown("""
<style>
.stApp {
    background-color: #0b1020;
}
section[data-testid="stSidebar"] {
    background-color: #11182b;
}
div[data-testid="stMetric"] {
    background-color: #151e33;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #293550;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🎬 Monitor Cine")
st.sidebar.caption("Sistema de análisis de secuencias")
pagina = st.sidebar.radio(
    "Navegación",
    ["Inicio", "Cargar datos", "Resultados", "Autómatas", "Métricas"],
)

st.title("Monitor de secuencias de cine")
st.caption("Análisis de patrones mediante AFND y AFD mínimo")

if pagina == "Inicio":
    st.subheader("Panel principal")
    st.write(
        "Carga un archivo CSV para ejecutar el monitor "
        "y consultar las secuencias reconocidas."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Motor", "AFD mínimo")
    c2.metric("Fuente", "CSV")
    c3.metric("Estado", "Preparado")

    st.info(
        "El reconocimiento de un patrón es una señal de "
        "seguimiento, no una prueba de fraude."
    )

elif pagina == "Cargar datos":
    st.subheader("Procesar archivo de datos")

    archivo = st.file_uploader("Selecciona un CSV", type=["csv"])

    if archivo is not None:
        try:
            df = pd.read_csv(archivo)
            st.write("Vista previa")
            st.dataframe(df.head(100), use_container_width=True)

            requeridas = {
                "id_evento", "fecha_hora",
                "id_sesion", "simbolo"
            }
            faltantes = requeridas - set(df.columns)

            if faltantes:
                st.error(
                    "Faltan columnas: " + ", ".join(sorted(faltantes))
                )
            elif st.button("Ejecutar monitor", type="primary"):
                with tempfile.TemporaryDirectory() as tmp:
                    entrada = Path(tmp) / "entrada.csv"
                    salida = Path(tmp) / "resultados.csv"

                    df.to_csv(entrada, index=False)
                    resumen = procesar(entrada, salida)

                    resultados = pd.read_csv(salida)
                    st.session_state["resultados"] = resultados

                    st.success("Procesamiento terminado.")
                    st.metric("Sesiones analizadas", resumen["casos"])
                    st.metric("Alertas detectadas", resumen["alertas"])
                    st.dataframe(
                        resultados, use_container_width=True
                    )

        except Exception as e:
            st.error(f"No se pudo procesar el archivo: {e}")

elif pagina == "Resultados":
    st.subheader("Resultados del análisis")

    resultados = st.session_state.get("resultados")

    if resultados is None:
        st.info("Primero carga y procesa un archivo CSV.")
    else:
        filtro = st.selectbox(
            "Filtrar por predicción",
            ["Todas", "alerta", "sin_alerta", "no_evaluable"],
        )

        vista = resultados
        if filtro != "Todas":
            vista = resultados[
                resultados["prediccion"] == filtro
            ]

        st.dataframe(vista, use_container_width=True)

        st.download_button(
            "Descargar resultados CSV",
            data=vista.to_csv(index=False).encode("utf-8"),
            file_name="resultados_monitor.csv",
            mime="text/csv",
        )

elif pagina == "Autómatas":
    st.subheader("Modelos de autómatas")

    modelos = [
        ROOT / "automatas" / "04_afd_minimo.json",
    ]

    for ruta in modelos:
        if ruta.exists():
            st.markdown(f"**{ruta.name}**")
            st.json(__import__("json").loads(
                ruta.read_text(encoding="utf-8")
            ))
        else:
            st.warning(f"No se encontró {ruta.relative_to(ROOT)}")

    st.caption(
        "Esta vista muestra la estructura JSON del modelo; "
        "todavía no dibuja el diagrama de estados."
    )

elif pagina == "Métricas":
    st.subheader("Resumen de resultados")

    resultados = st.session_state.get("resultados")

    if resultados is None:
        st.info("Ejecuta el monitor para consultar las métricas.")
    else:
        conteos = resultados["prediccion"].value_counts()
        a, b, c = st.columns(3)
        a.metric("Alertas", int(conteos.get("alerta", 0)))
        b.metric("Sin alerta", int(conteos.get("sin_alerta", 0)))
        c.metric("No evaluables", int(conteos.get("no_evaluable", 0)))

        st.bar_chart(conteos)

st.sidebar.divider()
st.sidebar.caption("Proyecto académico · Teoría de Autómatas")

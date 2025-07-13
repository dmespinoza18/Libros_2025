import os
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from tempfile import NamedTemporaryFile
import json

# === CONFIG ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters_libro")
RESULTS_FILE = os.path.join(BASE_DIR, "resultados_libro.json")

st.set_page_config(page_title="📖 Lectura Interactiva - Libro", layout="centered")
st.title("📖 Lectura Interactiva del Libro")

# === CARGAR QUIZZES (si existe archivo externo) ===
quizzes = {}
quiz_file = os.path.join(BASE_DIR, "quizzes_libro_3_al_10.json")
if os.path.exists(quiz_file):
    with open(quiz_file, "r", encoding="utf-8") as f:
        quizzes = json.load(f)

# === RESULTADOS POR USUARIO ===
def cargar_resultados():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_resultado(usuario, capitulo, puntaje):
    resultados = cargar_resultados()
    if usuario not in resultados:
        resultados[usuario] = {}
    resultados[usuario][capitulo] = puntaje
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

# === FUNCIONES ===
def obtener_capitulos():
    if not os.path.exists(CHAPTERS_DIR):
        return []
    return sorted([d for d in os.listdir(CHAPTERS_DIR) if os.path.isdir(os.path.join(CHAPTERS_DIR, d))])

def cargar_texto(capitulo):
    path = os.path.join(CHAPTERS_DIR, capitulo, "texto.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# === USUARIO TEMPORAL ===
usuario = st.text_input("👤 Nombre de usuario (para guardar tu progreso):", value="invitado")

# === INTERFAZ ===
capitulos = obtener_capitulos()
if not capitulos:
    st.warning("No se encontraron capítulos del libro.")
else:
    seleccionado = st.selectbox("Selecciona un capítulo:", capitulos)
    texto = cargar_texto(seleccionado)

    st.subheader(f"📘 {seleccionado.replace('_', ' ').title()}")
    st.write(texto)

    # Narración
    if st.button("🔊 Escuchar narración"):
        with st.spinner("Generando audio..."):
            tts = gTTS(texto, lang="es")
            with NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                tts.save(tmpfile.name)
                st.audio(tmpfile.name, format="audio/mp3")

    # Quiz si existe
    nombre_cap = seleccionado.replace("_", " ").title()
    if nombre_cap in quizzes:
        st.subheader("🧠 Quiz del capítulo")
        preguntas = quizzes[nombre_cap]
        score = 0
        total = len(preguntas)
        for pregunta, opciones in preguntas.items():
            respuesta = st.radio(pregunta, opciones, key=pregunta)
            if respuesta == opciones[0]:
                score += 1

        st.write(f"✅ Puntaje: {score}/{total}")
        guardar_resultado(usuario, nombre_cap, score)

        if score == total:
            st.success("¡Muy bien! Has comprendido el capítulo.")
        elif score >= total // 2:
            st.info("Vas bien, puedes repasarlo nuevamente.")
        else:
            st.warning("Intenta leer de nuevo y reflexionar sobre el contenido.")

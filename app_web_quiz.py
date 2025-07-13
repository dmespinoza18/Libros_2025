import os
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS

# === CONFIG ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")

st.set_page_config(page_title="Curso Interactivo de Python", layout="centered")
st.title("📘 Curso Interactivo de Python")

# === FUNCIONES ===
def obtener_capitulos():
    if not os.path.exists(CHAPTERS_DIR):
        return []
    return sorted([d for d in os.listdir(CHAPTERS_DIR) if os.path.isdir(os.path.join(CHAPTERS_DIR, d))])

def generar_codigo(path):
    ejemplo = '# Ejemplo básico en Python\nprint("Hola, mundo!")\n'
    with open(path, "w", encoding="utf-8") as f:
        f.write(ejemplo)

def generar_imagen(path, titulo="Python Visual"):
    img = Image.new("RGB", (600, 300), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 32)
    except:
        font = ImageFont.load_default()
    draw.text((40, 120), titulo, fill=(0, 0, 0), font=font)
    img.save(path)

def cargar_contenido(capitulo):
    ruta = os.path.join(CHAPTERS_DIR, capitulo)
    texto_path = os.path.join(ruta, "texto.txt")
    codigo_path = os.path.join(ruta, "codigo.py")
    imagen_path = os.path.join(ruta, "imagen.png")
    audio_path = os.path.join(ruta, "audio.mp3")

    contenido = {"texto": "", "codigo": "", "imagen": None, "audio": None}

    if os.path.exists(texto_path):
        with open(texto_path, "r", encoding="utf-8") as f:
            contenido["texto"] = f.read()

    if contenido["texto"]:
        if not os.path.exists(codigo_path):
            generar_codigo(codigo_path)
        if not os.path.exists(imagen_path):
            generar_imagen(imagen_path, capitulo.replace("_", " ").title())
        if not os.path.exists(audio_path):
            tts = gTTS(contenido["texto"], lang="es")
            tts.save(audio_path)

    if os.path.exists(codigo_path):
        with open(codigo_path, "r", encoding="utf-8") as f:
            contenido["codigo"] = f.read()

    if os.path.exists(imagen_path):
        contenido["imagen"] = imagen_path

    if os.path.exists(audio_path):
        contenido["audio"] = audio_path

    return contenido

# === INTERFAZ ===
capitulos = obtener_capitulos()
if not capitulos:
    st.warning("No se encontraron capítulos.")
else:
    seleccionado = st.selectbox("Selecciona un capítulo:", capitulos)
    contenido = cargar_contenido(seleccionado)

    st.subheader("📖 Texto del capítulo")
    st.write(contenido["texto"])

    if contenido["codigo"]:
        st.subheader("💻 Código de ejemplo")
        st.code(contenido["codigo"], language="python")

    if contenido["imagen"]:
        st.subheader("🖼️ Imagen visual")
        st.image(Image.open(contenido["imagen"]), use_column_width=True)

    if contenido["audio"]:
        st.subheader("🔊 Narración")
        with open(contenido["audio"], "rb") as f:
            st.audio(f.read(), format="audio/mp3")

    # === QUIZ por capítulo ===
    if seleccionado == "capitulo_1":
        st.subheader("🧠 Quiz - Capítulo 1")
        score = 0

        q1 = st.radio("¿Qué imprime `print('Hola')`?", ["Hola", "hola", "'Hola'"])
        if q1 == "Hola":
            score += 1

        q2 = st.radio("¿Qué símbolo se usa para comentarios en Python?", ["//", "#", "--"])
        if q2 == "#":
            score += 1

        q3 = st.radio("¿Cuál es el tipo de dato de `'42'` (entre comillas)?", ["int", "str", "float"])
        if q3 == "str":
            score += 1

        st.write(f"✅ Puntaje: {score}/3")
        if score == 3:
            st.success("¡Excelente! Has completado el capítulo correctamente.")
        elif score >= 1:
            st.info("Vas bien, pero puedes repasar algunas partes.")
        else:
            st.warning("Intenta repasar el capítulo antes de continuar.")

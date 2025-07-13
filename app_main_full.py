import streamlit as st
import importlib.util
import os
import streamlit_authenticator as stauth

# --- USUARIOS CON HASHES DIRECTOS ---
names = ["Alumno Uno", "Alumno Dos"]
usernames = ["alumno1", "alumno2"]
hashed_pw = [
    "$pbkdf2-sha256$29000$BF7LwFYFZqUd3ZaqU5ZIMw$bmWeuR0wEjStEStEZHeAN0JuEo6HKNpBMw9FPyLwvA8",  # python123
    "$pbkdf2-sha256$29000$OJ0meLPyzTZJzI9GMiFjvQ$d.wn1AqWmO3cKD0smLNmEoYGRMGq01ge5YfKAbW2AoY"   # curso456
]

authenticator = stauth.Authenticate(
    names, usernames, hashed_pw,
    "curso_python_app", "abcdef", cookie_expiry_days=1
)

name, auth_status, username = authenticator.login("👤 Iniciar sesión", "main")

if auth_status is False:
    st.error("Usuario o contraseña incorrectos.")
elif auth_status is None:
    st.warning("Por favor inicia sesión.")
elif auth_status:
    st.sidebar.success(f"Bienvenido, {name} 👋")

    st.title("🎓 Plataforma Educativa de Python")

    menu = st.sidebar.selectbox("Selecciona una sección:", [
        "📘 Curso Interactivo",
        "📚 Biblioteca",
        "📖 Lectura del Libro"
    ])

    if menu == "📘 Curso Interactivo":
        st.subheader("📘 Curso Interactivo de Python")
        curso_path = os.path.join(os.path.dirname(__file__), "app_web_quiz.py")
        if os.path.exists(curso_path):
            spec = importlib.util.spec_from_file_location("curso", curso_path)
            curso = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(curso)
        else:
            st.error("No se encontró el archivo del curso.")

    elif menu == "📚 Biblioteca":
        st.subheader("📚 Biblioteca de lectura")
        biblioteca_path = os.path.join(os.path.dirname(__file__), "app_biblioteca.py")
        if os.path.exists(biblioteca_path):
            spec = importlib.util.spec_from_file_location("biblioteca", biblioteca_path)
            biblioteca = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(biblioteca)
        else:
            st.error("No se encontró el archivo de la biblioteca.")

    elif menu == "📖 Lectura del Libro":
        st.subheader("📖 Lectura interactiva del libro")
        libro_path = os.path.join(os.path.dirname(__file__), "app_libro_interactivo.py")
        if os.path.exists(libro_path):
            spec = importlib.util.spec_from_file_location("libro", libro_path)
            libro = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(libro)
        else:
            st.error("No se encontró el archivo del libro.")

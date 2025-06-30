# 🤖 Chatbot Local con FastAPI

Este proyecto es una aplicación web construida con **Python** y **FastAPI**, que permite interactuar localmente con un chatbot de lenguaje natural. Incluye autenticación de usuarios, almacenamiento de conversaciones en base de datos y una interfaz web amigable.

---

## 🧭 Tabla de Contenidos

- [Características](#características)
- [Tecnologías Usadas](#tecnologías-usadas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Uso](#uso)
- [Archivos Relevantes](#archivos-relevantes)
- [Notas Adicionales](#notas-adicionales)
- [Licencia](#licencia)

---

## ✨ Características

- 💬 Interacción con un modelo de lenguaje natural.
- 🔐 Autenticación de usuarios mediante login básico.
- 💾 Almacenamiento local de conversaciones en SQLite.
- 🌐 Interfaz web sencilla construida con Jinja2.
- 🛠️ Modularidad y estructura clara para facilitar mantenimiento.

---

## 🧰 Tecnologías Usadas

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/)
- **Frontend:** HTML + Jinja2
- **Base de Datos:** SQLite
- **Autenticación:** Módulo personalizado con hashing de contraseñas
- **Cliente LLM:** Conexión a modelo de lenguaje (definido en `groq_client.py`)

---

## 🗂️ Estructura del Proyecto

```

├── auth.py           # Lógica de autenticación y gestión de usuarios
├── db.py             # Conexión y operaciones con SQLite
├── groq\_client.py    # Cliente para interactuar con el modelo de lenguaje
├── main.py           # Inicialización de FastAPI y definición de rutas
├── requirements.txt  # Lista de dependencias del proyecto
├── templates/        # Plantillas HTML para login, chat e inicio
├── data/             # Contiene la base de datos SQLite
├── .gitignore        # Archivos ignorados por Git

````

---

## ⚙️ Instalación

Sigue estos pasos para instalar y ejecutar el proyecto localmente:

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu_usuario/chatbot-fastapi.git
   cd chatbot-fastapi
````

2. Crea y activa un entorno virtual:

   ```bash
   python -m venv env
   # En Windows
   .\env\Scripts\activate
   # En Unix/macOS
   source env/bin/activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Inicia el servidor:

   ```bash
   uvicorn main:app --reload
   ```

5. Accede a la aplicación en tu navegador:
   👉 [http://localhost:8000](http://localhost:8000)

---

## 🚀 Uso

1. Dirígete a la URL del servidor local.
2. Inicia sesión con tu usuario (o crea uno si se ha habilitado el registro).
3. Comienza a interactuar con el chatbot desde la interfaz web.
4. Las conversaciones se almacenan automáticamente.

---

## 📁 Archivos Relevantes

* `auth.py`: Módulo de autenticación y manejo de usuarios.
* `db.py`: Funciones para interactuar con la base de datos.
* `groq_client.py`: Lógica para comunicarte con el modelo de lenguaje.
* `main.py`: Punto de entrada de la aplicación, contiene las rutas principales.
* `templates/`: Contiene las plantillas HTML de la interfaz.
* `data/chatbot.db`: Archivo SQLite generado automáticamente.

---

## 📝 Notas Adicionales

* El archivo `.gitignore` excluye archivos como `env/` y `*.db`.
* Puedes personalizar el diseño modificando los archivos en `templates/`.
* Asegúrate de que la carpeta `data/` exista o se creará automáticamente al iniciar.

---

## 📄 Licencia

Este proyecto se distribuye para **uso personal y educativo**. Puedes modificar y adaptar el código según tus necesidades.

---

¿Tienes sugerencias o mejoras? ¡Siéntete libre de hacer un fork o enviar un pull request!

```

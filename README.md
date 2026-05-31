# py-project-companion
Una herramienta ligera de consola en Python para automatizar la creación de entornos virtuales, gestionar proyectos locales mediante archivos JSON y realizar commits/pushes de Git en segundo plano usando subprocess y SSH.

# 🚀 py-project-companion

Una herramienta ligera de consola en Python diseñada para automatizar la configuración de tu espacio de trabajo. Permite gestionar proyectos locales mediante archivos JSON, automatizar la creación de entornos virtuales y realizar commits/pushes de Git en segundo plano.

---

## ✨ Características (Features)
* 📁 **Gestión Centralizada:** Almacena y lee rutas de tus proyectos desde un archivo JSON para evitar duplicados.
* 🤖 **Entornos Virtuales Inteligentes:** Detecta si falta el entorno virtual y lo crea automáticamente de forma invisible usando `subprocess`.
* 🛸 **Git en Segundo Plano:** Añade archivos, hace commits con mensajes personalizados y sube los cambios a GitHub sin abrir la terminal.

## 🛠️ Requisitos Previos (Prerequisites)
Para que el script pueda interactuar con GitHub de forma invisible en segundo plano, tu sistema operativo debe cumplir con:

1. **Claves SSH Configuradas:** GitHub debe tener registrada la clave SSH de tu máquina para evitar que el script se congele pidiendo usuario y contraseña.
2. **Origen SSH:** El repositorio local debe estar conectado mediante la URL de SSH (`git@github.com:...`), no por HTTPS.

## 🚀 Cómo Usar (How to use)

1. Clona este repositorio:
   ```bash
   git clone git@github.com:EmersonDavid1322/py-project-companion.git
   ```
2. Ejecuta el script principal:
   ```bash
   python main.py
   ```
3. Sigue las instrucciones en pantalla para registrar un nuevo proyecto o gestionar uno existente.

## 📝 Notas de Aprendizaje
Este es un proyecto personal desarrollado de forma **autodidacta** para dominar conceptos avanzados de Python como:
* Manipulación y persistencia de datos con **JSON**.
* Manejo de la terminal **BASH**.
* Automatización del sistema operativo Linux con el módulo **`subprocess`**.
* Manejo avanzado de rutas independientes del sistema con **`pathlib`**.
* Programación Orientada a Objetos (POO).

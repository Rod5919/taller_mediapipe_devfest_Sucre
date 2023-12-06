# Guía taller Mediapipe

## Paso 1: Virtualización

Para crear un entorno virtual de python, se debe instalar el paquete virtualenv o anaconda. Los comandos para crear un entorno virtual son:

### Virtualenv

#### Linux

```bash
# Instalar virtualenv
pip install virtualenv

# Crear entorno virtual
virtualenv -p python3 env

# Activar entorno virtual
source env/bin/activate

# Desactivar entorno virtual
deactivate
```

#### Windows

```bash
# Instalar virtualenv
python3 -m pip install virtualenv

# Crear entorno virtual
virtualenv -p python3 env

# Activar entorno virtual
.\env\Scripts\activate

# Desactivar entorno virtual
deactivate
```

### Anaconda

#### Linux

```bash
# Instalar anaconda (miniconda)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh

# Crear entorno virtual
conda create -n env_name python=3.11

# Activar entorno virtual
conda activate env_name

# Desactivar entorno virtual
conda deactivate
```

#### Windows

```bash
# Instalar anaconda (miniconda)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
Miniconda3-latest-Windows-x86_64.exe

# Crear entorno virtual
conda create -n env_name python=3.11

# Activar entorno virtual
conda activate env_name

# Desactivar entorno virtual
conda deactivate
```

## Paso 2: Instalar dependencias

Para instalar las dependencias del proyecto, se debe ejecutar el siguiente comando:

```bash
pip install -r requirements.txt

# Si está usando anaconda, se debe ejecutar el siguiente comando previamente:
conda install pip
```

## Paso 3: Hola mundo con flask

Para crear un servidor web con flask, se debe crear un archivo con el nombre app.py y escribir el siguiente código:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
```

Se puede ejecutar de 2 formas:

```bash
# 1. Ejecutar el archivo app.py
python app.py

# 2. Ejecutar el siguiente comando
flask run --host=host_name --port=port_number
```

## Paso 4: Crear el árbol de archivos del proyecto

El arbol de archivos del proyecto debe ser el siguiente:

```bash
.
├── app.py
├── models
│   └── gesture_recognizer.task
├── requirements.txt
├── static
│   └── script.js
└── templates
    └── index.html
```

## Paso 5: Crear el archivo index.html

Este archivo debe llevar el nombre de `index.html` y debe estar ubicado en la carpeta `templates`. El código deben copiarlo del repositorio.

## Paso 6: Crear el archivo script.js

Este archivo debe llevar el nombre de `script.js` y debe estar ubicado en la carpeta `static`. El código deben copiarlo del repositorio.

## Paso 7: Lógica de piedra, papel o tijera

Para crear la lógica del juego, se debe crear una función como la que se muestra en el archivo `app.py`.

## Paso 8: Conectar WebSockets

Para conectar los WebSockets, se debe crear una función como la que se muestra en el archivo `app.py`. Esta función a través de los emisores de SocketIO, pueden enviar información a los clientes conectados. Asi como también, pueden recibir información de los clientes conectados mediante sus decoradores.

## Paso 9: Descargar el modelo de reconocimiento de gestos

Para descargar el modelo de reconocimiento de gestos, se debe ingresar al siguiente enlace:

[Modelos de reconocimiento de gestos de Mediapipe](https://developers.google.com/mediapipe/solutions/vision/gesture_recognizer#models)

## Paso 10: Importar el modelo y utilizar OpenCV para separar las imágenes

Para importar el modelo, se debe crear una función como la que se muestra en el archivo `app.py`.

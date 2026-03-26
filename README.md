# Chat Model API

Una API construida en **FastAPI** diseñada para generar recomendaciones neuropsicológicas automatizadas utilizando la inteligencia artificial de **Groq** (modelo `llama-3.3-70b-versatile`).

El sistema recibe un resultado de evaluación diagnóstica preliminar, estructura la información y se conecta a un modelo de IA avanzado para proveer recomendaciones claras y comprensibles dirigidas a padres, educadores y psicólogos.

---

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd chat_model
```

### 2. Entorno Virtual y Dependencias
Crea un entorno virtual e instala las librerías necesarias (como `fastapi`, `uvicorn`, `groq`, `pydantic` y `python-dotenv`).

```bash
python -m venv .venv

# Activar en Windows
.venv\Scripts\activate

# Instalar dependencias esenciales
pip install fastapi uvicorn groq python-dotenv pydantic
```

### 3. Variables de Entorno
Crea un archivo llamado `.env` en la raíz del proyecto y agrega tu clave de acceso a la API de Groq:
```env
GROQ_API_KEY=tu_clave_api_aqui
```

---

## ⚙️ Uso y Ejecución

Levanta la aplicación localmente mediante Uvicorn:

```bash
uvicorn main:app --reload
```

Por defecto, la API estará expuesta en `http://127.0.0.1:8000`.

Puedes acceder a la documentación interactiva generada por FastAPI en:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 Endpoints Disponibles

### 1. Health Check (GET / HEAD)
Endpoints de salud para comprobar que la API está funcionando, especialmente útiles para monitoreo y despliegue (ej. balanceadores de carga o Docker).

- **`HEAD /`**
- **`GET /health`**
  - **Respuesta Exitosa:**
    ```json
    {
      "status": "ok",
      "message": "Service is running successfully"
    }
    ```

### 2. Generación de Recomendaciones (POST)
Endpoint principal de la aplicación.

- **`POST /chat_recomendaciones`**
  - **Cuerpo de la Petición (JSON):**
    ```json
    {
      "trastorno": "TDAH",
      "resultado": "Probable",
      "probabilidad": 0.85,
      "edad": 8,
      "genero": "Masculino"
    }
    ```
  - **Respuesta (JSON):**
    ```json
    {
      "response": "[Informe generado por la IA con recomendaciones para padres y docentes...]",
      "status": "success"
    }
    ```

---

## 📁 Estructura del Proyecto

```
chat_model/
│
├── .env                  # Variables de entorno (API keys)
├── main.py               # Punto de entrada de la app, contiene los endpoints
├── models/
│   └── models.py         # Definición del modelo de datos Pydantic (data_chat)
├── prompt/
│   └── prueba_1.py       # Contiene el prompt diseñado y de contexto para la IA
└── service/
    └── connect_model.py  # Lógica de conexión a Groq y parámetros del modelo
```

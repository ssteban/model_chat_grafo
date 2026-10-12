from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import logging
from service.connect_model import get_groq_response, get_groq_response_chat
from models.models import data_chat, data_chat_general
from prompt.prueba_1 import prompt_inicio
from prompt.chat_general import prompt_general

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Chat Model API",
    description="API for the Chat Model service providing recommendations.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.head("/", status_code=status.HTTP_200_OK, summary="Health Check (HEAD)")
async def health_check_head():
    """
    Health check endpoint for HEAD requests to verify system status.
    """
    return {"status": "ok"}

@app.get("/health", status_code=status.HTTP_200_OK, summary="Health Check (GET)")
async def health_check_get():
    """
    Health check endpoint for GET requests to verify system status.
    """
    return {"status": "ok", "message": "Service is running successfully"}

@app.post("/chat_recomendaciones")
async def chat(data: data_chat):
    """
    Endpoint that processes the diagnostic data and requests a Groq AI response
    using the designed prompt.
    """
    try:
        logger.info(f"Received chat request for disorder: {data.trastorno}")
        
        # Concatenate the prompt with the incoming data
        full_prompt = (
            f"{prompt_inicio}\n"
            f"Información recibida:\n"
            f"- Trastorno evaluado: {data.trastorno}\n"
            f"- Resultado de la evaluación: {data.resultado}\n"
            f"- Probabilidad de padecer el trastorno: {data.probabilidad}\n"
            f"- Edad del niño o niña: {data.edad}\n"
            f"- Género: {data.genero}\n"
        )
        
        ai_response = get_groq_response(full_prompt)
        
        return {
            "response": ai_response,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing the recommendation request."
        )


@app.post("/chat_general")
async def chat_general(data: data_chat_general):
    """
    Endpoint de pregunta-respuesta general (asistente NeuroIA).
    Sin memoria: cada request se responde de forma independiente,
    solo se envía la pregunta actual.
    """
    pregunta = data.pregunta.strip()
    if not pregunta:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La pregunta no puede estar vacía."
        )

    try:
        logger.info(f"General chat request received ({len(pregunta)} chars)")

        ai_response = get_groq_response_chat(prompt_general, pregunta)

        if not ai_response:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="No se pudo obtener respuesta del modelo."
            )

        return {
            "response": ai_response,
            "status": "success"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing general chat request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing the general chat request."
        )


        
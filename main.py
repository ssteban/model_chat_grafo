from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import logging
from service.connect_model import get_groq_response, get_groq_response_chat
from models.models import data_chat, data_chat_general, data_resumen_caso, data_redactar_correo
from prompt.prueba_1 import prompt_inicio
from prompt.chat_general import prompt_general
from prompt.resumen_caso import prompt_resumen_caso
from prompt.redactar_correo import prompt_redactar_correo

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


@app.post("/resumen_caso")
async def resumen_caso(data: data_resumen_caso):
    """
    Endpoint que genera un resumen del caso (para el módulo de seguimientos
    del psicólogo) a partir de los datos de una prueba: quién es el estudiante,
    qué prueba se le aplicó y qué resultado dio el modelo. Sin diagnóstico.
    """
    try:
        logger.info(f"Resumen de caso solicitado para: {data.nombre_prueba}")

        full_prompt = (
            f"{prompt_resumen_caso}\n"
            f"Datos del caso:\n"
            f"- Estudiante: {data.nombre_estudiante}\n"
            f"- Edad: {data.edad} años\n"
            f"- Género: {data.genero}\n"
            f"- Prueba aplicada: {data.nombre_prueba}\n"
            f"- Resultado del modelo: {data.resultado_modelo}\n"
            f"- Probabilidad estimada: {data.probabilidad}\n"
        )

        ai_response = get_groq_response(full_prompt)

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
        logger.error(f"Error generando resumen de caso: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating the case summary."
        )


@app.post("/redactar_correo")
async def redactar_correo(data: data_redactar_correo):
    """
    Endpoint que redacta (con IA) un correo del psicólogo a un acudiente:
    contacto general o solicitud de reunión por Meet. El front envía el
    parentesco REGISTRADO (p. ej. "padres") y la IA lo traduce al vínculo
    correcto del estudiante ("su hijo/hija") sin condicionales en el código.
    Respuesta estricta: primera línea "ASUNTO: ..." y el resto "CUERPO: ...".
    """
    tipo = data.tipo.strip().lower()
    if tipo not in ("contacto", "reunion"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El tipo debe ser 'contacto' o 'reunion'."
        )

    try:
        logger.info(f"Redaccion de correo solicitada ({tipo}) para: {data.nombre_estudiante}")

        full_prompt = (
            f"{prompt_redactar_correo}\n"
            f"Datos del correo:\n"
            f"- Tipo de correo: {tipo}\n"
            f"- Nombre del acudiente: {data.nombre_acudiente}\n"
            f"- Parentesco registrado en el sistema: {data.parentesco_registrado or 'no informado'}\n"
            f"- Estudiante: {data.nombre_estudiante}\n"
            f"- Género del estudiante: {data.genero_estudiante or 'no informado'}\n"
            f"- Curso: {data.nombre_curso or 'no informado'}\n"
            f"- Institución: {data.nombre_colegio or 'no informado'}\n"
            f"- Psicólogo: {data.nombre_psicologo}\n"
        )

        ai_response = get_groq_response(full_prompt)

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
        logger.error(f"Error redactando el correo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error drafting the email."
        )


        
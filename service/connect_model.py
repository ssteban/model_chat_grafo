import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

def get_groq_response(prompt):
    """
    Función para conectarse a la API de Groq y obtener una respuesta.
    """
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("Error: Por favor, configura tu GROQ_API_KEY en el archivo .env")
        return None

    client = Groq(api_key=api_key)

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Ocurrió un error al conectar con Groq: {e}")
        return None


from connect_model import get_groq_response
from prompt.prueba_1 import prompt_inicio

result = """

Trastorno evaluado: Dislexia
Resultado de la evaluación: PROBABLE
Probabilidad de padecer el trastorno: 0.85
Edad del niño o niña: 8 años
Género: Masculino

"""

print(get_groq_response(prompt_inicio + result))

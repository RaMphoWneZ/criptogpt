from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# Configuración de Ollama
OLLAMA_URL = "http://192.168.1.114:11434/api/generate"
MODEL_NAME = "phi:2"

# Modelo Pydantic para recibir comandos
class Command(BaseModel):
    command: str

# Llamada a la API de CoinGecko para precios
def get_crypto_price(symbol: str):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get(symbol, {}).get("usd", None)
    raise HTTPException(status_code=404, detail="Precio no encontrado")

# Procesar comandos con Ollama
def process_command_with_ollama(prompt: str):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result.get("response", "No se pudo procesar el comando.")
    raise HTTPException(status_code=500, detail="Error al comunicarse con Ollama")

# Ruta para manejar comandos
@app.post("/command")
async def handle_command(command: Command):
    user_input = command.command.strip()
    
    # Comando: !precio <symbol>
    if user_input.startswith("!precio"):
        symbol = user_input.split(" ")[1].lower()
        price = get_crypto_price(symbol)
        if price:
            return {"response": f"El precio de {symbol.upper()} es ${price}"}
        return {"response": f"No se encontró el precio de {symbol.upper()}"}
    
    # Comando: !analiza <symbol>
    elif user_input.startswith("!analiza"):
        symbol = user_input.split(" ")[1].upper()
        prompt = f"Analiza el comportamiento reciente de {symbol} basado en su precio y volumen."
        analysis = process_command_with_ollama(prompt)
        return {"response": analysis}
    
    # Comando desconocido
    else:
        return {"response": "Comando no reconocido. Prueba con '!precio <symbol>' o '!analiza <symbol>'."}

# Ruta de salud
@app.get("/health")
async def health_check():
    return {"status": "OK"}
from fastapi import FastAPI, HTTPException
from googletrans import Translator, LANGUAGES

app = FastAPI()
translator = Translator()

@app.get("/translate/")
async def translate(text: str):
    translation = translator.translate(text, src='fr', dest='en')
    return {"translated_text": translation.text}

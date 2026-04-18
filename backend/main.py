from collections import defaultdict
from datetime import datetime
from fastapi import FastAPI
import requests

import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.get("/cep/{cep}")
def home(cep:str):
    
    UrlCep = f"https://viacep.com.br/ws/{cep}/json/"

    resultado = requests.get(UrlCep)
    
    JsonCep = resultado.json()
    
    if "erro" in JsonCep:
        return "CEP INVALIDO"
    
    cidade = JsonCep['localidade']
    estado = JsonCep['uf']
    clima_url = "https://api.openweathermap.org/data/2.5/forecast"
    
    param = {
        "q": f"{cidade},{estado},BR",
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }
    
    clima = requests.get(clima_url, params=param).json()
    
    dias = defaultdict(list)
    
    for item in clima['list']:
        data = item["dt_txt"].split(" ")[0]
        dias[data].append(item)
    
    resultado_final = []

    for data, previsoes in dias.items():
        temp = [p["main"]['temp'] for p in previsoes] 
        # faz a ordenação das temperaturas pra cada temperatura daquele dia em um array usando um "list compreend"
        # quase como rodar um laço sem rodar um laço
        resultado_final.append({
            "data": data,
            "min":min(temp),
            "max":max(temp),
            "horarios":[
                {
                    "hora": p["dt_txt"].split(" ")[1],
                    "temp": p["main"]["temp"],
                    "descricao": p["weather"][0]["description"]
                }
                for p in previsoes
            ]
        })
    
    return resultado_final

        

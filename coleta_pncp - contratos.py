# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 14:06:47 2026

@author: Arlete Freitas

MBA USP/Esalq
Trabalho de Conclusão do MBA de Data Science 

Tema: Modelo preditivo de risco de aditivo contratual em obras públicas
"""
# %% Importando as Bibliotecas

import pandas as pd
import requests
from datetime import date, timedelta
import time

# %% Parâmetros
DataInicial = date(2025, 6, 23)
DataFinal = date(2026, 6, 30)

# %% Importando os dados do PNCP (De DataInicial até DataFinal)

data= DataInicial
Contratos_PNCP = []

while data <= DataFinal:
    
    PaginaPNCP = 1
    while True:
        try:
            response = requests.get("https://pncp.gov.br/api/consulta/v1/contratos", params={
                "dataInicial": data.strftime("%Y%m%d"),
                "dataFinal": data.strftime("%Y%m%d"),
                "pagina": PaginaPNCP}, timeout=180)
    
            if response.status_code==400:
                if "inexistente" in response.text and "Página" in response.text:
                    print(f"Fim da paginação da data {data} atingido.")
                    break
            elif response.status_code==204:
                    print(f"Fim da paginação da data {data} atingido.")
                    break
            
            response.raise_for_status() # Verifica código da requisição
            dados = response.json()
            
            Contratos_PNCP.extend(dados['data'])
            print(f"Página {PaginaPNCP} da data {data} coletada.")
            PaginaPNCP+=1 
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar a API: {e}")
            print(f"Página: {PaginaPNCP} e Data: {data}")
            time.sleep(10)
    
    data += timedelta(days=1)
    pd.DataFrame(Contratos_PNCP).to_parquet("coleta_pncp.parquet")
    
print("Coleta finalizada!")
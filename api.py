"""
Script: api.py
Descrição:
  - Carrega o modelo LSTM treinado para prever 10 dias à frente
  - Exibe um endpoint /predict que recebe >=60 preços históricos
  - Retorna 10 valores de previsão (multi-step) em uma única chamada
"""

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
import pickle
import time
import psutil
import os

# Cria a instância do FastAPI
app = FastAPI()

# Parâmetros do modelo
WINDOW_SIZE = 60        # Número de passos de entrada
FORECAST_HORIZON = 10   # Número de passos que o modelo retorna de uma só vez

@app.on_event("startup")
async def startup_event():
    print("Servidor iniciado. Acesse http://127.0.0.1:8000/docs para testar os endpoints.")

# Carrega o modelo treinado (deve ter saída (1, 10) quando input (1, 60, 1))
try:
    model = tf.keras.models.load_model("lstm_model_petr3.h5")
    print("Modelo carregado com sucesso (multi-step).")
except Exception as e:
    print("Erro ao carregar o modelo:", e)

# Carrega o objeto scaler
try:
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    print("Scaler carregado com sucesso.")
except Exception as e:
    print("Erro ao carregar o scaler:", e)

# Modelo de dados de entrada
class StockData(BaseModel):
    # Aceita pelo menos 60 valores
    historical_prices: list[float]

# Middleware para monitoramento (tempo, CPU, memória)
@app.middleware("http")
async def add_monitoring_headers(request: Request, call_next):
    start_time = time.time()
    process = psutil.Process(os.getpid())
    cpu_times_start = process.cpu_times()
    mem_start = process.memory_info().rss

    response = await call_next(request)

    end_time = time.time()
    cpu_times_end = process.cpu_times()
    mem_end = process.memory_info().rss

    process_time = end_time - start_time
    cpu_time_used = (cpu_times_end.user + cpu_times_end.system) - (cpu_times_start.user + cpu_times_start.system)
    cpu_usage = (cpu_time_used / process_time) * 100 if process_time > 0 else 0
    mem_usage_mb = mem_end / (1024 * 1024)
    mem_usage_diff_mb = (mem_end - mem_start) / (1024 * 1024)

    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    response.headers["X-CPU-Usage"] = f"{cpu_usage:.2f}%"
    response.headers["X-Memory-Usage"] = f"{mem_usage_mb:.2f} MB"
    response.headers["X-Memory-Usage-Diff"] = f"{mem_usage_diff_mb:.2f} MB"

    return response

# Endpoint: /predict
@app.post("/predict")
def predict_future(stock_data: StockData):
    if len(stock_data.historical_prices) < WINDOW_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"É necessário no mínimo {WINDOW_SIZE} preços históricos para a previsão."
        )
    
    # Se forem fornecidos mais que 60, pega só os últimos 60
    input_prices = stock_data.historical_prices[-WINDOW_SIZE:]
    
    # Converte para NumPy e aplica normalização
    data_array = np.array(input_prices).reshape(-1, 1)
    scaled_data = scaler.transform(data_array)
    
    # Formata para (1, 60, 1)
    X_input = scaled_data.reshape(1, WINDOW_SIZE, 1)
    
    # Realiza a predição (espera-se shape (1, 10))
    prediction_scaled = model.predict(X_input)  # shape: (1, 10)

    # Ajusta para (10, 1) para aplicar inverse_transform
    prediction_scaled = prediction_scaled.reshape(-1, 1)  # shape: (10, 1)

    # Reverte a normalização para obter valores reais
    prediction = scaler.inverse_transform(prediction_scaled).flatten()

    # Retorna como lista
    predicted_prices = prediction.tolist()

    return {"predicted_prices": predicted_prices}

# Execução local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

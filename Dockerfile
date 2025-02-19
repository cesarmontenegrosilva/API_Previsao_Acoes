# Usamos uma imagem base oficial do Python (ajuste a versão se necessário)
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos para o container e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do código para o container
COPY . .

# Expõe a porta que a aplicação utilizará (o Cloud Run utiliza 8080 por padrão)
EXPOSE 8080

# Comando para iniciar a aplicação usando Uvicorn (caso sua aplicação seja FastAPI e esteja em api.py)
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]

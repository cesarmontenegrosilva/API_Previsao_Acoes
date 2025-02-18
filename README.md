# API de Previsão de Ações com LSTM

Este projeto fornece uma API baseada em FastAPI que carrega um modelo LSTM treinado para prever o preço de ações (PETR3.sa) para 10 dias à frente. A API expõe um endpoint "/predict" que recebe pelo menos 60 preços históricos e retorna 10 valores de previsão em uma única chamada.

## Descrição

- Script Principal: api.py
- Funcionalidades:
  - Carrega o modelo LSTM treinado (lstm_model_petr3.h5) que espera uma entrada no formato (1, 60, 1) e retorna uma previsão com formato (1, 10).
  - Carrega um objeto "scaler" (armazenado em scaler.pkl) para normalização dos dados.
  - Expõe o endpoint /predict para receber uma lista de preços históricos (mínimo 60 valores) e retornar uma previsão multi-step (10 valores).
  - Inclui um middleware para monitoramento de tempo de execução, uso de CPU e memória em cada requisição.

## Pré-requisitos

- Python 3.8+
- FastAPI (https://fastapi.tiangolo.com/)
- TensorFlow (https://www.tensorflow.org/)
- Uvicorn (https://www.uvicorn.org/)
- Pydantic (https://pydantic-docs.helpmanual.io/)
- psutil (https://psutil.readthedocs.io/)
- NumPy (https://numpy.org/)
- (Opcional) scikit-learn, se o scaler foi criado com ele

## Instalação

1. Clone o repositório:

   git clone <URL_DO_REPOSITÓRIO>
   cd <NOME_DO_REPOSITÓRIO>

2. Crie e ative um ambiente virtual (opcional, mas recomendado):

   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows

3. Instale as dependências:

   pip install fastapi uvicorn tensorflow psutil numpy pydantic

   Se necessário, instale também o scikit-learn:

   pip install scikit-learn

## Arquivos Necessários

- api.py: Script principal da API.
- lstm_model_petr3.h5: Modelo LSTM treinado (deve estar na mesma pasta do api.py).
- scaler.pkl: Objeto de normalização (pickle) utilizado para transformar os dados.

## Como Executar

Para rodar a API localmente, utilize o comando:

   uvicorn api:app --reload

Após iniciar, acesse a documentação interativa da API em:
http://127.0.0.1:8000/docs

## Uso

### Endpoint /predict

- Método: POST
- Payload: Um JSON com a chave "historical_prices", que deve conter uma lista com pelo menos 60 valores (números reais) representando os preços históricos.

Exemplo de Requisição:

{
  "historical_prices": [23.45, 23.50, 23.55, ..., 24.10]
}

Exemplo de Resposta:

{
  "predicted_prices": [24.20, 24.30, 24.25, 24.15, 24.10, 24.05, 24.00, 23.95, 23.90, 23.85]
}

## Monitoramento

O middleware da API adiciona os seguintes headers nas respostas HTTP:

- X-Process-Time: Tempo total de processamento da requisição.
- X-CPU-Usage: Percentual de uso da CPU durante a requisição.
- X-Memory-Usage: Uso de memória (em MB) ao final da requisição.
- X-Memory-Usage-Diff: Diferença no uso de memória (em MB) durante a requisição.

## Troubleshooting

- Erro ao carregar o modelo ou scaler: Verifique se os arquivos "lstm_model_petr3.h5" e "scaler.pkl" estão no mesmo diretório que "api.py" e se os nomes estão corretos.
- Formato dos dados: Certifique-se de enviar pelo menos 60 preços históricos no endpoint /predict.

## Contato

Caso tenha dúvidas ou sugestões, sinta-se à vontade para abrir uma issue ou entrar em contato.

## Licença

Este projeto está licenciado sob [Nome da Licença] - veja o arquivo LICENSE para mais detalhes.

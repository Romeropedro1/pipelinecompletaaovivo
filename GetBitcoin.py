import requests
from datetime import datetime
import pandas as pd

def get_bitcoin_df():
    # URL para obter o preço do Bitcoin
    url = "https://api.coinbase.com/v2/prices/spot"

    # Requisição GET para API
    response = requests.get(url)

    # Converte resposta em dicionário
    data = response.json()

    # Extrair os dados
    preco = float(data['data']['amount'])
    ativo = data['data']['base']
    moeda = data['data']['currency']
    horario_coleta = datetime.now()

    # Criar DataFrame
    df = pd.DataFrame([{
        'ativo': ativo,
        'preco': preco,
        'moeda': moeda,
        'horario_coleta': horario_coleta
    }])

    return df


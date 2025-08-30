import pandas as pd
import time
from  GetBitcoin import get_bitcoin_df
from GetCommodities import get_commodities_df

valor_bitcoin = print(get_bitcoin_df())
valor_commodities = get_commodities_df()

print(valor_bitcoin)
print(valor_commodities)

while True: # loop infinito

    df = pd.concat([valor_bitcoin, valor_commodities], ignore_index=True)
    print(df)

    time.sleep(60) # espera 60 segundos antes de coletar novamente
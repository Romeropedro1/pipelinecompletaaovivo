import time
import pandas as pd
from sqlalchemy import create_engine
from GetBitcoin import get_bitcoin_df
from GetCommodities import get_commodities_df
from dotenv import load_dotenv
import os

# Carregar variáveis do .env
load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "meubanco")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

SLEEP_SECONDS = 60

def coletar_e_inserir():
    try:
        df_btc = get_bitcoin_df()
        df_comm = get_commodities_df()

        df = pd.concat([df_btc, df_comm], ignore_index=True)

        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).apply(
                lambda x: x.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
            )

        df.to_sql("cotacoes", engine, if_exists="append", index=False)
        print("✅ Cotações inseridas no banco com sucesso!")

    except Exception as e:
        print("❌ Erro ao inserir dados:", e)

if __name__ == "__main__":
    while True:
        coletar_e_inserir()
        time.sleep(SLEEP_SECONDS)


---

# Pipeline de Cotações – Bitcoin & Commodities

> Projeto Python que coleta cotações de **Bitcoin e commodities** periodicamente, salva em **PostgreSQL** e em **CSV**, pronto para análises e integração com outros sistemas.

---

## 🔧 Tecnologias

* Python 3.11+
* Pandas
* SQLAlchemy
* PostgreSQL
* dotenv (`python-dotenv`)
* yfinance (para commodities)

---

## 📁 Estrutura do Projeto

```
pipelinecompletaaovivo/
├── GetBitcoin.py              # Função get_bitcoin_df()
├── GetCommodities.py          # Função get_commodities_df()
├── main.py                    # Loop para inserir dados no PostgreSQL
├── GetPrices_loop_save.py     # Loop para salvar dados em CSV
├── requirements.txt           # Dependências Python
├── .env                       # Configurações do banco
└── README.md                  # Este arquivo
```

---

## ⚙️ Variáveis de Ambiente

Arquivo `.env` (não subir no GitHub):

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=meubanco
```

---

## ▶️ Como Executar

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Para salvar dados no **PostgreSQL** (loop infinito a cada 60s):

```bash
python Getprices_loop_db.py

```

3. Para salvar apenas em **CSV** (loop infinito a cada 60s):

```bash
python Getprices_csv.py

```

> ⚠️ Ambos os scripts rodam indefinidamente e coletam dados a cada 60 segundos.

---

## 🐍 Observações

* A tabela `cotacoes` será criada no PostgreSQL automaticamente ao inserir os dados.
* As cotações de commodities usam `yfinance`.
* Certifique-se de que o PostgreSQL está rodando e acessível pelo `.env`.
* No CSV, se não existir, ele será criado com cabeçalho automaticamente.

---

## 💡 Sugestões Futuras

* Adicionar logging para monitorar falhas de coleta.
* Implementar Docker para rodar o pipeline em contêiner.
* Integrar com n8n ou outras ferramentas de automação.

---


# AI Spreadsheet Analyst

Dashboard para explorar CSVs com métricas, gráficos e resumo opcional por IA.

## Executar
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Envie um CSV. O app mostra dimensões, dados ausentes, estatísticas e gráficos automáticos. Para um resumo em linguagem natural, configure `OPENAI_API_KEY` em `.env` usando `.env.example` como modelo.

## CSV de exemplo
O arquivo `data/vendas.csv` contém dados fictícios e pode ser usado para testar.

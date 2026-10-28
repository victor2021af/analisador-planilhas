import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="AI Spreadsheet Analyst", layout="wide")
st.title("AI Spreadsheet Analyst")
st.write("Envie um CSV para explorar os dados e gerar um resumo.")

uploaded = st.file_uploader("Arquivo CSV", type=["csv"])
if uploaded:
    try:
        df = pd.read_csv(uploaded)
    except Exception as exc:
        st.error(f"Não foi possível ler o CSV: {exc}")
        st.stop()
    if df.empty:
        st.warning("O arquivo está vazio.")
        st.stop()
    c1, c2, c3 = st.columns(3)
    c1.metric("Linhas", f"{len(df):,}")
    c2.metric("Colunas", len(df.columns))
    c3.metric("Células vazias", int(df.isna().sum().sum()))
    st.subheader("Prévia")
    st.dataframe(df.head(100), use_container_width=True)
    st.subheader("Resumo estatístico")
    st.dataframe(df.describe(include="all").transpose(), use_container_width=True)
    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        st.subheader("Distribuição das colunas numéricas")
        col = st.selectbox("Escolha uma coluna", list(numeric.columns))
        st.bar_chart(df[col].dropna().value_counts().sort_index().head(50))
    st.subheader("Qualidade dos dados")
    missing = df.isna().sum().rename("valores_ausentes").to_frame()
    missing["percentual_ausente"] = (missing["valores_ausentes"] / len(df) * 100).round(2)
    st.dataframe(missing, use_container_width=True)
    if st.button("Gerar resumo com IA"):
        if not os.getenv("OPENAI_API_KEY"):
            st.warning("Configure OPENAI_API_KEY no arquivo .env para usar o resumo generativo.")
        else:
            try:
                from openai import OpenAI
                summary = df.head(30).to_csv(index=False)
                stats = df.describe(include="all").to_string()
                client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                result = client.chat.completions.create(
                    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                    messages=[
                        {"role": "system", "content": "Você é um analista de dados. Responda em português, diferencie fatos de hipóteses e não invente conclusões."},
                        {"role": "user", "content": f"Analise esta amostra de dados e estatísticas. Aponte tendências possíveis, limitações e perguntas úteis.\nAmostra CSV:\n{summary}\nEstatísticas:\n{stats}"}
                    ],
                    temperature=0.2,
                )
                st.subheader("Resumo gerado")
                st.write(result.choices[0].message.content)
            except Exception as exc:
                st.error(f"Erro ao gerar resumo: {exc}")
else:
    st.info("Dica: teste com data/vendas.csv.")

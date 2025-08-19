
# 💰 Dashboard Financeiro

Dashboard interativo para análise de transações financeiras usando **Streamlit** e **PostgreSQL**.  
Permite importar, filtrar e visualizar dados com métricas e gráficos.

---

## 🚀 Rodar com Docker

```bash
docker-compose up --build
````

O app sobe em: [http://localhost:8501](http://localhost:8501)

⚡ Isso já sobe também um **PostgreSQL** configurado via `docker-compose`.

---

## 🖥️ Rodar localmente (sem Docker)

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

pip install -r requirements.txt
streamlit run main/main.py
```

---

## 📊 Funcionalidades

* Filtro por **contas** e **período** (Mensal, Semanal, Diário)
* Indicadores de:

  * Saldo líquido
  * Total de créditos e débitos
  * Crescimento percentual
* Gráficos:

  * Linha de evolução do saldo
  * Pizza comparativa Crédito vs Débito
* Tabelas detalhadas por período
* Opção de **excluir registros por mês**

---

## 🛠 Tecnologias

* [Python](https://www.python.org/)
* [Streamlit](https://streamlit.io/)
* [Pandas](https://pandas.pydata.org/)
* [Altair](https://altair-viz.github.io/) e [Plotly](https://plotly.com/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [PostgreSQL](https://www.postgresql.org/)
* [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

---


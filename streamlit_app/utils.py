import os

import pandas as pd
import psycopg2
import streamlit as st


def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname='elt_meltano',
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host='172.19.0.20',
            port='5432',
        )
        return conn
    except Exception as e:
        st.error(f'Erro ao conectar ao banco de dados: {e}')
        return None


def run_query(query, conn):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        return pd.DataFrame(result, columns=columns)
    except Exception as e:
        st.error(f'Erro ao executar a query: {e}')
        return None

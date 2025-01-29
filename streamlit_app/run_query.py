import streamlit as st
from utils import connect_to_db
from utils import run_query


def run_custom_query():
    placeholder_query = """
        SELECT o.order_id, o.customer_id, o.order_date, o.ship_city, o.ship_country,
               od.product_id, od.unit_price, od.quantity, od.discount
        FROM analytics.orders o
        JOIN analytics.order_details od
            ON o.order_id = od.order_id::numeric
    """
    query = st.text_area('Digite sua query SQL aqui:', value=placeholder_query)

    if st.button('Executar Query'):
        conn = connect_to_db()
        if conn:
            df = run_query(query, conn)
            if df is not None:
                st.success('Query executada com sucesso!')
                st.write('Resultados:')
                st.dataframe(df)  # Exibe os resultados em uma tabela
            conn.close()

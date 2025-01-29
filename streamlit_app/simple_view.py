import streamlit as st
from utils import connect_to_db
from utils import run_query


def simple_report():
    conn = connect_to_db()

    def load_data():
        query = """
        SELECT o.order_id, o.customer_id, o.order_date, o.ship_city, o.ship_country,
               od.product_id, od.unit_price, od.quantity, od.discount
        FROM analytics.orders o
        JOIN analytics.order_details od
            ON o.order_id = od.order_id::numeric
        """
        df_query = run_query(query, conn)
        return df_query

    st.title('Overview dos Pedidos')

    df = load_data()

    st.write('### Join das tabelas *Orders* e *Order Details*')
    st.dataframe(df)
    df = df.astype(
        {
            'product_id': 'int16',
            'quantity': 'int16',
            'unit_price': 'float16',
            'discount': 'float16',
        },
    )

    st.write('### Estatísticas Básicas')
    st.write(f"Número total de pedidos: {df['order_id'].nunique()}")
    st.write(f"Número total de produtos vendidos: {df['product_id'].nunique()}")
    st.write(f"Produto mais vendido: {df.groupby('product_id')['quantity'].sum().idxmax()}")
    st.write(f"Cliente que mais comprou: {df.groupby('customer_id')['quantity'].sum().idxmax()}")
    st.write(f"Receita total: ${df['unit_price'].mul(df['quantity']).mul(1 - df['discount']).sum():.2f}")

    st.write('### Pedidos por País')
    orders_by_country = df.groupby('ship_country')['order_id'].nunique().reset_index()
    st.bar_chart(data=orders_by_country.set_index('ship_country'), x_label='País', y_label='Número de Pedidos')

    st.write('### Pedidos por Cliente')
    orders_by_country = df.groupby('customer_id')['order_id'].nunique().reset_index()
    st.bar_chart(data=orders_by_country.set_index('customer_id'), x_label='Cliente', y_label='Número de Pedidos')

    st.write('### Produtos mais Vendidos')
    products_sold = df.groupby('product_id')['quantity'].sum().reset_index()
    st.bar_chart(data=products_sold.set_index('product_id'), x_label='Produto', y_label='Número de Pedidos')

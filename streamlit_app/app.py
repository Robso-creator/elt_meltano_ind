import streamlit as st
from run_query import run_custom_query
from simple_view import simple_report

st.set_page_config(
    page_title='Streamlit-App',
    layout='centered',
    initial_sidebar_state='expanded',
)

st.title('Streamlit APP')
st.sidebar.markdown('Feito para visualização de dados do resultado das pipelines de dados')

PAGES = {
    'Report de pedidos': simple_report,
    'Executar queries personalizadas': run_custom_query,
}

selection = st.sidebar.selectbox('Escolha a página', list(PAGES.keys()))
page = PAGES[selection]
page()

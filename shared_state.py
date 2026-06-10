import streamlit as st
from datetime import datetime


@st.cache_resource
def get_shared_state():
    return {
        'fila_global': [],
        'numeros_usados': set(),
        'ultimo_avanco_fila': datetime.now(),
        'atendidos_hoje': [],
    }

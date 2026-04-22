#%%

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import requests
from datetime import datetime, timedelta


# 1. Configuração:

st.set_page_config(
    page_title="Torre de Controle Logístico", 
    layout="wide", 
    page_icon="📦"
)

st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.8rem; color: #1f77b4; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def carregar_e_preparar_dados():
    """
    Carrega a base e faz a 'limpeza de casa'. 
    Usa cache para não carregar o arquivo toda vez que você clicar em algo.
    """
    try:
        try:
            df = pd.read_csv("supply_chain_data.csv")
        except FileNotFoundError:
            df = pd.read_csv("archive/supply_chain_data.csv")
    except Exception as e:
        st.error(f"⚠️ Ops! Não encontrei a base de dados: {e}")
        st.stop()

    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df = df.rename(columns={
        'lead_times': 'tempo_entrega_cliente_dias',
        'lead_time': 'tempo_entrega_fornecedor_dias',
        'manufacturing_lead_time': 'tempo_fabricacao_dias'
    })

    # KPIs:
    df['lucro_liquido'] = df['revenue_generated'] - (df['manufacturing_costs'] + df['shipping_costs'])
    df['alerta_qualidade'] = df['defect_rates'].apply(lambda x: 'Risco Alto' if x > 5 else 'Normal')
    
    colunas_fin = ['price', 'revenue_generated', 'shipping_costs', 'manufacturing_costs', 'costs', 'lucro_liquido']
    df[colunas_fin] = df[colunas_fin].round(2)

    np.random.seed(42)
    hoje = datetime(2026, 4, 20) 
    df['data_pedido'] = [hoje - timedelta(days=np.random.randint(0, 180)) for _ in range(len(df))]
    df['data_entrega'] = df.apply(lambda row: row['data_pedido'] + timedelta(days=row['shipping_times']), axis=1)

    return df

with st.spinner("Sincronizando Torre de Controle..."):
    df = carregar_e_preparar_dados()


# 2. Barra lateral:

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2311/2311523.png", width=80)
    st.title("Estratégia de Filtros")
    
    st.subheader("⚙️ Refinar Visão")
    fornecedores = st.multiselect(
        "Fornecedores Específicos", 
        df['supplier_name'].unique(), 
        default=df['supplier_name'].unique()
    )
    modais = st.multiselect(
        "Modais de Transporte", 
        df['transportation_modes'].unique(), 
        default=df['transportation_modes'].unique()
    )
    
    st.divider()
    st.info("💡 **Dica do Analista:** Use os filtros para isolar problemas de frete ou defeitos por modal.")

# Aplicação dos filtros
df_filtrado = df[
    (df['supplier_name'].isin(fornecedores)) & 
    (df['transportation_modes'].isin(modais))
]

# 3. Painel de indicadores:

st.title("📦 Torre de Controle Logístico")
st.caption("Visibilidade de Ponta a Ponta · Inteligência Prescritiva · Decisões em Tempo Real")

m1, m2, m3, m4 = st.columns(4)
m1.metric("💰 Receita Total", f"$ {df_filtrado['revenue_generated'].sum():,.2f}")
m2.metric("📈 Lucro Líquido", f"$ {df_filtrado['lucro_liquido'].sum():,.2f}")
m3.metric("⚠️ Média de Defeitos", f"{df_filtrado['defect_rates'].mean():.2f}%")
m4.metric("🚨 Alertas Críticos", df_filtrado[df_filtrado['alerta_qualidade'] == 'Risco Alto'].shape[0])

st.divider()


# 4. Análises visuais:

col_esq, col_dir = st.columns(2)

with col_esq:
    st.subheader("⚠️ Risco por Fornecedor")
    fig_bar = px.bar(
        df_filtrado, x='supplier_name', y='defect_rates', color='alerta_qualidade',
        color_discrete_map={'Normal': '#1f77b4', 'Risco Alto': '#EF553B'},
        title="Impacto de Qualidade no Estoque",
        labels={'supplier_name': 'Fornecedor', 'defect_rates': 'Taxa de Defeito (%)'}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_dir:
    st.subheader("⚖️ Eficiência: Custo vs. Tempo")
    fig_scatter = px.scatter(
        df_filtrado, x='shipping_costs', y='tempo_entrega_cliente_dias',
        color='transportation_modes', size='revenue_generated',
        hover_name='sku', title="Correlação Custo de Frete x Lead Time",
        labels={'shipping_costs': 'Custo de Envio ($)', 'tempo_entrega_cliente_dias': 'Dias para Entrega'}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with st.expander("🔍 Explorar Auditoria Detalhada de Dados"):
    st.dataframe(
        df_filtrado[['sku', 'supplier_name', 'data_pedido', 'lucro_liquido', 'alerta_qualidade']], 
        use_container_width=True
    )

# 5. IA:

st.divider()
st.subheader("🤖 Assistente de Inteligência Prescritiva")

if not df_filtrado.empty:
    pior = df_filtrado.loc[df_filtrado['defect_rates'].idxmax()]
    st.warning(f"O sistema isolou o fornecedor **{pior['supplier_name']}** com a maior taxa de defeito operacional ({pior['defect_rates']:.2f}%).")

    if st.button("Gerar Recomendações Estratégicas"):
        with st.spinner("Llama 3 redigindo plano de ação..."):
            prompt = (f"Diretor, o fornecedor {pior['supplier_name']} de {pior['location']} "
                      f"tem {pior['defect_rates']}% de defeito em {pior['product_type']}. "
                      f"O lucro é de ${pior['lucro_liquido']}. Dê 2 recomendações curtas em Português.")
            
            try:
                r = requests.post("http://localhost:11434/api/generate", 
                                  json={"model": "llama3", "prompt": prompt, "stream": False}, timeout=30)
                st.info(r.json().get("response", "Erro na resposta."))
            except:
                st.error("Erro: Verifique se o Ollama está rodando o Llama 3 localmente.")

with st.sidebar:
    st.divider()
    st.subheader("💬 Chat com Especialista")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "ai", "content": "Olá João! Sou seu analista virtual. O que deseja descobrir nos dados?"}]

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if query := st.chat_input("Pergunte sobre fretes ou lucros..."):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"): st.markdown(query)

        with st.chat_message("ai"):
            with st.spinner("Analisando base..."):
                contexto = f"Lucro Total: {df_filtrado['lucro_liquido'].sum()}. Pior fornecedor: {pior['supplier_name']}."
                full_prompt = f"Dados: {contexto}. Pergunta: {query}. Responda curto e profissional em Português."
                try:
                    r = requests.post("http://localhost:11434/api/generate", 
                                      json={"model": "llama3", "prompt": full_prompt, "stream": False}, timeout=30)
                    ans = r.json().get("response", "Sem resposta.")
                    st.markdown(ans)
                    st.session_state.messages.append({"role": "ai", "content": ans})
                except:
                    st.markdown("⚠️ O assistente está offline. Verifique o Ollama.")

st.divider()
st.caption("© 2026 · Torre de Controle Logística · Desenvolvido por João Carlos Escaliante")
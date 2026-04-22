# 📦 Supply Chain AI Control Tower

Este projeto é uma **Torre de Controle Logística Inteligente** desenvolvida em Python. Ela integra análise de dados clássica (Pandas) com Inteligência Artificial Generativa (Llama 3 via Ollama) para fornecer diagnósticos automáticos sobre a cadeia de suprimentos.

🛡️ Privacidade e Governança de Dados (O Diferencial)
O grande diferencial técnico deste projeto é a utilização de IA Generativa Local (Ollama/Llama 3). Em um cenário corporativo real, a segurança da informação é prioridade. Ao processar dados sensíveis de margem de lucro e performance de fornecedores sem que eles saiam da infraestrutura interna, eliminamos o risco de vazamento de dados estratégicos em nuvens públicas.

## 🚀 Funcionalidades Chave

* **Dashboards Interativos**: Visualização em tempo real de Lucro Líquido, Receita e Performance por Modal.
* **Análise de Eficiência (Scatter Plot)**: Identificação visual de gargalos cruzando Custo de Frete vs. Lead Time.
* **Auditoria Prescritiva**: Botão dedicado que utiliza o Llama 3 para analisar o pior fornecedor e gerar um plano de ação executivo.
* **Assistente Conversacional (RAG)**: Chatbot integrado na barra lateral que permite "conversar com a planilha" para tirar dúvidas rápidas sobre a operação.


## 🛠️ Tecnologias Utilizadas

* **Python**: Core do processamento e lógica de negócio.
* **Pandas**: Engenharia de dados e cálculo de KPIs financeiros.
* **Streamlit**: Framework para criação da interface web e dashboard.
* **Plotly**: Gráficos dinâmicos e interativos.
* **Ollama/Llama 3**: Engine de Inteligência Artificial para análise de dados e chat.


## ⚙️ Como Executar o Projeto

1. **Clone o repositório:** `git clone https://github.com/JoaoEscaliante/SupplyChain-AI-ControlTower.git`
2. **Instale as dependências:** `pip install -r requirements.txt`
3. **Configure a IA Local:** Certifique-se de que o [Ollama](https://ollama.com/) está instalado e rodando o modelo Llama 3 (`ollama run llama3`).
4. **Inicie o Painel:** `streamlit run app_logistica.py`


---
## 🏁 Sobre o Autor
Desenvolvido por **João Carlos Escaliante** (Escaliante). 
Sou Analista de Sistemas formado em ADS, com foco em transformar dados complexos em decisões estratégicas, seja na logística corporativa ou na engenharia de performance automobilística.

[LinkedIn](https://www.linkedin.com/in/joaoescaliante/)

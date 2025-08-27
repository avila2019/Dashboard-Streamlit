import pandas as pd
import plotly.express as px
import streamlit as st

# Carregar CSV
df = pd.read_csv("Crianca_telefone.csv")

st.title("📊 Conjunto de dados sobre o impacto do uso de smartphones e do vício em adolescentes")

st.write("### Prévia dos Dados do Dataset")
st.dataframe(df.head())

st.write("### Distribuição do Uso de Smartphones pelas Idades")
# Histograma da Idade 
if "Age" in df.columns:
    fig1 = px.histogram(
        df,
        x="Age",
        nbins=10,
        color="Gender",  # cor por gênero
        barmode="overlay",
        #title="Distribuição do Uso de Smartphones pelas Idades"
    )
    fig1.update_layout(
        xaxis_title="Idade",
        yaxis_title="Quantidade",
        bargap=0.2,
        plot_bgcolor="white"
    )
    st.plotly_chart(fig1, use_container_width=True)    

st.write("### Uso Diário de horas no Smartphone pelo Gênero")
#  Gráfico 2: Uso de telefone por gênero
if "Gender" in df.columns and "Daily_Usage_Hours" in df.columns:
    fig2 = px.box(
        df,
        x="Gender",
        y="Daily_Usage_Hours",
        color="Gender",  # cores diferentes por gênero
        points="all",  # mostra os pontos individuais além da caixa
        #title="Uso Diário de horas no Smartphone pelo Gênero"
    )
    fig2.update_layout(
        xaxis_title="Gênero",
        yaxis_title="Horas de Uso Diário pelo Gênero",
        plot_bgcolor="white",
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

st.write("### Idade x Tempo de Uso do Telefone")
# --- Gráfico 3: Dispersão entre idade e tempo de uso do telefone ---
if "Age" in df.columns and "Daily_Usage_Hours" in df.columns:
    fig3 = px.scatter(
        df,
        x="Age",
        y="Daily_Usage_Hours",
        color="Gender" if "Gender" in df.columns else None,  # cor por gênero, se existir
        size="Daily_Usage_Hours",  # bolha proporcional ao tempo de uso
        hover_data=df.columns,  # mostra todas as colunas no hover
        #title="Idade x Tempo de Uso do Telefone",
        trendline="ols",  # adiciona linha de regressão (se statsmodels estiver instalado)
        opacity=0.7
    )
    fig3.update_layout(
        xaxis_title="Idade",
        yaxis_title="Horas de Uso Diário do Telefone",
        plot_bgcolor="white",
        legend_title="Gênero"
    )
    st.plotly_chart(fig3, use_container_width=True)    


    st.write("### Relação entre Horas de Uso Diário do Telefone e Horas de Sono")
    # Gráfico de dispersão: Horas de uso do telefone vs Horas de sono
if "Daily_Usage_Hours" in df.columns and "Daily_Usage_Hours" in df.columns:
    fig4 = px.scatter(
        df,
        x="Daily_Usage_Hours",
        y="Sleep_Hours",
        color=None,
        size="Daily_Usage_Hours",
        trendline="ols",  # Adiciona linha de tendência
        #title="Relação entre Horas de Uso Diário do Telefone e Horas de Sono",
        labels={"Daily_Usage_Hours": "Horas de Uso Diário do Telefone", "Sleep_Hours": "Horas de Sono"}
    )
    st.plotly_chart(fig4)

st.write("### Análise das crianças que utilizam Smartphones, Relação ao Nível de Ansiedade, Controle Parental,Autoestima e Nível de Depressão")
# Indicadores Psicológicos das Crianças
# Selecionando uma criança para análise individual
opcao = st.selectbox("Selecione uma criança para visualizar:", df.index)
# COLOCAR O NOME DA CRIANÇA 

# Pegar valores dessa linha
dados = df.loc[opcao, ["Anxiety_Level", "Depression_Level", "Self_Esteem", "Parental_Control"]]

# Criar DataFrame no formato longo para o radar
radar_df = pd.DataFrame({
    "Indicador": ["Nível de Ansiedade", "Nível de Depressão", "Autoestima", "Controle Parental"],
    "Valor": dados.values
})

# Gráfico radar por nivel de ansiedade , controle parental, autoestima e nível de depressão
fig4 = px.line_polar(
    radar_df,
    r="Valor",
    theta="Indicador",
    line_close=True,
    title=f"Perfil Psicológico da Criança {opcao}",
)
fig4.update_traces(fill="toself")

st.plotly_chart(fig4)    
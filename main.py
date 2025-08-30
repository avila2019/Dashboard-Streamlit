import pandas as pd
import plotly.express as px
import streamlit as st

# Carregar CSV
df = pd.read_csv("Crianca_telefone.csv")

st.title("📊 Conjunto de dados sobre o impacto do uso de smartphones e do vício em adolescentes")

st.write("### Prévia dos Dados do Dataset")
st.dataframe(df.head())

# Plot 1
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


# Plot 2
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


# Plot 3
st.write("### Relação entre Idade e Uso do Telefone")

if "Age" in df.columns and "Daily_Usage_Hours" in df.columns:
    fig3 = px.scatter(
        df,
        x="Age",
        y="Daily_Usage_Hours",
        color="Gender" if "Gender" in df.columns else None,
        size="Daily_Usage_Hours",
        hover_data=df.columns,
        
    )
    st.plotly_chart(fig3, use_container_width=True)



# Plot 4 
st.set_page_config(page_title="Análise Psicológica", layout="centered")
st.write("### Análise Psicológica dos Alunos")

# -------------------
# Seleção do Aluno
# -------------------
if "Name" in df.columns:
    aluno_sel = st.selectbox("Selecione o Aluno:", df["Name"].unique())

    # Filtrar dados do aluno escolhido
    aluno_dados = df[df["Name"] == aluno_sel].iloc[0]

    # Criar dataframe com métricas
    dados_plot = pd.DataFrame({
        "Indicador": ["Nível de Ansiedade", "Nível de Depressão", "Autoestima", "Controle Parental"],
        "Valor": [
            aluno_dados["Anxiety_Level"] if "Anxiety_Level" in df.columns else None,
            aluno_dados["Depression_Level"] if "Depression_Level" in df.columns else None,
            aluno_dados["Self_Esteem"] if "Self_Esteem" in df.columns else None,
            aluno_dados["Parental_Control"] if "Parental_Control" in df.columns else None
        ]
    })

    # -------------------
    # Gráfico Radar
    # -------------------
    fig4 = px.line_polar(
        dados_plot,
        r="Valor",
        theta="Indicador",
        line_close=True,
        title=f"Perfil Psicológico do Aluno: {aluno_sel}"
    )
    fig4.update_traces(fill="toself")
    st.plotly_chart(fig4, use_container_width=True)    



# Plot 5
    st.title("📊 Uso de Aplicativos por Aluno")

# -------------------
# Seleção do Aluno
# -------------------
if "Name" in df.columns:
    aluno_sel = st.selectbox("Selecione o Aluno:", df["Name"].unique())

    # Filtrar dados do aluno escolhido
    aluno_dados = df[df["Name"] == aluno_sel].iloc[0]

    # Criar dataframe com métricas
    dados_plot = pd.DataFrame({
        "Categoria": [
            "Aplicativos Usados Diariamente",
            "Tempo em Redes Sociais",
            "Tempo em Jogos",
            "Tempo em Educação"
        ],
        "Valor": [
            aluno_dados["Apps_Diarios"] if "Apps_Diarios" in df.columns else None,
            aluno_dados["Tempo_RedesSociais"] if "Tempo_RedesSociais" in df.columns else None,
            aluno_dados["Tempo_Jogos"] if "Tempo_Jogos" in df.columns else None,
            aluno_dados["Tempo_Educacao"] if "Tempo_Educacao" in df.columns else None
        ]
    })

    # -------------------
    # Gráfico Radar
    # -------------------
    fig = px.line_polar(
        dados_plot,
        r="Valor",
        theta="Categoria",
        line_close=True,
        title=f"Perfil de Uso de Aplicativos: {aluno_sel}"
    )
    fig.update_traces(fill="toself")
    st.plotly_chart(fig, use_container_width=True)

    # -------------------
    # Gráfico de Barras
    # -------------------
    fig2 = px.bar(
        dados_plot,
        x="Categoria",
        y="Valor",
        color="Categoria",
        text="Valor",
        title=f"Uso de Aplicativos por Categoria - {aluno_sel}"
    )
    fig2.update_layout(xaxis_title="Categoria", yaxis_title="Tempo / Quantidade")
    st.plotly_chart(fig2, use_container_width=True)



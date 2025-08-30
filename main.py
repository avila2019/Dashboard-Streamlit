import pandas as pd
import plotly.express as px
import streamlit as st

# Carregar CSV
df = pd.read_csv("Crianca_telefone.csv")

st.title("📊 Conjunto de dados sobre o impacto do uso de smartphones e do vício em adolescentes")

st.write("### Prévia dos Dados do Dataset")
st.dataframe(df.head())

# Plot 1 #################################################################################################################################
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


# Plot 2 ##########################################################################################################################
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


# Plot 3 ######################################################################################################################
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



# Plot 4 #########################################################################################################
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



# Plot 5 Com intração Humana ########################################################################################

st.set_page_config(page_title="Análise de Crianças e Telefone", layout="wide")
st.title("📊 Análise Interativa do Uso de Telefone por Crianças")

st.markdown("Este painel contém **3 elementos de interatividade** para explorar os dados.")

# ============================================================
# 1) Filtro por Gênero (Sidebar)
# ============================================================
if "Gender" in df.columns:
    genero_sel = st.sidebar.multiselect(
        "Selecione o Gênero:",
        options=df["Gender"].unique(),
        default=df["Gender"].unique()
    )
    df = df[df["Gender"].isin(genero_sel)]

# ============================================================
# 2) Seleção de Aluno pelo Nome
# ============================================================
if "Name" in df.columns:
    aluno_sel = st.selectbox("Selecione um Aluno:", df["Name"].unique())

    aluno_dados = df[df["Name"] == aluno_sel].iloc[0]

    st.subheader(f"📌 Dados do Aluno Selecionado: {aluno_sel}")
    st.write(aluno_dados)

# ============================================================
# 3) Slider de Idade
# ============================================================
if "Age" in df.columns:
    idade_min = int(df["Age"].min())
    idade_max = int(df["Age"].max())

    idade_sel = st.slider(
        "Selecione a faixa etária:",
        min_value=idade_min,
        max_value=idade_max,
        value=(idade_min, idade_max)
    )
    df = df[(df["Age"] >= idade_sel[0]) & (df["Age"] <= idade_sel[1])]

# ============================================================
# Gráficos
# ============================================================
col1, col2 = st.columns(2)

# Gráfico 1 - Idade vs Uso do Telefone
if "Age" in df.columns and "UsoTelefone" in df.columns:
    with col1:
        st.subheader("📱 Idade vs Uso do Telefone")
        fig1 = px.scatter(
            df,
            x="Age",
            y="UsoTelefone",
            color="Genero" if "Genero" in df.columns else None,
            hover_data=df.columns,
            title="Relação entre Idade e Tempo de Uso do Telefone"
        )
        st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2 - Horas de Sono
if "Sleep_Hours" in df.columns:
    with col2:
        st.subheader("😴 Distribuição das Horas de Sono")
        fig2 = px.histogram(
            df,
            x="Sleep_Hours",
            nbins=15,
            color="Gender" if "Gender" in df.columns else None,
            title="Distribuição de Horas de Sono"
        )
        st.plotly_chart(fig2, use_container_width=True)

# Gráfico 3 - Uso de Aplicativos (se colunas existirem)
if all(col in df.columns for col in ["Apps_Used_Daily","Time_on_Social_Media","Time_on_Gaming","Time_on_Education"]):
    st.subheader("📊 Perfil de Uso de Aplicativos pelo Aluno Selecionado")
    dados_apps = pd.DataFrame({
        "Categoria": ["Apps Usados Diariamente", "Redes Sociais", "Jogos", "Educação"],
        "Valor": [
            aluno_dados["Apps_Used_Daily"],
            aluno_dados["Time_on_Social_Media"],
            aluno_dados["Time_on_Gaming"],
            aluno_dados["Time_on_Education"]
        ]
    })
    fig3 = px.bar(
        dados_apps,
        x="Categoria",
        y="Valor",
        color="Categoria",
        text="Valor",
        title=f"Uso de Aplicativos - {aluno_sel}"
    )
    st.plotly_chart(fig3, use_container_width=True)

import streamlit as st
import pandas as pd


def about():
    
    if st.session_state.layout != "centered":
        st.session_state.layout = "centered"
        st.experimental_rerun()

    st.markdown("""---""")
    col1, col2, col3 = st.columns([15,1,1])
    with col1:
        st.markdown("Abraão Andrade — 28 Dez 2022 — 1 min leitura")
    with col2:
        st.markdown("[![Title](https://img.icons8.com/ios-glyphs/30/null/github.png)](https://github.com/AbraaoAndrade/bird_tracking_analysis)")
    with col3:
        st.markdown("[![Title](https://img.icons8.com/ios-glyphs/30/null/linkedin-circled--v1.png)](https://linkedin.com/in/abraão-andrade-3632031b0)")
    
    st.markdown("## Contextualização")
    st.markdown("""
    Essa ferramenta é parte do processamento de dados de um Doutorado desenvolvido no Instituto do Cérebro - UFRN. Não existe \
    melhor forma de contextualizar o projeto, senão a partir do vídeo abaixo:
    """)
    st.video('https://www.youtube.com/watch?v=eM_Fcy8uFNU')
    st.markdown("""
    Esse trabalho me proporcionou o Prêmio de Trabalho Destaque de Iniciação Científica de 2020 e o recorte tratado nesse artigo \
    faz parte do esforço de interpretar os resultados de um experimento de rastreio dessas aves, cujo objetivo, dentre eles, era \
    avaliar a presença de comportamentos esteriotipados, característica comum nos Transtornos do Espectro Autista.
    """)

    st.markdown("## Projeto")
    st.markdown("""
    Para realizar o rastreio desses animais foi utilizado um algoritmo de deleção de plano de fundo, que rodou ao vivo durante \
    5 dias de experimentação com cada animal. Os dados resultantes desse processamento são arquivos CSV de 17 minutos com \
    valores de coordenadas e tempo:
    """)
    st.dataframe(pd.read_csv("https://raw.githubusercontent.com/AbraaoAndrade/bird_tracking_analysis/main/data/Or328_28-Sep-2019%2002_21_51.csv", names=['Taxa de Atualização (s)','Coordenada X (px)','Coordenada Y (px)','X','Hora','Minuto','Segundo']).head(), height=200)
    st.markdown("""
    O longo período de experimentação trouxe a necessidade de um algoritmo de rastreio mais simples e, consequentemente, \
    algumas deficiências. Portanto, para resolver os ruídos da aquisição, desenvolvemos uma interface de pre processamento e \
    limpeza dos dados:
    """)
    st.video("images/preprocess.mp4")
    c1, c2, c3 = st.columns(3)

    # with c3:
    st.image("https://raw.githubusercontent.com/AbraaoAndrade/bird_tracking_analysis/main/images/tracking_process.png", )
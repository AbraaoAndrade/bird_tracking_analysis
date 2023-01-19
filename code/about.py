import streamlit as st
import pandas as pd


def about():
    
    if st.session_state.layout != "centered":
        st.session_state.layout = "centered"
        st.experimental_rerun()

    st.markdown("""---""")
    col1, col2, col3 = st.columns([15,1,1])
    with col1:
        st.markdown("Abraão Andrade — 18 Jan 2023 — 2 min leitura")
    with col2:
        st.markdown("[![Title](https://img.icons8.com/ios-glyphs/30/null/github.png)](https://github.com/AbraaoAndrade/bird_tracking_analysis)")
    with col3:
        st.markdown("[![Title](https://img.icons8.com/ios-glyphs/30/null/linkedin-circled--v1.png)](https://linkedin.com/in/abraão-andrade-3632031b0)")
    

    st.markdown("""
    <style>
    .text-font {
        font-size:19px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    markdown_template = '<p class="text-font">{}</p>'

    st.warning('Prêmio de Trabalho Destaque de Iniciação Científica 2020', icon="🏆")

    st.markdown("## Contextualização")
    st.markdown(markdown_template.format("""
    Essa ferramenta é parte do processamento de dados de um Doutorado desenvolvido no Laboratório de Neurogenética do Instituto do Cérebro - UFRN. Não existe melhor forma de contextualizar o projeto, senão a partir do vídeo abaixo:
    """), unsafe_allow_html=True)
    st.video('https://www.youtube.com/watch?v=eM_Fcy8uFNU')
    st.markdown(markdown_template.format("""
    Esse trabalho me proporcionou o Prêmio de Trabalho Destaque de Iniciação Científica de 2020 e o recorte tratado nesse artigo faz parte do esforço de interpretar os resultados de um experimento de rastreio dessas aves, cujo objetivo, dentre eles, era avaliar a presença de comportamentos estereotipados, característica comum nos Transtornos do Espectro Autista.
    """), unsafe_allow_html=True)

    st.markdown("## Projeto")
    _, c2, _= st.columns([0.25, 0.5, 0.25])
    with c2:
        st.image("https://raw.githubusercontent.com/AbraaoAndrade/bird_tracking_analysis/main/images/tracking_process.png")

    st.markdown(markdown_template.format("""
    Para realizar o rastreio desses animais foi utilizado um algoritmo de deleção de plano de fundo, que processava as informações de vídeo em tempo real durante 5 dias de experimentação com cada animal. Os dados resultantes desse processamento são centenas de arquivos CSV com valores de coordenadas e tempo:
    """), unsafe_allow_html=True)
    st.dataframe(pd.read_csv("https://raw.githubusercontent.com/AbraaoAndrade/bird_tracking_analysis/main/data/Or328_28-Sep-2019%2002_21_51.csv", names=['Taxa de Atualização (s)','Coordenada X (px)','Coordenada Y (px)','X','Hora','Minuto','Segundo']).head(), height=200)
    st.markdown(markdown_template.format("""
    O longo período de experimentação foi o que pautou a necessidade de um algoritmo de rastreio mais simples e, em contrapartida, tivemos que lidar com algumas deficiências do método. Dentre elas, inúmeros bugs de preenchimento de valores, perda do animal no rastreio, rastreio de artefatos, e todo esse tratamento foi realizado pós experimentação. Em meio a esse processo, para resolver os ruídos da aquisição  causados por artefatos, como acúmulo de ração, desenvolvemos uma interface para realizar essa limpeza manualmente:
    """), unsafe_allow_html=True)
    st.info('Todas as etapas de limpeza dos dados estão presentes no link a seguir: [link](https://github.com/AbraaoAndrade/bird_tracking_analysis/blob/main/preprocess_and_distance.ipynb)', icon="ℹ️")
    st.video("images/preprocess.mp4")
    st.markdown(markdown_template.format("""
    Finalmente, com os dados limpos podemos partir para as visualizações …
    """), unsafe_allow_html=True)

    st.markdown("#### Quantificação da distância Percorrida ")

    st.image("https://raw.githubusercontent.com/AbraaoAndrade/bird_tracking_analysis/main/images/distancia.png")

    st.markdown("#### Mapa de calor ")
    st.image("https://raw.githubusercontent.com/AbraaoAndrade/bird_tracking_analysis/main/images/heatmap.jpg")
    st.markdown(markdown_template.format("""
    O mapa de calor é uma ferramenta de visualização espacial perfeita para representação de um perfil posicional do animal durante a experimentação. O animal apresentado acima, por exemplo, demonstrou uma preferência pelo poleiro esquerdo.
    """), unsafe_allow_html=True)

    st.markdown(markdown_template.format("""
    As conclusões tiradas desses dados deverão passar por validações estatísticas, mas essas análises ficarão reservadas para as futuras publicações do laboratório.
    """), unsafe_allow_html=True)

    st.markdown("""---""")

    st.markdown("## Contato")
    with st.form("email_form", clear_on_submit=False):
        fullname = st.text_input(label="Nome Completo", placeholder="Digite seu nome completo")
        email = st.text_input(label="Email", placeholder="Digite seu email")
        text = st.text_area(label="Texto", placeholder="Digite sua mensagem aqui")

        submitted = st.form_submit_button("Enviar")

    if submitted:
        extra_info = """
        ---------------------------------------------------------------------------- \n
         Email Address of Sender: {} 
         Sender Full Name: {} \n
        ---------------------------------------------------------------------------- \n \n
        """.format(email, fullname)

        message = extra_info + text

        send_email(sender=st.secrets["EMAIL_USER"], password=st.secrets["EMAIL_KEY"],
                   receiver=st.secrets["EMAIL_USER"], smtp_server="smtp.gmail.com", smtp_port=587,
                   email_message=message, subject="Tracking Analysis App")
    
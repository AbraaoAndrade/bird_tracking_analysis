# Bird Tracking Analysis

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://abraaoandrade-bird-tracking-analysis-heatmap-app-f90ep5.streamlit.app)

## Contextualização

Essa ferramenta é parte do processamento de dados de um Doutorado desenvolvido no Laboratório de Neurogenética do Instituto do Cérebro - UFRN. Não existe melhor forma de contextualizar o projeto, senão a partir do vídeo abaixo:
    
[![IMAGE ALT TEXT](http://img.youtube.com/vi/eM_Fcy8uFNU/0.jpg)](http://www.youtube.com/watch?v=eM_Fcy8uFNU "Video Title")

Esse trabalho me proporcionou o Prêmio de Trabalho Destaque de Iniciação Científica de 2020 e o recorte tratado nesse artigo faz parte do esforço de interpretar os resultados de um experimento de rastreio dessas aves, cujo objetivo, dentre eles, era avaliar a presença de comportamentos esteriotipados, característica comum nos Transtornos do Espectro Autista.
    
## Projeto

![alt text](https://raw.githubusercontent.com/AbraaoAndrade/bird_tracking_analysis/main/images/tracking_process.png)

Para realizar o rastreio desses animais foi utilizado um algoritmo de deleção de plano de fundo, que processava as informações de vídeo ao vivo durante 5 dias de experimentação com cada animal. Os dados resultantes desse processamento são centenas de arquivos CSV com valores de coordenadas e tempo:

O longo período de experimentação foi o que pautou a necessidade de um algoritmo de rastreio mais simples e, em contrapartida, tivemos que lidar com algumas deficiências do método. Dentre elas, inúmeros bugs de preenchimento de valores, perda do animal no rastreio, rastreio de artefatos, e todo esse tratamento foi realizado pós experimentação. Em meio a esse processo, para resolver os ruídos da aquisição  causados por artefatos, como acúmulo de ração, desenvolvemos uma interface para realizar essa limpeza manualmente:
    
Finalmente, com os dados limpos podemos partir para as visualizações …

#### Quantificação da distância Percorrida

![alt text](https://raw.githubusercontent.com/AbraaoAndrade/bird_tracking_analysis/main/images/distancia.png)

#### Mapa de calor 

![alt text](https://raw.githubusercontent.com/AbraaoAndrade/bird_tracking_analysis/main/images/heatmap.jpg)

O mapa de calor é uma ferramenta de visualização espacial perfeita para representação de um perfil posicional do animal durante a experimentação. O animal apresentado acima, por exemplo, demonstrou uma preferência pelo poleiro esquerdo.
    
É claro que as conclusões tiradas desses dados deverão passar por validações estatísticas, mas essas análises deixarei reservadas para as futuras publicações do laboratório.
    
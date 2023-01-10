import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import  pickle

def app():
    
    if st.session_state.layout != "wide":
        st.session_state.layout = "wide"
        st.experimental_rerun()

    st.session_state.checkbox_status = st.checkbox("Data Already Processed")

    if not st.session_state.checkbox_status:
        # 1. interface ------------------------------------------------------------------------------------------------
        st.session_state.tracking_analysis_env.path = st.text_input("File Path") # D:\IC\VPA\Arquivos de Registro\Tracking\Sozinho\controle\Or328

        st.session_state.tracking_analysis_env.progress_bar = st.progress(0)

        c1, c2, c3, c4, c5 = st.columns([2.4, 2.3, 1.3, 4, 16])

        if st.session_state.tracking_analysis_env.path != None:
            with c1:
                button_submit = st.button("Submit Files")
        
        if st.session_state.tracking_analysis_env.list_filenames != None:
            with c2:
                button_get_light = st.button("Check Light")
        st.text(st.session_state.tracking_analysis_env.list_filenames)
        if st.session_state.tracking_analysis_env.light_on != None:
            with c3:
                button_get_heatmap_df = st.button("Run")

        if not st.session_state.tracking_analysis_env.dataSet_all.empty:
            with c4:
                st.download_button(label="Download Heatmap File",
                                    data= st.session_state.tracking_analysis_env.dataSet_all.to_parquet(),
                                    file_name="heatmap_{}.parquet".format(st.session_state.tracking_analysis_env.animal))

        if st.session_state.tracking_analysis_env.label_dict:
            with c5:
                st.download_button("Download Label File",
                                data=pickle.dumps(st.session_state.tracking_analysis_env.label_dict),
                                file_name="label_dict_{}.pkl".format(st.session_state.tracking_analysis_env.animal))
                
        # 2. processamento --------------------------------------------------------------------------------------------
        if st.session_state.tracking_analysis_env.path != None:
            if button_submit:
                st.session_state.tracking_analysis_env.get_dir_list()
                st.experimental_rerun()

        if st.session_state.tracking_analysis_env.list_filenames != None:
            if button_get_light:
                st.session_state.tracking_analysis_env.checking_light()
                st.experimental_rerun()
        
        if st.session_state.tracking_analysis_env.light_on != None:
            if button_get_heatmap_df:
                st.session_state.tracking_analysis_env.get_heatmap_df()
                st.experimental_rerun()

    else:
        # 1. interface ------------------------------------------------------------------------------------------------
        heatmap_file = st.file_uploader("Heatmap File (parquet)")
        dict_file = st.file_uploader("Labels File (dict)")
        filter_file = st.file_uploader("Filter File (csv)")
        
        # 2. processamento --------------------------------------------------------------------------------------------
        if heatmap_file is not None:
            st.session_state.tracking_analysis_env.dataSet_all = pd.read_parquet(heatmap_file)
        
        if dict_file:
            st.session_state.tracking_analysis_env.label_dict = pickle.load(dict_file)

        # if filter_file:
        #     st.session_state.tracking_analysis_env.filter_mask = pd.read_csv(filter_file)

    # 3. plot ---------------------------------------------------------------------------------------------------
    st.markdown("---")

    if not  st.session_state.tracking_analysis_env.dataSet_all.empty:
        title_html = "<h1 style='text-align: center; color: #31333F; font-size: 30px;'>{}</h1>"
        st.markdown(title_html.format("Plot Config"), unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            plot_interval = st.select_slider('Select a plot interval',
                                    options=['3h', '5h', '7h30m', 'day'])
        with c2:
            plot_step = st.slider('Select a data granularity',
                                      1, 30, 5)
        
        c1, c2 = st.columns([1.1, 17])
        with c1:
            checkbox_filter = st.checkbox("Filter")
        with c2:
            checkbox_transparent_bg = st.checkbox("Transparent Background")

        c1, c2 = st.columns([1, 20])
        with c1:
            button_plot = st.button("Plot")
        with c2:
            fn = f'heatmap{st.session_state.tracking_analysis_env.animal}_{plot_interval}_{plot_step}.png'
            st.session_state.fig.savefig(fn, transparent=checkbox_transparent_bg)
            with open(fn, "rb") as img:
                st.download_button(label="Download image",
                                data=img,
                                file_name=fn)

        
    # 4. resultados --------------------------------------------------------------------------------------------
    if not  st.session_state.tracking_analysis_env.dataSet_all.empty:
        # st.markdown("### Resultados por Região")

        if button_plot:
            step = plot_step
            y_cats = list(range(0,240+step, step))
            x_cats = list(range(0,320+step, step))
            y_labels = [(y_cats[i]+y_cats[i+1])/2 for i in range(len(y_cats)-1)]
            x_labels = [(x_cats[i]+x_cats[i+1])/2 for i in range(len(x_cats)-1)]

            st.session_state.tracking_analysis_env.dataSet_all["coord_x_cat"] = pd.cut(st.session_state.tracking_analysis_env.dataSet_all["coord_x"].replace([120.5, 160.5], np.nan), bins=x_cats, labels=x_labels)
            st.session_state.tracking_analysis_env.dataSet_all["coord_y_cat"] = pd.cut(st.session_state.tracking_analysis_env.dataSet_all["coord_y"].replace([120.5, 160.5], np.nan), bins=y_cats, labels=y_labels)

            values = st.session_state.tracking_analysis_env.dataSet_all[plot_interval].dropna().unique()

            if plot_interval == "3h":
                j_subplot = 5
                i_subplot = np.ceil(len(values) / j_subplot)
                figsize = [22, 20]
            elif plot_interval == "5h":
                j_subplot = 3
                i_subplot = np.ceil(len(values) / j_subplot)
                figsize = [18, 25]
            elif plot_interval == "7h30m":
                j_subplot = 2
                i_subplot = np.ceil(len(values) / j_subplot)
                figsize = [15, 25]
            else:
                j_subplot = 1
                i_subplot = np.ceil(len(values) / j_subplot)
                figsize = [10, 30]

            st.session_state.fig, ax = plt.subplots(figsize=figsize)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            for i, value in enumerate(values):
                df = st.session_state.tracking_analysis_env.dataSet_all[st.session_state.tracking_analysis_env.dataSet_all["7h30m"] == value][["coord_x_cat", "coord_y_cat"]].dropna()

                ax = st.session_state.fig.add_subplot(int(i_subplot),int(j_subplot),i+1)
                ax.hist2d(df["coord_x_cat"], df["coord_y_cat"], bins=[x_cats, y_cats], cmap="turbo")
                ax.set_title(st.session_state.tracking_analysis_env.label_dict[plot_interval][value])
                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_xlabel("")
                ax.set_ylabel("")
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.spines['left'].set_visible(False)
                ax.spines['bottom'].set_visible(False)
        
        st.pyplot(st.session_state.fig)
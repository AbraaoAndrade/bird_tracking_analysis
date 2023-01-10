import sys
sys.path.append("code")
sys.path.append("data")

from utils import *
from app import *
from about import *

from st_switcher import st_switcher

if 'checkbox_status' not in st.session_state:
    st.session_state['checkbox_status'] = False

if 'tracking_analysis_env' not in st.session_state:
    st.session_state['tracking_analysis_env'] = tracking_analysis()

if 'fig' not in st.session_state:
    st.session_state['fig'] = plt.figure()

if 'layout' not in st.session_state:
    st.session_state['layout'] = "wide"

st.set_page_config(page_title="HeatMap Plot",
                   page_icon=":compass:",
                   layout= st.session_state.layout,
                   initial_sidebar_state="auto")

page = st_switcher()
st.markdown("# Bird Tracking Analysis")

if page == 'yang':
    about()
else:
    app()
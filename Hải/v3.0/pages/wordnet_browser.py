import streamlit as st
from components.wn_utils import *
from components.search_utils import *
from components.display_utils import *
from nltk.corpus import wordnet as wn
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🌐 Trình tra cứu WordNet")

# Tạo 3 cột cho ba input hàng ngang
col1, col2, col3 = st.columns([1.5, 1, 1.5])
with col1:
    relationship_type = st.selectbox("🔗 Loại quan hệ:", ['hypernym', 'hyponym', 'meronym', 'holonym'])
with col2:
    max_recursive = st.slider("📏 Độ sâu đệ quy:", min_value=1, max_value=10, value=3)
with col3:
    view_mode = st.radio("👁️ Chế độ hiển thị:", ['Dạng chữ', 'Dạng đồ thị'], horizontal=True)

# Thanh nhập từ
word = st.text_input("🔍 Nhập từ cần tìm:")

if word:
    synsets = wn.synsets(word, pos='n')
    tree_data = build_tree_list(synsets, relationship_type, max_recursive=max_recursive)
    nested_dict = to_nested_dict(tree_data)    
    
    if view_mode == 'Dạng chữ':
        st.subheader("🌲 Dạng chữ (Tree View)")
        st.markdown(get_tree_view_css(), unsafe_allow_html=True)
        html = render_details_tree(nested_dict)
        st.markdown(html, unsafe_allow_html=True)

    else:
        st.subheader("📊 Dạng biểu đồ (Graph View)")
        elements = dict_to_cytoscape(nested_dict)
        render_cytoscape(elements)

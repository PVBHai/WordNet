# Streamlit
import streamlit as st

# Components
from components.utils_wn import *
from components.utils_search import *
from components.utils_display import *
# from components.class_Node import *
from components.class_NodeFamily import *
import streamlit.components.v1 as components

# WordNet
# from nltk.corpus import wordnet as wn
import wn
# from wn_editor.editor import LexiconEditor

# Resolve save thread of wn library
import os
import sqlite3

# # ✅ Override đúng cách để tránh lỗi thread
# _orig_connect = sqlite3.connect
# def connect_threadsafe(*args, **kwargs):
#     kwargs["check_same_thread"] = False
#     return _orig_connect(*args, **kwargs)
# sqlite3.connect = connect_threadsafe

# ------------- UI ------------- #
st.set_page_config(layout="wide", page_title="Trình tra cứu VietNet")

# Custom CSS
st.markdown("""
<style>
    .big-title {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f1f1f;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.3rem;
        text-align: center;
        color: #555;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .info-title {
        font-weight: bold;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
        opacity: 0.9;
    }
    .info-name {
        font-size: 1rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# Main Title
st.markdown('<div class="big-title">🌐 Trình tra cứu VietNet</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">HỆ THỐNG NHÃN NGỮ NGHĨA MỤC TỪ DANH TỪ TRÊN NHÁNH "THỨC ĂN"</div>', unsafe_allow_html=True)

# Information Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <div class="info-title">👨‍🏫 NGƯỜI HƯỚNG DẪN KHOA HỌC</div>
        <div class="info-name">
            PGS.TS. Đinh Điền<br>
            TS. Trần Thị Minh Phượng
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <div class="info-title">👩‍🔬 NGHIÊN CỨU SINH THỰC HIỆN</div>
        <div class="info-name">
            Phan Thị Mỹ Trang
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <div class="info-title">💻 HỖ TRỢ KỸ THUẬT (CNTT)</div>
        <div class="info-name">
            Phan Văn Bá Hải<br>
            Đỗ Quốc Trí
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Checkbox for "Show All"
show_all = st.checkbox("📚 Hiển thị toàn bộ dữ liệu")

# Tạo 3 cột cho ba input hàng ngang
col1, col2, col3 = st.columns([1.5, 1, 1.5])
with col1:
    relationship_type = st.selectbox("🔗 Loại quan hệ:", ['hypernym', 'hyponym', 'meronym', 'holonym'], index=1)
with col2:
    max_recursive = st.slider("📏 Độ sâu đệ quy:", min_value=1, max_value=10, value=6)
with col3:
    view_mode = st.radio("👁️ Chế độ hiển thị:", ['Dạng chữ', 'Dạng đồ thị'], horizontal=True)

# Thanh nhập từ (disabled if show_all is checked)
word = st.text_input("🔍 Nhập từ cần tìm:", disabled=show_all)

# Initialize lexicon
lexicon = wn.Wordnet('vietnet-food:1.0')

if show_all:
    # Get all root synsets (synsets with no hypernyms)
    all_synsets = list(lexicon.synsets())
    root_synsets = [syn for syn in all_synsets if not syn.hypernyms()]
    
    if root_synsets:
        families = NodeFamily(root_synsets, relationship_type, max_recursive)
        
        if view_mode == 'Dạng chữ':
            st.subheader("🌲 Dạng chữ (Tree View) - Toàn bộ dữ liệu")
            st.markdown(get_tree_view_css(), unsafe_allow_html=True)
            html = render_details_tree(families.nodes)
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.subheader("📊 Dạng biểu đồ (Graph View) - Toàn bộ dữ liệu")
            elements = nodefamily_to_cytoscape_elements(families.nodes)
            render_cytoscape(elements)
    else:
        st.warning("⚠️ Không tìm thấy node gốc trong dữ liệu!")

elif word:
    synsets = lexicon.synsets(word)

    if not synsets:
        st.text('Từ bạn tìm không tồn tại !!!')
        pass

    else:
        families = NodeFamily(synsets, relationship_type, max_recursive)
        
        if view_mode == 'Dạng chữ':
            st.subheader("🌲 Dạng chữ (Tree View)")
            st.markdown(get_tree_view_css(), unsafe_allow_html=True)
            html = render_details_tree(families.nodes)
            st.markdown(html, unsafe_allow_html=True)

        else:
            st.subheader("📊 Dạng biểu đồ (Graph View)")
            elements = nodefamily_to_cytoscape_elements(families.nodes)
            render_cytoscape(elements)
            

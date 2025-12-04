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
        <div class="info-title">💻 ĐỒNG THỰC HIỆN (CNTT)</div>
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
word_raw = st.text_input("🔍 Nhập từ cần tìm:", disabled=show_all)

# Function to clean and normalize input
def clean_input(text):
    """
    Clean and normalize user input:
    - Remove leading/trailing whitespace
    - Replace multiple spaces with single space
    - Remove special characters that might cause issues
    - Normalize Unicode characters
    """
    if not text:
        return ""
    
    import re
    import unicodedata
    
    # Normalize Unicode (NFC normalization for Vietnamese characters)
    text = unicodedata.normalize('NFC', text)
    
    # Remove leading/trailing whitespace (first pass)
    text = text.strip()
    
    # Replace multiple spaces/tabs/newlines with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove control characters and other non-printable characters
    # but keep Vietnamese characters, letters, numbers, hyphens, and underscores
    text = re.sub(r'[^\w\s\-]', '', text, flags=re.UNICODE)
    
    # Strip again after removing special characters (second pass)
    text = text.strip()
    
    # Remove any remaining multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text

# Clean the input
word = clean_input(word_raw)

# Initialize lexicon
lexicon = wn.Wordnet('vietnet-food:1.0')

# Try to load English WordNet (OEWN) for English lemma search
try:
    # Check if OEWN is available
    oewn_lexicons = [lex for lex in wn.lexicons() if 'oewn' in lex.id.lower()]
    if not oewn_lexicons:
        # Try to download OEWN if not available
        try:
            with st.spinner('⏳ Đang tải English WordNet (OEWN)...'):
                wn.download('oewn:2024')
        except Exception as download_error:
            pass
    
    # Load OEWN lexicon
    oewn = wn.Wordnet('oewn:2024')
    oewn_available = True
except Exception as e:
    oewn = None
    oewn_available = False

if show_all:
    # Get all root synsets (synsets with no hypernyms)
    all_synsets = list(lexicon.synsets())
    root_synsets = [syn for syn in all_synsets if not syn.hypernyms()]
    
    if root_synsets:
        families = NodeFamily(root_synsets, relationship_type, max_recursive)
        
        if view_mode == 'Dạng chữ':
            st.subheader("🌲 Dạng chữ (Tree View) - Toàn bộ dữ liệu")
            st.markdown(get_tree_view_css(), unsafe_allow_html=True)
            html = render_details_tree(families.nodes, max_recursive=max_recursive)
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.subheader("📊 Dạng biểu đồ (Graph View) - Toàn bộ dữ liệu")
            elements = nodefamily_to_cytoscape_elements(families.nodes)
            render_cytoscape(elements)
    else:
        st.warning("⚠️ Không tìm thấy node gốc trong dữ liệu!")

elif word:
    synsets = []
    
    # Try searching by synset_id first
    try:
        synset = lexicon.synset(word)
        if synset:
            synsets = [synset]
    except:
        pass
    
    # If not found by synset_id, try searching by exact lemma match (Vietnamese)
    if not synsets:
        synsets = lexicon.synsets(word)
    
    # If still not found, try searching by ILI (Inter-Lingual Index)
    if not synsets:
        all_synsets = list(lexicon.synsets())
        for syn in all_synsets:
            if syn.ili and syn.ili.id == word:
                synsets.append(syn)
    
    # If still not found and OEWN is available, try searching by English lemma
    if not synsets and oewn_available:
        try:
            # Search for English lemma in OEWN
            english_synsets = oewn.synsets(word)
            
            if english_synsets:
                # Get synset IDs from OEWN (VietNet stores OEWN synset IDs, not ILI IDs)
                oewn_synset_ids = set()
                for en_syn in english_synsets:
                    oewn_synset_ids.add(en_syn.id)
                
                # Search VietNet synsets with matching ILI (which contains OEWN synset ID)
                if oewn_synset_ids:
                    all_vnnet_synsets = list(lexicon.synsets())
                    for syn in all_vnnet_synsets:
                        # VietNet ILI stores OEWN synset ID
                        if syn.ili and syn.ili.id in oewn_synset_ids:
                            synsets.append(syn)
                    
                    if synsets:
                        # Show info about English to Vietnamese mapping
                        st.success(f"🌍 Tìm thấy từ tiếng Anh **'{word}'** → {len(synsets)} synset(s) tương ứng trong VietNet")
                    else:
                        st.info(f"💡 Tìm thấy '{word}' trong English WordNet nhưng chưa có bản dịch tiếng Việt tương ứng")
        except Exception as e:
            # Silently fail if OEWN search fails
            pass

    if not synsets:
        # Not found - show suggestions instead of displaying all nodes with partial matches
        st.warning(f'⚠️ Không tìm thấy từ chính xác: **"{word}"**')
        
        # Find similar words (containing the search string)
        all_synsets = list(lexicon.synsets())
        suggestions = set()  # Use set to avoid duplicates
        
        for syn in all_synsets:
            lemmas = syn.lemmas()
            for lemma in lemmas:
                # Check if lemma contains the search word (case-insensitive partial match)
                if word.lower() in lemma.lower():
                    suggestions.add(lemma)
        
        if suggestions:
            st.info(f"💡 **Gợi ý các từ liên quan** ({len(suggestions)} từ):")
            
            # Sort suggestions alphabetically
            sorted_suggestions = sorted(list(suggestions))
            
            # Display suggestions in columns for better layout
            cols_per_row = 4
            for i in range(0, len(sorted_suggestions), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, col in enumerate(cols):
                    if i + j < len(sorted_suggestions):
                        suggestion = sorted_suggestions[i + j]
                        # Make suggestions clickable-looking with markdown
                        col.markdown(f"• **{suggestion}**")
        else:
            st.error('❌ Không tìm thấy từ nào liên quan!')

    else:
        families = NodeFamily(synsets, relationship_type, max_recursive)
        
        if view_mode == 'Dạng chữ':
            st.subheader("🌲 Dạng chữ (Tree View)")
            st.markdown(get_tree_view_css(), unsafe_allow_html=True)
            html = render_details_tree(families.nodes, max_recursive=max_recursive)
            st.markdown(html, unsafe_allow_html=True)

        else:
            st.subheader("📊 Dạng biểu đồ (Graph View)")
            elements = nodefamily_to_cytoscape_elements(families.nodes)
            render_cytoscape(elements)

# Footer with copyright and citation information
st.markdown("---")
st.markdown("""
<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 30px;">
    <div style="color: #333; font-size: 0.95em; line-height: 1.8;">
        <p style="margin-bottom: 15px;">
            <strong>📅 Hệ thống được hoàn thành:</strong> 08/11/2025
        </p>
        <p style="margin-bottom: 15px;">
            <strong>©️ Bản quyền:</strong> Trung tâm Ngôn ngữ học Tính toán, Trường Đại học Khoa học Tự nhiên – ĐHQG HCM.
        </p>
        <p style="margin-bottom: 0; padding: 15px; background-color: #fff; border-left: 4px solid #4A90E2; border-radius: 5px;">
            <strong>📖 Nguồn trích dẫn:</strong><br>
            <span style="color: #555; display: block; margin-left: 2em; margin-top: 8px;">
                Phan Thị Mỹ Trang, Phan Văn Bá Hải, Đỗ Quốc Trí, Đinh Điền &amp; Trần Thị Minh Phượng (2025, ngày 08 tháng 11). 
                <em>Trình tra cứu VietNet: Hệ thống nhãn ngữ nghĩa mục từ danh từ trên nhánh &quot;thức ăn&quot;</em>. 
                Trung tâm Ngôn ngữ học Tính toán, Trường ĐH Khoa học Tự nhiên – ĐH Quốc gia Tp.HCM. 
                <a href="https://vietnet-food.streamlit.app/" target="_blank" style="color: #4A90E2; text-decoration: none;">https://vietnet-food.streamlit.app/</a>
            </span>
        </p>
    </div>
</div>
""", unsafe_allow_html=True)


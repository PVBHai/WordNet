# import os
# import streamlit as st
# import wn
# import sqlite3

# # ✅ Override đúng cách để tránh lỗi thread
# _orig_connect = sqlite3.connect
# def connect_threadsafe(*args, **kwargs):
#     kwargs["check_same_thread"] = False
#     return _orig_connect(*args, **kwargs)
# sqlite3.connect = connect_threadsafe

# st.set_page_config(layout="wide")
# st.title("🌐 Trình tra cứu WordNet")

# # Đảm bảo thư mục ./data tồn tại
# if not os.path.exists('./data'):
#     os.mkdir('./data')

# # Nhập từ
# word = st.text_input("🔍 Nhập từ cần tìm:")

# # Xử lý tìm kiếm
# if word:
#     try:
#         lexicon = wn.Wordnet('oewn:2024')
#         synsets = lexicon.synsets(word, pos='n')

#         if synsets:
#             st.subheader(f"Kết quả cho từ: {word}")
#             for i, s in enumerate(synsets, 1):
#                 st.markdown(f"**{i}.** {s.definition()}")
#         else:
#             st.warning("❗ Không tìm thấy từ.")
#     except Exception as e:
#         st.error(f"🚫 Lỗi khi tra cứu: {e}")

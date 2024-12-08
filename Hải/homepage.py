"""
    WORDNET BROWSER by HẢI.PVB
    Version: coding ver
"""

# WORDNET
#import wn
#from wn_editor.editor import LexiconEditor

# NLTK (WORDNET)
import nltk
from nltk.corpus import wordnet as wn

# FRONT-END
from nicegui import ui

# OS DIRECTORY
import os


# ------------------------------------------------------------------------------------
#                                   Cấu hình
# ------------------------------------------------------------------------------------


# # Cấu hình thư mục
# wn.config.data_directory = './data'

# # Tải dữ liệu nếu chưa có
# LEXICON = ['odenet', 'omw-en31:1.4', 'omw-en']
# lexicon_name = LEXICON[1]

# # Tạo thư mục
# if not os.path.exists('./data'):
#     os.mkdir('./data')

# # Kiểm tra lexicon có tồn tại hay chưa
# available_lexicons = [lex.id for lex in wn.lexicons()]
# if lexicon_name not in available_lexicons:
#     wn.download(lexicon_name)

# # Khởi tạo database
# lexicon = wn.Wordnet(lexicon=lexicon_name)


# Tải lexicon (NLTK - WORNET)
nltk.download('wordnet')

# Thêm CSS tùy chỉnh để phóng to các thành phần giao diện
ui.add_head_html('''
<style>
    .big-button {
        font-size: 20px;
        padding: 15px 30px;
    }
    .big-input {
        font-size: 24px;
        padding: 10px;
    }
    .big-knob {
        --size: 100px;
    }
    .full-screen-mermaid, .full-screen-card {
        width: 100vw;  /* Chiều rộng 100% viewport */
        height: 100vh; /* Chiều cao 100% viewport */
        overflow: auto; /* Đảm bảo có thể cuộn */
    }
    .scalable-mermaid svg {
        width: 100%;             /* Full width of the parent container */
        height: 100%;            /* Set height explicitly to avoid scaling issues */
        overflow: auto;          /* Allow scrolling if needed */
        display: flex;           /* Ensure proper alignment */
        justify-content: center; /* Center content horizontally */
        align-items: center;     /* Center content vertically */
    }
    .scalable-mermaid svg {
        width: 100%;        /* SVG adjusts to the width of the container */
        height: auto;       /* Maintains aspect ratio */
    }
    .small-slider {
        width: 200px; /* Điều chỉnh kích thước chiều rộng */
        height: 20px; /* Điều chỉnh chiều cao */
    }
</style>
''')



# ------------------------------------------------------------------------------------
#                                Các biến toàn cục
# ------------------------------------------------------------------------------------


# Card
card = None

# Switch view (Tree - Mermaid)
view_mode = None


# ------------------------------------------------------------------------------------
#                                  Các hàm hỗ trợ
# ------------------------------------------------------------------------------------


# Hàm để lấy danh sách các quan hệ (relationship) của một synset
def get_relationships(synset, relationship_type):
    if relationship_type == 'hypernym':
        return synset.hypernyms()
    elif relationship_type == 'hyponym':
        return synset.hyponyms()
    elif relationship_type == 'meronym':
        return synset.part_meronyms() + synset.substance_meronyms()
    elif relationship_type == 'holonym':
        return synset.part_holonyms() + synset.substance_holonyms()
    else:
        return []


# Hàm giải mã lemmas
def process_lemmas(lemmas, recursive_level=None):
    result_list = ''
    if recursive_level is not None:
        result_list += f'Lv{recursive_level + 1}. '
    for i, lemma in enumerate(lemmas):
        result_list += lemma.name()
        if (i + 1) < len(lemmas):
            result_list += '/'
    return result_list


# Hàm để xây dựng biểu đồ cây bằng cú pháp Mermaid với giới hạn đệ quy
def build_mermaid_list(synset, relationship_type, parent_id=None, recursive_level=0, max_recursive=1, result_list=[]):
    if recursive_level >= max_recursive:
        return  

    synset_id = synset.name().replace('.', '_')
    if parent_id:
        parent_lemmas = f'{parent_id}-#-' + process_lemmas(wn.synset(parent_id).lemmas())
        synset_lemmas = f'{synset_id}-#-' + process_lemmas(synset.lemmas())
        result_list.append(f'{parent_lemmas} --> {synset_lemmas}')
    else:
        synset_lemmas = f'{synset_id}-#-' + process_lemmas(synset.lemmas())
        result_list.append(f'{synset_lemmas}["{synset_lemmas}"]')

    relationships = get_relationships(synset, relationship_type)
    for relation_synset in relationships:
        build_mermaid_list(relation_synset, relationship_type, synset_id, recursive_level + 1, max_recursive, result_list)


# Hàm để xây dựng biểu đồ cây bằng cú pháp Mermaid bằng kết quả của hàm build_mermaid_list
def build_mermaid_tree(synsets, relationship_type, max_recursive=1):
    # Khởi tạo mảng lưu dữ liệu tạo ra
    result_list = []

    # Tìm max_recursive thích hợp để Fix lỗi "Hiển thị MERMAID" (Chỉ cho HYPERNYM)
    if relationship_type == 'hypernym':
        min_level = 20
        max_level = 0
        for synset in synsets:
            # Tìm độ sâu của synset có path ngắn nhất đến "entity"
            hyper_path = synset.hypernym_paths()
            for path in hyper_path:
                if len(path) + 1 < min_level:
                    min_level = len(path) + 1
                if len(path) + 1 > max_level:
                    max_level = len(path) + 1

        # Cập nhật max_recursive 
        # Nếu có 1 nhánh nào đó chạy tới entity (max_recursive > min_level)
        # => Gán giá trị max_recursive bằng max_level (để chạy từ entity xuống)
        if max_recursive >= min_level:
            max_recursive = max_level

    # Gọi hàm để tạo Mermaid code
    for synset in synsets:
        temp_list = []
        build_mermaid_list(synset=synset, relationship_type=relationship_type, max_recursive=max_recursive, result_list=temp_list)
        result_list += temp_list

    # Loại bỏ trùng lặp
    result_list = list(set(result_list))

    # Cập nhật mermaid_code
    mermaid_code = []
    for item in result_list:
        mermaid_code.append(item)
    
    # Trả về mermaid code để xây dựng cây
    return mermaid_code


# Hàm để xây tree
def build_tree_list(synsets, relationship_type, recursive_level=0, max_recursive=1):
    if recursive_level >= max_recursive:
        return []
    if not synsets:
        return []

    children_list = []
    for synset in synsets:
        node = {}
        relations = get_relationships(synset, relationship_type)
        node['id'] = process_lemmas(synset.lemmas(), recursive_level) + f' (id: {synset.name()})'
        node['description'] = synset.definition()
        node['children'] = build_tree_list(relations, relationship_type, recursive_level + 1, max_recursive)
        children_list.append(node)
    return children_list


# Hàm xây cây
def build_tree(synsets, relationship_type, max_recursive=1):
    tree_nodes = build_tree_list(synsets=synsets, relationship_type=relationship_type, max_recursive=max_recursive)
    if not tree_nodes:
        tree_nodes = [{"id": "No synsets found", "children": []}]
    return tree_nodes


# Hàm cập nhật card dựa trên chế độ hiển thị
def update_card(word, relationship_type, max_recursive):
    global card, view_mode
    
    if card is not None:
        card.delete()
        card = None

    synsets = wn.synsets(word, pos='n')

    with ui.card().classes('full-screen-card') as card:
        if view_mode == 'Danh sách':
            tree_nodes = build_tree(synsets, relationship_type, max_recursive)
            tree = ui.tree(tree_nodes, label_key='id', on_select=lambda e: ui.notify(e.value))
            tree.add_slot('default-header', '''
            <span :props="props"> <strong>{{ props.node.id }}</strong></span>
            ''')
            tree.add_slot('default-body', '''
                <span :props="props">Định nghĩa: "{{ props.node.description }}"</span>
            ''')
        else:
            mermaid_code = build_mermaid_tree(synsets, relationship_type, max_recursive)
            mermaid_diagram = ui.mermaid('graph TD\n').classes('full-screen-mermaid').classes('scalable-mermaid')
            mermaid_diagram.content = 'graph TD\n' + '\n'.join(mermaid_code)
            mermaid_diagram.update()


# Hàm thực thi khi bấm nút
def search_word():
    # Khai báo sử dụng biến toàn cục và cập nhật lại view_mode
    global view_mode
    view_mode = toggle_button.value

    # Lấy kết quả của thanh tìm kiếm
    word = search_bar.value

    # Lấy loại quan hệ được chọn
    relationship_type = relationship_select.value  

    # Lấy giá trị tối đa của đệ quy
    max_recursive = int(recursive_input.value) if recursive_input.value != 0 else 50

    # In ra kết quả
    update_card(word, relationship_type, max_recursive)


# ------------------------------------------------------------------------------------
#                                   Giao diện
# ------------------------------------------------------------------------------------


with ui.row():
    search_bar = ui.input(label='Tìm kiếm từ', placeholder='Nhập từ bạn cần tìm vào đây').classes('big-input')
    relationship_select = ui.select(['hypernym', 'hyponym', 'meronym', 'holonym'], value='hypernym', label='Loại quan hệ').classes('big-input')

with ui.row():
    toggle_button = ui.toggle(['Danh sách', 'Biểu đồ'], value='Danh sách', on_change=lambda: search_word())
    search_button = ui.button('Tìm kiếm', on_click=lambda: search_word())
    ui.label('Độ sâu tìm kiếm')
    recursive_input = ui.slider(min=1, max=20, step=1, value=3, on_change=lambda: search_word()).props('label-always').classes('small-slider')

ui.label('Kết quả sẽ được hiển thị ở đây').classes('big-input')
ui.run(title='WordNet App')
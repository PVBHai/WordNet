# WORDNET
import wn
from wn_editor.editor import LexiconEditor

# FRONT-END
from nicegui import ui


# ------------------------------------------------------------------------------------
#                                   Cấu hình
# ------------------------------------------------------------------------------------


# Cấu hình thư mục
wn.config.data_directory = './data'

# Tải dữ liệu nếu chưa có
LEXICON = ['odenet', 'omw-en']
lexicon_name = LEXICON[1]
if not wn.lexicons():
    wn.download(lexicon_name)

# Khởi tạo database
lexicon = wn.Wordnet(lexicon=lexicon_name)

# Thêm CSS tùy chỉnh để phóng to các thành phần giao diện
ui.add_head_html('''
<style>
    .big-button {
        font-size: 24px;
        padding: 20px 40px;
    }
    .big-input {
        font-size: 24px;
        padding: 10px;
    }
    .big-knob {
        --size: 100px;
    }
    .full-screen-mermaid {
        width: 100vw;  /* Chiều rộng 100% viewport */
        height: 100vh; /* Chiều cao 100% viewport */
    }
</style>
''')



# ------------------------------------------------------------------------------------
#                                Các biến toàn cục
# ------------------------------------------------------------------------------------






# ------------------------------------------------------------------------------------
#                                  Các hàm hỗ trợ
# ------------------------------------------------------------------------------------


'''# Hàm để tìm kiếm
def search_word():
    # Lấy kết quả của thanh tìm kiếm
    word = search_bar.value
    synsets = lexicon.synsets(word)
    label.text = f'Từ {word} tổng cộng {len(synsets)} nghĩa'

    if not synsets:
        mermaid_code.append("No synsets found.")
    else:
        for synset in synsets:
            build_mermaid_tree(synset)
    
    mermaid_diagram.content = 'graph TD\n' + '\n'.join(mermaid_code)

    # Update the tree with new data
    tree_nodes = build_tree(synsets)

    # Display tree
    #tree = ui.tree(tree_nodes, label_key='id', on_select=lambda e: ui.notify(e.value))
    @ui.refreshable
    def draw_tree(tree_nodes):    
        ui.tree(tree_nodes, label_key='id', on_select=lambda e: ui.notify(e.value))
        
    draw_tree(tree_nodes)
    #return tree_nodes

# Hàm để biểu diễn các cây
def build_tree(synsets, relative=''):
    result = []
    for i, ss in enumerate(synsets):
        hypernyms = ss.hypernyms()
        children = [{'id': h.lemmas()[0]} for h in hypernyms] if hypernyms else []
        dictionary = {'id': ss.lemmas()[0], 'children': children}
        result.append(dictionary)
    return result'''


# Hàm để lấy danh sách các quan hệ (relationship) của một synset
def get_relationships(synset, relationship_type):
    if relationship_type == 'hypernym':
        return synset.hypernyms()
    elif relationship_type == 'hyponym':
        return synset.hyponyms()
    elif relationship_type == 'meronym':
        return synset.meronyms()
    elif relationship_type == 'holonym':
        return synset.holonyms()
    else:
        return []


# Hàm giải mã lemmas
def process_lemmas(lemmas):
    result_list = ''
    for i, lemma in enumerate(lemmas):
        result_list += lemma.replace(' ', '_')
        # Thêm dấu ,
        if (i + 1) < len(lemmas):
            result_list += '/'
    return result_list


# Hàm để xây dựng biểu đồ cây bằng cú pháp Mermaid với giới hạn đệ quy
def build_mermaid_list(synset, relationship_type, parent_id=None, recursive_level=0, max_recursive=1, check_duplicate_list=[]):
    # Dừng đệ quy nếu đã đạt đến mức đệ quy tối đa
    if recursive_level >= max_recursive:
        return  

    synset_id = synset.id.replace('.', '_')
    if parent_id:
        # Thêm một liên kết từ parent_id đến synset_id trong mã Mermaid
        parent_lemmas = process_lemmas(wn.synset(parent_id).lemmas())
        synset_lemmas = process_lemmas(wn.synset(synset_id).lemmas())
        # Nếu quan hệ hyponym và quan hệ meronym thì: synset --> relation
        if relationship_type == 'hyponym' or relationship_type == 'meronym':
            check_duplicate_list.append(f'{parent_lemmas} --> {synset_lemmas}')
        # Nếu quan hệ hypernym và quan hệ relation thì: relation --> synset
        else: 
            check_duplicate_list.append(f'{synset_lemmas} --> {parent_lemmas}')
    else:
        # Bắt đầu một node mới cho synset_id
        synset_lemmas = process_lemmas(wn.synset(synset_id).lemmas())
        check_duplicate_list.append(f'{synset_lemmas}["{synset_lemmas}"]')

    # Lấy danh sách các quan hệ của synset hiện tại
    relationships = get_relationships(synset, relationship_type)  

    # Lấy danh sách các quan hệ của synset hiện tại
    for rel_synset in relationships:
        # Đệ quy xây dựng cây cho mỗi quan hệ tìm được, tăng recursive_level
        build_mermaid_list(rel_synset, relationship_type, synset_id, recursive_level + 1, max_recursive, check_duplicate_list)



# Hàm để xây dựng biểu đồ cây bằng cú pháp Mermaid bằng kết quả của hàm build_mermaid_list
def build_mermaid_tree(synsets, relationship_type, max_recursive=1):
    # Khởi tạo mảng kết quả
    result_list = []

    # Gọi hàm để tạo 
    for synset in synsets:
        temp_list = []
        build_mermaid_list(synset=synset, relationship_type=relationship_type, max_recursive=max_recursive, check_duplicate_list=temp_list)
        result_list += temp_list

    # Loại bỏ trùng lặp
    result_list = list(set(result_list))

    # Cập nhật mermaid_code
    for item in result_list:
        mermaid_code.append(item)


# Hàm thực thi khi bấm nút
def search_word():
    # Lấy kết quả của thanh tìm kiếm
    word = search_bar.value

    # Lấy loại quan hệ được chọn
    relationship_type = relationship_select.value  

    # Lấy giá trị tối đa của đệ quy
    max_recursive = int(recursive_input.value)  

    # Tính toán các synset
    synsets = lexicon.synsets(word, pos='n')
    label.text = f'Từ {word} tổng cộng {len(synsets)} nghĩa'

    # Reset dữ liệu
    mermaid_code.clear()
    if not synsets:
        mermaid_code.append("No synsets found.")
    else:
        #for synset in synsets:
            #build_mermaid_tree(synset, relationship_type, max_recursive=max_recursive)
        build_mermaid_tree(synsets, relationship_type, max_recursive)
    
    mermaid_diagram.content = 'graph TD\n' + '\n'.join(mermaid_code)



# ------------------------------------------------------------------------------------
#                                   Giao diện
# ------------------------------------------------------------------------------------


# Tạo giao diện với thanh tìm kiếm và nút tìm kiếm
with ui.row():
    # Thanh tìm kiếm
    search_bar = ui.input(label='Tìm kiếm từ', placeholder='Nhập từ bạn cần tìm vào đây').classes('big-input')

    # Lựa chọn quan hệ
    relationship_select = ui.select(['hypernym', 'hyponym', 'meronym', 'holonym'], label='Loại quan hệ').classes('big-input')

    # Nhập giới hạn đệ quy
    #recursive_input = ui.input(label='Max Recursive Depth', value='3')
    recursive_input = ui.knob(value=3, min=1, max=10, step=1, show_value=True).classes('big-knob')
    #ui.label('Chọn độ sâu tìm kiếm')

# Nút tìm kiếm
search_button = ui.button('Tìm kiếm', on_click=search_word)

# Thanh kết quả
label = ui.label('Kết quả sẽ được hiển thị ở đây').classes('big-input')


'''# Tree
tree_nodes = []
tree = ui.tree(tree_nodes, label_key='id', on_select=lambda e: ui.notify(e.value))'''

# Biến để lưu trữ mã Mermaid
mermaid_code = []
mermaid_diagram = ui.mermaid('graph TD\n').classes('full-screen-mermaid')

# Khởi chạy giao diện
#ui.run()
ui.run(title='WordNet App')
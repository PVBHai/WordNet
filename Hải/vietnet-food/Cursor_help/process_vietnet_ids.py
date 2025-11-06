"""
Script xử lý cập nhật LexicalEntry ID và Synset ID cho VietNet Food
Dựa trên file từ điển Hoàng Phê

LOGIC MỚI:
1. LexicalEntry & Sense: So sánh writtenForm với cột "word" trong Excel
2. Synset: So sánh Definition với cột "meaning" trong Excel
3. Xử lý chuỗi: Loại bỏ tiền tố [...], normalize khoảng trắng
"""

import pandas as pd
import xml.etree.ElementTree as ET
from collections import defaultdict
import re
import unicodedata

def normalize_text(text):
    """
    Chuẩn hóa chuỗi text để so sánh:
    1. Loại bỏ tiền tố dạng [...] ở đầu (vd: [kng], [ph], [cũ])
    2. Loại bỏ số ở đầu chuỗi (vd: "1 ", "2 ")
    3. Normalize Unicode (NFC)
    4. Chuyển về chữ thường
    5. Loại bỏ dấu chấm, phẩy, dấu hai chấm ở cuối
    6. Strip khoảng trắng đầu/cuối
    7. Thay khoảng trắng kép thành đơn
    """
    if not text or pd.isna(text):
        return ""
    
    text = str(text)
    
    # 1. Loại bỏ các tiền tố [...] ở đầu
    # Pattern: bắt đầu bằng [, theo sau bởi các ký tự không phải ], kết thúc bằng ]
    text = re.sub(r'^\[[^\]]+\]\s*', '', text)
    
    # 2. Loại bỏ số và khoảng trắng ở đầu chuỗi (vd: "1 ", "12 ")
    text = re.sub(r'^\d+\s+', '', text)
    
    # 3. Normalize Unicode về dạng NFC
    text = unicodedata.normalize('NFC', text)
    
    # 4. Chuyển về chữ thường để không phân biệt hoa/thường
    text = text.lower()
    
    # 5. Strip khoảng trắng đầu/cuối
    text = text.strip()
    
    # 6. Loại bỏ các dấu câu ở cuối (dấu chấm, dấu 3 chấm, dấu phẩy, dấu hai chấm)
    text = re.sub(r'[.,;:]+$', '', text)
    text = text.strip()  # Strip lại sau khi loại bỏ dấu câu
    
    # 7. Thay nhiều khoảng trắng liên tiếp thành 1
    text = re.sub(r'\s+', ' ', text)
    
    return text

def main():
    print("=" * 80)
    print("📋 SCRIPT XỬ LÝ CẬP NHẬT ID CHO VIETNET FOOD (LOGIC MỚI)")
    print("=" * 80)
    
    # === 1️⃣ Đọc dữ liệu từ Excel ===
    print("\n[1/5] Đọc dữ liệu từ Excel...")
    excel_path = "data/edit_id/tu_dien_Hoang_Phe.xlsx"
    df = pd.read_excel(excel_path)
    
    # Tạo mapping {word: [list of indices]}
    word_to_indices = {}
    for idx, row in df.iterrows():
        word = normalize_text(row["word"])
        if word:
            if word not in word_to_indices:
                word_to_indices[word] = []
            word_to_indices[word].append(idx + 1)  # index bắt đầu từ 1
    
    # Tạo mapping {normalized_meaning: [list of indices]}
    # KEY: normalized meaning (đã loại bỏ tiền tố)
    # VALUE: list of indices
    meaning_to_indices = {}
    for idx, row in df.iterrows():
        meaning = normalize_text(row["meaning"])
        if meaning:
            if meaning not in meaning_to_indices:
                meaning_to_indices[meaning] = []
            meaning_to_indices[meaning].append(idx + 1)
    
    print(f"   ✓ Tổng số dòng trong Excel: {len(df)}")
    print(f"   ✓ Số từ khác nhau: {len(word_to_indices)}")
    print(f"   ✓ Số nghĩa khác nhau: {len(meaning_to_indices)}")
    
    # === 2️⃣ Đọc XML ===
    print("\n[2/5] Đọc file XML gốc...")
    xml_path = "vietnet_food (thủ công).xml"
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    ns = {"dc": "https://globalwordnet.github.io/schemas/dc/"}
    lexicon = root.find(".//Lexicon", ns)
    
    # === 3️⃣ Xử lý LexicalEntry ID ===
    print("\n[3/5] Xử lý LexicalEntry ID và Sense ID...")
    
    entry_not_found = []  # Không tìm được trong Excel
    entry_more_than_1 = []  # Tìm được >= 2 dòng
    entry_updated = 0
    
    for entry in lexicon.findall("LexicalEntry", ns):
        lemma = entry.find("Lemma", ns)
        if lemma is None:
            continue
        
        word_raw = lemma.attrib.get("writtenForm", "")
        word = normalize_text(word_raw)
        pos = lemma.attrib.get("partOfSpeech", "")
        old_entry_id = entry.attrib.get("id", "")
        
        if pos != "n":
            continue
        
        # Tìm trong Excel (sử dụng normalized word)
        if word not in word_to_indices:
            # Không tìm thấy
            entry_not_found.append({
                "word": word,
                "old_id": old_entry_id
            })
        elif len(word_to_indices[word]) == 1:
            # Tìm được đúng 1 dòng
            index = word_to_indices[word][0]
            new_entry_id = f"vietnet-food-{index:08d}"
            entry.set("id", new_entry_id)
            
            # Cập nhật Sense ID
            for sense in entry.findall("Sense", ns):
                sense.set("id", f"{new_entry_id}-1")
            
            entry_updated += 1
        else:
            # Tìm được >= 2 dòng
            entry_more_than_1.append({
                "word": word,
                "old_id": old_entry_id,
                "indices": word_to_indices[word],
                "count": len(word_to_indices[word])
            })
    
    print(f"   ✓ Đã cập nhật: {entry_updated} LexicalEntry")
    print(f"   ⚠️  Không tìm thấy: {len(entry_not_found)} entries")
    print(f"   ⚠️  Tìm được >= 2: {len(entry_more_than_1)} entries")
    
    # === 4️⃣ Xử lý Synset ID ===
    print("\n[4/5] Xử lý Synset ID...")
    
    synset_not_found = []  # Không tìm được trong Excel
    synset_more_than_1 = []  # Tìm được >= 2 dòng
    synset_updated = 0
    synset_id_mapping = {}  # old_synset_id -> new_synset_id
    
    for synset in lexicon.findall("Synset", ns):
        old_synset_id = synset.attrib.get("id", "")
        
        # Lấy Definition
        definition_elem = synset.find("Definition", ns)
        if definition_elem is None or not definition_elem.text:
            continue
        
        definition_raw = definition_elem.text
        definition = normalize_text(definition_raw)
        
        # Tìm trong Excel theo normalized meaning
        if definition not in meaning_to_indices:
            # Không tìm thấy
            synset_not_found.append({
                "definition": definition[:100] + "..." if len(definition) > 100 else definition,
                "old_id": old_synset_id
            })
        elif len(meaning_to_indices[definition]) == 1:
            # Tìm được đúng 1 dòng
            index = meaning_to_indices[definition][0]
            new_synset_id = f"vietnet-food-{index:08d}-n"
            synset.set("id", new_synset_id)
            synset_id_mapping[old_synset_id] = new_synset_id
            synset_updated += 1
        else:
            # Tìm được >= 2 dòng
            synset_more_than_1.append({
                "definition": definition[:100] + "..." if len(definition) > 100 else definition,
                "old_id": old_synset_id,
                "indices": meaning_to_indices[definition],
                "count": len(meaning_to_indices[definition])
            })
    
    print(f"   ✓ Đã cập nhật: {synset_updated} Synset")
    print(f"   ⚠️  Không tìm thấy: {len(synset_not_found)} synsets")
    print(f"   ⚠️  Tìm được >= 2: {len(synset_more_than_1)} synsets")
    
    # === 4.5️⃣ Cập nhật tham chiếu đến Synset ===
    print("\n   → Cập nhật tham chiếu trong Sense...")
    updated_sense_refs = 0
    for entry in lexicon.findall("LexicalEntry", ns):
        for sense in entry.findall("Sense", ns):
            old_synset_id = sense.attrib.get("synset", "")
            if old_synset_id in synset_id_mapping:
                sense.set("synset", synset_id_mapping[old_synset_id])
                updated_sense_refs += 1
    
    print(f"   ✓ Đã cập nhật: {updated_sense_refs} tham chiếu trong Sense")
    
    print("   → Cập nhật tham chiếu trong SynsetRelation...")
    updated_relation_refs = 0
    for synset in lexicon.findall("Synset", ns):
        for relation in synset.findall("SynsetRelation", ns):
            old_target = relation.attrib.get("target", "")
            if old_target in synset_id_mapping:
                relation.set("target", synset_id_mapping[old_target])
                updated_relation_refs += 1
    
    print(f"   ✓ Đã cập nhật: {updated_relation_refs} tham chiếu trong SynsetRelation")
    
    # === 5️⃣ Xuất kết quả ===
    print("\n[5/5] Xuất kết quả...")
    
    # Tạo thư mục output nếu chưa có
    import os
    output_dir = "Cursor_help"
    os.makedirs(output_dir, exist_ok=True)
    
    # Xuất file XML mới
    output_xml = os.path.join(output_dir, "vietnet_food_final.xml")
    tree.write(output_xml, encoding="UTF-8", xml_declaration=True)
    print(f"   ✓ Đã xuất file XML: {output_xml}")
    
    # Xuất các file phụ cho LexicalEntry
    not_found_file = os.path.join(output_dir, "not_found.xlsx")
    pd.DataFrame(entry_not_found).to_excel(not_found_file, index=False)
    print(f"   ✓ Đã xuất file: {not_found_file} ({len(entry_not_found)} entries)")
    
    more_than_1_file = os.path.join(output_dir, "more_than_1.xlsx")
    pd.DataFrame(entry_more_than_1).to_excel(more_than_1_file, index=False)
    print(f"   ✓ Đã xuất file: {more_than_1_file} ({len(entry_more_than_1)} entries)")
    
    # Xuất các file phụ cho Synset
    synset_not_found_file = os.path.join(output_dir, "synset_not_found.xlsx")
    pd.DataFrame(synset_not_found).to_excel(synset_not_found_file, index=False)
    print(f"   ✓ Đã xuất file: {synset_not_found_file} ({len(synset_not_found)} synsets)")
    
    synset_more_than_1_file = os.path.join(output_dir, "synset_more_than_1.xlsx")
    pd.DataFrame(synset_more_than_1).to_excel(synset_more_than_1_file, index=False)
    print(f"   ✓ Đã xuất file: {synset_more_than_1_file} ({len(synset_more_than_1)} synsets)")
    
    # === 📊 Tổng kết ===
    print("\n" + "=" * 80)
    print("✅ HOÀN THÀNH!")
    print("=" * 80)
    print(f"""
📝 TỔNG KẾT:

🔹 LEXICAL ENTRY:
   • Đã cập nhật: {entry_updated}
   • Không tìm thấy: {len(entry_not_found)}
   • Tìm được >= 2: {len(entry_more_than_1)}

🔹 SYNSET:
   • Đã cập nhật: {synset_updated}
   • Không tìm thấy: {len(synset_not_found)}
   • Tìm được >= 2: {len(synset_more_than_1)}

🔹 THAM CHIẾU:
   • Sense.synset đã cập nhật: {updated_sense_refs}
   • SynsetRelation.target đã cập nhật: {updated_relation_refs}

📂 CÁC FILE ĐÃ TẠO (trong thư mục {output_dir}/):
   • vietnet_food_final.xml - File XML đã cập nhật
   • not_found.xlsx - LexicalEntry không tìm thấy
   • more_than_1.xlsx - LexicalEntry tìm được >= 2
   • synset_not_found.xlsx - Synset không tìm thấy
   • synset_more_than_1.xlsx - Synset tìm được >= 2
    """)

if __name__ == "__main__":
    main()


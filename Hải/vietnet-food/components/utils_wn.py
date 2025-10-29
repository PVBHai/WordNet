# import nltk
# from nltk.corpus import wordnet as wn
import sqlite3

# ✅ Đặt thật sớm
_orig_connect = sqlite3.connect
def connect_threadsafe(*args, **kwargs):
    kwargs["check_same_thread"] = False
    return _orig_connect(*args, **kwargs)
sqlite3.connect = connect_threadsafe

import os
import wn

# Data
if not os.path.exists('./data'):
    os.mkdir('./data')

# Tải dữ liệu WordNet nếu chưa có
# nltk.download('wordnet')
wn.config.data_directory = './data'
# wn.download('oewn:2024')
wn.add('./vietnet_food (thủ công).xml')

def get_relationships(synset, relationship_type):
    if relationship_type == 'hypernym':
        return synset.hypernyms()
    elif relationship_type == 'hyponym':
        return synset.hyponyms()
    elif relationship_type == 'meronym':
        return synset.part_meronyms() + synset.substance_meronyms()
    elif relationship_type == 'holonym':
        return synset.part_holonyms() + synset.substance_holonyms()
    return []

def get_depth_from_root(synset):
    """
    Calculate the depth/level of a synset from the root of the tree.
    The root (node with no hypernyms) is at level 1.
    """
    depth = 1
    current = synset
    visited = set()  # Prevent infinite loops
    
    # Traverse up the hypernym chain to find the root
    while True:
        # Prevent infinite loops in case of circular references
        if current.id in visited:
            break
        visited.add(current.id)
        
        hypernyms = current.hypernyms()
        if not hypernyms:
            # Reached the root
            break
        
        # Move to the first hypernym (go up one level)
        current = hypernyms[0]
        depth += 1
    
    return depth

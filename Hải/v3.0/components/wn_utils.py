import nltk
from nltk.corpus import wordnet as wn

# Tải dữ liệu WordNet nếu chưa có
nltk.download('wordnet')

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

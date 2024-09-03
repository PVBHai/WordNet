import wn
from nicegui import ui

from nicegui.elements.input import Input

def synset_info(synset: wn.synset):
    return f'{", ".join(synset.lemmas())} ({synset.id}) -- {synset.definition()}'

def show_synsets(word: Input, out_col: ui.column):
    word = word.value.strip()

    synsets = wn.synsets(word)

    out_col.clear()
    with out_col:
        for i, ss in enumerate(synsets):
            out_col.markdown(f'Sense {i+1}:')
            out_col.markdown(synset_info(ss))

    
    
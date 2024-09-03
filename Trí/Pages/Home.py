from nicegui import ui
from Utilities import pages, utils

def page():
    with ui.row():
        ui.link('Graph Search', pages.page_graph)
        ui.link('Lowest Common Hypernym', pages.page_lch)

    with ui.row() as row:
        word_input = ui.input(label='Enter a word')

    with ui.column() as output_column:
        ui.button('Find', on_click=lambda: utils.show_synsets(word_input, output_column))
        
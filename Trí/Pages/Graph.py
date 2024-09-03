from nicegui import ui
from Utilities import pages, utils

def page():
    with ui.row():
        ui.link('Home', pages.page_home)
        ui.link('Lowest Common Hypernym', pages.page_lch)

    ui.label('Graph')

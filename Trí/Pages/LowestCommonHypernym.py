from nicegui import ui
from Utilities import pages, utils

def page():
    with ui.row():
        ui.link('Home', pages.page_home)
        ui.link('Graph Search', pages.page_graph)

    ui.label('LCH')

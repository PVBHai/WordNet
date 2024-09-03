from nicegui import ui
from Pages import LowestCommonHypernym, Graph, Home
from Pages import Graph

@ui.page('/')
def page_home():
    ui.label('Welcome to Home')
    Home.page()

@ui.page('/graph')
def page_graph():
    ui.label('Welcome to Graph')
    Graph.page()

@ui.page('/lch')
def page_lch():
    ui.label('Welcome to Lowest Common Hypernyms')
    LowestCommonHypernym.page()
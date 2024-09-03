import wn
from nicegui import ui
from Utilities import utils, pages

def main():
    # Đặt thư mục lưu trữ cơ sở dữ liệu WordNet
    wn.config.data_directory = './Data'

    LEXICON_NAME = 'oewn:2023'
    if not wn.lexicons():
        wn.download(LEXICON_NAME)

    pages.page_home()

    ui.run()

if __name__ in {"__main__", "__mp_main__"}:
    main()
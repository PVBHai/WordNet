import streamlit as st

def render_details_tree(data, level=0):
    html = ""
    margin = level * 20  # mỗi cấp cách trái 20px

    for key, value in data.items():
        if isinstance(value, dict) and value:
            html += f'<div style="margin-left:{margin}px;">'
            html += f"<details>\n"
            html += f"<summary>{key}</summary>\n"
            html += render_details_tree(value, level + 1)
            html += f"</details>\n"
            html += f"</div>"
        elif isinstance(value, dict) and not value:
            html += f'<div style="margin-left:{margin}px;">{key}</div>\n'
        else:
            html += f'<div style="margin-left:{margin}px;">{key}: {value}</div>\n'

    return html

# Dữ liệu mẫu 4 cấp - mỗi cấp có 2 node con
tree_data = {
    "Level 1 - A": {
        "Level 2 - A1": {
            "Level 3 - A1a": {
                "Level 4 - A1a1": {},
                "Level 4 - A1a2": {},
            },
            "Level 3 - A1b": {
                "Level 4 - A1b1": {},
                "Level 4 - A1b2": {},
            },
        },
        "Level 2 - A2": {
            "Level 3 - A2a": {
                "Level 4 - A2a1": {},
                "Level 4 - A2a2": {},
            },
            "Level 3 - A2b": {
                "Level 4 - A2b1": {},
                "Level 4 - A2b2": {},
            },
        },
    },
    "Level 1 - B": {
        "Level 2 - B1": {
            "Level 3 - B1a": {
                "Level 4 - B1a1": {},
                "Level 4 - B1a2": {},
            },
            "Level 3 - B1b": {
                "Level 4 - B1b1": {},
                "Level 4 - B1b2": {},
            },
        },
        "Level 2 - B2": {
            "Level 3 - B2a": {
                "Level 4 - B2a1": {},
                "Level 4 - B2a2": {},
            },
            "Level 3 - B2b": {
                "Level 4 - B2b1": {},
                "Level 4 - B2b2": {},
            },
        },
    }
}

# Giao diện Streamlit
st.set_page_config(page_title="Indented Tree Viewer", layout="centered")
st.title("🌲 Tree Viewer with Indentation and HTML `<details>`")
st.write("Cây được thụt lề đúng theo cấp bậc:")

# Render cây ra HTML
tree_html = render_details_tree(tree_data)
st.markdown(tree_html, unsafe_allow_html=True)

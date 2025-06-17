# import streamlit as st
# import json
# st.set_page_config(page_title="Indented Tree Viewer", layout="centered")



# """ TREE IN STREAMLIT """
# def render_details_tree(data, level=0):
#     html = ""
#     margin = level * 20  # mỗi cấp cách trái 20px

#     for key, value in data.items():
#         if isinstance(value, dict) and value:
#             html += f'<div style="margin-left:{margin}px;">'
#             html += f"<details>\n"
#             html += f"<summary>{key}</summary>\n"
#             html += render_details_tree(value, level + 1)
#             html += f"</details>\n"
#             html += f"</div>"
#         elif isinstance(value, dict) and not value:
#             html += f'<div style="margin-left:{margin}px;">{key}</div>\n'
#         else:
#             html += f'<div style="margin-left:{margin}px;">{key}: {value}</div>\n'

#     return html


# """ MERMAID GRAPH """
# def dict_to_mermaid(data, parent=None, lines=None):
#     if lines is None:
#         lines = ["graph TD"]

#     for key, value in data.items():
#         node_id = key.replace(" ", "_").replace("-", "_")  # Mermaid không hỗ trợ dấu cách/dấu -
#         label = f'"{key}"'

#         if parent:
#             parent_id = parent.replace(" ", "_").replace("-", "_")
#             lines.append(f"    {parent_id} --> {node_id}")

#         if isinstance(value, dict):
#             dict_to_mermaid(value, key, lines)

#     return "\n".join(lines)

# def render_mermaid_html(mermaid_code: str) -> str:
#     return f"""
#     <script type="module">
#       import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
#       mermaid.initialize({{ startOnLoad: true }});
#     </script>
#     <div class="mermaid">
#     {mermaid_code}
#     </div>
#     """


# """ TEST graph khác """
# def dict_to_cytoscape(data, parent_id=None, elements=None, counter=None):
#     if elements is None:
#         elements = []
#     if counter is None:
#         counter = [0]

#     for key, value in data.items():
#         node_id = f"n{counter[0]}"
#         elements.append({
#             "data": {"id": node_id, "label": key}
#         })
#         if parent_id:
#             elements.append({
#                 "data": {"source": parent_id, "target": node_id}
#             })
#         counter[0] += 1
#         if isinstance(value, dict):
#             dict_to_cytoscape(value, node_id, elements, counter)
#     return elements


# """ DISPLAY UI """
# # Dữ liệu mẫu 4 cấp - mỗi cấp có 2 node con
# tree_data = {
#     "Level 1 - A": {
#         "Level 2 - A1": {
#             "Level 3 - A1a": {
#                 "Level 4 - A1a1": {},
#                 "Level 4 - A1a2": {},
#             },
#             "Level 3 - A1b": {
#                 "Level 4 - A1b1": {},
#                 "Level 4 - A1b2": {},
#             },
#         },
#         "Level 2 - A2": {
#             "Level 3 - A2a": {
#                 "Level 4 - A2a1": {},
#                 "Level 4 - A2a2": {},
#             },
#             "Level 3 - A2b": {
#                 "Level 4 - A2b1": {},
#                 "Level 4 - A2b2": {},
#             },
#         },
#     },
#     "Level 1 - B": {
#         "Level 2 - B1": {
#             "Level 3 - B1a": {
#                 "Level 4 - B1a1": {},
#                 "Level 4 - B1a2": {},
#             },
#             "Level 3 - B1b": {
#                 "Level 4 - B1b1": {},
#                 "Level 4 - B1b2": {},
#             },
#         },
#         "Level 2 - B2": {
#             "Level 3 - B2a": {
#                 "Level 4 - B2a1": {},
#                 "Level 4 - B2a2": {},
#             },
#             "Level 3 - B2b": {
#                 "Level 4 - B2b1": {},
#                 "Level 4 - B2b2": {},
#             },
#         },
#     }
# }


# # Giao diện Streamlit
# # st.set_page_config(page_title="Indented Tree Viewer", layout="centered")
# st.title("🌲 Tree Viewer with Indentation and HTML `<details>`")
# st.write("Cây được thụt lề đúng theo cấp bậc:")


# # Render cây ra HTML
# tree_html = render_details_tree(tree_data)
# st.markdown(tree_html, unsafe_allow_html=True)


# # Tạo mermaid_code từ cây như trước
# mermaid_code = dict_to_mermaid(tree_data)
# mermaid_html = render_mermaid_html(mermaid_code)
# st.markdown("### 🌐 Mermaid Tree Diagram")
# st.components.v1.html(mermaid_html, height=600, scrolling=True)


# # Tạo danh sách node + edge
# elements = dict_to_cytoscape(tree_data)
# html_code = f"""
# <!DOCTYPE html>
# <html>
#   <head>
#     <meta charset="utf-8">
#     <script src="https://unpkg.com/cytoscape@3.23.0/dist/cytoscape.min.js"></script>
#   </head>
#   <body>
#     <div id="cy" style="width: 100%; height: 700px;"></div>
#     <script>
#       var cy = cytoscape({{
#         container: document.getElementById('cy'),
#         elements: {json.dumps(elements)},
#         layout: {{
#           name: 'breadthfirst',
#           directed: true,
#           padding: 30,
#           spacingFactor: 1.3,
#           animate: false
#         }},
#         style: [
#           {{
#             selector: 'node',
#             style: {{
#               'shape': 'rectangle',
#               'content': 'data(label)',
#               'text-valign': 'center',
#               'text-halign': 'center',
#               'background-color': '#A8D0E6',
#               'color': '#000',
#               'width': 'label',
#               'height': 'label',
#               'padding': '8px',
#               'font-size': '14px',
#               'border-width': 1,
#               'border-color': '#333'
#             }}
#           }},
#           {{
#             selector: 'edge',
#             style: {{
#               'width': 2,
#               'line-color': '#ccc',
#               'target-arrow-shape': 'triangle',
#               'target-arrow-color': '#ccc',
#               'curve-style': 'bezier'
#             }}
#           }}
#         ],
#         userZoomingEnabled: true,
#         userPanningEnabled: true,
#         boxSelectionEnabled: false,
#         autoungrabify: true  // ❗️Khoá kéo node
#       }});
#     </script>
#   </body>
# </html>
# """
# st.markdown("🌳 Interactive Tree with Zoom (Cytoscape.js)")
# st.components.v1.html(html_code, height=650, scrolling=True)

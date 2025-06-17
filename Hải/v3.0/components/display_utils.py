import json
import streamlit as st

# Hàm dựng HTML <details> tree
def render_details_tree(data, level=0):
    html = ""

    for key, value in data.items():
        has_children = isinstance(value, dict) and value

        html += f'''
        <div class="tree-node level-{level}">
            <div class="tree-line"></div>
            <details{' open' if level == 0 else ''}>
                <summary>{key}</summary>
        '''

        if has_children:
            html += render_details_tree(value, level + 1)

        html += '''
            </details>
        </div>
        '''

    return html


# Hàm tạo dữ liệu Cytoscape từ dict lồng dict
def dict_to_cytoscape(data, parent_id=None, elements=None, counter=None):
    if elements is None:
        elements = []
    if counter is None:
        counter = [0]

    for key, value in data.items():
        node_id = f"n{counter[0]}"
        elements.append({"data": {"id": node_id, "label": key}})
        if parent_id:
            elements.append({"data": {"source": parent_id, "target": node_id}})
        counter[0] += 1
        if isinstance(value, dict):
            dict_to_cytoscape(value, node_id, elements, counter)
    return elements

# Hàm hiển thị Cytoscape trong Streamlit
def render_cytoscape(elements):
    html_code = f"""
    <html>
    <head>
        <script src="https://unpkg.com/cytoscape@3.23.0/dist/cytoscape.min.js"></script>
    </head>
    <body>
        <div id="cy" style="width: 100%; height: 700px;"></div>
        <script>
            var cy = cytoscape({{
                container: document.getElementById('cy'),
                elements: {json.dumps(elements)},
                layout: {{
                    name: 'breadthfirst',
                    directed: true,
                    padding: 30,
                    spacingFactor: 1.3
                }},
                style: [
                    {{
                        selector: 'node',
                        style: {{
                            'shape': 'rectangle',
                            'content': 'data(label)',
                            'text-valign': 'center',
                            'text-halign': 'center',
                            'background-color': '#A8D0E6',
                            'color': '#000',
                            'font-size': '14px',
                            'padding': '8px',
                            'border-width': 1,
                            'border-color': '#333'
                        }}
                    }},
                    {{
                        selector: 'edge',
                        style: {{
                            'width': 2,
                            'line-color': '#ccc',
                            'target-arrow-shape': 'triangle',
                            'target-arrow-color': '#ccc',
                            'curve-style': 'bezier'
                        }}
                    }}
                ],
                userZoomingEnabled: true,
                userPanningEnabled: true,
                autoungrabify: true
            }});
        </script>
    </body>
    </html>
    """
    st.components.v1.html(html_code, height=700, scrolling=True)

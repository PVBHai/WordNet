import json
import streamlit as st

# Hàm dựng HTML <details> tree
def render_details_tree(data, level=0, max_recursive=None):
    html = ""
    indent_px = level * 15

    for node in data:
        has_children = isinstance(node.children, list) and bool(node.children)
        examples_str = ", ".join(node._example) if isinstance(node._example, list) and node._example else "không có"
        ili_display = node._ili
        
        # Check if this is a leaf node:
        # 1. Node at max recursive level (reached search depth limit), OR
        # 2. Node has no children (actual leaf in the data)
        is_leaf_node = (max_recursive is not None and node._relative_level == max_recursive - 1) or not has_children
        
        # New format: (<level>) {<lemmas>} [<synset_id> (<ili>)]: <definition> (vd: <examples>)
        # Styling: lemmas = bold, synset_id = bold+italic, examples = italic, others = normal
        display_text = f"({node._level - 1}) {{<strong>{node._lemmas}</strong>}} [<em>{node._synset.id}</em> ({ili_display})]: <strong>{node._definition}</strong> (vd: <em>{examples_str}</em>)"

        # If it's a leaf node, render without <details> tag but with placeholder for alignment
        if is_leaf_node:
            html += f'''
<div class="tree-node leaf-node" style="margin-left:{indent_px}px;">
    <div class="tree-line"></div>
    <div class="leaf-content">
        <span class="leaf-placeholder">▶</span>{display_text}
    </div>
</div>
'''.strip()
        else:
            # Regular node with <details> tag
            html += f'''
<div class="tree-node" style="margin-left:{indent_px}px;">
    <div class="tree-line"></div>
    <details>
        <summary>
            {display_text}
        </summary>
'''.strip()

            if has_children:
                html += render_details_tree(node.children, level + 1, max_recursive)

            html += '</details></div>'

    return html

# Hàm hiển thị Tree HTML trong Streamlit
def get_tree_view_css():
    return """
    <style>
    .tree-node {
        position: relative;
        padding-left: 20px;
        margin: 4px 0;
    }

    .tree-node .tree-line {
        position: absolute;
        top: 0;
        bottom: 0;
        left: 10px;
        width: 1px;
        background-color: #ccc;
    }

    .tree-node summary {
        list-style: none;
        cursor: pointer;
        font-weight: normal;
        padding-left: 5px;
    }

    .tree-node summary::-webkit-details-marker {
        display: none;
    }

    .tree-node details > summary::before {
        content: "▶";
        display: inline-block;
        transform: rotate(0deg);
        margin-right: 5px;
        transition: transform 0.2s ease;
    }

    .tree-node details[open] > summary::before {
        transform: rotate(90deg);
        content: "▼";
    }
    
    /* Style for leaf nodes - placeholder triangle for alignment */
    .tree-node.leaf-node .leaf-content {
        padding-left: 0px;
        font-weight: normal;
    }
    
    .tree-node.leaf-node .leaf-placeholder {
        display: inline-block;
        margin-right: 5px;
        margin-left: 5px;
        opacity: 0;
        width: 0.7em;
        text-align: center;
        /* Match exact properties of the real triangle for perfect alignment */
    }

    .node-extra {
        color: #666;
        font-size: 13px;
        padding-left: 20px;
        padding-top: 4px;
    }

    </style>
    """

# Hàm tạo dữ liệu Cytoscape từ dict lồng dict
def nodefamily_to_cytoscape_elements(nodes, parent_id=None, elements=None, seen=None, added_edges=None):
    if elements is None:
        elements = []
    if seen is None:
        seen = {}
    if added_edges is None:
        added_edges = set()

    for node in nodes:
        # synset_id = node._synset.name()
        synset_id = node._synset.id

        # Gán ID duy nhất cho node theo synset name
        if synset_id in seen:
            node_id = seen[synset_id]
        else:
            node_id = f"n{len(seen)}"
            seen[synset_id] = node_id
            # lemmas_label = ', '.join([l.name() for l in node._synset.lemmas()])
            lemmas_label = ', '.join(node._synset.lemmas())
            
            # Format examples
            examples_str = ", ".join(node._example) if isinstance(node._example, list) and node._example else "không có"
            
            # Get ILI
            ili_display = node._ili if node._ili else ""
            
            # Create label: (synset_id) lemmas
            label = f"({synset_id})\n{lemmas_label}"
            
            # Create tooltip content
            tooltip = f"Mục từ: {lemmas_label}\\nSynset ID: {synset_id} ({ili_display})\\nĐịnh nghĩa: {node._definition}\\nVí dụ: {examples_str}"
            
            elements.append({
                "data": {
                    "id": node_id, 
                    "label": label,
                    "synset_id": synset_id,
                    "lemmas": lemmas_label,
                    "definition": node._definition,
                    "examples": examples_str,
                    "ili": ili_display,
                    "tooltip": tooltip
                },
                "classes": "wordnode"
            })

        # Thêm edge nếu chưa có trong added_edges
        if parent_id and (parent_id, node_id) not in added_edges:
            elements.append({
                "data": {"source": parent_id, "target": node_id}
            })
            added_edges.add((parent_id, node_id))

        # Duyệt đệ quy các con
        if node.children:
            nodefamily_to_cytoscape_elements(
                node.children,
                parent_id=node_id,
                elements=elements,
                seen=seen,
                added_edges=added_edges
            )

    return elements



# Hàm hiển thị Cytoscape trong Streamlit
def render_cytoscape(elements):
    html_code = f"""
    <html>
    <head>
        <script src="https://unpkg.com/cytoscape@3.23.0/dist/cytoscape.min.js"></script>
        <style>
            #tooltip {{
                display: none;
                position: absolute;
                background-color: rgba(0, 0, 0, 0.85);
                color: white;
                padding: 12px;
                border-radius: 6px;
                font-size: 13px;
                max-width: 350px;
                z-index: 9999;
                pointer-events: none;
                line-height: 1.6;
                white-space: pre-wrap;
                word-wrap: break-word;
            }}
        </style>
    </head>
    <body>
        <div id="cy" style="width: 100%; height: 500px;"></div>
        <div id="tooltip"></div>
        <script>
            var cy = cytoscape({{
                container: document.getElementById('cy'),
                elements: {json.dumps(elements)},
                layout: {{
                    name: 'breadthfirst',
                    directed: true,
                    padding: 40,
                    spacingFactor: 1
                }},
                style: [
                    {{
                        selector: 'node',
                        style: {{
                            'shape': 'rectangle',
                            'label': 'data(label)',
                            'text-valign': 'center',
                            'text-halign': 'center',
                            'background-color': '#A8D0E6',
                            'color': '#000',
                            'padding': '8px',
                            'font-size': '14px',
                            'border-width': 1,
                            'border-color': '#333',
                            'width': 'label',
                            'height': 'label',
                            'text-wrap': 'wrap',
                            'text-max-width': 100,
                            'font-weight': 'normal'
                        }}
                    }},
                    {{
                        selector: 'edge',
                        style: {{
                            'width': 5,
                            'line-color': '#ccc',
                            'target-arrow-shape': 'triangle',
                            'target-arrow-color': '#ccc',
                            'curve-style': 'bezier',
                            'arrow-scale': 2,
                            'target-distance-from-node': 2
                        }}
                    }}
                ],
                userPanningEnabled: true,
                userZoomingEnabled: true,
                boxSelectionEnabled: true,
                autoungrabify: false
            }});
            
            // Tooltip functionality
            var tooltip = document.getElementById('tooltip');
            
            cy.on('mouseover', 'node', function(evt) {{
                var node = evt.target;
                var data = node.data();
                
                // Create formatted tooltip content
                var tooltipContent = 
                    '• Mục từ: ' + data.lemmas + '\\n' +
                    '• Synset ID: ' + data.synset_id + (data.ili ? ' (' + data.ili + ')' : '') + '\\n' +
                    '• Định nghĩa: ' + data.definition + '\\n' +
                    '• Ví dụ: ' + data.examples;
                
                tooltip.innerHTML = tooltipContent;
                tooltip.style.display = 'block';
            }});
            
            cy.on('mousemove', 'node', function(evt) {{
                tooltip.style.left = evt.originalEvent.pageX + 15 + 'px';
                tooltip.style.top = evt.originalEvent.pageY + 15 + 'px';
            }});
            
            cy.on('mouseout', 'node', function(evt) {{
                tooltip.style.display = 'none';
            }});
        </script>
    </body>
    </html>
    """
    st.components.v1.html(html_code, height=500, scrolling=False)



#!/usr/bin/env python3
"""
Convert Markdown Architecture Document to HTML (for PDF conversion)
"""

import re
import os

def convert_mermaid_to_description(content):
    """Convert Mermaid diagrams to descriptive text for PDF"""
    
    # Replace mermaid code blocks with descriptive text
    mermaid_patterns = [
        (r'```mermaid\ngraph TB\n(.*?)\n```', lambda m: create_graph_description(m.group(1), "Top-Bottom")),
        (r'```mermaid\ngraph LR\n(.*?)\n```', lambda m: create_graph_description(m.group(1), "Left-Right")),
        (r'```mermaid\nsequenceDiagram\n(.*?)\n```', lambda m: create_sequence_description(m.group(1))),
    ]
    
    for pattern, replacement in mermaid_patterns:
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    return content

def create_graph_description(graph_content, layout):
    """Create a text description of a mermaid graph"""
    lines = graph_content.strip().split('\n')
    description = f"\n**System Diagram ({layout} Layout)**\n\n"
    
    # Extract nodes and connections
    nodes = []
    connections = []
    
    for line in lines:
        line = line.strip()
        if '-->' in line or '<-->' in line:
            connections.append(line)
        elif line.startswith('subgraph'):
            description += f"📦 **{line.replace('subgraph', '').strip().strip('\"')}**\n"
        elif '[' in line and ']' in line:
            # Extract node definition
            parts = line.split('[')
            if len(parts) > 1:
                node_id = parts[0].strip()
                node_label = parts[1].split(']')[0]
                nodes.append((node_id, node_label))
    
    if nodes:
        description += "\n**Components:**\n"
        for node_id, node_label in nodes:
            description += f"- {node_label.replace('<br>', ' ')}\n"
    
    if connections:
        description += "\n**Connections:**\n"
        for conn in connections[:10]:  # Limit to first 10 connections
            conn_clean = conn.replace('-->', '→').replace('<-->', '↔')
            description += f"- {conn_clean}\n"
    
    return description + "\n"

def create_sequence_description(seq_content):
    """Create a text description of a sequence diagram"""
    lines = seq_content.strip().split('\n')
    description = "\n**Process Flow Sequence**\n\n"
    
    participants = []
    interactions = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('participant'):
            participant = line.replace('participant', '').strip()
            participants.append(participant)
        elif '->>' in line or '-->>' in line:
            interactions.append(line)
    
    if participants:
        description += "**Participants:**\n"
        for participant in participants:
            description += f"- {participant}\n"
        description += "\n"
    
    if interactions:
        description += "**Process Steps:**\n"
        for i, interaction in enumerate(interactions, 1):
            interaction_clean = interaction.replace('->>', ' → ').replace('-->>', ' → ')
            description += f"{i}. {interaction_clean}\n"
    
    return description + "\n"

def markdown_to_html(markdown_content):
    """Convert markdown to HTML with styling"""
    
    # Convert mermaid diagrams first
    html_content = convert_mermaid_to_description(markdown_content)
    
    # Basic markdown to HTML conversion
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html_content, flags=re.MULTILINE)
    
    # Convert **bold** to <strong>
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    
    # Convert *italic* to <em>
    html_content = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html_content)
    
    # Convert code blocks
    html_content = re.sub(r'```yaml\n(.*?)\n```', r'<pre class="code yaml"><code>\1</code></pre>', html_content, flags=re.DOTALL)
    html_content = re.sub(r'```python\n(.*?)\n```', r'<pre class="code python"><code>\1</code></pre>', html_content, flags=re.DOTALL)
    html_content = re.sub(r'```\n(.*?)\n```', r'<pre class="code"><code>\1</code></pre>', html_content, flags=re.DOTALL)
    
    # Convert inline code
    html_content = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_content)
    
    # Convert lists
    html_content = re.sub(r'^- (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', html_content, flags=re.DOTALL)
    html_content = re.sub(r'</ul>\s*<ul>', '', html_content)
    
    # Convert links
    html_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html_content)
    
    # Convert line breaks
    html_content = html_content.replace('\n\n', '</p><p>')
    html_content = '<p>' + html_content + '</p>'
    html_content = re.sub(r'<p></p>', '', html_content)
    html_content = re.sub(r'<p>(<h[1-6]>)', r'\1', html_content)
    html_content = re.sub(r'(</h[1-6]>)</p>', r'\1', html_content)
    html_content = re.sub(r'<p>(<ul>)', r'\1', html_content)
    html_content = re.sub(r'(</ul>)</p>', r'\1', html_content)
    html_content = re.sub(r'<p>(<pre)', r'\1', html_content)
    html_content = re.sub(r'(</pre>)</p>', r'\1', html_content)
    
    return html_content

def create_html_document(title, content):
    """Create a complete HTML document with CSS styling"""
    
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            font-size: 2.5em;
            margin-bottom: 30px;
        }}
        
        h2 {{
            color: #2c3e50;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 8px;
            font-size: 2em;
            margin-top: 40px;
            margin-bottom: 20px;
        }}
        
        h3 {{
            color: #34495e;
            font-size: 1.5em;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        
        h4 {{
            color: #34495e;
            font-size: 1.3em;
            margin-top: 25px;
            margin-bottom: 12px;
        }}
        
        p {{
            margin-bottom: 15px;
            text-align: justify;
        }}
        
        ul {{
            margin-bottom: 15px;
        }}
        
        li {{
            margin-bottom: 5px;
            list-style-type: disc;
            margin-left: 20px;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        pre.code {{
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 16px;
            overflow-x: auto;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 14px;
            line-height: 1.45;
            margin: 15px 0;
        }}
        
        code {{
            background-color: #f1f3f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.9em;
        }}
        
        .diagram-description {{
            background-color: #f8f9ff;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 20px 0;
            border-radius: 0 6px 6px 0;
        }}
        
        strong {{
            color: #2c3e50;
            font-weight: 600;
        }}
        
        em {{
            color: #34495e;
            font-style: italic;
        }}
        
        .page-break {{
            page-break-before: always;
        }}
        
        @media print {{
            body {{
                font-size: 12px;
                line-height: 1.4;
            }}
            
            h1 {{
                font-size: 2em;
            }}
            
            h2 {{
                font-size: 1.6em;
                page-break-after: avoid;
            }}
            
            h3 {{
                font-size: 1.4em;
                page-break-after: avoid;
            }}
            
            pre.code {{
                page-break-inside: avoid;
                font-size: 10px;
            }}
            
            table {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    {content}
</body>
</html>
"""
    return html_template

def main():
    """Main conversion function"""
    
    # Read the markdown file
    with open('SOLUTION_ARCHITECTURE.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert to HTML
    html_content = markdown_to_html(markdown_content)
    
    # Create complete HTML document
    html_document = create_html_document("G1 Solution Architecture", html_content)
    
    # Write HTML file
    with open('SOLUTION_ARCHITECTURE.html', 'w', encoding='utf-8') as f:
        f.write(html_document)
    
    print("✅ HTML version created: SOLUTION_ARCHITECTURE.html")
    print("📄 To create PDF: Open the HTML file in a browser and use 'Print to PDF'")
    print("🎯 For best results, use Chrome/Edge browser with these print settings:")
    print("   - Paper size: A4 or Letter")
    print("   - Margins: Minimum")
    print("   - Options: Background graphics enabled")

if __name__ == "__main__":
    main()
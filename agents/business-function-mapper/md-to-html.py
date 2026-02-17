#!/usr/bin/env python3
"""
Markdown to HTML Converter for Clean Core Assessment Reports

Converts markdown reports to professionally styled HTML with:
- Responsive design
- Print-friendly styles
- Mermaid chart support
- Professional color scheme

Usage:
    python3 md-to-html.py <input.md> <output.html>
"""

import sys
import os
import re
import tempfile
from pathlib import Path

# Professional HTML template with embedded CSS
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        :root {{
            --primary-color: #232f3e;
            --secondary-color: #ff9900;
            --accent-color: #0073bb;
            --success-color: #1e8e3e;
            --warning-color: #f9a825;
            --danger-color: #d93025;
            --text-color: #16191f;
            --text-light: #545b64;
            --bg-color: #ffffff;
            --bg-light: #f7f8f9;
            --border-color: #d5dbdb;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px 40px;
            background: var(--bg-color);
        }}

        /* Header styling */
        h1 {{
            color: var(--primary-color);
            border-bottom: 3px solid var(--secondary-color);
            padding-bottom: 15px;
            margin-top: 0;
            font-size: 2em;
        }}

        h2 {{
            color: var(--primary-color);
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 10px;
            margin-top: 40px;
            font-size: 1.5em;
        }}

        h3 {{
            color: var(--accent-color);
            margin-top: 30px;
            font-size: 1.2em;
        }}

        h4 {{
            color: var(--text-color);
            margin-top: 20px;
        }}

        /* Table styling */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.95em;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        thead tr {{
            background-color: var(--primary-color);
            color: white;
            text-align: left;
        }}

        th, td {{
            padding: 12px 15px;
            border: 1px solid var(--border-color);
        }}

        tbody tr {{
            background-color: var(--bg-color);
        }}

        tbody tr:nth-of-type(even) {{
            background-color: var(--bg-light);
        }}

        tbody tr:hover {{
            background-color: #e8f4fc;
        }}

        /* Level indicators */
        .level-a {{ color: var(--success-color); font-weight: bold; }}
        .level-b {{ color: var(--accent-color); font-weight: bold; }}
        .level-c {{ color: var(--warning-color); font-weight: bold; }}
        .level-d {{ color: var(--danger-color); font-weight: bold; }}

        /* Code blocks */
        pre {{
            background-color: #1e1e1e;
            color: #d4d4d4;
            padding: 15px 20px;
            border-radius: 6px;
            overflow-x: auto;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
        }}

        code {{
            background-color: var(--bg-light);
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
        }}

        pre code {{
            background: none;
            padding: 0;
        }}

        /* Lists */
        ul, ol {{
            padding-left: 25px;
        }}

        li {{
            margin-bottom: 8px;
        }}

        /* Checkboxes */
        input[type="checkbox"] {{
            margin-right: 8px;
            transform: scale(1.2);
        }}

        /* Blockquotes */
        blockquote {{
            border-left: 4px solid var(--secondary-color);
            margin: 20px 0;
            padding: 10px 20px;
            background-color: var(--bg-light);
            color: var(--text-light);
        }}

        /* Horizontal rules */
        hr {{
            border: none;
            border-top: 1px solid var(--border-color);
            margin: 30px 0;
        }}

        /* Links */
        a {{
            color: var(--accent-color);
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        /* Strong/Bold */
        strong {{
            color: var(--text-color);
        }}

        /* Mermaid charts */
        .mermaid {{
            text-align: center;
            margin: 20px 0;
        }}

        /* Report metadata box */
        table:first-of-type {{
            width: auto;
            min-width: 400px;
            box-shadow: none;
            border: 2px solid var(--primary-color);
        }}

        /* Footer */
        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid var(--border-color);
            color: var(--text-light);
            font-size: 0.9em;
            text-align: center;
        }}

        /* Print styles */
        @media print {{
            body {{
                padding: 0;
                max-width: none;
            }}

            h1, h2, h3 {{
                page-break-after: avoid;
            }}

            table, pre {{
                page-break-inside: avoid;
            }}

            .mermaid {{
                page-break-inside: avoid;
            }}

            a {{
                color: var(--text-color);
            }}

            @page {{
                margin: 2cm;
            }}
        }}

        /* Responsive design */
        @media (max-width: 768px) {{
            body {{
                padding: 15px;
            }}

            table {{
                font-size: 0.85em;
            }}

            th, td {{
                padding: 8px 10px;
            }}
        }}
    </style>
</head>
<body>
    {content}

    <script>
        // Initialize Mermaid
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});

        // Add level classes to table cells
        document.querySelectorAll('td').forEach(cell => {{
            const text = cell.textContent.trim();
            if (text.startsWith('A ') || text === 'A' || text.includes('Level A')) {{
                cell.classList.add('level-a');
            }} else if (text.startsWith('B ') || text === 'B' || text.includes('Level B')) {{
                cell.classList.add('level-b');
            }} else if (text.startsWith('C ') || text === 'C' || text.includes('Level C')) {{
                cell.classList.add('level-c');
            }} else if (text.startsWith('D ') || text === 'D' || text.includes('Level D')) {{
                cell.classList.add('level-d');
            }}
        }});
    </script>
</body>
</html>
"""


def convert_markdown_to_html(md_content: str) -> str:
    """Convert markdown content to HTML."""
    html = md_content

    # Handle code blocks first (to protect them from other transformations)
    code_blocks = []
    def save_code_block(match):
        code_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(code_blocks) - 1}__"

    # Save fenced code blocks
    html = re.sub(r'```(\w*)\n(.*?)```', save_code_block, html, flags=re.DOTALL)

    # Handle Mermaid blocks specially
    for i, block in enumerate(code_blocks):
        if block.startswith('```mermaid'):
            mermaid_content = block[10:-3].strip()
            code_blocks[i] = f'<div class="mermaid">\n{mermaid_content}\n</div>'
        else:
            lang_match = re.match(r'```(\w*)\n', block)
            lang = lang_match.group(1) if lang_match else ''
            code_content = re.sub(r'```\w*\n', '', block)[:-3]
            code_content = code_content.replace('<', '&lt;').replace('>', '&gt;')
            code_blocks[i] = f'<pre><code class="language-{lang}">{code_content}</code></pre>'

    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    # Headers
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # Bold and italic
    html = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)

    # Horizontal rules
    html = re.sub(r'^---+$', '<hr>', html, flags=re.MULTILINE)

    # Tables
    def convert_table(match):
        lines = match.group(0).strip().split('\n')
        if len(lines) < 2:
            return match.group(0)

        # Parse header
        header_cells = [cell.strip() for cell in lines[0].split('|')[1:-1]]

        # Skip separator line

        # Parse body rows
        body_rows = []
        for line in lines[2:]:
            if '|' in line:
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                body_rows.append(cells)

        # Build HTML table
        table_html = '<table>\n<thead>\n<tr>\n'
        for cell in header_cells:
            table_html += f'<th>{cell}</th>\n'
        table_html += '</tr>\n</thead>\n<tbody>\n'

        for row in body_rows:
            table_html += '<tr>\n'
            for cell in row:
                table_html += f'<td>{cell}</td>\n'
            table_html += '</tr>\n'

        table_html += '</tbody>\n</table>'
        return table_html

    # Match tables (lines starting with |)
    html = re.sub(r'(\|[^\n]+\|\n\|[-:| ]+\|\n(?:\|[^\n]+\|\n?)+)', convert_table, html)

    # Unordered lists
    def convert_ul(match):
        items = match.group(0).strip().split('\n')
        list_html = '<ul>\n'
        for item in items:
            item_text = re.sub(r'^[-*] ', '', item.strip())
            # Handle checkboxes
            if item_text.startswith('[ ]'):
                item_text = f'<input type="checkbox" disabled> {item_text[3:].strip()}'
            elif item_text.startswith('[x]') or item_text.startswith('[X]'):
                item_text = f'<input type="checkbox" checked disabled> {item_text[3:].strip()}'
            list_html += f'<li>{item_text}</li>\n'
        list_html += '</ul>'
        return list_html

    html = re.sub(r'(^[-*] .+$\n?)+', convert_ul, html, flags=re.MULTILINE)

    # Ordered lists
    def convert_ol(match):
        items = match.group(0).strip().split('\n')
        list_html = '<ol>\n'
        for item in items:
            item_text = re.sub(r'^\d+\. ', '', item.strip())
            list_html += f'<li>{item_text}</li>\n'
        list_html += '</ol>'
        return list_html

    html = re.sub(r'(^\d+\. .+$\n?)+', convert_ol, html, flags=re.MULTILINE)

    # Blockquotes
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)

    # Paragraphs - wrap remaining text blocks
    lines = html.split('\n')
    result = []
    in_paragraph = False
    paragraph_content = []

    for line in lines:
        stripped = line.strip()

        # Check if line is already HTML or special
        is_html = (stripped.startswith('<') and not stripped.startswith('&lt;')) or \
                  stripped.startswith('__CODE_BLOCK_') or \
                  stripped == ''

        if is_html:
            if in_paragraph and paragraph_content:
                result.append('<p>' + ' '.join(paragraph_content) + '</p>')
                paragraph_content = []
                in_paragraph = False
            result.append(line)
        else:
            in_paragraph = True
            paragraph_content.append(stripped)

    if paragraph_content:
        result.append('<p>' + ' '.join(paragraph_content) + '</p>')

    html = '\n'.join(result)

    # Restore code blocks
    for i, block in enumerate(code_blocks):
        html = html.replace(f'__CODE_BLOCK_{i}__', block)

    # Clean up empty paragraphs
    html = re.sub(r'<p>\s*</p>', '', html)

    return html


def main():
    # Maximum input size to prevent ReDoS attacks (10MB)
    MAX_INPUT_SIZE = 10 * 1024 * 1024

    if len(sys.argv) != 3:
        print("Usage: python3 md-to-html.py <input.md> <output.html>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    # Check file size before reading to prevent memory issues
    file_size = input_path.stat().st_size
    if file_size > MAX_INPUT_SIZE:
        print(f"Error: Input file too large ({file_size:,} bytes, max {MAX_INPUT_SIZE:,} bytes)")
        sys.exit(1)

    # Read markdown content
    md_content = input_path.read_text(encoding='utf-8')

    # Extract title from first H1
    title_match = re.search(r'^# (.+)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else 'Clean Core Assessment Report'

    # Convert markdown to HTML
    html_content = convert_markdown_to_html(md_content)

    # Generate final HTML
    final_html = HTML_TEMPLATE.format(
        title=title,
        content=html_content
    )

    # Write output atomically
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(dir=output_path.parent, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(final_html)
        os.replace(temp_path, output_path)
    except Exception:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise

    print(f"HTML report generated: {output_path}")


if __name__ == '__main__':
    main()

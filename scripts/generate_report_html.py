from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import markdown
import re
import base64
import os
from datetime import datetime

md_path = "/Users/evanhan/.gemini/antigravity/brain/751a1504-dfcb-4a0e-b973-d2c16e782820/project_report.md"
html_path = "/Users/evanhan/项目/光伏项目/项目总结报告内容/project_report_v5.html"

# Read MD
with open(md_path, 'r') as f:
    text = f.read()

# Replace images with base64
def img_replacer(match):
    alt = match.group(1)
    path = match.group(2)
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            b64 = base64.b64encode(img_file.read()).decode('utf-8')
            ext = os.path.splitext(path)[1][1:]
            if ext == 'jpg': ext = 'jpeg'
            return f'<img src="data:image/{ext};base64,{b64}" alt="{alt}" class="embedded-img">'
    return match.group(0)

text = re.sub(r'!\[(.*?)\]\((.*?)\)', img_replacer, text)

# Replace mermaid code blocks
def mermaid_replacer(match):
    return f'<div class="mermaid">\n{match.group(1)}\n</div>'

text = re.sub(r'```mermaid\n(.*?)\n```', mermaid_replacer, text, flags=re.DOTALL)

# Insert Page Break BEFORE Section 3.2 to prevent awkward empty space
text = text.replace('### 3.2', '<div class="page-break"></div>\n\n### 3.2')

# Convert rest to HTML
html_content = markdown.markdown(text, extensions=['fenced_code', 'tables'])
html_content = re.sub(r'<h1.*?>.*?</h1>', '', html_content, count=1)

# HTML Template (B/W Professional + Split Diagrams)
today_str = datetime.now().strftime("%Y年%m月%d日")

template = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>SolarGuard Project Report</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
/* Academic / LaTeX Style - B/W */
@page {{
    size: A4;
    margin: 2.5cm;
}}
body {{ 
    font-family: "Times New Roman", Times, serif; 
    line-height: 1.6; 
    color: #000;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background: #fff;
}}

/* Cover Page */
.cover-page {{
    height: 90vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    page-break-after: always;
}}
.cover-title {{
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 34px;
    font-weight: bold;
    margin-bottom: 20px;
    color: #000;
}}
.cover-subtitle {{
    font-size: 24px;
    color: #333;
    margin-bottom: 80px;
    font-style: italic;
}}
.cover-team {{
    font-size: 20px;
    font-weight: bold;
    color: #000;
    margin-bottom: 15px;
    text-transform: uppercase;
    letter-spacing: 2px;
}}
.cover-meta {{
    font-size: 16px;
    color: #333;
    margin-top: 40px;
}}

/* Content Styling */
h1, h2, h3 {{ 
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; 
    color: #000; 
    font-weight: bold;
}}
h1 {{ 
    border-bottom: 2px solid #000; 
    padding-bottom: 10px; 
    font-size: 24px;
    text-align: center;
}}
h2 {{ 
    border-bottom: 1px solid #000; 
    padding-bottom: 5px; 
    margin-top: 30px; 
    font-size: 20px;
    page-break-after: avoid; /* Keep title with content */
}}
h3 {{ 
    font-size: 16px; 
    margin-top: 25px; 
    margin-bottom: 10px;
    font-style: italic;
}}
.page-break {{
    page-break-after: always;
    height: 1px;
    display: block;
}}
img {{ 
    display: block; 
    margin: 20px auto; 
    max-width: 95%; 
    border: 1px solid #ccc;
}}
.embedded-img {{
    max-width: 90%;
}}

/* Mermaid Optimization */
.mermaid {{ 
    text-align: center; 
    margin: 10px auto;
    width: 100%;
}}

/* Print Optimization */
@media print {{
  body {{ margin: 0; padding: 0; }}
  .cover-page {{ height: 100vh; margin: 0; }}
  h1 {{ page-break-before: always; }}
  
  /* Strictly prevent diagrams from breaking inside */
  .mermaid {{ 
      page-break-inside: avoid !important; 
      break-inside: avoid !important; 
      display: inline-block; 
      width: 100%;
  }}
  .mermaid svg {{
      page-break-inside: avoid !important;
      break-inside: avoid !important;
  }}
  
  .page-break {{ page-break-after: always; }}
  img, pre {{ page-break-inside: avoid; }}
  a {{ text-decoration: none; color: #000; }}
}}
</style>
</head>
<body>

<!-- Cover Page -->
<div class="cover-page">
    <div class="cover-title">SolarGuard: 分布式光伏 RWA 资产上链系统</div>
    <div class="cover-subtitle">项目总结与优化报告</div>
    
    <div style="margin-top: 100px;">
        <div class="cover-team">绿链未来 (GreenChain Future)</div>
        <div class="cover-meta">
            作者：Evan Han<br>
            日期：{today_str}
        </div>
    </div>
</div>

<!-- Report Content -->
<div class="report-content">
PLACEHOLDER
</div>

<script>
mermaid.initialize({{
    startOnLoad:true, 
    theme: 'base',
    themeVariables: {{
      primaryColor: '#ffffff',
      primaryTextColor: '#000000',
      primaryBorderColor: '#000000',
      lineColor: '#000000',
      tertiaryColor: '#f8f8f8',
      fontSize: '20px',     /* Even Larger font */
      fontFamily: 'arial'
    }},
    flowchart: {{
        useMaxWidth: true,
        htmlLabels: true,
        curve: 'basis',
        rankSpacing: 50,    /* More space between ranks */
        nodeSpacing: 50
    }}
}});
</script>
</body>
</html>
"""

final_html = template.replace("PLACEHOLDER", html_content)

with open(html_path, 'w') as f:
    f.write(final_html)

print(f"Generated {{html_path}}")

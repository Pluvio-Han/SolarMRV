from pathlib import Path

W, H = 1280, 1320
BG = '#FFFFFF'
PAGE = '#FAFBFA'
BORDER = '#D1D5DB'
LINE = '#6B7280'
TITLE = '#1F2937'
GREEN_FILL = '#E8F3EC'
GREEN_STROKE = '#2E6B4F'
GREEN_TEXT = '#123524'
BLUE_FILL = '#EAF0F8'
BLUE_STROKE = '#355C8A'
BLUE_TEXT = '#17324D'
AMBER_FILL = '#F7F3EA'
AMBER_STROKE = '#A46A1F'
AMBER_TEXT = '#5C3A10'

nodes = [
    ('风险识别', '识别技术、合规、市场与资源风险', 'green', (640, 180)),
    ('分类研判', '区分轻重缓急与当前阶段影响', 'blue', (930, 360)),
    ('控制措施', '形成分阶段、可执行的控制方案', 'green', (930, 700)),
    ('小场景验证', '以试点和材料验证真实有效性', 'amber', (640, 890)),
    ('持续修正', '根据政策与场景变化迭代调整', 'blue', (350, 700)),
    ('材料更新', '同步更新 BP、图表与对外表达', 'green', (350, 360)),
]

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
svg.append(f'<rect width="100%" height="100%" fill="{BG}"/>')
svg.append(f'''<defs>
  <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto" markerUnits="strokeWidth">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="{LINE}" opacity="0.95"/>
  </marker>
  <style>
    .title {{ font: 700 24px 'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif; fill: {TITLE}; }}
    .subtitle {{ font: 500 13px 'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif; fill: #6B7280; }}
    .node-title {{ font: 700 15px 'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif; text-anchor: middle; }}
    .node-text {{ font: 500 12px 'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif; text-anchor: middle; fill: #4B5563; }}
    .connector {{ stroke: {LINE}; stroke-width: 2; fill: none; stroke-linecap: round; marker-end: url(#arrow); }}
  </style>
</defs>''')

svg.append(f'<text x="{W/2}" y="42" text-anchor="middle" class="title">风险应对闭环图</text>')
svg.append(f'<text x="{W/2}" y="70" text-anchor="middle" class="subtitle">SolarGuard 通过识别、控制、验证与修正形成稳健推进闭环</text>')
svg.append(f'<rect x="80" y="110" width="1120" height="1120" rx="18" ry="18" fill="{PAGE}" stroke="{BORDER}" stroke-width="1.8"/>')

# center helper circle
svg.append(f'<circle cx="640" cy="530" r="250" fill="#FFFFFF" stroke="{BORDER}" stroke-width="1.4" stroke-dasharray="6 6"/>')

for title, desc, kind, (cx, cy) in nodes:
    if kind == 'green':
        fill, stroke, text = GREEN_FILL, GREEN_STROKE, GREEN_TEXT
    elif kind == 'blue':
        fill, stroke, text = BLUE_FILL, BLUE_STROKE, BLUE_TEXT
    else:
        fill, stroke, text = AMBER_FILL, AMBER_STROKE, AMBER_TEXT
    w, h = 300, 120
    x, y = cx - w/2, cy - h/2
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" ry="18" fill="{fill}" stroke="{stroke}" stroke-width="2.2"/>')
    svg.append(f'<text x="{cx}" y="{cy-8}" class="node-title" fill="{text}">{title}</text>')
    svg.append(f'<text x="{cx}" y="{cy+24}" class="node-text">{desc}</text>')

# loop connectors
points = [(640,180),(930,360),(930,700),(640,890),(350,700),(350,360),(640,180)]
for (x1,y1),(x2,y2) in zip(points, points[1:]):
    svg.append(f'<line x1="{x1}" y1="{y1+60 if y2>y1 else y1-60 if y2<y1 else y1}" x2="{x2}" y2="{y2-60 if y2>y1 else y2+60 if y2<y1 else y2}" class="connector"/>')

# center label
svg.append(f'<text x="640" y="525" text-anchor="middle" style="font:700 20px PingFang SC,Microsoft YaHei,Noto Sans SC,sans-serif; fill:{TITLE};">风险控制闭环</text>')
svg.append(f'<text x="640" y="555" text-anchor="middle" style="font:500 13px PingFang SC,Microsoft YaHei,Noto Sans SC,sans-serif; fill:#6B7280;">围绕真实原型、合规边界与小场景验证持续推进</text>')

svg.append('</svg>')
Path('/Users/evanhan/项目/光伏项目/比赛材料/素材库/最终图片/10_风险应对闭环图_v2.svg').write_text('\n'.join(svg), encoding='utf-8')

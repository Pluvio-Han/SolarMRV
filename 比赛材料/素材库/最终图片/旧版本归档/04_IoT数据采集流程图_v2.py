from pathlib import Path

W, H = 1280, 1960
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

steps = [
    ('真实光伏设备接入', 'green'),
    ('Modbus / RS485 通信读取', 'green'),
    ('关键字段解析与结构化提取', 'green'),
    ('时间戳与设备标识补全', 'green'),
    ('签名处理与可信封装', 'blue'),
    ('本地记录与CSV落盘', 'blue'),
    ('自动监测图表生成', 'blue'),
    ('联盟链存证写入', 'blue'),
    ('前端与报告输出', 'amber'),
]

colors = {
    'green': (GREEN_FILL, GREEN_STROKE, GREEN_TEXT),
    'blue': (BLUE_FILL, BLUE_STROKE, BLUE_TEXT),
    'amber': (AMBER_FILL, AMBER_STROKE, AMBER_TEXT),
}

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
svg.append(f'<rect width="100%" height="100%" fill="{BG}"/>')
svg.append(f'''<defs>
  <marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto" markerUnits="strokeWidth">
    <path d="M 0 0 L 9 4.5 L 0 9 z" fill="{LINE}" opacity="0.95"/>
  </marker>
  <style>
    .title {{ font: 700 24px 'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif; fill: {TITLE}; }}
    .subtitle {{ font: 500 13px 'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif; fill: #6B7280; }}
    .panel {{ fill: {PAGE}; stroke: {BORDER}; stroke-width: 1.8; }}
    .section-title {{ font: 700 17px 'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif; fill: {TITLE}; }}
    .node-text {{ font: 600 13px 'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif; text-anchor: middle; dominant-baseline: middle; }}
    .connector {{ stroke: {LINE}; stroke-width: 2; fill: none; stroke-linecap: round; marker-end: url(#arrow); }}
  </style>
</defs>''')

# title
svg.append(f'<text x="{W/2}" y="42" text-anchor="middle" class="title">IoT 数据采集与可信处理流程图</text>')
svg.append(f'<text x="{W/2}" y="70" text-anchor="middle" class="subtitle">从真实设备接入到链上存证与展示输出的关键流程</text>')

# panels
panel_x = 60
panel_w = W - 120
panel_h = 520
svg.append(f'<rect x="{panel_x}" y="110" width="{panel_w}" height="{panel_h}" rx="18" ry="18" class="panel"/>')
svg.append(f'<rect x="{panel_x}" y="670" width="{panel_w}" height="{panel_h}" rx="18" ry="18" class="panel"/>')
svg.append(f'<rect x="{panel_x}" y="1230" width="{panel_w}" height="{panel_h}" rx="18" ry="18" class="panel"/>')
svg.append(f'<text x="{W/2}" y="138" text-anchor="middle" class="section-title">设备接入与数据生成阶段</text>')
svg.append(f'<text x="{W/2}" y="698" text-anchor="middle" class="section-title">可信处理与自动监测阶段</text>')
svg.append(f'<text x="{W/2}" y="1258" text-anchor="middle" class="section-title">存证与应用输出阶段</text>')

x = W/2 - 190
w = 380
h = 72
ys = [190, 305, 420, 535, 750, 865, 980, 1310, 1490]

for (label, kind), y in zip(steps, ys):
    fill, stroke, text = colors[kind]
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" ry="16" fill="{fill}" stroke="{stroke}" stroke-width="2.2"/>')
    svg.append(f'<text x="{W/2}" y="{y+h/2+1}" class="node-text" fill="{text}">{label}</text>')

# arrows
pairs = [(190+72,305),(305+72,420),(420+72,535),(535+72,750),(750+72,865),(865+72,980),(980+72,1310),(1310+72,1490)]
for y1, y2 in pairs:
    svg.append(f'<line x1="{W/2}" y1="{y1}" x2="{W/2}" y2="{y2-14}" class="connector"/>')

# side notes
notes = [
    (860, '形成结构化、可追溯的原始数据记录'),
    (1470, '支撑前端展示、历史追溯与业务报告输出'),
]
for y, txt in notes:
    svg.append(f'<rect x="780" y="{y}" width="360" height="54" rx="14" ry="14" fill="#FFFFFF" stroke="{BORDER}" stroke-width="1.4"/>')
    svg.append(f'<text x="960" y="{y+29}" class="node-text" fill="#4B5563">{txt}</text>')
    svg.append(f'<line x1="760" y1="{y+27}" x2="690" y2="{y+27}" stroke="{BORDER}" stroke-width="1.6"/>')

svg.append('</svg>')
Path('/Users/evanhan/项目/光伏项目/比赛材料/素材库/最终图片/04_IoT数据采集流程图_v2.svg').write_text('\n'.join(svg), encoding='utf-8')

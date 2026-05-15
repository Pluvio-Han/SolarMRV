from pathlib import Path

W, H = 1280, 1700
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

sections = [
    ('设备接入与数据生成阶段', [
        ('真实光伏设备接入', 'green'),
        ('Modbus / RS485 通信读取', 'green'),
        ('关键字段解析与结构化提取', 'green'),
        ('时间戳与设备标识补全', 'green'),
    ]),
    ('可信处理与自动监测阶段', [
        ('签名处理与可信封装', 'blue'),
        ('本地记录与CSV落盘', 'blue'),
        ('自动监测图表生成', 'blue'),
    ]),
    ('存证与应用输出阶段', [
        ('联盟链存证写入', 'blue'),
        ('前端与报告输出', 'amber'),
    ]),
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

svg.append(f'<text x="{W/2}" y="42" text-anchor="middle" class="title">IoT 数据采集与可信处理流程图</text>')
svg.append(f'<text x="{W/2}" y="70" text-anchor="middle" class="subtitle">从真实设备接入到链上存证与展示输出的关键流程</text>')

panel_x = 60
panel_w = W - 120
panel_h = [470, 360, 260]
panel_y = [110, 620, 1020]
for y,h in zip(panel_y, panel_h):
    svg.append(f'<rect x="{panel_x}" y="{y}" width="{panel_w}" height="{h}" rx="18" ry="18" class="panel"/>')

for (title, _), y in zip(sections, panel_y):
    svg.append(f'<text x="{W/2}" y="{y+30}" text-anchor="middle" class="section-title">{title}</text>')

box_w = 430
box_h = 68
x = (W - box_w) / 2
section_positions = [
    [180, 290, 400, 510],
    [690, 800, 910],
    [1095, 1235],
]

for (_, steps), ys in zip(sections, section_positions):
    for (label, kind), y in zip(steps, ys):
        fill, stroke, text = colors[kind]
        svg.append(f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="16" ry="16" fill="{fill}" stroke="{stroke}" stroke-width="2.2"/>')
        svg.append(f'<text x="{W/2}" y="{y+box_h/2+1}" class="node-text" fill="{text}">{label}</text>')

# vertical arrows inside sections and across sections
all_y = [180, 290, 400, 510, 690, 800, 910, 1095, 1235]
for top, nxt in zip(all_y, all_y[1:]):
    start = top + box_h
    end = nxt - 14
    svg.append(f'<line x1="{W/2}" y1="{start}" x2="{W/2}" y2="{end}" class="connector"/>')

# compact footnote
svg.append(f'<rect x="180" y="1510" width="920" height="90" rx="16" ry="16" fill="#FFFFFF" stroke="{BORDER}" stroke-width="1.6"/>')
svg.append(f'<text x="640" y="1546" text-anchor="middle" style="font:700 14px PingFang SC,Microsoft YaHei,Noto Sans SC,sans-serif; fill:{TITLE};">流程图说明</text>')
svg.append(f'<text x="640" y="1576" text-anchor="middle" style="font:500 12px PingFang SC,Microsoft YaHei,Noto Sans SC,sans-serif; fill:#6B7280;">系统先完成设备接入与结构化采集，再进行可信封装与自动监测，最终进入联盟链存证与前端展示输出。</text>')

svg.append('</svg>')
Path('/Users/evanhan/项目/光伏项目/比赛材料/素材库/最终图片/04_IoT数据采集流程图_v3.svg').write_text('\n'.join(svg), encoding='utf-8')

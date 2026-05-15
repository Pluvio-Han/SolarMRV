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
AMBER_FILL = '#F7F3EA'
AMBER_STROKE = '#A46A1F'
AMBER_TEXT = '#5C3A10'
BLUE_TEXT = '#17324D'

stages = [
    ('第一阶段', '技术研发与原型验证', '打通设备采集、签名、联盟链与前端闭环'),
    ('第二阶段', '比赛立项与材料打磨', '形成商业计划书、展示材料与项目定位'),
    ('第三阶段', '小范围场景试点', '验证真实应用场景中的稳定运行与使用价值'),
    ('第四阶段', '模块复制与标准化输出', '形成可复用的模块能力与标准化交付包'),
    ('第五阶段', '平台化升级', '向绿证、ESG 与绿色金融辅助场景延伸'),
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
    .stage-title {{ font: 700 15px 'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif; fill: {GREEN_TEXT}; }}
    .stage-sub {{ font: 600 13px 'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif; fill: {TITLE}; }}
    .stage-desc {{ font: 500 12px 'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif; fill: #4B5563; }}
    .output-title {{ font: 700 14px 'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif; fill: {AMBER_TEXT}; }}
    .output-text {{ font: 500 12px 'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif; fill: #5B4630; }}
    .connector {{ stroke: {LINE}; stroke-width: 2; fill: none; stroke-linecap: round; marker-end: url(#arrow); }}
  </style>
</defs>''')

svg.append(f'<text x="{W/2}" y="42" text-anchor="middle" class="title">商业路径阶段图</text>')
svg.append(f'<text x="{W/2}" y="70" text-anchor="middle" class="subtitle">SolarGuard 从原型验证到平台化升级的阶段推进路径</text>')
svg.append(f'<rect x="70" y="110" width="1140" height="1120" rx="18" ry="18" fill="{PAGE}" stroke="{BORDER}" stroke-width="1.8"/>')

left_x, left_w = 100, 360
right_x, right_w = 820, 320
center_line_x = 640
stage_y0 = 180
step_gap = 200

for i, (s1, s2, desc) in enumerate(stages):
    y = stage_y0 + i * step_gap
    svg.append(f'<rect x="{left_x}" y="{y}" width="{left_w}" height="110" rx="18" ry="18" fill="{GREEN_FILL}" stroke="{GREEN_STROKE}" stroke-width="2.2"/>')
    svg.append(f'<text x="{left_x+left_w/2}" y="{y+34}" text-anchor="middle" class="stage-title">{s1}</text>')
    svg.append(f'<text x="{left_x+left_w/2}" y="{y+60}" text-anchor="middle" class="stage-sub">{s2}</text>')
    svg.append(f'<text x="{left_x+left_w/2}" y="{y+86}" text-anchor="middle" class="stage-desc">{desc}</text>')

    svg.append(f'<rect x="{right_x}" y="{y+8}" width="{right_w}" height="94" rx="16" ry="16" fill="{AMBER_FILL}" stroke="{AMBER_STROKE}" stroke-width="2"/>')
    svg.append(f'<text x="{right_x+right_w/2}" y="{y+36}" text-anchor="middle" class="output-title">阶段产出</text>')
    outputs = [
        '形成原型闭环与技术锚点',
        '完成材料体系与比赛定位',
        '积累真实试点案例与反馈',
        '沉淀标准化模块与交付能力',
        '拓展高价值应用场景与合作空间',
    ]
    svg.append(f'<text x="{right_x+right_w/2}" y="{y+66}" text-anchor="middle" class="output-text">{outputs[i]}</text>')

    # connectors for each row
    svg.append(f'<line x1="{left_x+left_w}" y1="{y+55}" x2="{right_x-20}" y2="{y+55}" stroke="{BORDER}" stroke-width="1.8"/>')

    # vertical spine and row connector
    spine_y = y + 55
    svg.append(f'<circle cx="{center_line_x}" cy="{spine_y}" r="8" fill="{GREEN_STROKE}" opacity="0.9"/>')
    svg.append(f'<line x1="{left_x+left_w+20}" y1="{spine_y}" x2="{center_line_x-10}" y2="{spine_y}" class="connector"/>')
    if i < len(stages)-1:
        next_y = stage_y0 + (i+1) * step_gap + 55
        svg.append(f'<line x1="{center_line_x}" y1="{spine_y+12}" x2="{center_line_x}" y2="{next_y-20}" class="connector"/>')

svg.append('</svg>')
Path('/Users/evanhan/项目/光伏项目/比赛材料/素材库/最终图片/09_商业路径阶段图_v2.svg').write_text('\n'.join(svg), encoding='utf-8')

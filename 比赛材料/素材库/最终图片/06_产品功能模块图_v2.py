from pathlib import Path

W, H = 1280, 1680
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
    .node-title {{ font: 700 15px 'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif; text-anchor: middle; }}
    .node-text {{ font: 500 12px 'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif; text-anchor: middle; fill: #4B5563; }}
    .connector {{ stroke: {LINE}; stroke-width: 2; fill: none; stroke-linecap: round; marker-end: url(#arrow); }}
  </style>
</defs>''')

svg.append(f'<text x="{W/2}" y="42" text-anchor="middle" class="title">产品功能模块图</text>')
svg.append(f'<text x="{W/2}" y="70" text-anchor="middle" class="subtitle">SolarGuard 围绕可信数据采集、存证、展示与场景服务形成六大核心模块</text>')

# central platform card
svg.append(f'<rect x="260" y="120" width="760" height="150" rx="22" ry="22" fill="#FFFFFF" stroke="{GREEN_STROKE}" stroke-width="2.2"/>')
svg.append(f'<text x="{W/2}" y="175" text-anchor="middle" style="font:700 28px PingFang SC,Microsoft YaHei,Noto Sans SC,sans-serif; fill:{GREEN_STROKE};">SolarGuard</text>')
svg.append(f'<text x="{W/2}" y="210" text-anchor="middle" style="font:600 16px PingFang SC,Microsoft YaHei,Noto Sans SC,sans-serif; fill:{TITLE};">分布式光伏可信存证与绿色资产服务平台</text>')
svg.append(f'<text x="{W/2}" y="240" text-anchor="middle" style="font:500 13px PingFang SC,Microsoft YaHei,Noto Sans SC,sans-serif; fill:#6B7280;">从真实设备采集到业务场景服务的整链路功能闭环</text>')

# section panels
svg.append(f'<rect x="70" y="340" width="1140" height="500" rx="18" ry="18" class="panel"/>')
svg.append(f'<text x="640" y="372" text-anchor="middle" class="section-title">核心产品能力</text>')
svg.append(f'<rect x="70" y="900" width="1140" height="320" rx="18" ry="18" class="panel"/>')
svg.append(f'<text x="640" y="932" text-anchor="middle" class="section-title">场景延伸能力</text>')

cards = [
    (140, 430, '硬件数据采集', '连接光伏控制器\n读取功率、电压、电量等关键指标', GREEN_FILL, GREEN_STROKE, GREEN_TEXT),
    (515, 430, '数据签名与可信封装', '结构化处理原始数据\n形成可验证的可信记录', GREEN_FILL, GREEN_STROKE, GREEN_TEXT),
    (890, 430, '联盟链存证', '关键数据上链\n支持查询、追溯与留痕', BLUE_FILL, BLUE_STROKE, BLUE_TEXT),
    (140, 650, '自动监测与告警', '周期采样、图表生成\n消息推送与异常提醒', BLUE_FILL, BLUE_STROKE, BLUE_TEXT),
    (515, 650, 'API 与前端可视化', '对外接口服务\n承接仪表盘与数据展示', BLUE_FILL, BLUE_STROKE, BLUE_TEXT),
    (890, 650, '历史记录与报告输出', '沉淀运行记录\n输出摘要报告与分析依据', BLUE_FILL, BLUE_STROKE, BLUE_TEXT),
    (270, 1010, '绿色资产服务原型', '围绕绿证、ESG、绿色金融辅助决策\n探索可信数据的高价值应用场景', AMBER_FILL, AMBER_STROKE, AMBER_TEXT),
    (730, 1010, '多场景业务衔接', '服务分布式光伏运维、园区能源管理\n审计核验与绿色治理需求', AMBER_FILL, AMBER_STROKE, AMBER_TEXT),
]

for x,y,title,desc,fill,stroke,text in cards:
    w = 250 if y < 900 else 280
    h = 130
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" ry="18" fill="{fill}" stroke="{stroke}" stroke-width="2.2"/>')
    svg.append(f'<text x="{x+w/2}" y="{y+36}" class="node-title" fill="{text}">{title}</text>')
    lines = desc.splitlines()
    if not lines:
        lines = [desc]
    svg.append(f'<text x="{x+w/2}" y="{y+72}" class="node-text">{lines[0]}</text>')
    if len(lines) > 1:
        svg.append(f'<text x="{x+w/2}" y="{y+94}" class="node-text">{lines[1]}</text>')

# connectors from central platform
for tx in [265, 640, 1015]:
    svg.append(f'<line x1="640" y1="270" x2="{tx}" y2="405" class="connector"/>')
# row connectors
svg.append(f'<line x1="390" y1="495" x2="515" y2="495" stroke="{LINE}" stroke-width="2"/>')
svg.append(f'<line x1="765" y1="495" x2="890" y2="495" stroke="{LINE}" stroke-width="2"/>')
svg.append(f'<line x1="390" y1="715" x2="515" y2="715" stroke="{LINE}" stroke-width="2"/>')
svg.append(f'<line x1="765" y1="715" x2="890" y2="715" stroke="{LINE}" stroke-width="2"/>')
# connectors downward
svg.append(f'<line x1="640" y1="560" x2="640" y2="635" class="connector"/>')
svg.append(f'<line x1="640" y1="780" x2="640" y2="965" class="connector"/>')
svg.append(f'<line x1="550" y1="1075" x2="730" y2="1075" stroke="{LINE}" stroke-width="2"/>')

svg.append('</svg>')
Path('/Users/evanhan/项目/光伏项目/比赛材料/素材库/最终图片/06_产品功能模块图_v2.svg').write_text('\n'.join(svg), encoding='utf-8')

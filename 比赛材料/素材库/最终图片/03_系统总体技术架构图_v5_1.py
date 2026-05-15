from pathlib import Path

W, H = 1280, 1820
BG = '#FFFFFF'
PAGE = '#FAFBFA'
LAYER_STROKE = '#D1D5DB'
LINE = '#6B7280'
TITLE = '#1F2937'

COLORS = {
    'device_fill': '#E8F3EC', 'device_stroke': '#2E6B4F', 'device_text': '#123524',
    'chain_fill': '#EAF0F8', 'chain_stroke': '#355C8A', 'chain_text': '#17324D',
    'service_fill': '#EEF4FB', 'service_stroke': '#355C8A', 'service_text': '#17324D',
    'app_fill': '#F7F3EA', 'app_stroke': '#A46A1F', 'app_text': '#5C3A10',
}

layers = [
    ('设备层', ['分布式光伏面板', '光伏控制器/逆变器', '本地边缘通信总线'], 'device'),
    ('采集与可信处理层', ['边缘网关/Python脚本', '数据结构化提取', 'SM2/ECDSA 数字签名'], 'device'),
    ('可信存证层', ['FISCO-BCOS 联盟链节点', '存证智能合约', '分布式防篡改账本'], 'chain'),
    ('服务与API层', ['定时监测守护程序', '数据可视化 API', '链上状态与账本 API'], 'service'),
    ('可视化展示层', ['前端控制台仪表盘', '自动监测图表报表', '项目运行摘要报告'], 'service'),
    ('应用场景层', ['绿证辅助核验', 'ESG 披露支持', '绿色金融尽调辅助'], 'app'),
]

layer_x = 45
layer_w = W - 90
layer_h = 155
start_y = 18
layer_gap = 72
node_w = 250
node_h = 62
node_y = 66
center_x = W / 2
node_gap = 70
row_total = node_w * 3 + node_gap * 2
row_start = (W - row_total) / 2
left_x = row_start
mid_x = row_start + node_w + node_gap
right_x = row_start + 2 * (node_w + node_gap)
line_y = node_y + node_h/2

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
svg.append(f'<rect width="100%" height="100%" fill="{BG}"/>')
svg.append(f'''<defs>
  <marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto" markerUnits="strokeWidth">
    <path d="M 0 0 L 9 4.5 L 0 9 z" fill="{LINE}" opacity="0.95"/>
  </marker>
  <style>
    .layer-box {{ fill: {PAGE}; stroke: {LAYER_STROKE}; stroke-width: 1.8; }}
    .layer-title {{ font: 700 17px 'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif; fill: {TITLE}; }}
    .node-label {{ font: 600 13px 'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif; text-anchor: middle; dominant-baseline: middle; }}
    .connector {{ stroke: {LINE}; stroke-width: 2; fill: none; stroke-linecap: round; }}
    .vertical {{ stroke: {LINE}; stroke-width: 2; fill: none; stroke-linecap: round; marker-end: url(#arrow); }}
  </style>
</defs>''')

for i, (title, nodes, kind) in enumerate(layers):
    y = start_y + i * (layer_h + layer_gap)
    title_y = y + 22
    svg.append(f'<rect x="{layer_x}" y="{y}" width="{layer_w}" height="{layer_h}" rx="16" ry="16" class="layer-box"/>')
    svg.append(f'<text x="{center_x}" y="{title_y}" text-anchor="middle" class="layer-title">{title}</text>')

    fill = COLORS[f'{kind}_fill']
    stroke = COLORS[f'{kind}_stroke']
    text = COLORS[f'{kind}_text']
    xs = [left_x, mid_x, right_x]
    for x, label in zip(xs, nodes):
        svg.append(f'<rect x="{x:.1f}" y="{y+node_y}" width="{node_w}" height="{node_h}" rx="13" ry="13" fill="{fill}" stroke="{stroke}" stroke-width="2.1"/>')
        svg.append(f'<text x="{x + node_w/2:.1f}" y="{y+node_y+node_h/2+1:.1f}" class="node-label" fill="{text}">{label}</text>')

    svg.append(f'<line x1="{left_x + node_w:.1f}" y1="{y+line_y:.1f}" x2="{mid_x:.1f}" y2="{y+line_y:.1f}" class="connector"/>')
    svg.append(f'<line x1="{mid_x + node_w:.1f}" y1="{y+line_y:.1f}" x2="{right_x:.1f}" y2="{y+line_y:.1f}" class="connector"/>')

    if i < len(layers) - 1:
        y1 = y + layer_h
        y2 = start_y + (i + 1) * (layer_h + layer_gap)
        svg.append(f'<line x1="{center_x:.1f}" y1="{y1:.1f}" x2="{center_x:.1f}" y2="{y2 - 12:.1f}" class="vertical"/>')

svg.append('</svg>')
Path('/Users/evanhan/项目/光伏项目/比赛材料/素材库/最终图片/03_系统总体技术架构图_v5_1.svg').write_text('\n'.join(svg), encoding='utf-8')

from pathlib import Path

W, H = 1600, 2200
margin_x = 80
layer_w = 1440
layer_h = 180
layer_x = (W - layer_w) / 2
node_w = 320
node_h = 72
left_x = 150
center_x = (W - node_w) / 2
right_x = W - 150 - node_w
node_y_offset = 68
line_y = node_y_offset + node_h/2
layer_gap = 105
start_y = 40

layers = [
    ("设备层", ["分布式光伏面板", "光伏控制器/逆变器", "本地边缘通信总线"], "device"),
    ("采集与可信处理层", ["边缘网关/Python脚本", "数据结构化提取", "SM2/ECDSA 数字签名"], "device"),
    ("可信存证层", ["FISCO-BCOS 联盟链节点", "存证智能合约", "分布式防篡改账本"], "chain"),
    ("服务与API层", ["定时监测守护程序", "数据可视化 API", "链上状态与账本 API"], "chain"),
    ("可视化展示层", ["前端控制台仪表盘", "自动监测图表报表", "项目运行摘要报告"], "service"),
    ("应用场景层", ["绿证辅助核验", "ESG 披露支持", "绿色金融尽调辅助"], "app"),
]

styles = {
    'bg': '#FFFFFF',
    'page': '#FAFBFA',
    'layer_stroke': '#D1D5DB',
    'title': '#1F2937',
    'line': '#6B7280',
    'device_fill': '#E8F3EC', 'device_stroke': '#2E6B4F', 'device_text': '#123524',
    'chain_fill': '#EAF0F8', 'chain_stroke': '#355C8A', 'chain_text': '#17324D',
    'service_fill': '#EEF4FB', 'service_stroke': '#355C8A', 'service_text': '#17324D',
    'app_fill': '#F7F3EA', 'app_stroke': '#A46A1F', 'app_text': '#5C3A10',
}

out = []
out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
out.append(f'<rect width="100%" height="100%" fill="{styles["bg"]}"/>')
out.append("""
<style>
  .layer-title { font: 700 34px 'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif; fill: #1F2937; }
  .node-text { font: 600 25px 'PingFang SC','Microsoft YaHei','Noto Sans SC',sans-serif; text-anchor: middle; dominant-baseline: middle; }
  .connector { stroke: #6B7280; stroke-width: 5; fill: none; stroke-linecap: round; }
  .layer-box { fill: #FAFBFA; stroke: #D1D5DB; stroke-width: 2.5; }
</style>
<defs>
  <marker id="arrow" markerWidth="12" markerHeight="12" refX="6" refY="6" orient="auto">
    <path d="M 0 0 L 12 6 L 0 12 z" fill="#6B7280" />
  </marker>
</defs>
""")

y = start_y
centers = []
for idx, (title, nodes, kind) in enumerate(layers):
    out.append(f'<rect x="{layer_x}" y="{y}" width="{layer_w}" height="{layer_h}" rx="18" ry="18" class="layer-box"/>')
    out.append(f'<text x="{W/2}" y="{y+28}" text-anchor="middle" class="layer-title">{title}</text>')
    xs = [left_x, center_x, right_x]
    fill = styles[f'{kind}_fill']
    stroke = styles[f'{kind}_stroke']
    textc = styles[f'{kind}_text']
    for x, text in zip(xs, nodes):
        out.append(f'<rect x="{x}" y="{y+node_y_offset}" width="{node_w}" height="{node_h}" rx="16" ry="16" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')
        out.append(f'<text x="{x+node_w/2}" y="{y+node_y_offset+node_h/2+1}" class="node-text" fill="{textc}">{text}</text>')
    out.append(f'<line x1="{left_x+node_w}" y1="{y+line_y}" x2="{center_x}" y2="{y+line_y}" class="connector"/>')
    out.append(f'<line x1="{center_x+node_w}" y1="{y+line_y}" x2="{right_x}" y2="{y+line_y}" class="connector"/>')
    centers.append((y, y+layer_h))
    y += layer_h + layer_gap

for i in range(len(centers)-1):
    y1 = centers[i][1]
    y2 = centers[i+1][0]
    out.append(f'<line x1="{W/2}" y1="{y1}" x2="{W/2}" y2="{y2-16}" class="connector" marker-end="url(#arrow)"/>')

out.append('</svg>')
svg = '\n'.join(out)
path = Path('/Users/evanhan/项目/光伏项目/比赛材料/素材库/最终图片/03_系统总体技术架构图_v6.svg')
path.write_text(svg, encoding='utf-8')
print(path)

from pathlib import Path
import re

base = Path('/Users/evanhan/项目/光伏项目')
word_dir = base / '比赛材料' / 'Word定稿'
total = base / '比赛材料' / 'BP总稿_第一轮精修版.md'
out_md = word_dir / 'SolarGuard商业计划书_装配版_第一版.md'
out_docx = word_dir / 'SolarGuard商业计划书_互联网杯与大创省赛版_第一版.docx'

text = total.read_text(encoding='utf-8')

# start from chapter 1; cover and abstract are added separately
start = text.index('# 第一章 项目概述')
body = text[start:]

# remove suggestion lines
body = re.sub(r'^> 建议.*\n?', '', body, flags=re.M)

# map adopted image lines to actual markdown images
body = re.sub(
    r'\[当前采用图稿：`([^`]+)`\]',
    lambda m: f'![插图]({m.group(1)})',
    body,
)

image_map = {
    '合规边界示意图': None,
    '前端原型界面图': '/Users/evanhan/项目/光伏项目/比赛材料/素材库/最终图片/07_前端页面展示图_v6.png',
    '应用场景矩阵图': None,
    '市场机会逻辑图': None,
    '商业模式画布简化图': None,
    '推广路径漏斗图': None,
    '项目形成路径图': '/Users/evanhan/项目/光伏项目/比赛材料/素材库/最终图片/18_项目形成路径图_v1.png',
    '附录结构导览图': None,
}

for label, path in image_map.items():
    pat = f'[图片占位：{label}]'
    if path:
        body = body.replace(pat, f'![{label}]({path})')
    else:
        body = body.replace(pat, f'> 说明：{label} 暂不放入正文图片版，后续可在附录或补充材料中加入。')

page_map = {
    '团队能力结构页': '本页在 Word 定稿时采用原生版式排版，不使用 PNG 图片。请按 `/Users/evanhan/项目/光伏项目/比赛材料/Word定稿/第七章页面稿/17_团队能力结构图_Word版式稿.md` 排版。',
    '教育实效总结页': '本页在 Word 定稿时采用原生版式排版，不使用 PNG 图片。请按 `/Users/evanhan/项目/光伏项目/比赛材料/Word定稿/第七章页面稿/19_教育实效总结图_Word版式稿.md` 排版。',
}
for label, repl in page_map.items():
    body = re.sub(rf'\[页面占位：{label}[^\]]*\]', f'> 说明：{repl}', body)

# convert table placeholders to notes
body = re.sub(r'\[表格占位：([^\]]+)\]', r'> 待补表格：\1', body)

# remove duplicate top title from body if any extra blank lines
body = re.sub(r'\n{3,}', '\n\n', body)

cover = f'''# SolarGuard：分布式光伏可信存证与绿色资产服务平台

中国国际大学生创新大赛 / 大学生创新创业训练计划项目

互联网杯与大创省赛商业计划书

项目类型：创意组 / 学生创新项目

项目方向：新能源可信数据、联盟链存证、绿色资产服务

团队名称：待补  
学校：待补  
学院：待补  
指导老师：待补  
完成时间：2026年3月

\\newpage
'''

abstract = '''# 执行摘要

SolarGuard 是一个面向分布式光伏场景的可信数据采集、联盟链存证与绿色资产服务平台。项目围绕“新能源场景中的底层数据如何可信获取、可信记录并服务上层应用”这一现实问题展开，形成了从设备接入、自动监测、数字签名、链上存证到前端展示和报告输出的完整原型链路。

与传统光伏监控系统相比，SolarGuard 的核心价值不在于简单展示设备运行状态，而在于把分散、易丢失、难验证的运行数据转化为可追溯、可核验、可服务绿证、ESG 与绿色金融辅助决策的可信数据资产基础。项目当前已经完成真实设备读取、自动监测图表生成、链上交互原型、前端可视化页面和系统级商业计划书材料整合，具备继续向比赛申报、试点展示和后续深化推进的现实基础。

在政策环境方面，项目主动根据最新监管口径完成叙事调整，不再将自身定义为高风险的代币化或公开交易项目，而是明确定位为新能源可信数据与绿色资产服务平台。这一定位更加符合当前数据要素、绿色金融、可信数据空间和分布式光伏规范化建设的政策方向，也使项目具备更强的比赛适配度和现实落地可能性。

在技术上，项目已经完成设备数据采集、自动监测脚本、签名处理、FISCO-BCOS 联盟链交互、前端原型和图表输出等关键模块，证明项目并非停留在概念层，而是具备真实系统雏形。在应用上，项目面向分布式光伏运维、园区能源管理、绿证辅助核验、ESG 披露支持和绿色金融辅助决策等场景，具有较强的延展性。在团队训练上，项目体现了从知识迁移、工程实践到材料组织和综合表达的完整创新训练路径，符合创新大赛和大创项目对学生成长与专创融合的要求。

当前阶段，SolarGuard 已完成商业计划书第一版、核心图片体系、政策资料归档和 Word 定稿结构搭建。后续随着市场数据、用户调研、财务资料和真实实验材料的进一步补充，项目有条件进一步提升为更加完整的省赛和网评提交版本。

\\newpage
'''

assembled = cover + abstract + body
out_md.write_text(assembled, encoding='utf-8')
print(out_md)

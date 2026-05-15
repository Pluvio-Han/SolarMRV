from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = Path('/Users/evanhan/项目/光伏项目/比赛材料/素材库/最终图片')
CHARTS = Path('/Users/evanhan/项目/光伏项目/charts')
ASSETS = Path('/Users/evanhan/项目/光伏项目/assets')
FONT = '/System/Library/Fonts/Hiragino Sans GB.ttc'
W, H = 1280, 1680
BG = '#FFFFFF'
PAGE = '#FAFBFA'
BORDER = '#D1D5DB'
TITLE = '#1F2937'
SUB = '#6B7280'
TEXT = '#374151'
GREEN = '#2E6B4F'
PALE_GREEN = '#E8F3EC'
BLUE = '#355C8A'
PALE_BLUE = '#EAF0F8'
AMBER = '#A46A1F'
PALE_AMBER = '#F7F3EA'
PURPLE = '#7C3AED'
PALE_PURPLE = '#F3E8FF'
RED = '#B45309'
PALE_RED = '#FFF7ED'
LINE = '#6B7280'
GRAY_FILL = '#F8FAFC'


def f(size):
    return ImageFont.truetype(FONT, size)


def shadow(base, xy, radius=22):
    layer = Image.new('RGBA', base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x1, y1, x2, y2 = xy
    d.rounded_rectangle((x1 + 8, y1 + 12, x2 + 8, y2 + 12), radius=radius, fill=(15, 23, 42, 26))
    return layer.filter(ImageFilter.GaussianBlur(18))


def rounded(d, xy, fill, outline=BORDER, width=2, radius=22):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def center_text(d, x, y, text, font, fill=TITLE):
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text((x - tw / 2, y - th / 2), text, font=font, fill=fill)


def wrapped_text(d, x, y, text, font, fill=TEXT, max_width=240, line_gap=8, center=False):
    paras = text.split('\n')
    cy = y
    for para in paras:
        chars, lines = [], []
        for ch in para:
            test = ''.join(chars) + ch
            if d.textlength(test, font=font) <= max_width:
                chars.append(ch)
            else:
                lines.append(''.join(chars))
                chars = [ch]
        if chars:
            lines.append(''.join(chars))
        for line in lines:
            bbox = d.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            tx = x - w / 2 if center else x
            d.text((tx, cy), line, font=font, fill=fill)
            cy += h + line_gap
        cy += 2
    return cy


def draw_arrow(d, x1, y1, x2, y2, color=LINE, width=3, head=16):
    d.line((x1, y1, x2, y2), fill=color, width=width)
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - head * math.cos(ang) + head * 0.55 * math.sin(ang), y2 - head * math.sin(ang) - head * 0.55 * math.cos(ang))
    p2 = (x2 - head * math.cos(ang) - head * 0.55 * math.sin(ang), y2 - head * math.sin(ang) + head * 0.55 * math.cos(ang))
    d.polygon([(x2, y2), p1, p2], fill=color)


def build_01():
    img = Image.new('RGBA', (W, H), BG)
    d = ImageDraw.Draw(img)
    center_text(d, W/2, 48, '项目总览图', f(24), TITLE)
    center_text(d, W/2, 78, 'SolarGuard 从真实光伏设备到高价值绿色场景服务的整体闭环', f(13), SUB)

    # core three-stage overview
    rounded(d, (100, 170, 1180, 950), PAGE, outline=BORDER, radius=26)
    cols = [220, 640, 1060]
    stage_boxes = [
        (120, 260, 320, 760, PALE_GREEN, GREEN, '真实设备与数据入口', ['分布式光伏设备', 'Modbus 采集读取', '结构化字段提取', '时间戳与签名']),
        (440, 240, 840, 780, '#FFFFFF', GREEN, '可信处理与系统能力', ['联盟链存证', '自动监测与告警', '数据管理与 API', '历史记录与摘要报告', '前端仪表盘展示']),
        (960, 260, 1160, 760, PALE_AMBER, AMBER, '高价值应用场景', ['绿证辅助核验', 'ESG 披露支持', '绿色金融辅助决策', '园区与企业能源管理'])
    ]
    for x1,y1,x2,y2,fill,stroke,title,items in stage_boxes:
        rounded(d, (x1,y1,x2,y2), fill, outline=stroke, width=2, radius=22)
        center_text(d, (x1+x2)/2, y1+34, title, f(18), stroke)
        yy = y1 + 88
        for item in items:
            rounded(d, (x1+24, yy, x2-24, yy+64), '#FFFFFF' if fill != '#FFFFFF' else GRAY_FILL, outline=stroke if fill=='#FFFFFF' else BORDER, width=2 if fill=='#FFFFFF' else 1, radius=16)
            center_text(d, (x1+x2)/2, yy+32, item, f(15), TITLE)
            yy += 82

    draw_arrow(d, 320, 520, 440, 520, color=LINE, width=4, head=18)
    draw_arrow(d, 840, 520, 960, 520, color=LINE, width=4, head=18)
    center_text(d, 380, 476, '可信链路形成', f(14), SUB)
    center_text(d, 900, 476, '场景价值释放', f(14), SUB)

    rounded(d, (140, 1020, 1140, 1240), '#FFFFFF', outline=BORDER, radius=22)
    center_text(d, 640, 1062, '项目核心标签', f(18), TITLE)
    tags = ['真实设备采集', '自动监测', '联盟链存证', '可视化展示', '绿证衔接', 'ESG 支持', '绿色金融辅助']
    tx = 180
    ty = 1115
    for tag in tags:
        bbox = d.textbbox((0,0), tag, font=f(14))
        tw = bbox[2]-bbox[0] + 44
        if tx + tw > 1080:
            tx = 180
            ty += 66
        rounded(d, (tx, ty, tx+tw, ty+42), PALE_GREEN if '链' not in tag and '金融' not in tag and 'ESG' not in tag else (PALE_BLUE if '链' in tag else PALE_AMBER), outline=(GREEN if '链' not in tag and '金融' not in tag and 'ESG' not in tag else (BLUE if '链' in tag else AMBER)), width=2, radius=16)
        center_text(d, tx+tw/2, ty+21, tag, f(14), TITLE)
        tx += tw + 18

    rounded(d, (140, 1310, 1140, 1460), PAGE, outline=BORDER, radius=20)
    center_text(d, 640, 1346, '一句话总结', f(18), TITLE)
    wrapped_text(d, 188, 1386, 'SolarGuard 不是单一监控软件，而是以真实光伏设备数据为起点，把可信采集、签名存证、自动监测、展示输出和绿色场景服务组织成完整业务闭环的系统原型。', f(15), fill=TEXT, max_width=900, line_gap=8, center=False)
    img.convert('RGB').save(OUT / '01_项目总览图_v1.png', quality=95)


def build_05():
    img = Image.new('RGBA', (W, H), BG)
    d = ImageDraw.Draw(img)
    center_text(d, W/2, 48, '自动监测图表', f(24), TITLE)
    center_text(d, W/2, 78, '基于真实运行记录生成的自动监测曲线与结果说明', f(13), SUB)

    top = (80, 130, 1200, 980)
    img.alpha_composite(shadow(Image.new('RGBA', (W, H), (0,0,0,0)), top))
    rounded(d, top, PAGE, outline=BORDER, radius=26)
    center_text(d, 640, 172, '自动监测运行结果', f(18), TITLE)
    center_text(d, 640, 204, '图表来源于自动采样、CSV 落盘与持续监测脚本的真实输出', f(13), SUB)

    chart = Image.open('/Users/evanhan/Downloads/IMG_0343.JPG').convert('RGBA').resize((960, 768))
    chart_box = (160, 240, 1120, 1008)
    rounded(d, chart_box, '#FFFFFF', outline='#CBD5E1', width=1, radius=20)
    mask = Image.new('L', (960, 768), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, 960, 768), radius=20, fill=255)
    img.paste(chart, (160, 240), mask)

    rounded(d, (120, 1050, 620, 1450), PAGE, outline=BORDER, radius=22)
    rounded(d, (660, 1050, 1160, 1450), PAGE, outline=BORDER, radius=22)
    center_text(d, 370, 1090, '图表信息解读', f(18), TITLE)
    bullets = [
        '通过定时采样形成连续运行曲线，而不是单次瞬时读数。',
        '同时记录功率、电压与电池相关状态，便于识别运行波动。',
        '图表可直接作为答辩、路演和材料中的真实性证明。',
    ]
    y = 1136
    for b in bullets:
        d.ellipse((150, y+6, 162, y+18), fill=GREEN)
        wrapped_text(d, 180, y, b, f(14), fill=TEXT, max_width=380, line_gap=8)
        y += 92

    center_text(d, 910, 1090, '模块意义', f(18), TITLE)
    points = [
        ('持续记录', '把临时实验升级为可周期运行的监测能力。'),
        ('自动生成', '自动落盘、出图和推送，降低人工整理成本。'),
        ('展示真实', '证明系统已经跑通，不是仅靠静态页面演示。'),
    ]
    yy = 1130
    for title, desc in points:
        rounded(d, (720, yy, 1100, yy+86), '#FFFFFF', outline=BORDER, radius=16)
        d.text((742, yy+18), title, font=f(15), fill=GREEN)
        wrapped_text(d, 742, yy+44, desc, f(13), fill=TEXT, max_width=318, line_gap=6)
        yy += 102

    img.convert('RGB').save(OUT / '05_自动监测图表_v2.png', quality=95)


def build_14():
    img = Image.new('RGBA', (W, H), BG)
    d = ImageDraw.Draw(img)
    center_text(d, W/2, 48, '用户与场景关系图', f(24), TITLE)
    center_text(d, W/2, 78, 'SolarGuard 围绕分布式光伏数据使用链条服务的主要对象', f(13), SUB)

    rounded(d, (100, 150, 1180, 1500), PAGE, outline=BORDER, radius=26)

    center_box = (390, 560, 890, 860)
    img.alpha_composite(shadow(Image.new('RGBA', (W, H), (0,0,0,0)), center_box))
    rounded(d, center_box, '#FFFFFF', outline=GREEN, width=2, radius=24)
    center_text(d, 640, 620, 'SolarGuard', f(30), GREEN)
    center_text(d, 640, 666, '可信数据采集、联盟链存证与绿色资产服务平台', f(16), TITLE)
    center_text(d, 640, 714, '把设备侧原始数据转化为可被机构采信和长期调用的业务数据', f(14), SUB)

    users = [
        ((120, 250, 430, 470), PALE_GREEN, GREEN, '分布式光伏运营方', '关注设备状态、发电数据连续记录、运维效率与历史留痕。'),
        ((850, 250, 1160, 470), PALE_BLUE, BLUE, '园区与企业能源管理方', '关注多个项目的汇总管理、绿色绩效、能源治理与数据治理能力。'),
        ((120, 930, 430, 1150), PALE_AMBER, AMBER, 'ESG / 审计 / 核验机构', '关注数据可信来源、可追溯记录、披露支持和核验效率。'),
        ((850, 930, 1160, 1150), '#F3E8FF', PURPLE, '绿色金融相关机构', '关注项目尽调、绿色贷款辅助判断、保险风险评估与可信依据。'),
    ]
    for (x1,y1,x2,y2), fill, stroke, title, desc in users:
        rounded(d, (x1,y1,x2,y2), fill, outline=stroke, width=2, radius=22)
        center_text(d, (x1+x2)/2, y1+42, title, f(18), stroke)
        wrapped_text(d, x1+22, y1+86, desc, f(13), fill=TEXT, max_width=(x2-x1)-44, line_gap=7)
        cx = (x1+x2)/2
        cy = (y1+y2)/2
        if cy < 640:
            draw_arrow(d, cx, y2, 640, 560, color=LINE, width=3)
        else:
            draw_arrow(d, cx, y1, 640, 860, color=LINE, width=3)

    rounded(d, (200, 1230, 1080, 1420), '#FFFFFF', outline=BORDER, radius=20)
    center_text(d, 640, 1270, '核心关系', f(18), TITLE)
    wrapped_text(d, 250, 1310, '项目的共同价值不在于单一监控功能，而在于为不同主体提供同一套可信底层数据基础，使运维、治理、披露、审计和绿色金融判断能够建立在更统一的记录之上。', f(14), fill=TEXT, max_width=780, line_gap=8)
    img.convert('RGB').save(OUT / '14_用户与场景关系图_v1.png', quality=95)


def build_20():
    img = Image.new('RGBA', (W, H), BG)
    d = ImageDraw.Draw(img)
    center_text(d, W/2, 48, '阶段预算柱状图', f(24), TITLE)
    center_text(d, W/2, 78, '以保守示意预算展示项目从比赛推进到平台化升级的投入节奏', f(13), SUB)

    rounded(d, (90, 140, 1190, 1080), PAGE, outline=BORDER, radius=26)
    center_text(d, 640, 184, '后续阶段性预算设计（示意）', f(18), TITLE)
    center_text(d, 640, 216, '单位：万元。数值用于展示投入结构与节奏，不等同于已确定融资计划。', f(13), SUB)

    stages = [
        ('比赛与立项推进', 0.8, PALE_GREEN, GREEN),
        ('试点验证阶段', 2.4, PALE_BLUE, BLUE),
        ('平台化升级阶段', 5.2, PALE_AMBER, AMBER),
    ]
    axis_x = 170
    axis_y0 = 960
    axis_y1 = 300
    draw_arrow(d, axis_x, axis_y0, axis_x, axis_y1, color=LINE, width=3)
    draw_arrow(d, axis_x, axis_y0, 1090, axis_y0, color=LINE, width=3)
    maxv = 6.0
    for i in range(0, 7):
        y = axis_y0 - (axis_y0-axis_y1) * (i/maxv)
        d.line((axis_x, y, 1080, y), fill='#E5E7EB', width=1)
        center_text(d, 138, y, str(i), f(12), SUB)

    xs = [320, 620, 920]
    bar_w = 150
    for (label, val, pale, stroke), x in zip(stages, xs):
        h = (axis_y0-axis_y1) * (val/maxv)
        y = axis_y0 - h
        rounded(d, (x-bar_w/2, y, x+bar_w/2, axis_y0), pale, outline=stroke, width=2, radius=18)
        center_text(d, x, y-24, f'{val:.1f}', f(18), stroke)
        wrapped_text(d, x-95, axis_y0+26, label, f(14), fill=TITLE, max_width=190, line_gap=6, center=True)

    rounded(d, (110, 1130, 1170, 1470), '#FFFFFF', outline=BORDER, radius=22)
    center_text(d, 640, 1168, '预算构成重点', f(18), TITLE)
    cols = [
        (170, '比赛与立项推进', ['材料与展示优化', '图表与页面整理', '答辩与申报准备'], GREEN),
        (510, '试点验证阶段', ['硬件重新接入', '服务器与运行维护', '小范围试点支持'], BLUE),
        (850, '平台化升级阶段', ['接口扩展与兼容', '前后端产品化完善', '场景模块标准化'], AMBER),
    ]
    for x, title, items, stroke in cols:
        rounded(d, (x, 1210, x+260, 1400), PAGE, outline=stroke, width=2, radius=18)
        center_text(d, x+130, 1244, title, f(16), stroke)
        yy = 1288
        for item in items:
            d.ellipse((x+22, yy+5, x+34, yy+17), fill=stroke)
            wrapped_text(d, x+46, yy, item, f(13), fill=TEXT, max_width=190, line_gap=6)
            yy += 40
    img.convert('RGB').save(OUT / '20_阶段预算柱状图_v1.png', quality=95)


if __name__ == '__main__':
    build_01()
    build_05()
    build_14()
    build_20()

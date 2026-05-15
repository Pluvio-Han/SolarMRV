from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = Path('/Users/evanhan/项目/光伏项目/比赛材料/素材库/最终图片')
ASSETS = Path('/Users/evanhan/项目/光伏项目/assets')
CHARTS = Path('/Users/evanhan/项目/光伏项目/charts')
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
RED = '#B45309'
PALE_RED = '#FFF7ED'
GRAY_FILL = '#F8FAFC'
LINE = '#6B7280'


def f(size, bold=False):
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


def wrapped_text(d, x, y, text, font, fill=TEXT, max_width=240, line_gap=10, center=False):
    chars = []
    lines = []
    for ch in text:
        test = ''.join(chars) + ch
        if d.textlength(test, font=font) <= max_width:
            chars.append(ch)
        else:
            lines.append(''.join(chars))
            chars = [ch]
    if chars:
        lines.append(''.join(chars))
    cy = y
    for line in lines:
        bbox = d.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        tx = x - w / 2 if center else x
        d.text((tx, cy), line, font=font, fill=fill)
        cy += h + line_gap
    return cy


def draw_arrow(d, x1, y1, x2, y2, color=LINE, width=3, head=16):
    d.line((x1, y1, x2, y2), fill=color, width=width)
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - head * math.cos(ang) + head * 0.55 * math.sin(ang), y2 - head * math.sin(ang) - head * 0.55 * math.cos(ang))
    p2 = (x2 - head * math.cos(ang) - head * 0.55 * math.sin(ang), y2 - head * math.sin(ang) + head * 0.55 * math.cos(ang))
    d.polygon([(x2, y2), p1, p2], fill=color)


def build_07():
    img = Image.new('RGBA', (W, H), BG)
    d = ImageDraw.Draw(img)
    center_text(d, W/2, 48, '前端页面展示图', f(24), TITLE)
    center_text(d, W/2, 78, '基于真实项目界面与监测图表的产品化展示效果', f(13), SUB)

    top = (70, 120, 1210, 760)
    img.alpha_composite(shadow(Image.new('RGBA', (W, H), (0,0,0,0)), top))
    rounded(d, top, PAGE, outline=BORDER, width=2, radius=26)
    d.text((110, 156), '仪表盘主界面', font=f(18), fill=TITLE)
    d.text((110, 188), '展示资产概览、链上交易计数、设备状态与发电曲线等核心信息', font=f(12), fill=SUB)
    dash = Image.open('/Users/evanhan/Downloads/091d77119a563ff074d89d497c6c198a.jpg').convert('RGBA')
    # Preserve the KPI cards and the start of the chart area, but avoid pushing the screenshot into the lower modules.
    dash = dash.crop((0, 0, 1082, 760)).resize((920, 646))
    shot_xy = (180, 230, 1100, 760)
    rounded(d, shot_xy, '#FFFFFF', outline='#CBD5E1', width=1, radius=18)
    mask = Image.new('L', (920, 530), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, 920, 530), radius=18, fill=255)
    dash_visible = dash.crop((0, 0, 920, 530))
    img.paste(dash_visible, (180, 230), mask)

    # bottom cards
    left = (70, 800, 610, 1520)
    right = (670, 800, 1210, 1520)
    img.alpha_composite(shadow(Image.new('RGBA', (W, H), (0,0,0,0)), left))
    img.alpha_composite(shadow(Image.new('RGBA', (W, H), (0,0,0,0)), right))
    rounded(d, left, PAGE, outline=BORDER, radius=24)
    rounded(d, right, PAGE, outline=BORDER, radius=24)

    center_text(d, 340, 835, '实时图表与运行趋势', f(18), TITLE)
    center_text(d, 940, 835, '产品展示要点', f(18), TITLE)

    chart = Image.open(CHARTS / 'solar_data_chart.png').convert('RGBA')
    chart = chart.resize((470, 376))
    img.alpha_composite(chart, (105, 870))

    points = [
        ('可信采集', '接入真实光伏设备与模拟模式，支撑硬件不在场条件下的持续演示。', PALE_GREEN, GREEN),
        ('链上留痕', '关键数据完成签名与联盟链存证，形成可查询、可追溯的可信记录。', PALE_BLUE, BLUE),
        ('展示友好', '前端仪表盘、自动监测图表与摘要报告可直接支撑路演和材料呈现。', PALE_AMBER, AMBER),
    ]
    y = 870
    for title, desc, fill, stroke in points:
        rounded(d, (720, y, 1160, y+170), fill, outline=stroke, width=2, radius=20)
        d.text((748, y+26), title, font=f(16), fill=stroke)
        wrapped_text(d, 748, y+62, desc, f(13), fill=TEXT, max_width=380, line_gap=8)
        y += 190

    # Bottom caption strip
    rounded(d, (105, 1275, 575, 1445), GRAY_FILL, outline=BORDER, radius=18)
    d.text((130, 1308), '界面说明', font=f(15), fill=TITLE)
    wrapped_text(d, 130, 1343, '上方展示带真实数据的仪表盘主界面，重点呈现资产卡片、设备状态与发电曲线入口；下方监测图则补充自动生成的运行趋势效果。', f(13), fill=TEXT, max_width=420, line_gap=8)

    img.convert('RGB').save(OUT / '07_前端页面展示图_v6.png', quality=95)


def build_21():
    img = Image.new('RGBA', (W, H), BG)
    d = ImageDraw.Draw(img)
    center_text(d, W/2, 48, '资源需求结构图', f(24), TITLE)
    center_text(d, W/2, 78, 'SolarGuard 从原型走向试点需要的关键资源结构', f(13), SUB)

    top_panel = (70, 130, 1210, 710)
    bottom_panel = (70, 760, 1210, 1260)
    rounded(d, top_panel, PAGE, outline=BORDER, radius=24)
    rounded(d, bottom_panel, PAGE, outline=BORDER, radius=24)

    # donut proportions
    cx, cy = 335, 430
    outer = 178
    inner = 96
    box = (cx-outer, cy-outer, cx+outer, cy+outer)
    parts = [
        ('试点场景资源', 32, GREEN, PALE_GREEN),
        ('技术与算力资源', 26, BLUE, PALE_BLUE),
        ('导师与专家资源', 20, AMBER, PALE_AMBER),
        ('展示与传播资源', 22, '#7C3AED', '#F3E8FF'),
    ]
    start = -90
    for _, pct, color, _ in parts:
        end = start + pct * 3.6
        d.pieslice(box, start, end, fill=color, outline=BG, width=8)
        start = end
    d.ellipse((cx-inner, cy-inner, cx+inner, cy+inner), fill=BG)
    center_text(d, cx, cy-16, '资源支持', f(22), TITLE)
    center_text(d, cx, cy+18, '四类关键输入', f(14), SUB)

    # legend cards on right
    y = 180
    for label, pct, color, pale in parts:
        rounded(d, (640, y, 1140, y+112), pale, outline=color, width=2, radius=18)
        d.rounded_rectangle((664, y+20, 700, y+56), radius=10, fill=color)
        d.text((722, y+18), label, font=f(15), fill=TITLE)
        d.text((722, y+50), f'{pct}%', font=f(19), fill=color)
        desc = {
            '试点场景资源':'优先获取校园、园区、小型分布式光伏项目等真实验证场景。',
            '技术与算力资源':'需要服务器、接口联调、链上环境与持续开发测试条件。',
            '导师与专家资源':'补足新能源、政策合规、商业展示与产业对接能力。',
            '展示与传播资源':'用于视觉设计、图表制作、路演打磨与项目传播输出。',
        }[label]
        wrapped_text(d, 722, y+78, desc, f(12), fill=TEXT, max_width=385, line_gap=6)
        y += 126

    center_text(d, 640, 798, '资源获取优先顺序', f(18), TITLE)
    steps = [
        ('1', '场景支持优先', '先获得可落地试点，才能验证系统稳定性与材料可信度。'),
        ('2', '技术条件跟进', '围绕试点需求完善服务器、接口、持续监测与展示条件。'),
        ('3', '专家辅导增强', '在场景明确后引入导师与专家，补强政策与商业表达。'),
        ('4', '传播能力放大', '最后将案例、图稿、路演与申报材料统一打磨输出。'),
    ]
    xs = [140, 400, 660, 920]
    for (num, title, desc), x in zip(steps, xs):
        rounded(d, (x, 860, x+200, 1110), '#FFFFFF', outline=BORDER, radius=18)
        d.ellipse((x+70, 882, x+130, 942), fill=GREEN)
        center_text(d, x+100, 912, num, f(18), '#FFFFFF')
        center_text(d, x+100, 974, title, f(15), TITLE)
        wrapped_text(d, x+22, 1008, desc, f(12), fill=TEXT, max_width=156, line_gap=6)
    img.convert('RGB').save(OUT / '21_资源需求结构图_v4.png', quality=95)


def build_22():
    img = Image.new('RGBA', (W, H), BG)
    d = ImageDraw.Draw(img)
    center_text(d, W/2, 48, '风险分类图', f(24), TITLE)
    center_text(d, W/2, 78, '项目推进过程中的四类核心风险及其控制重点', f(13), SUB)

    rounded(d, (90, 130, 1190, 1220), PAGE, outline=BORDER, radius=24)
    # axis
    draw_arrow(d, 220, 1140, 220, 240)
    draw_arrow(d, 220, 1140, 1060, 1140)
    center_text(d, 126, 220, '影响程度', f(14), SUB)
    center_text(d, 1080, 1180, '可控程度', f(14), SUB)

    # quadrant labels
    center_text(d, 430, 300, '高影响 低可控', f(15), '#9A3412')
    center_text(d, 850, 300, '高影响 高可控', f(15), GREEN)
    center_text(d, 430, 930, '低影响 低可控', f(15), SUB)
    center_text(d, 850, 930, '低影响 高可控', f(15), BLUE)

    # guide lines
    d.line((220, 690, 1060, 690), fill=BORDER, width=2)
    d.line((640, 240, 640, 1140), fill=BORDER, width=2)

    cards = [
        (300, 340, 560, 520, PALE_RED, RED, '政策与合规风险', '政策收紧或边界变化将直接影响项目对外表述与场景推进。'),
        (700, 320, 980, 520, PALE_GREEN, GREEN, '技术实现风险', '硬件接入、稳定运行与接口完善度决定系统原型是否可靠。'),
        (710, 760, 990, 940, PALE_BLUE, BLUE, '团队推进与资源风险', '时间、分工、场景和导师支持不足会影响项目持续推进效率。'),
        (300, 790, 560, 970, '#F9FAFB', '#6B7280', '市场与场景验证风险', '需求存在但试点验证节奏慢，短期内难形成完整外部反馈。'),
    ]
    for x1,y1,x2,y2,fill,stroke,title,desc in cards:
        rounded(d, (x1,y1,x2,y2), fill, outline=stroke, width=2, radius=20)
        center_text(d, (x1+x2)/2, y1+34, title, f(15), stroke)
        wrapped_text(d, x1+22, y1+70, desc, f(12), fill=TEXT, max_width=(x2-x1)-44, line_gap=7)

    rounded(d, (180, 1260, 1100, 1360), '#FFFFFF', outline=BORDER, radius=18)
    center_text(d, 640, 1292, '控制思路', f(15), TITLE)
    center_text(d, 640, 1330, '以小场景试点、保守合规表达、双路径验证和团队分工固化降低整体推进不确定性', f(13), SUB)
    img.convert('RGB').save(OUT / '22_风险分类图_v3.png', quality=95)


if __name__ == '__main__':
    build_07()
    build_21()
    build_22()

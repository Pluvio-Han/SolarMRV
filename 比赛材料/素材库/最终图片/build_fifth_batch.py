from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = Path('/Users/evanhan/项目/光伏项目/比赛材料/素材库/最终图片')
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


def build_17():
    img = Image.new('RGBA', (W, H), BG)
    d = ImageDraw.Draw(img)
    center_text(d, W/2, 48, '团队能力结构图', f(24), TITLE)
    center_text(d, W/2, 78, '围绕 SolarGuard 项目形成的四类核心协同能力', f(13), SUB)

    rounded(d, (100, 150, 1180, 1485), PAGE, outline=BORDER, radius=26)

    center_box = (360, 595, 920, 895)
    img.alpha_composite(shadow(Image.new('RGBA', (W, H), (0,0,0,0)), center_box))
    rounded(d, center_box, '#FFFFFF', outline=GREEN, width=2, radius=24)
    center_text(d, 640, 658, 'SolarGuard', f(34), GREEN)
    center_text(d, 640, 714, '项目协同核心', f(20), TITLE)
    wrapped_text(
        d, 430, 760,
        '把硬件接入、自动监测、联盟链存证、政策研判、商业计划书与展示图表整合为一套可参赛、可解释、可持续迭代的完整原型。',
        f(16), fill=TEXT, max_width=420, line_gap=8, center=True
    )

    cards = [
        ((140, 255, 475, 495), PALE_GREEN, GREEN, '技术研发能力', '设备接入\n自动监测\n联盟链交互\n前后端原型'),
        ((805, 255, 1140, 495), PALE_BLUE, BLUE, '产品与场景能力', '用户对象梳理\n功能模块定义\n场景延展判断\n解决方案表达'),
        ((140, 995, 475, 1235), PALE_AMBER, AMBER, '政策与材料能力', '政策搜集\n合规边界分析\n商业计划书撰写\n申报材料整合'),
        ((805, 995, 1140, 1235), PALE_PURPLE, PURPLE, '展示与传播能力', '图表制作\n页面呈现\nGitHub 维护\n答辩与路演支持'),
    ]
    for (x1,y1,x2,y2), fill, stroke, title, desc in cards:
        rounded(d, (x1,y1,x2,y2), fill, outline=stroke, width=2, radius=22)
        center_text(d, (x1+x2)/2, y1+38, title, f(20), stroke)
        wrapped_text(d, x1+46, y1+92, desc, f(16), fill=TEXT, max_width=(x2-x1)-92, line_gap=10, center=True)
        cx = (x1+x2)//2
        cy = (y1+y2)//2
        target = (640, 595) if cy < 700 else (640, 895)
        if cx < 640:
            draw_arrow(d, x2, cy, target[0]-10, target[1], color=LINE, width=3)
        else:
            draw_arrow(d, x1, cy, target[0]+10, target[1], color=LINE, width=3)

    rounded(d, (170, 1320, 1110, 1438), '#FFFFFF', outline=BORDER, radius=18)
    center_text(d, 640, 1354, '核心判断', f(18), TITLE)
    center_text(d, 640, 1395, '项目不是依赖单一技术点，而是依赖跨模块协同，把复杂问题稳定推进为完整原型。', f(15), SUB)
    img.convert('RGB').save(OUT / '17_团队能力结构图_v2.png', quality=95)


def build_18():
    img = Image.new('RGBA', (W, H), BG)
    d = ImageDraw.Draw(img)
    center_text(d, W/2, 48, '项目形成路径图', f(24), TITLE)
    center_text(d, W/2, 78, 'SolarGuard 从技术问题出发逐步形成系统原型与比赛项目的成长路径', f(13), SUB)

    rounded(d, (90, 140, 1190, 1480), PAGE, outline=BORDER, radius=26)
    center_text(d, 640, 190, '从问题发现到项目定型', f(18), TITLE)

    steps = [
        ('01', '真实问题触发', '从分布式光伏设备数据采集与可信留痕问题出发，发现普通监控方案难以支撑更高价值场景。', PALE_GREEN, GREEN),
        ('02', '技术链路打通', '先完成设备读取、自动监测、签名处理、联盟链交互和前端展示等关键链路验证。', PALE_BLUE, BLUE),
        ('03', '原型系统形成', '把原本分散的脚本、合约、页面和图表整理为可展示、可解释、可继续迭代的原型系统。', PALE_AMBER, AMBER),
        ('04', '场景与政策重构', '结合政策环境，把项目从偏金融化探索转向新能源可信数据与绿色资产服务叙事。', PALE_PURPLE, PURPLE),
        ('05', '比赛版本成型', '沉淀代码、图表、政策资料、BP、总结报告和展示图，形成适合参赛和立项的完整材料。', '#F9FAFB', '#6B7280'),
    ]
    y = 270
    for i, (num, title, desc, fill, stroke) in enumerate(steps):
        rounded(d, (170, y, 1110, y+180), fill, outline=stroke, width=2, radius=22)
        d.ellipse((210, y+28, 286, y+104), fill=stroke)
        center_text(d, 248, y+66, num, f(22), '#FFFFFF')
        d.text((330, y+28), title, font=f(20), fill=stroke)
        wrapped_text(d, 330, y+66, desc, f(14), fill=TEXT, max_width=720, line_gap=7)
        if i < len(steps)-1:
            draw_arrow(d, 640, y+180, 640, y+220, color=LINE, width=3)
        y += 240

    rounded(d, (170, 1470, 1110, 1560), '#FFFFFF', outline=BORDER, radius=18)
    center_text(d, 640, 1500, '形成特征', f(18), TITLE)
    center_text(d, 640, 1534, '先有真实技术链路，再反推产品定位与比赛表达，而不是先编故事再找技术支撑。', f(14), SUB)
    img.convert('RGB').save(OUT / '18_项目形成路径图_v1.png', quality=95)


def build_19():
    img = Image.new('RGBA', (W, H), BG)
    d = ImageDraw.Draw(img)
    center_text(d, W/2, 48, '教育实效总结图', f(24), TITLE)
    center_text(d, W/2, 78, 'SolarGuard 在专业学习、工程实践、研究训练和综合表达上的训练价值', f(13), SUB)

    rounded(d, (100, 150, 1180, 1470), PAGE, outline=BORDER, radius=26)

    cards = [
        ((130, 235, 555, 520), PALE_GREEN, GREEN, '知识迁移能力', '把通信协议、程序设计、数据处理、前后端与区块链知识迁移到一个真实复杂问题中。'),
        ((725, 235, 1150, 520), PALE_BLUE, BLUE, '工程实践能力', '围绕设备、脚本、接口、页面、图表和系统运行逻辑，形成完整原型而非孤立代码片段。'),
        ((130, 610, 555, 895), PALE_AMBER, AMBER, '研究与论证能力', '在做系统的同时进行政策研判、场景分析、商业论证和合规边界判断。'),
        ((725, 610, 1150, 895), PALE_PURPLE, PURPLE, '综合表达能力', '把代码、实验、图表、仓库、BP 和答辩材料组织成可被评委快速理解的项目成果。'),
    ]
    for (x1,y1,x2,y2), fill, stroke, title, desc in cards:
        rounded(d, (x1,y1,x2,y2), fill, outline=stroke, width=2, radius=22)
        center_text(d, (x1+x2)/2, y1+42, title, f(21), stroke)
        wrapped_text(d, x1+34, y1+92, desc, f(16), fill=TEXT, max_width=(x2-x1)-68, line_gap=8)

    center_box = (290, 980, 990, 1215)
    img.alpha_composite(shadow(Image.new('RGBA', (W, H), (0,0,0,0)), center_box))
    rounded(d, center_box, '#FFFFFF', outline=GREEN, width=2, radius=22)
    center_text(d, 640, 1032, '教育实效结论', f(24), GREEN)
    wrapped_text(
        d, 360, 1088,
        'SolarGuard 的训练价值不只在于“做出一个项目”，而在于让成员完成从知识学习到系统实现、从技术验证到现实表达的完整成长闭环。',
        f(17), fill=TEXT, max_width=560, line_gap=9, center=True
    )

    rounded(d, (180, 1300, 1100, 1390), '#FFFFFF', outline=BORDER, radius=18)
    center_text(d, 640, 1345, '适合创新大赛口径：以赛促学、以创促用、专创融合、跨模块协同', f(16), SUB)
    img.convert('RGB').save(OUT / '19_教育实效总结图_v2.png', quality=95)


if __name__ == '__main__':
    build_17()
    build_18()
    build_19()


def build_17_v3():
    img = Image.new('RGBA', (W, H), BG)
    d = ImageDraw.Draw(img)
    center_text(d, W/2, 48, '团队能力结构图', f(24), TITLE)
    center_text(d, W/2, 78, '围绕 SolarGuard 项目形成的分工能力与协同输出结构', f(13), SUB)

    rounded(d, (90, 150, 1190, 1460), PAGE, outline=BORDER, radius=26)

    # top summary
    top = (130, 210, 1150, 360)
    rounded(d, top, '#FFFFFF', outline=GREEN, width=2, radius=24)
    center_text(d, 640, 258, 'SolarGuard 团队协同结构', f(28), GREEN)
    center_text(d, 640, 306, '以技术实现为基础，以政策研判、产品组织和展示表达为支撑，形成完整参赛产出。', f(16), SUB)

    # four horizontal capability bars
    rows = [
        (430, PALE_GREEN, GREEN, '技术研发能力', '设备接入、自动监测、联盟链交互、前后端原型', '形成可运行的系统底座'),
        (600, PALE_BLUE, BLUE, '产品与场景能力', '用户对象梳理、功能模块定义、场景延展判断、解决方案表达', '把技术能力转为可解释的产品结构'),
        (770, PALE_AMBER, AMBER, '政策与材料能力', '政策搜集、合规边界分析、商业计划书撰写、申报材料整合', '保证项目叙事和比赛口径稳定'),
        (940, PALE_PURPLE, PURPLE, '展示与传播能力', '图表制作、页面呈现、GitHub 维护、答辩与路演支持', '把原型整理为可展示成果'),
    ]
    for y, fill, stroke, title, left_desc, right_desc in rows:
        rounded(d, (130, y, 1150, y + 120), fill, outline=stroke, width=2, radius=20)
        center_text(d, 245, y + 38, title, f(19), stroke)
        wrapped_text(d, 340, y + 24, left_desc, f(15), fill=TEXT, max_width=410, line_gap=7)
        d.line((740, y + 18, 740, y + 102), fill=stroke, width=2)
        wrapped_text(d, 790, y + 32, right_desc, f(15), fill=stroke, max_width=290, line_gap=7)

    rounded(d, (170, 1185, 1110, 1325), '#FFFFFF', outline=BORDER, radius=18)
    center_text(d, 640, 1232, '协同结果', f(20), TITLE)
    center_text(d, 640, 1278, '代码、实验、图表、政策材料、商业计划书和答辩内容可以被统一组织为一套完整项目资产。', f(15), SUB)

    rounded(d, (170, 1360, 1110, 1435), '#FFFFFF', outline=BORDER, radius=18)
    center_text(d, 640, 1398, '核心判断：项目靠的不是单点能力，而是多模块协同把复杂问题稳定推进为完整原型。', f(15), SUB)
    img.convert('RGB').save(OUT / '17_团队能力结构图_v3.png', quality=95)


def build_19_v3():
    img = Image.new('RGBA', (W, H), BG)
    d = ImageDraw.Draw(img)
    center_text(d, W/2, 48, '教育实效总结图', f(24), TITLE)
    center_text(d, W/2, 78, 'SolarGuard 在知识迁移、工程实践、研究论证与综合表达上的训练闭环', f(13), SUB)

    rounded(d, (90, 150, 1190, 1460), PAGE, outline=BORDER, radius=26)

    # training path
    steps = [
        ((130, 255, 455, 520), PALE_GREEN, GREEN, '知识迁移', '把通信协议、程序设计、数据处理、前后端与区块链知识迁移到真实问题中。'),
        ((478, 255, 803, 520), PALE_BLUE, BLUE, '工程实践', '围绕设备、脚本、接口、页面和系统运行逻辑形成完整原型。'),
        ((826, 255, 1150, 520), PALE_AMBER, AMBER, '研究论证', '同步进行政策研判、场景分析、商业论证和合规边界判断。'),
    ]
    for (x1,y1,x2,y2), fill, stroke, title, desc in steps:
        rounded(d, (x1,y1,x2,y2), fill, outline=stroke, width=2, radius=22)
        center_text(d, (x1+x2)/2, y1+42, title, f(21), stroke)
        wrapped_text(d, x1+28, y1+92, desc, f(16), fill=TEXT, max_width=(x2-x1)-56, line_gap=8)

    d.line((455, 388, 478, 388), fill=LINE, width=3)
    draw_arrow(d, 455, 388, 478, 388, color=LINE, width=3)
    d.line((803, 388, 826, 388), fill=LINE, width=3)
    draw_arrow(d, 803, 388, 826, 388, color=LINE, width=3)

    mid = (220, 620, 1060, 860)
    rounded(d, mid, '#FFFFFF', outline=GREEN, width=2, radius=24)
    center_text(d, 640, 678, '综合表达与组织输出', f(24), GREEN)
    wrapped_text(
        d, 300, 730,
        '把代码、实验、图表、仓库、BP 和答辩材料组织成可被评委快速理解的项目成果，完成从“做系统”到“讲清系统”的能力转换。',
        f(17), fill=TEXT, max_width=680, line_gap=9, center=True
    )

    bottom = (170, 970, 1110, 1245)
    img.alpha_composite(shadow(Image.new('RGBA', (W, H), (0,0,0,0)), bottom))
    rounded(d, bottom, '#FFFFFF', outline=GREEN, width=2, radius=24)
    center_text(d, 640, 1032, '教育实效结论', f(24), GREEN)
    wrapped_text(
        d, 250, 1090,
        '项目训练价值不只在于“做出一个项目”，而在于让成员完成从知识学习到系统实现、从技术验证到现实表达的完整成长闭环。它符合创新大赛“以赛促学、以创促用、专创融合”的核心要求。',
        f(18), fill=TEXT, max_width=780, line_gap=10, center=True
    )

    rounded(d, (190, 1315, 1090, 1390), '#FFFFFF', outline=BORDER, radius=18)
    center_text(d, 640, 1353, '适合创新大赛口径：真实问题驱动、跨模块协同、工程化训练、综合表达', f(16), SUB)
    img.convert('RGB').save(OUT / '19_教育实效总结图_v3.png', quality=95)

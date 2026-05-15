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
RED = '#B45309'
PALE_RED = '#FFF7ED'
LINE = '#6B7280'
PURPLE = '#7C3AED'
PALE_PURPLE = '#F3E8FF'


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
        chars = []
        lines = []
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


def build_11():
    img = Image.new('RGBA', (W, H), BG)
    d = ImageDraw.Draw(img)
    center_text(d, W/2, 48, '项目亮点总结图', f(24), TITLE)
    center_text(d, W/2, 78, 'SolarGuard 在真实场景、可信链路、系统闭环与政策适配上的核心优势', f(13), SUB)

    center = (250, 190, 1030, 360)
    img.alpha_composite(shadow(Image.new('RGBA', (W, H), (0,0,0,0)), center))
    rounded(d, center, '#FFFFFF', outline=GREEN, width=2, radius=26)
    center_text(d, 640, 245, 'SolarGuard', f(34), GREEN)
    center_text(d, 640, 288, '分布式光伏可信存证与绿色资产服务平台', f(18), TITLE)
    center_text(d, 640, 326, '以真实设备数据为锚点，构建可信采集、存证、展示与场景服务闭环', f(14), SUB)

    cards = [
        (110, 470, 585, 760, PALE_GREEN, GREEN, '真实场景', '围绕实际光伏控制器完成数据读取、状态监测与连续记录实验。\n项目具有明确物理世界锚点，不是停留在概念层的空转方案。'),
        (695, 470, 1170, 760, PALE_BLUE, BLUE, '可信链路', '通过数字签名、联盟链存证、自动监测与多模块联动，\n把普通看板式监控升级为具备可验证能力的数据底座。'),
        (110, 860, 585, 1150, PALE_AMBER, AMBER, '系统闭环', '现有代码和实验结果已打通硬件采集、边缘处理、链上记录、\n前端可视化等关键环节，形成可演示的系统原型。'),
        (695, 860, 1170, 1150, PALE_PURPLE, PURPLE, '政策适配', '项目主动从 RWA 金融化叙事切换到新能源可信数据、\n绿色资产核验与绿色金融辅助服务，更适合当前申报环境。'),
    ]
    for x1, y1, x2, y2, fill, stroke, title, desc in cards:
        img.alpha_composite(shadow(Image.new('RGBA', (W, H), (0,0,0,0)), (x1, y1, x2, y2), radius=18))
        rounded(d, (x1, y1, x2, y2), fill, outline=stroke, width=2, radius=22)
        center_text(d, (x1+x2)/2, y1+42, title, f(20), stroke)
        wrapped_text(d, x1+28, y1+86, desc, f(14), fill=TEXT, max_width=(x2-x1)-56, line_gap=8)

    rounded(d, (110, 1260, 1170, 1455), PAGE, outline=BORDER, radius=22)
    center_text(d, 640, 1304, '比赛表达重点', f(18), TITLE)
    bullets = [
        '突出“真实设备 + 可信数据 + 合规服务”三位一体，不再以代币化为对外核心卖点。',
        '强调系统原型已完成关键闭环验证，兼具技术深度与应用场景延展性。',
        '将绿证、ESG、绿色金融辅助判断作为高价值服务方向，而非面向公众的金融化交易工具。',
    ]
    y = 1345
    for b in bullets:
        d.ellipse((156, y+4, 168, y+16), fill=GREEN)
        wrapped_text(d, 186, y-2, b, f(14), fill=TEXT, max_width=920, line_gap=7)
        y += 40
    img.convert('RGB').save(OUT / '11_项目亮点总结图_v1.png', quality=95)


def build_12():
    img = Image.new('RGBA', (W, H), BG)
    d = ImageDraw.Draw(img)
    center_text(d, W/2, 48, '政策支持逻辑图', f(24), TITLE)
    center_text(d, W/2, 78, '国家政策方向与 SolarGuard 项目定位之间的对应关系', f(13), SUB)

    rounded(d, (90, 130, 1190, 1460), PAGE, outline=BORDER, radius=24)
    # top policy cards
    top_cards = [
        (130, 210, 480, 360, PALE_GREEN, GREEN, '数据要素与可信数据空间', '支持数据要素化、可信流通与多主体协同，强调可控、可管、可核验。'),
        (465, 210, 815, 360, PALE_BLUE, BLUE, '数字金融与绿色金融', '强调数字技术服务实体经济，提升绿色项目判断、尽调与信息核验效率。'),
        (800, 210, 1150, 360, PALE_AMBER, AMBER, '绿证制度与分布式光伏管理', '围绕可再生能源环境权益确权与分布式光伏开发建设管理形成制度锚点。'),
    ]
    for x1, y1, x2, y2, fill, stroke, title, desc in top_cards:
        rounded(d, (x1, y1, x2, y2), fill, outline=stroke, width=2, radius=20)
        center_text(d, (x1+x2)/2, y1+34, title, f(17), stroke)
        wrapped_text(d, x1+22, y1+72, desc, f(13), fill=TEXT, max_width=(x2-x1)-44, line_gap=7)

    center_box = (280, 520, 1000, 720)
    img.alpha_composite(shadow(Image.new('RGBA', (W, H), (0,0,0,0)), center_box))
    rounded(d, center_box, '#FFFFFF', outline=GREEN, width=2, radius=24)
    center_text(d, 640, 576, 'SolarGuard 合规项目定位', f(26), GREEN)
    center_text(d, 640, 622, '面向分布式光伏场景的可信数据采集、联盟链存证与绿色资产服务平台', f(16), TITLE)
    center_text(d, 640, 662, '重点放在可信数据、绿证衔接、ESG 披露支持与绿色金融辅助决策', f(14), SUB)

    for x in [305, 640, 975]:
        draw_arrow(d, x, 360, 640, 520, color=LINE, width=3)

    bottom_cards = [
        (130, 900, 470, 1120, PALE_GREEN, GREEN, '项目获得的正向支撑', '数据可信化、行业数字化、可再生能源权益管理、绿色项目核验与审计场景均有明确政策支撑。'),
        (490, 900, 790, 1120, PALE_BLUE, BLUE, '项目当前可稳妥表达', '可信采集\n联盟链存证\n绿证辅助核验\nESG 披露支持\n绿色金融辅助判断'),
        (810, 900, 1150, 1120, PALE_AMBER, AMBER, '未来延伸方向', '在合规前提下继续拓展面向园区、企业、机构的可信数据服务与绿色治理应用。'),
    ]
    for x1, y1, x2, y2, fill, stroke, title, desc in bottom_cards:
        rounded(d, (x1, y1, x2, y2), fill, outline=stroke, width=2, radius=20)
        center_text(d, (x1+x2)/2, y1+34, title, f(17), stroke)
        wrapped_text(d, x1+22, y1+72, desc, f(13), fill=TEXT, max_width=(x2-x1)-44, line_gap=7)
        draw_arrow(d, 640, 720, (x1+x2)/2, y1, color=LINE, width=3)

    rounded(d, (170, 1230, 1110, 1360), '#FFFFFF', outline=BORDER, radius=18)
    center_text(d, 640, 1270, '结论', f(18), TITLE)
    center_text(d, 640, 1314, '项目不是去做公众代币化平台，而是在新能源场景中建设可信数据基础设施并服务正式制度场景。', f(14), SUB)
    img.convert('RGB').save(OUT / '12_政策支持逻辑图_v1.png', quality=95)


def build_13():
    img = Image.new('RGBA', (W, H), BG)
    d = ImageDraw.Draw(img)
    center_text(d, W/2, 48, '合规边界示意图', f(24), TITLE)
    center_text(d, W/2, 78, '明确 SolarGuard 当前能做什么、不能怎么表达，以及可延伸的合规方向', f(13), SUB)

    rounded(d, (90, 130, 1190, 1460), PAGE, outline=BORDER, radius=24)

    left = (120, 220, 560, 1120)
    center = (420, 460, 860, 1260)
    right = (720, 220, 1160, 1120)

    rounded(d, left, PALE_GREEN, outline=GREEN, width=2, radius=24)
    center_text(d, 340, 264, '当前重点可做', f(22), GREEN)
    ok_items = [
        '分布式光伏设备数据采集',
        '数据结构化与数字签名',
        '联盟链存证与链上查询',
        '自动监测、图表和摘要报告',
        '绿证辅助核验与 ESG 披露支持',
        '绿色金融辅助尽调与审计支持',
    ]
    y = 320
    for item in ok_items:
        d.ellipse((150, y+4, 164, y+18), fill=GREEN)
        wrapped_text(d, 184, y, item, f(16), fill=TITLE, max_width=330, line_gap=6)
        y += 94

    rounded(d, right, PALE_RED, outline=RED, width=2, radius=24)
    center_text(d, 940, 264, '当前不能这样写', f(22), RED)
    no_items = [
        '公开代币发行',
        '稳定币兑换作为主体业务',
        'DEX 交易平台作为项目核心',
        '面向公众的金融化募集与流转',
        '将 RWA 叙事作为当前大陆落地主路径',
    ]
    y = 330
    for item in no_items:
        d.line((756, y+11, 772, y+27), fill=RED, width=3)
        d.line((772, y+11, 756, y+27), fill=RED, width=3)
        wrapped_text(d, 792, y, item, f(16), fill=TITLE, max_width=320, line_gap=6)
        y += 108

    rounded(d, center, '#FFFFFF', outline=BORDER, width=2, radius=26)
    center_text(d, 640, 506, '合规表达转换', f(24), TITLE)
    center_text(d, 640, 548, '从“RWA 金融化叙事”切换到“新能源可信数据与绿色资产服务叙事”', f(14), SUB)
    steps = [
        ('原有技术探索', '价值映射逻辑、自动结算原型、绿色资产数字化机制验证'),
        ('当前对外表达', '可信数据采集、联盟链存证、绿证衔接、ESG 披露与绿色金融辅助服务'),
        ('后续延伸原则', '始终在监管允许框架下推进，不把代币发行和公众交易作为当前项目卖点'),
    ]
    y = 620
    for i, (title, desc) in enumerate(steps, start=1):
        rounded(d, (470, y, 810, y+150), PAGE, outline=BORDER, width=2, radius=18)
        d.ellipse((490, y+24, 534, y+68), fill=GREEN)
        center_text(d, 512, y+46, str(i), f(18), '#FFFFFF')
        d.text((556, y+22), title, font=f(16), fill=TITLE)
        wrapped_text(d, 556, y+56, desc, f(13), fill=TEXT, max_width=224, line_gap=6)
        if i < len(steps):
            draw_arrow(d, 640, y+150, 640, y+190, color=LINE, width=3)
        y += 190

    draw_arrow(d, 560, 670, 470, 670, color=GREEN, width=3)
    draw_arrow(d, 860, 670, 980, 670, color=RED, width=3)

    rounded(d, (170, 1320, 1110, 1415), '#FFFFFF', outline=BORDER, radius=18)
    center_text(d, 640, 1350, '结论', f(18), TITLE)
    center_text(d, 640, 1385, '保留技术深度，收紧金融化表述，强化可信数据与绿色治理场景，是当前最稳妥的比赛与落地方向。', f(14), SUB)
    img.convert('RGB').save(OUT / '13_合规边界示意图_v1.png', quality=95)


if __name__ == '__main__':
    build_11()
    build_12()
    build_13()

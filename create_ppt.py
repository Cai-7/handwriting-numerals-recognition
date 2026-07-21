from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import math

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

BG_DARK = RGBColor(0x0F, 0x0F, 0x1A)
BG_CARD = RGBColor(0x1A, 0x1A, 0x2E)
ACCENT = RGBColor(0x00, 0xD2, 0xFF)
ACCENT2 = RGBColor(0x7C, 0x3A, 0xED)
GOLD = RGBColor(0xFF, 0xD7, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0xAA, 0xAA, 0xCC)

def set_slide_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_shape(slide, left, top, width, height, fill_color=None, line_color=None, line_width=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.line.fill.background()
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.fill.solid()
        shape.line.color.rgb = line_color
        if line_width:
            shape.line.width = line_width
    return shape

def add_rounded_rect(slide, left, top, width, height, fill_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.line.fill.background()
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    return shape

def add_text_box(slide, left, top, width, height, text, font_size=18, color=WHITE, bold=False, alignment=PP_ALIGN.LEFT, font_name="Microsoft YaHei"):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox

def add_paragraph(text_frame, text, font_size=16, color=WHITE, bold=False, alignment=PP_ALIGN.LEFT, space_before=Pt(6), font_name="Microsoft YaHei"):
    p = text_frame.add_paragraph()
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    if space_before:
        p.space_before = space_before
    return p

def add_accent_bar(slide, left, top, width, height, color=ACCENT):
    return add_shape(slide, left, top, width, height, fill_color=color)

def add_gradient_overlay(slide):
    for i in range(60):
        alpha = int(30 * (1 - i / 60))
        c = RGBColor(0x00, 0xD2, 0xFF)
        shape = add_shape(slide, Inches(13.333) - Inches(i * 0.05), Inches(0),
                          Inches(0.05), Inches(7.5), fill_color=c)
        shape.fill.fore_color.brightness = 1.0 - (i / 60) * 0.3

def add_circle(slide, left, top, size, fill_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, size, size)
    shape.line.fill.background()
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    return shape

def add_grid_dots(slide):
    for x in range(0, 14, 2):
        for y in range(0, 8, 2):
            dot = add_circle(slide, Inches(x + 0.1), Inches(y + 0.1), Inches(0.04))
            dot.fill.solid()
            dot.fill.fore_color.rgb = RGBColor(0x2A, 0x2A, 0x44)
            dot.fill.fore_color.brightness = 0.7


# ==================== PAGE 1: COVER ====================
slide1 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide1, BG_DARK)

# Decorative circles
add_circle(slide1, Inches(-0.8), Inches(-0.8), Inches(2.5), fill_color=RGBColor(0x00, 0xD2, 0xFF))
slide1.shapes[-1].fill.fore_color.brightness = 0.85

add_circle(slide1, Inches(11.5), Inches(-1.0), Inches(3.0), fill_color=RGBColor(0x7C, 0x3A, 0xED))
slide1.shapes[-1].fill.fore_color.brightness = 0.85

add_circle(slide1, Inches(10.0), Inches(5.5), Inches(2.0), fill_color=RGBColor(0x00, 0xD2, 0xFF))
slide1.shapes[-1].fill.fore_color.brightness = 0.9

# Left accent bar
add_accent_bar(slide1, Inches(0.8), Inches(1.8), Inches(0.08), Inches(3.8), ACCENT)

# Tag line
add_text_box(slide1, Inches(1.3), Inches(2.0), Inches(6), Inches(0.6),
             "DEEP LEARNING · COMPUTER VISION", font_size=14, color=ACCENT,
             bold=True, alignment=PP_ALIGN.LEFT)

# Main title
add_text_box(slide1, Inches(1.3), Inches(2.6), Inches(8), Inches(1.2),
             "手写数字识别系统", font_size=52, color=WHITE,
             bold=True, alignment=PP_ALIGN.LEFT)

# Subtitle
add_text_box(slide1, Inches(1.3), Inches(3.9), Inches(8), Inches(0.8),
             "基于 PyTorch 的卷积神经网络 · MNIST 数据集 · 端到端解决方案",
             font_size=20, color=GRAY, alignment=PP_ALIGN.LEFT)

# Divider line
add_shape(slide1, Inches(1.3), Inches(5.0), Inches(2.5), Inches(0.04), fill_color=ACCENT)

# Bottom info
add_text_box(slide1, Inches(1.3), Inches(5.4), Inches(5), Inches(0.5),
             "2026 · 项目展示", font_size=13, color=GRAY, alignment=PP_ALIGN.LEFT)

# Right side decorative code block
code_bg = add_rounded_rect(slide1, Inches(8.0), Inches(2.0), Inches(4.5), Inches(3.8), fill_color=BG_CARD)
code_text = add_text_box(slide1, Inches(8.3), Inches(2.3), Inches(4.0), Inches(3.2),
             "model.eval()\nwith torch.no_grad():\n    output = model(img)\n    pred = output.argmax(1)\n\nprint(f\"预测结果: {pred}\")",
             font_size=13, color=ACCENT2, font_name="Consolas", alignment=PP_ALIGN.LEFT)

# ==================== PAGE 2: TECH ARCHITECTURE ====================
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide2, BG_DARK)

# Top accent line
add_accent_bar(slide2, Inches(0), Inches(0), Inches(13.333), Inches(0.04), ACCENT)

# Page number
add_text_box(slide2, Inches(12.3), Inches(0.3), Inches(0.8), Inches(0.4),
             "02", font_size=12, color=ACCENT, bold=True, alignment=PP_ALIGN.RIGHT, font_name="Arial")

# Section title
add_accent_bar(slide2, Inches(0.8), Inches(0.6), Inches(0.06), Inches(0.5), ACCENT)
add_text_box(slide2, Inches(1.1), Inches(0.5), Inches(6), Inches(0.7),
             "系统架构", font_size=30, color=WHITE, bold=True)

# Three tech stack cards
card_data = [
    {
        "title": "模型定义",
        "icon": "🧠",
        "items": [
            "SimpleNet · CNN 架构",
            "卷积层 Conv2d(1→32→64)",
            "BatchNorm + ReLU 激活",
            "MaxPool 2×2 下采样",
            "全连接层 12544→128→10",
            "Dropout 0.5 防过拟合",
        ]
    },
    {
        "title": "训练流程",
        "icon": "⚙️",
        "items": [
            "MNIST 数据集 60000 张",
            "9:1 训练验证集划分",
            "Adam 优化器 · lr=0.001",
            "ReduceLROnPlateau 调度",
            "CrossEntropyLoss 损失",
            "10 Epochs 迭代训练",
        ]
    },
    {
        "title": "推理部署",
        "icon": "🚀",
        "items": [
            "单图片预测接口",
            "GUI 可视化预测界面",
            "预处理: Resize→灰度→归一化",
            "GPU/CUDA 自动加速",
            "模型权重 mnist_net.pth",
            "即插即用 · 无需重新训练",
        ]
    }
]

for i, card in enumerate(card_data):
    x = Inches(0.8 + i * 4.1)
    y = Inches(1.6)
    w = Inches(3.7)
    h = Inches(5.2)

    card_bg = add_rounded_rect(slide2, x, y, w, h, fill_color=BG_CARD)

    # Icon
    add_text_box(slide2, Inches(0.8 + i * 4.1 + 0.3), Inches(1.9), Inches(0.5), Inches(0.5),
                 card["icon"], font_size=28)

    # Card title
    add_text_box(slide2, Inches(0.8 + i * 4.1 + 1.0), Inches(1.95), Inches(2.5), Inches(0.5),
                 card["title"], font_size=20, color=ACCENT, bold=True)

    # Divider
    add_accent_bar(slide2, Inches(0.8 + i * 4.1 + 0.3), Inches(2.6), Inches(3.1), Inches(0.02), ACCENT2)

    # Items
    txBox = slide2.shapes.add_textbox(Inches(0.8 + i * 4.1 + 0.3), Inches(2.9), Inches(3.1), Inches(3.6))
    tf = txBox.text_frame
    tf.word_wrap = True
    for j, item in enumerate(card["items"]):
        if j == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
            p.space_before = Pt(10)
        p.text = item
        p.font.size = Pt(14)
        p.font.color.rgb = WHITE
        p.font.name = "Microsoft YaHei"

# Bottom flow arrow
flow_y = Inches(7.0)
arrow_shapes = ["数据加载", "模型推理", "结果输出"]
for i, label in enumerate(arrow_shapes):
    x = Inches(1.8 + i * 4.5)
    box = add_rounded_rect(slide2, x, flow_y, Inches(2.5), Inches(0.4), fill_color=RGBColor(0x2A, 0x2A, 0x44))
    add_text_box(slide2, x, flow_y, Inches(2.5), Inches(0.4),
                 label, font_size=13, color=ACCENT, alignment=PP_ALIGN.CENTER, bold=True)
    if i < 2:
        add_text_box(slide2, Inches(4.4 + i * 4.5), flow_y, Inches(0.5), Inches(0.4),
                     "→", font_size=18, color=GOLD, alignment=PP_ALIGN.CENTER)


# ==================== PAGE 3: RESULTS ====================
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide3, BG_DARK)

# Top accent line
add_accent_bar(slide3, Inches(0), Inches(0), Inches(13.333), Inches(0.04), ACCENT)

# Page number
add_text_box(slide3, Inches(12.3), Inches(0.3), Inches(0.8), Inches(0.4),
             "03", font_size=12, color=ACCENT, bold=True, alignment=PP_ALIGN.RIGHT, font_name="Arial")

# Section title
add_accent_bar(slide3, Inches(0.8), Inches(0.6), Inches(0.06), Inches(0.5), ACCENT)
add_text_box(slide3, Inches(1.1), Inches(0.5), Inches(6), Inches(0.7),
             "性能与成果", font_size=30, color=WHITE, bold=True)

# Big metrics boxes
metrics = [
    ("99%+", "测试准确率", "在 10000 张\nMNIST 测试集上"),
    ("96%+", "就业级就业率", "模型稳定\n高精度推理"),
    ("<5ms", "单图推理", "GPU 加速\n毫秒级响应"),
    ("10", "训练轮次", "快速收敛\n高效训练"),
]

for i, (value, label, desc) in enumerate(metrics):
    x = Inches(0.8 + i * 3.15)
    y = Inches(1.6)
    w = Inches(2.8)
    h = Inches(2.5)

    card_bg = add_rounded_rect(slide3, x, y, w, h, fill_color=BG_CARD)
    # Gold top border
    add_accent_bar(slide3, x + Inches(0.5), y + Inches(0.2), Inches(1.8), Inches(0.03), GOLD)

    add_text_box(slide3, x, Inches(0.6 + y), w, Inches(0.8),
                 value, font_size=36, color=GOLD, bold=True, alignment=PP_ALIGN.CENTER, font_name="Arial")
    add_text_box(slide3, x, Inches(1.3 + y), w, Inches(0.4),
                 label, font_size=16, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide3, x, Inches(1.8 + y), w, Inches(0.6),
                 desc, font_size=12, color=GRAY, alignment=PP_ALIGN.CENTER)

# Project structure section
add_text_box(slide3, Inches(0.8), Inches(4.5), Inches(6), Inches(0.5),
             "项目文件结构", font_size=20, color=ACCENT, bold=True)
add_accent_bar(slide3, Inches(0.8), Inches(5.1), Inches(1.5), Inches(0.02), ACCENT2)

files_text = (
    "my_model.py    卷积神经网络模型定义\n"
    "train.py       训练与评估函数\n"
    "main.py        主训练管线入口\n"
    "predict.py     单图片预测工具\n"
    "gui_predict.py 图形化预测界面\n"
    "mnist_net.pth  预训练模型权重"
)
add_text_box(slide3, Inches(0.8), Inches(5.3), Inches(5.5), Inches(2.0),
             files_text, font_size=13, color=WHITE, font_name="Consolas")

# Tech stack on the right
add_text_box(slide3, Inches(7.5), Inches(4.5), Inches(5.5), Inches(0.5),
             "技术栈", font_size=20, color=ACCENT, bold=True)
add_accent_bar(slide3, Inches(7.5), Inches(5.1), Inches(1.5), Inches(0.02), ACCENT2)

tech_items = [
    ("PyTorch", "深度学习框架"),
    ("TorchVision", "数据处理与变换"),
    ("Pillow", "图像加载与处理"),
    ("Tkinter", "GUI 界面构建"),
    ("Python 3.13", "运行环境"),
]

for i, (tech, desc) in enumerate(tech_items):
    y = Inches(5.3 + i * 0.38)
    add_text_box(slide3, Inches(7.5), y, Inches(2.5), Inches(0.35),
                 f"▸ {tech}", font_size=14, color=GOLD, bold=True, font_name="Consolas")
    add_text_box(slide3, Inches(10.0), y, Inches(3.0), Inches(0.35),
                 desc, font_size=12, color=GRAY)

# Bottom closing line
add_accent_bar(slide3, Inches(4.0), Inches(7.2), Inches(5.333), Inches(0.02), ACCENT)
add_text_box(slide3, Inches(4.0), Inches(7.1), Inches(5.333), Inches(0.4),
             "从数据到模型 · 从训练到部署 · 端到端深度学习解决方案",
             font_size=11, color=GRAY, alignment=PP_ALIGN.CENTER)

# Save
output_path = "手写数字识别系统.pptx"
prs.save(output_path)
print(f"PPT saved: {output_path}")

"""生成论文第4章所需图表PNG — 加宽布局，避免文字遮挡"""
from PIL import Image, ImageDraw, ImageFont
import os, math

OUT = "diagrams"
os.makedirs(OUT, exist_ok=True)

# 加载中文字体
FONT_PATHS = [
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/simsun.ttc",
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simfang.ttf",
]
FONT = FONT_SM = FONT_BOLD = FONT_TITLE = None
for fp in FONT_PATHS:
    if os.path.exists(fp):
        try:
            FONT   = ImageFont.truetype(fp, 16)
            FONT_SM= ImageFont.truetype(fp, 13)
            FONT_BOLD=ImageFont.truetype(fp, 17)
            FONT_TITLE=ImageFont.truetype(fp, 20)
            break
        except Exception:
            continue
if FONT is None:
    FONT = FONT_SM = FONT_BOLD = FONT_TITLE = ImageFont.load_default()


def text_w(text, font=None):
    """测量文本宽度"""
    if font is None:
        font = FONT
    b = ImageDraw.Draw(Image.new("RGB", (1, 1))).textbbox((0, 0), text, font=font)
    return b[2] - b[0]


def draw_box(draw, x1, y1, x2, y2, lines, fill="#E8F0FE", outline="#1A73E8",
             font=None, text_color="#222"):
    """绘制圆角矩形，lines 为字符串列表，逐行居中"""
    r = 8
    draw.rounded_rectangle([x1, y1, x2, y2], radius=r, fill=fill, outline=outline, width=2)
    if font is None:
        font = FONT
    lh = 26
    total_h = len(lines) * lh
    cy = (y1 + y2 - total_h) // 2 + 2
    for line in lines:
        tw = text_w(line, font)
        draw.text(((x2 + x1 - tw) // 2, cy), line, fill=text_color, font=font)
        cy += lh


def draw_arrow(draw, x1, y1, x2, y2, color="#555", lw=2):
    """绘制带箭头直线"""
    draw.line([x1, y1, x2, y2], fill=color, width=lw)
    al = 12
    angle = math.atan2(y2 - y1, x2 - x1)
    ax1 = x2 - al * math.cos(angle - 0.45)
    ay1 = y2 - al * math.sin(angle - 0.45)
    ax2 = x2 - al * math.cos(angle + 0.45)
    ay2 = y2 - al * math.sin(angle + 0.45)
    draw.polygon([(x2, y2), (ax1, ay1), (ax2, ay2)], fill=color)


def draw_label(draw, x, y, text, font=None, color="#666"):
    if font is None:
        font = FONT_SM
    draw.text((x, y), text, fill=color, font=font)


# ══════════════════════════════════════
# 图1：系统总体架构
# ══════════════════════════════════════
def gen_architecture():
    W, H = 900, 580
    img = Image.new("RGB", (W, H), "#FAFAFA")
    draw = ImageDraw.Draw(img)

    tw = text_w("系统总体架构图", FONT_TITLE)
    draw.text(((W - tw) // 2, 16), "系统总体架构图", fill="#333", font=FONT_TITLE)

    # 左侧主层
    bw, bh = 460, 76
    lx = 40
    gap = 32  # 层间距

    layers = [
        ("#FFF3E0", "#E65100", ["前端层", "Vue 3 + Element Plus + Axios", "浏览器端 (localhost:5173)"]),
        ("#E8F5E9", "#2E7D32", ["API 网关层", "FastAPI + CORS 中间件", "服务端 (127.0.0.1:8000)"]),
        ("#E3F2FD", "#1565C0", ["业务逻辑层", "NL2SQL Service | SQL安全校验", "数据查询服务"]),
        ("#FFF8E1", "#F9A825", ["数据层", "MySQL 数据库", "localhost:3306"]),
    ]

    y_positions = []
    cy = 55
    for i, (fill, out, lines) in enumerate(layers):
        draw_box(draw, lx, cy, lx + bw, cy + bh, lines, fill=fill, outline=out)
        y_positions.append((cy, cy + bh))
        if i < len(layers) - 1:
            draw_arrow(draw, lx + bw // 2, cy + bh, lx + bw // 2, cy + bh + gap)
        cy += bh + gap

    # AI服务层 — 业务逻辑层右侧
    ai_w, ai_h = 280, 76
    ai_x = lx + bw + 60  # 560
    biz_mid = (y_positions[2][0] + y_positions[2][1]) // 2
    ai_y = biz_mid - ai_h // 2

    draw_box(draw, ai_x, ai_y, ai_x + ai_w, ai_y + ai_h,
             ["AI 服务层", "DashScope API (Qwen-Plus)", "通义千问大语言模型"],
             fill="#F3E5F5", outline="#7B1FA2")

    # 连线
    draw_arrow(draw, lx + bw, biz_mid, ai_x, biz_mid, color="#7B1FA2")
    # 标签放在箭头下方
    draw_label(draw, lx + bw + 8, biz_mid + 8, "HTTP / REST (JSON)", color="#7B1FA2")

    img.save(f"{OUT}/architecture.png", dpi=(150, 150))
    print("architecture.png saved")


# ══════════════════════════════════════
# 图2：后端模块调用关系
# ══════════════════════════════════════
def gen_backend_modules():
    W, H = 880, 420
    img = Image.new("RGB", (W, H), "#FAFAFA")
    draw = ImageDraw.Draw(img)

    tw = text_w("后端模块调用关系", FONT_TITLE)
    draw.text(((W - tw) // 2, 14), "后端模块调用关系", fill="#333", font=FONT_TITLE)

    bw, bh = 180, 80
    gap_x = 50

    # 第一行：API层 → Service层 → DB层
    lx1, ly = 40, 70
    lx2 = lx1 + bw + gap_x
    lx3 = lx2 + bw + gap_x

    draw_box(draw, lx1, ly, lx1 + bw, ly + bh, ["API 层", "(endpoints/)"], fill="#E3F2FD", outline="#1565C0")
    draw_box(draw, lx2, ly, lx2 + bw, ly + bh, ["Service 层", "(services/)"], fill="#E8F5E9", outline="#2E7D32")
    draw_box(draw, lx3, ly, lx3 + bw, ly + bh, ["DB 层", "(db/)"], fill="#FFF3E0", outline="#E65100")

    draw_arrow(draw, lx1 + bw, ly + bh // 2, lx2, ly + bh // 2)
    draw_arrow(draw, lx2 + bw, ly + bh // 2, lx3, ly + bh // 2)

    # 第二行：LLM Service（Service层下方）     MySQL（DB层下方）
    row2_y = ly + bh + 70
    llm_w, llm_h = 260, 80
    db2_w, db2_h = 260, 80
    llm_x = lx2 + bw // 2 - llm_w // 2
    db2_x = lx3 + bw // 2 - db2_w // 2

    draw_box(draw, llm_x, row2_y, llm_x + llm_w, row2_y + llm_h,
             ["LLM Service", "(nlp2sql_service.py)", "调用 DashScope API (Qwen-Plus)"],
             fill="#F3E5F5", outline="#7B1FA2")
    draw_box(draw, db2_x, row2_y, db2_x + db2_w, row2_y + db2_h,
             ["MySQL 数据库", "(localhost:3306)", "存储医疗业务数据"],
             fill="#FFF8E1", outline="#F9A825")

    # Service层 → LLM Service
    draw_arrow(draw, lx2 + bw // 2, ly + bh, lx2 + bw // 2, row2_y)
    # DB层 → MySQL
    draw_arrow(draw, lx3 + bw // 2, ly + bh, lx3 + bw // 2, row2_y)

    # 标签
    draw_label(draw, lx2 + bw // 2 + 6, ly + bh + 4, "PyMySQL", color="#888")

    img.save(f"{OUT}/backend_modules.png", dpi=(150, 150))
    print("backend_modules.png saved")


# ══════════════════════════════════════
# 图3：前端数据流
# ══════════════════════════════════════
def gen_dataflow():
    W, H = 820, 340
    img = Image.new("RGB", (W, H), "#FAFAFA")
    draw = ImageDraw.Draw(img)

    tw = text_w("前端数据流", FONT_TITLE)
    draw.text(((W - tw) // 2, 12), "前端数据流", fill="#333", font=FONT_TITLE)

    bw, bh = 150, 64

    # 布局：左输入→中上text→中下handleQuery→中右request→右后端
    #                                             ↓
    #                                         右下 sql/tableData → 右模板渲染
    nodes = {
        "input":  (30, 140, ["用户输入"]),
        "text":   (220, 55, ["text (ref)", "响应式变量"]),
        "handle": (220, 225, ["handleQuery()", "异步处理函数"]),
        "req":    (420, 140, ["request.post", "POST /api/v1/query/"]),
        "backend":(620, 140, ["后端处理"]),
        "refs":   (420, 250, ["sql (ref)", "tableData (ref)"]),
        "render": (620, 250, ["模板渲染", "表格 / 卡片"]),
    }

    for key, (x, y, lines) in nodes.items():
        draw_box(draw, x, y, x + bw, y + bh, lines, fill="#E8F0FE", outline="#1A73E8")

    # 箭头
    draw_arrow(draw, 180, 172, 220, 87)                      # input→text
    draw_arrow(draw, 180, 172, 220, 257)                     # input→handle
    draw_arrow(draw, 370, 182, 420, 182)                     # handle→req
    draw_arrow(draw, 570, 172, 620, 172)                     # req→backend
    draw_arrow(draw, 620 + bw // 2, 204, 620 + bw // 2, 250) # backend→render
    draw_arrow(draw, 495, 282, 495, 272, color="#1A73E8")    # req→refs (向下回写)

    draw_label(draw, 450, 194, "HTTP JSON", color="#888")

    img.save(f"{OUT}/dataflow.png", dpi=(150, 150))
    print("dataflow.png saved")


# ══════════════════════════════════════
# 图4：ER 实体关系图 (7表)
# ══════════════════════════════════════
def gen_er():
    W, H = 1240, 820
    img = Image.new("RGB", (W, H), "#FAFAFA")
    draw = ImageDraw.Draw(img)

    tw = text_w("实体关系图 (ER Diagram)", FONT_TITLE)
    draw.text(((W - tw) // 2, 14), "实体关系图 (ER Diagram)", fill="#333", font=FONT_TITLE)

    bw, bh = 185, 174  # 统一盒子尺寸
    lh = 20  # 行高

    def draw_entity(draw, x, y, title, fields, fill, outline, title_color=None):
        if title_color is None:
            title_color = outline
        h_actual = 42 + len(fields) * lh + 10
        draw.rounded_rectangle([x, y, x + bw, y + h_actual], radius=8, fill=fill, outline=outline, width=2)
        draw.text((x + 10, y + 8), title, fill=title_color, font=FONT_BOLD)
        fy = y + 36
        for f in fields:
            draw.text((x + 12, fy), f, fill="#333", font=FONT_SM)
            fy += lh

    # ── 布局 ──
    # Row 0: departments (top center)
    dep_x, dep_y = (W - bw) // 2, 50

    # Row 1: doctors (left), patients (right)
    doc_x, doc_y = 80, 280
    pat_x, pat_y = W - bw - 80, 280

    # Row 2: four tables evenly spaced
    bottom_y = 530
    bot_tables = [
        ("diagnoses", "诊断记录表"),
        ("prescriptions", "处方记录表"),
        ("examinations", "检查记录表"),
        ("metrics", "生理指标表"),
    ]
    bot_n = len(bot_tables)
    bot_total_w = bot_n * bw + (bot_n - 1) * 25
    bot_start_x = (W - bot_total_w) // 2
    bot_positions = []
    for i in range(bot_n):
        bot_positions.append(bot_start_x + i * (bw + 25))

    # ── 实体定义 ──
    # departments
    dep_fields = [
        "PK  id      INT",
        "    name    VARCHAR(50)",
        "    location VARCHAR(50)",
        "    phone   VARCHAR(20)",
    ]
    draw_entity(draw, dep_x, dep_y, "departments", dep_fields, "#FFE0B2", "#E65100")

    # doctors
    doc_fields = [
        "PK  id            INT",
        "    name          VARCHAR(50)",
        "    gender        VARCHAR(5)",
        "    title         VARCHAR(30)",
        "FK  department_id INT",
        "    specialty     VARCHAR(100)",
    ]
    h_doc = 42 + len(doc_fields) * lh + 10
    draw_entity(draw, doc_x, doc_y, "doctors", doc_fields, "#E3F2FD", "#1565C0")

    # patients
    pat_fields = [
        "PK  id             INT",
        "    name           VARCHAR(50)",
        "    gender         VARCHAR(5)",
        "    age            INT",
        "    phone          VARCHAR(20)",
        "    address        VARCHAR(200)",
        "    admission_date DATE",
        "    discharge_date DATE",
        "FK  department_id  INT",
    ]
    h_pat = 42 + len(pat_fields) * lh + 10
    draw_entity(draw, pat_x, pat_y, "patients", pat_fields, "#FFF9C4", "#F9A825", "#F57F17")

    # diagnoses
    diag_fields = [
        "PK  id            INT",
        "",
        "FK  patient_id    INT",
        "FK  doctor_id     INT",
        "    disease_name  VARCHAR(100)",
        "    diagnosis_type VARCHAR(20)",
        "    diagnosis_date DATE",
        "    notes         TEXT",
    ]
    draw_entity(draw, bot_positions[0], bottom_y, "diagnoses", diag_fields, "#C8E6C9", "#2E7D32")

    # prescriptions
    pres_fields = [
        "PK  id          INT",
        "",
        "FK  patient_id  INT",
        "FK  doctor_id   INT",
        "    drug_name   VARCHAR(100)",
        "    dosage      VARCHAR(50)",
        "    frequency   VARCHAR(50)",
        "    start_date  DATE",
        "    end_date    DATE",
        "    cost        DECIMAL(10,2)",
    ]
    draw_entity(draw, bot_positions[1], bottom_y, "prescriptions", pres_fields, "#B2DFDB", "#00695C")

    # examinations
    exam_fields = [
        "PK  id          INT",
        "",
        "FK  patient_id  INT",
        "FK  doctor_id   INT",
        "    exam_type   VARCHAR(50)",
        "    exam_item   VARCHAR(100)",
        "    exam_date   DATE",
        "    result      TEXT",
        "    cost        DECIMAL(10,2)",
    ]
    draw_entity(draw, bot_positions[2], bottom_y, "examinations", exam_fields, "#D1C4E9", "#512DA8")

    # metrics
    met_fields = [
        "PK  id                 INT",
        "",
        "FK  patient_id         INT",
        "    measure_date       DATETIME",
        "    heart_rate         INT",
        "    systolic_pressure  INT",
        "    diastolic_pressure INT",
        "    temperature        DECIMAL(3,1)",
        "    blood_sugar        DECIMAL(5,2)",
        "    oxygen_saturation  DECIMAL(4,1)",
        "    respiratory_rate   INT",
        "    notes              VARCHAR(200)",
    ]
    draw_entity(draw, bot_positions[3], bottom_y, "metrics", met_fields, "#FFCDD2", "#C62828")

    # ── 连线 ──
    # departments → doctors (左下)
    d_doc_cx, d_doc_cy = doc_x + bw // 2, doc_y
    draw_arrow(draw, dep_x + bw // 3, dep_y + 42 + len(dep_fields) * lh + 10,
               d_doc_cx, d_doc_cy, color="#888", lw=1)
    draw_label(draw, dep_x + bw // 3 - 50, d_doc_cy - 20, "1 : N", color="#888")

    # departments → patients (右下)
    d_pat_cx, d_pat_cy = pat_x + bw // 2, pat_y
    draw_arrow(draw, dep_x + 2 * bw // 3, dep_y + 42 + len(dep_fields) * lh + 10,
               d_pat_cx, d_pat_cy, color="#888", lw=1)
    draw_label(draw, dep_x + 2 * bw // 3 + 10, d_pat_cy - 20, "1 : N", color="#888")

    # doctors bottom → diagnoses, prescriptions, examinations
    doc_bottom_y = doc_y + h_doc
    doc_bottom_cx = doc_x + bw // 2
    for i in range(3):
        btop = bot_positions[i] + bw // 2
        draw_arrow(draw, doc_bottom_cx, doc_bottom_y, btop, bottom_y, color="#666", lw=1)

    # patients bottom → diagnoses, prescriptions, examinations, metrics
    pat_bottom_y = pat_y + h_pat
    pat_bottom_cx = pat_x + bw // 2
    for i in range(4):
        btop = bot_positions[i] + bw // 2
        draw_arrow(draw, pat_bottom_cx, pat_bottom_y, btop, bottom_y, color="#666", lw=1)

    # FK labels
    draw_label(draw, doc_bottom_cx - 160, doc_bottom_y + 8, "FK: doctor_id", color="#555")
    draw_label(draw, pat_bottom_cx + 15, pat_bottom_y + 8, "FK: patient_id", color="#555")
    draw_label(draw, bot_positions[0] + bw + 5, bottom_y + 42, "FK: patient_id, doctor_id", color="#555")

    img.save(f"{OUT}/er_diagram.png", dpi=(150, 150))
    print("er_diagram.png saved")


# ══════════════════════════════════════
# 图5：Prompt 结构化设计
# ══════════════════════════════════════
def gen_prompt_structure():
    W, H = 640, 480
    img = Image.new("RGB", (W, H), "#FAFAFA")
    draw = ImageDraw.Draw(img)

    tw = text_w("Prompt 结构化设计", FONT_TITLE)
    draw.text(((W - tw) // 2, 12), "Prompt 结构化设计", fill="#333", font=FONT_TITLE)

    margin = 30
    bw = W - margin * 2
    bh = 62
    gap = 20

    parts = [
        ("#E3F2FD", "#1565C0", ["1. 角色设定", "你是一个医疗数据库 SQL 生成助手"]),
        ("#E8F5E9", "#2E7D32", ["2. 数据库结构", "SHOW TABLES / SHOW COLUMNS 获取的表与字段信息"]),
        ("#FFF3E0", "#E65100", ["3. 行为规则", "仅 SELECT · 纯 SQL 输出 · 兜底策略 · 安全响应"]),
        ("#F3E5F5", "#7B1FA2", ["4. 注意事项", "中文字段映射 · 聚合/排序/分页 · 类型匹配 · 中文别名"]),
        ("#FFF8E1", "#F9A825", ["5. 用户问题", "{ 用户输入的自然语言文本 }"]),
    ]

    cy = 52
    for i, (fill, out, lines) in enumerate(parts):
        draw_box(draw, margin, cy, margin + bw, cy + bh, lines, fill=fill, outline=out)
        if i < len(parts) - 1:
            draw_arrow(draw, W // 2, cy + bh, W // 2, cy + bh + gap)
        cy += bh + gap

    img.save(f"{OUT}/prompt_structure.png", dpi=(150, 150))
    print("prompt_structure.png saved")


# ══════════════════════════════════════
# 图6：用例图
# ══════════════════════════════════════
def gen_usecase():
    W, H = 1000, 540
    img = Image.new("RGB", (W, H), "#FAFAFA")
    draw = ImageDraw.Draw(img)

    tw = text_w("系统用例图", FONT_TITLE)
    draw.text(((W - tw) // 2, 12), "系统用例图", fill="#333", font=FONT_TITLE)

    # ── 系统边界 ──
    box_x1, box_y1 = 170, 50
    box_x2, box_y2 = 730, 440
    draw.rounded_rectangle([box_x1, box_y1, box_x2, box_y2], radius=10,
                           fill="#F5F5F5", outline="#999", width=2)
    label = "医疗自然语言查询系统"
    lw = text_w(label, FONT_BOLD)
    draw.text((box_x1 + 14, box_y1 + 8), label, fill="#555", font=FONT_BOLD)

    # ── 参与者（火柴人） ──
    def draw_actor(draw, cx, top_y, label_text):
        r = 8
        draw.ellipse([cx - r, top_y, cx + r, top_y + 2 * r], outline="#444", width=2)
        body_top = top_y + 2 * r
        body_bot = body_top + 22
        draw.line([cx, body_top, cx, body_bot], fill="#444", width=2)
        draw.line([cx, body_top + 6, cx - 12, body_top + 16], fill="#444", width=2)
        draw.line([cx, body_top + 6, cx + 12, body_top + 16], fill="#444", width=2)
        draw.line([cx, body_bot, cx - 10, body_bot + 18], fill="#444", width=2)
        draw.line([cx, body_bot, cx + 10, body_bot + 18], fill="#444", width=2)
        lw_l = text_w(label_text, FONT_SM)
        draw.text((cx - lw_l // 2, body_bot + 22), label_text, fill="#333", font=FONT_SM)

    actors = [
        (80, 110, "临床医生"),
        (80, 280, "护理人员"),
        (80, 420, "医院管理人员"),
    ]
    for cx, ay, aname in actors:
        draw_actor(draw, cx, ay, aname)

    # ── 用例椭圆 ──
    def draw_usecase(draw, cx, cy, text, fill="#E3F2FD", outline="#1565C0", font=None):
        if font is None:
            font = FONT
        tw_uc = text_w(text, font)
        ew, eh = max(tw_uc + 40, 130), 42
        draw.ellipse([cx - ew // 2, cy - eh // 2, cx + ew // 2, cy + eh // 2],
                      fill=fill, outline=outline, width=2)
        draw.text((cx - tw_uc // 2, cy - 8), text, fill="#222", font=font)

    # 主用例
    main_cx, main_cy = 460, 100
    draw_usecase(draw, main_cx, main_cy, "自然语言查询", fill="#BBDEFB", outline="#1565C0", font=FONT_BOLD)

    # 子用例（被 include 的，在系统边界内偏右）
    uc_sql_x, uc_sql_y = 630, 210
    uc_tbl_x, uc_tbl_y = 630, 280
    uc_hist_x, uc_hist_y = 630, 350

    draw_usecase(draw, uc_sql_x, uc_sql_y, "查看生成SQL")
    draw_usecase(draw, uc_tbl_x, uc_tbl_y, "浏览数据库结构")
    draw_usecase(draw, uc_hist_x, uc_hist_y, "查看查询历史")

    # 安全校验（系统内部，主用例下方）
    draw_usecase(draw, main_cx, 200, "SQL安全校验", fill="#FFECB3", outline="#F57C00")

    # ── 外部系统（系统边界右侧，框内） ──
    ext_w, ext_h = 170, 50
    ext1_x, ext1_y = 790, 100
    ext2_x, ext2_y = 790, 280

    for ex, ey, elabel, efill, eout in [
        (ext1_x, ext1_y, "通义千问 LLM\n(Qwen-Plus)", "#F3E5F5", "#7B1FA2"),
        (ext2_x, ext2_y, "MySQL 数据库", "#E8F5E9", "#2E7D32"),
    ]:
        draw.rounded_rectangle([ex, ey, ex + ext_w, ey + ext_h], radius=8,
                               fill=efill, outline=eout, width=2)
        lines_el = elabel.split("\n")
        lh_ext = 20
        total_h_ext = len(lines_el) * lh_ext
        cy_ext = ey + (ext_h - total_h_ext) // 2 + 2
        for line in lines_el:
            tw_line = text_w(line, FONT_SM)
            draw.text((ex + (ext_w - tw_line) // 2, cy_ext), line, fill="#333", font=FONT_SM)
            cy_ext += lh_ext

    # ── 连线 ──
    # 三种角色 → 自然语言查询
    for cx, ay, _ in actors:
        draw.line([cx + 30, ay + 50, main_cx - 120, main_cy], fill="#555", width=1)

    # 自然语言查询 → 子用例 (include 虚线)
    def draw_include(draw, x1, y1, x2, y2):
        dash_len = 6
        gap_len = 4
        total = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        if total == 0:
            return
        dx = (x2 - x1) / total * dash_len
        dy = (y2 - y1) / total * dash_len
        steps = int(total / (dash_len + gap_len))
        for i in range(steps):
            sx = x1 + i * (dash_len + gap_len) * (x2 - x1) / total
            sy = y1 + i * (dash_len + gap_len) * (y2 - y1) / total
            ex_line = sx + dx
            ey_line = sy + dy
            draw.line([sx, sy, ex_line, ey_line], fill="#1565C0", width=1)

    draw_include(draw, main_cx + 60, main_cy + 15, uc_sql_x - 65, uc_sql_y)
    draw_include(draw, main_cx + 60, main_cy + 15, uc_tbl_x - 65, uc_tbl_y)
    draw_include(draw, main_cx + 60, main_cy + 15, uc_hist_x - 65, uc_hist_y)

    # include 标签
    draw_label(draw, main_cx + 90, main_cy + 55, "<<include>>", color="#1565C0")

    # 自然语言查询 → 安全校验
    draw_arrow(draw, main_cx, main_cy + 21, main_cx, 200 - 21, color="#F57C00", lw=1)
    draw_label(draw, main_cx + 8, 155, "<<include>>", color="#F57C00")

    # 自然语言查询 → 外部系统
    draw_arrow(draw, main_cx + 100, main_cy, ext1_x, ext1_y + ext_h // 2, color="#7B1FA2", lw=1)
    draw_arrow(draw, main_cx + 100, main_cy + 20, ext2_x, ext2_y + ext_h // 2, color="#2E7D32", lw=1)

    # 连线标签
    draw_label(draw, 650, main_cy - 10, "调用API", color="#7B1FA2")
    draw_label(draw, 650, main_cy + 35, "读写数据", color="#2E7D32")

    img.save(f"{OUT}/usecase.png", dpi=(150, 150))
    print("usecase.png saved")


# ══════════════════════════════════════
# 图7：核心用例时序图
# ══════════════════════════════════════
def gen_query_sequence():
    W, H = 1060, 680
    img = Image.new("RGB", (W, H), "#FAFAFA")
    draw = ImageDraw.Draw(img)

    tw = text_w("核心用例：自然语言查询时序图", FONT_TITLE)
    draw.text(((W - tw) // 2, 12), "核心用例：自然语言查询时序图", fill="#333", font=FONT_TITLE)

    # 参与者
    participants = [
        ("用户", 70),
        ("前端\n(Vue 3)", 220),
        ("后端\n(FastAPI)", 400),
        ("通义千问\n(Qwen-Plus)", 610),
        ("MySQL\n数据库", 830),
    ]
    head_w, head_h = 76, 36

    for name, cx in participants:
        x = cx - head_w // 2
        y = 55
        draw.rounded_rectangle([x, y, x + head_w, y + head_h], radius=6,
                               fill="#E3F2FD", outline="#1565C0", width=2)
        # 多行参与者名
        name_lines = name.split("\n")
        lh_n = 16
        total_nh = len(name_lines) * lh_n
        ny = y + (head_h - total_nh) // 2
        for nl in name_lines:
            nlw = text_w(nl, FONT_SM)
            draw.text((cx - nlw // 2, ny), nl, fill="#222", font=FONT_SM)
            ny += lh_n

        # 生命线（虚线）
        ly = y + head_h
        for dy in range(ly, H - 40, 10):
            draw.line([cx, dy, cx, dy + 5], fill="#AAA", width=1)

    # ── 箭头辅助 ──
    def seq_arrow(x1, x2, y, label, color="#1565C0", dashed=False):
        """水平箭头 + 标签"""
        lw = 1
        if dashed:
            # 虚线箭头
            dx_total = x2 - x1
            seg = 8
            n_seg = abs(dx_total) // seg
            for i in range(n_seg):
                sx = x1 + i * seg * (1 if dx_total > 0 else -1)
                draw.line([sx, y, sx + seg // 2 * (1 if dx_total > 0 else -1), y], fill=color, width=lw)
                i += 1
            # 箭头
            if dx_total > 0:
                draw.polygon([(x2, y), (x2 - 8, y - 4), (x2 - 8, y + 4)], fill=color)
            else:
                draw.polygon([(x2, y), (x2 + 8, y - 4), (x2 + 8, y + 4)], fill=color)
        else:
            draw.line([x1, y, x2, y], fill=color, width=lw)
            if x2 > x1:
                draw.polygon([(x2, y), (x2 - 8, y - 4), (x2 - 8, y + 4)], fill=color)
            else:
                draw.polygon([(x2, y), (x2 + 8, y - 4), (x2 + 8, y + 4)], fill=color)

        tw_l = text_w(label, FONT_SM)
        mid_x = (x1 + x2) // 2
        draw.text((mid_x - tw_l // 2, y - 18), label, fill="#333", font=FONT_SM)

    def seq_return(x1, x2, y, label, color="#888"):
        """返回箭头（虚线+开箭头）"""
        # 只用虚线表示返回
        dx = x2 - x1
        seg = 6
        n = abs(dx) // seg
        for i in range(n):
            sx = x1 + i * seg * (1 if dx > 0 else -1)
            draw.line([sx, y, sx + seg // 2 * (1 if dx > 0 else -1), y], fill=color, width=1)
        if dx > 0:
            draw.line([x2 - 10, y - 4, x2, y], fill=color, width=1)
            draw.line([x2 - 10, y + 4, x2, y], fill=color, width=1)
        else:
            draw.line([x2 + 10, y - 4, x2, y], fill=color, width=1)
            draw.line([x2 + 10, y + 4, x2, y], fill=color, width=1)

        tw_l = text_w(label, FONT_SM)
        mid_x = (x1 + x2) // 2
        draw.text((mid_x - tw_l // 2, y + 4), label, fill=color, font=FONT_SM)

    # ── 正常流程 ──
    p_x = [px for _, px in participants]  # 各参与者x坐标
    y = 110
    gap = 38

    # 1. 用户输入
    draw_label(draw, p_x[0] + 10, y, "1. 输入中文查询问题", color="#333")
    y += gap

    # 2. 前端→后端 POST
    seq_arrow(p_x[1], p_x[2], y, "2. POST /api/v1/query/ {text}")
    y += gap

    # 3. 后端→MySQL Schema
    seq_arrow(p_x[2], p_x[4], y, "3. SHOW TABLES / SHOW COLUMNS")
    y += gap

    # 4. MySQL→后端 返回
    seq_return(p_x[4], p_x[2], y, "4. 返回表结构元数据")
    y += gap

    # 5. 后端→LLM
    seq_arrow(p_x[2], p_x[3], y, "5. 发送拼接完成的 Prompt")
    y += gap

    # 6. LLM→后端 返回
    seq_return(p_x[3], p_x[2], y, "6. 返回生成的 SQL 文本")
    y += gap

    # 7. 自调用：SQL安全校验
    draw_label(draw, p_x[2] - 80, y - 12, "7. SQL安全校验", color="#F57C00")
    # 自调用环
    bx = p_x[2]
    draw.rounded_rectangle([bx + 10, y - 8, bx + 80, y + 16], radius=4,
                           fill="#FFF8E1", outline="#F57C00", width=1)
    tw_chk = text_w("check_sql_safe()", FONT_SM)
    draw.text((bx + 45 - tw_chk // 2, y - 5), "check_sql_safe()", fill="#F57C00", font=FONT_SM)
    y += gap

    # 8. 后端→MySQL 执行SQL
    seq_arrow(p_x[2], p_x[4], y, "8. 执行通过校验的 SQL", color="#2E7D32")
    y += gap

    # 9. MySQL→后端 返回
    seq_return(p_x[4], p_x[2], y, "9. 返回查询结果集")
    y += gap

    # 10. 后端→前端 响应
    seq_arrow(p_x[2], p_x[1], y, "10. 返回 {success, sql, data}")
    y += gap

    # 11. 前端更新
    draw_label(draw, p_x[1] + 10, y - 12, "11. 更新 SQL卡片 + 结果表格", color="#333")
    y += gap

    # 12. 前端→localStorage
    draw_label(draw, p_x[1] + 10, y - 12, "12. 写入浏览器 localStorage", color="#666")

    # ── 异常分支（侧边标注） ──
    alt_x = 890
    alt_y = 310
    draw.rounded_rectangle([alt_x, alt_y, W - 25, alt_y + 130], radius=8,
                           fill="#FFEBEE", outline="#C62828", width=1)
    draw.text((alt_x + 12, alt_y + 8), "异常分支", fill="#C62828", font=FONT_BOLD)

    alt_items = [
        "安全校验失败 → 返回提示",
        "SQL执行错误 → 透传错误",
        "网络超时 → 统一错误",
    ]
    ay = alt_y + 34
    for item in alt_items:
        draw.text((alt_x + 14, ay), item, fill="#555", font=FONT_SM)
        ay += 26

    # 异常分支连线到安全校验步骤
    draw.line([p_x[2] + 84, 312, alt_x, 340], fill="#C62828", width=1)
    draw.line([p_x[2] + 84, 312, alt_x, 380], fill="#C62828", width=1)

    img.save(f"{OUT}/query_sequence.png", dpi=(150, 150))
    print("query_sequence.png saved")


if __name__ == "__main__":
    gen_architecture()
    gen_backend_modules()
    gen_dataflow()
    gen_er()
    gen_prompt_structure()
    gen_usecase()
    gen_query_sequence()
    print("All diagrams generated in", OUT)

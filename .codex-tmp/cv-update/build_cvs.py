from copy import deepcopy
from pathlib import Path
import shutil

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt


ROOT = Path(__file__).resolve().parents[2]
REFERENCE = Path("/Users/linxiao/.codex/skills/artifact-template-linxiao-wu-cv/assets/reference.docx")
OUT = ROOT / "deliverables"


def clear_body(doc):
    body = doc._element.body
    sect = body.sectPr
    for child in list(body):
        if child is not sect:
            body.remove(child)


def set_cellless_border(paragraph):
    p_pr = paragraph._p.get_or_add_pPr()
    p_bdr = p_pr.find(qn("w:pBdr"))
    if p_bdr is None:
        p_bdr = OxmlElement("w:pBdr")
        p_pr.append(p_bdr)
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "000000")
    p_bdr.append(bottom)


def set_font(run, *, size=8.7, bold=False, italic=False, lang="en"):
    latin = "Times New Roman"
    cjk = "Noto Serif CJK SC"
    family = cjk if lang == "zh" else latin
    run.bold = bold
    run.italic = italic
    run.font.name = family
    run.font.size = Pt(size)
    rpr = run._element.get_or_add_rPr()
    fonts = rpr.rFonts
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        rpr.insert(0, fonts)
    fonts.set(qn("w:ascii"), family)
    fonts.set(qn("w:hAnsi"), family)
    fonts.set(qn("w:eastAsia"), family)
    fonts.set(qn("w:cs"), family)
    lang_el = rpr.find(qn("w:lang"))
    if lang_el is None:
        lang_el = OxmlElement("w:lang")
        rpr.append(lang_el)
    lang_el.set(qn("w:val"), "zh-CN" if lang == "zh" else "en-US")
    lang_el.set(qn("w:eastAsia"), "zh-CN" if lang == "zh" else "en-US")
    color = rpr.find(qn("w:color"))
    if color is None:
        color = OxmlElement("w:color")
        rpr.append(color)
    color.set(qn("w:val"), "000000")


def add_paragraph(doc, text="", *, size=8.7, bold=False, italic=False, align=None,
                  before=0, after=0, line=9.6, lang="en", keep=False):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = Pt(line)
    pf.keep_with_next = keep
    r = p.add_run(text)
    set_font(r, size=size, bold=bold, italic=italic, lang=lang)
    return p


def add_rich_paragraph(doc, parts, *, size=8.7, align=None, before=0, after=0,
                       line=9.6, lang="en", keep=False):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = Pt(line)
    pf.keep_with_next = keep
    for text, bold, italic in parts:
        r = p.add_run(text)
        set_font(r, size=size, bold=bold, italic=italic, lang=lang)
    return p


def add_section(doc, text, lang):
    p = add_paragraph(doc, text, size=9.5, bold=True, before=2.2, after=0.8,
                      line=10.4, lang=lang, keep=True)
    set_cellless_border(p)
    return p


def add_heading(doc, left, right, lang, *, size=9.1, before=0.8):
    p = add_paragraph(doc, "", before=before, line=9.8, lang=lang, keep=True)
    p.paragraph_format.tab_stops.add_tab_stop(Inches(7.45), WD_TAB_ALIGNMENT.RIGHT)
    r = p.add_run(left)
    set_font(r, size=size, bold=True, lang=lang)
    r = p.add_run("\t" + right)
    set_font(r, size=size, lang=lang)
    return p


def add_subheading(doc, left, right, lang):
    p = add_paragraph(doc, "", line=9.5, lang=lang, keep=True)
    p.paragraph_format.tab_stops.add_tab_stop(Inches(7.45), WD_TAB_ALIGNMENT.RIGHT)
    r = p.add_run(left)
    set_font(r, size=8.5, bold=True, lang=lang)
    r = p.add_run("\t" + right)
    set_font(r, size=8.5, lang=lang)
    return p


def add_bullet(doc, text, lang, *, size=8.35):
    p = add_paragraph(doc, "", size=size, line=9.15, lang=lang)
    pf = p.paragraph_format
    pf.left_indent = Inches(0.18)
    pf.first_line_indent = Inches(-0.14)
    r = p.add_run("•\t" + text)
    set_font(r, size=size, lang=lang)
    return p


def add_skill(doc, label, value, lang):
    return add_rich_paragraph(
        doc,
        [(label, True, False), (value, False, False)],
        size=8.35,
        line=9.15,
        lang=lang,
    )


def build(lang, filename):
    path = OUT / filename
    shutil.copy2(REFERENCE, path)
    doc = Document(path)
    clear_body(doc)
    section = doc.sections[0]
    section.top_margin = Inches(0.43)
    section.bottom_margin = Inches(0.43)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)

    if lang == "en":
        add_paragraph(doc, "Linxiao Wu", size=22, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER,
                      after=0.5, line=23, lang=lang)
        add_paragraph(doc, "+1 917-329-6388  |  lw3227@columbia.edu  |  www.linxiaowu.com  |  github.com/lw3227",
                      size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, after=1.2, line=9.5, lang=lang)

        add_section(doc, "EDUCATION", lang)
        add_heading(doc, "Columbia University", "New York, NY", lang)
        add_subheading(doc, "M.S. in Electrical Engineering | GPA: 4.0/4.0", "Expected Dec 2026", lang)
        add_heading(doc, "Sun Yat-sen University", "Guangzhou, China", lang, before=0.4)
        add_subheading(doc, "B.Eng. in Microelectronics Science and Engineering | GPA: 3.7/4.0", "Jun 2025", lang)
        add_rich_paragraph(doc, [("Honors: ", True, False), ("Sun Yat-sen University Scholarship; Outstanding Undergraduate Thesis Award", False, False)], size=8.4, line=9.2, lang=lang)

        add_section(doc, "EXPERIENCE", lang)
        add_heading(doc, "WingSemi Technology", "Shanghai Zhangjiang, China", lang)
        add_subheading(doc, "CPU IP Design Intern", "Jun 2026 - Sep 2026", lang)
        for t in [
            "Contributed to an RVA23-compliant RISC-V CPU IP, focusing on VFPU design and integration within the VPU.",
            "Owned the VFCVT module, implementing conversions among FP64, FP32, FP16, BF16, and integer formats for RVV instructions.",
            "Designed a three-stage pipeline with shared multi-precision datapaths, lane-level parallelism, configurable DLEN, and PPA-driven hardware reuse.",
            "Supported VFPU/VCTRL integration, vector micro-op control, mask/lane management, valid/stall/flush handling, and pipeline forwarding.",
            "Performed RTL synthesis and timing analysis in Synopsys Design Compiler and optimized critical datapaths.",
        ]: add_bullet(doc, t, lang)
        add_heading(doc, "Guangzhou CanSemi Technology Inc.", "Guangzhou, China", lang, before=0.5)
        add_subheading(doc, "TCAD / Device Engineering Intern", "Jul 2024 - Sep 2024", lang)
        for t in [
            "Built and calibrated a reusable 32 V PMOS TCAD model against foundry process data; analyzed wafer electrical and WAT data.",
            "Simulated IGBT device structures and supported patent-related device development.",
        ]: add_bullet(doc, t, lang)

        add_section(doc, "PROJECTS", lang)
        add_heading(doc, "Apple-Sponsored Gesture-Recognition CNN Accelerator ASIC", "Feb 2026 - Present", lang)
        for t in [
            "Designed a fully hardware INT8 CNN for 64 x 64 grayscale gesture recognition; taped out in TSMC 65 nm in July 2026.",
            "Built a 64-PE INT8 systolic array with approximately 464K MACs per inference and 8 KB on-chip SRAM.",
            "Completed RTL, DFT scan-chain design, Genus synthesis, Innovus place and route, and post-layout verification; evaluated quantization in Python and MATLAB.",
        ]: add_bullet(doc, t, lang)
        add_heading(doc, "P6-Based Out-of-Order RISC-V Processor", "Mar 2026 - Jun 2026", lang, before=0.5)
        for t in [
            "Designed two-wide fetch/dispatch/retirement with single-issue out-of-order execution and in-order commit.",
            "Implemented a 16-entry ROB, 8-entry reservation station, map table, and CDB for ROB-tag-based register renaming and issue.",
            "Developed a 5-bit-GHR, 32-entry BHT/BTB gshare predictor with speculative updates and ROB-snapshot recovery.",
            "Implemented split LQ/SQ and a two-way non-blocking D-cache with store-to-load forwarding, four-entry MSHR capacity, and a four-entry victim cache.",
        ]: add_bullet(doc, t, lang)
        add_heading(doc, "N-Body Accelerator Formal Verification", "Oct 2025 - Dec 2025", lang, before=0.5)
        for t in [
            "Authored SystemVerilog assertions, assumptions, and cover properties in Cadence JasperGold for FSM, shift-register, and pointer checks.",
            "Found an illegal FSM transition missed by simulation and a one-cycle pointer-range violation.",
        ]: add_bullet(doc, t, lang)
        add_heading(doc, "64-Tap 16-Bit FIR Digital Filter", "Oct 2025 - Dec 2025", lang, before=0.5)
        for t in [
            "Designed a fixed-point FIR core with a multiply-accumulate datapath, CMEM/IMEM, and control FSM.",
            "Used an asynchronous FIFO for CDC between the 10 kHz input domain and the high-speed FIR core.",
        ]: add_bullet(doc, t, lang)

        add_section(doc, "TECHNICAL SKILLS", lang)
        add_skill(doc, "EDA Tools: ", "Synopsys Design Compiler, PrimeTime; Cadence Genus, Innovus, Xcelium; JasperGold, ModelSim, Verdi", lang)
        add_skill(doc, "Programming: ", "Verilog, SystemVerilog, Python (NumPy, PyTorch), C, MATLAB", lang)
        add_skill(doc, "Focus Areas: ", "ASIC design, RISC-V CPU/VPU architecture, CNN hardware accelerators", lang)
    else:
        add_paragraph(doc, "吴林晓", size=22, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER,
                      after=0.5, line=23, lang=lang)
        add_paragraph(doc, "+1 917-329-6388  |  lw3227@columbia.edu  |  www.linxiaowu.com  |  github.com/lw3227",
                      size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, after=1.2, line=9.5, lang=lang)

        add_section(doc, "教育背景", lang)
        add_heading(doc, "哥伦比亚大学", "纽约，美国", lang)
        add_subheading(doc, "电气工程硕士 | GPA：4.0/4.0", "预计 2026 年 12 月毕业", lang)
        add_heading(doc, "中山大学", "广州，中国", lang, before=0.4)
        add_subheading(doc, "微电子科学与工程学士 | GPA：3.7/4.0", "2025 年 6 月毕业", lang)
        add_rich_paragraph(doc, [("荣誉：", True, False), ("中山大学奖学金；本科优秀毕业论文奖", False, False)], size=8.4, line=9.2, lang=lang)

        add_section(doc, "实习经历", lang)
        add_heading(doc, "隼瞻科技", "上海张江，中国", lang)
        add_subheading(doc, "CPU IP 设计实习生", "2026 年 6 月 - 2026 年 9 月", lang)
        for t in [
            "参与符合 RVA23 Profile 的 RISC-V CPU IP 开发，负责 VPU 中 VFPU 的设计与集成。",
            "负责 VFCVT 向量浮点转换模块，支持 FP64、FP32、FP16、BF16 与整数格式转换。",
            "设计三级流水线、多精度数据通路融合、Lane 级并行处理与可配置 DLEN，并围绕 PPA 复用硬件资源。",
            "参与 VFPU 与 VCTRL 控制逻辑、vector uop 分发、mask/lane 管理及 valid/stall/flush 和 forwarding 机制。",
            "使用 Synopsys Design Compiler 完成 RTL 综合及时序分析，并针对关键路径优化数据通路。",
        ]: add_bullet(doc, t, lang)
        add_heading(doc, "粤芯半导体", "广州，中国", lang, before=0.5)
        add_subheading(doc, "TCAD / 器件工程实习生", "2024 年 7 月 - 2024 年 9 月", lang)
        for t in [
            "基于代工厂工艺数据建立并校准可复用的 32V PMOS TCAD 模型，参与晶圆电特性与 WAT 数据分析。",
            "模拟 IGBT 器件结构，为专利相关器件研究提供支持。",
        ]: add_bullet(doc, t, lang)

        add_section(doc, "项目经历", lang)
        add_heading(doc, "Apple 赞助手势识别 CNN 加速器 ASIC", "2026 年 2 月 - 至今", lang)
        for t in [
            "设计面向 64×64 灰度手势识别的纯硬件 INT8 CNN，并于 2026 年 7 月在 TSMC 65 nm 工艺完成投片。",
            "实现 64 个 PE 的 INT8 脉动阵列，单次推理约 464K 次 MAC 运算，并集成 8 KB 片上 SRAM。",
            "完成 RTL、DFT scan chain、Genus 综合、Innovus 布局布线及版图后验证，并使用 Python/MATLAB 进行量化评估。",
        ]: add_bullet(doc, t, lang)
        add_heading(doc, "基于 P6 微架构的乱序执行 RISC-V 处理器", "2026 年 3 月 - 2026 年 6 月", lang, before=0.5)
        for t in [
            "支持 2-wide Fetch、Dispatch 与 Retire、单发射乱序执行及顺序提交。",
            "实现 16-entry ROB、8-entry Reservation Station、Map Table 与 CDB，支持基于 ROB Tag 的寄存器重命名和乱序发射。",
            "实现 5-bit GHR 与 32-entry BHT/BTB 的 gshare 分支预测器，支持投机更新和 ROB snapshot 恢复。",
            "实现独立 LQ/SQ 与 2-way non-blocking D-cache，支持 Store-to-Load Forwarding、4-entry MSHR 与 4-entry Victim Cache。",
        ]: add_bullet(doc, t, lang)
        add_heading(doc, "N-Body 硬件加速器形式验证", "2025 年 10 月 - 2025 年 12 月", lang, before=0.5)
        for t in [
            "使用 Cadence JasperGold 编写 SVA assertion、assumption 与 cover property，验证 FSM、移位寄存器及指针边界。",
            "发现仿真测试未覆盖的非法 FSM 跳转及持续一个周期的指针越界问题。",
        ]: add_bullet(doc, t, lang)
        add_heading(doc, "64-tap 16-bit FIR 数字滤波器", "2025 年 10 月 - 2025 年 12 月", lang, before=0.5)
        for t in [
            "设计定点 FIR 核心，实现乘加数据通路、CMEM/IMEM 及控制 FSM。",
            "使用异步 FIFO 解决 10 kHz 输入时钟域与高速 FIR 内核之间的跨时钟域通信问题。",
        ]: add_bullet(doc, t, lang)

        add_section(doc, "技能", lang)
        add_skill(doc, "EDA：", "Synopsys Design Compiler、PrimeTime；Cadence Genus、Innovus、Xcelium；JasperGold、ModelSim、Verdi", lang)
        add_skill(doc, "编程：", "Verilog、SystemVerilog、Python（NumPy、PyTorch）、C、MATLAB", lang)
        add_skill(doc, "方向：", "ASIC 设计、RISC-V CPU/VPU 架构、CNN 硬件加速器", lang)

    doc.core_properties.title = "Linxiao Wu CV" if lang == "en" else "吴林晓简历"
    doc.core_properties.author = "Linxiao Wu"
    doc.save(path)
    return path


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for p in [build("en", "Linxiao_Wu_CV.docx"), build("zh", "吴林晓_简历.docx")]:
        print(p)

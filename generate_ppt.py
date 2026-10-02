"""
Generate a professional project defense presentation.
Run: python generate_ppt.py
Output: presentation/MetaEvalAI_Presentation.pptx
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
import os

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ── Color Palette ──
BG = RGBColor(0x0F, 0x0F, 0x1A)
CARD = RGBColor(0x1A, 0x1A, 0x2E)
ACCENT = RGBColor(0x00, 0xD4, 0xAA)
ACCENT2 = RGBColor(0x6B, 0xCB, 0xFF)
ACCENT3 = RGBColor(0xFF, 0x6B, 0x6B)
ACCENT4 = RGBColor(0xFF, 0xD9, 0x3D)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT = RGBColor(0xBB, 0xBB, 0xCC)
DIM = RGBColor(0x88, 0x88, 0x99)

def set_bg(slide, color=BG):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_shape(slide, left, top, width, height, color=CARD, radius=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape

def add_text(slide, left, top, width, height, text, size=18, color=WHITE, bold=False, align=PP_ALIGN.LEFT, font_name="Calibri"):
    txbox = slide.shapes.add_textbox(left, top, width, height)
    tf = txbox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = align
    return tf

def add_bullet_frame(slide, left, top, width, height, items, size=16, color=LIGHT, bullet_color=ACCENT):
    txbox = slide.shapes.add_textbox(left, top, width, height)
    tf = txbox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.space_after = Pt(8)
        # bullet symbol
        run1 = p.add_run()
        run1.text = "▸ "
        run1.font.size = Pt(size)
        run1.font.color.rgb = bullet_color
        run1.font.bold = True
        run1.font.name = "Calibri"
        # text
        run2 = p.add_run()
        run2.text = item
        run2.font.size = Pt(size)
        run2.font.color.rgb = color
        run2.font.name = "Calibri"
    return tf

def add_metric_card(slide, left, top, width, height, label, value, accent=ACCENT):
    add_shape(slide, left, top, width, height, CARD)
    add_text(slide, left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.4),
             value, size=28, color=accent, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, left + Inches(0.2), top + Inches(0.65), width - Inches(0.4), Inches(0.35),
             label, size=12, color=DIM, align=PP_ALIGN.CENTER)

def slide_header(slide, title, subtitle=None):
    # accent line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.5), Inches(0.08), Inches(0.6))
    line.fill.solid()
    line.fill.fore_color.rgb = ACCENT
    line.line.fill.background()
    add_text(slide, Inches(1.1), Inches(0.45), Inches(10), Inches(0.7), title, size=32, color=WHITE, bold=True)
    if subtitle:
        add_text(slide, Inches(1.1), Inches(1.05), Inches(10), Inches(0.4), subtitle, size=16, color=DIM)

# ============================================================
# SLIDE 1 — Title Slide
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])  # blank
set_bg(s)

# Decorative accent bar at top
bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, Inches(0.06))
bar.fill.solid()
bar.fill.fore_color.rgb = ACCENT
bar.line.fill.background()

add_text(s, Inches(1), Inches(1.5), Inches(11), Inches(1.2),
         "Meta-Evaluation Framework for\nAI Model Outputs", size=42, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

add_text(s, Inches(1), Inches(3.0), Inches(11), Inches(0.6),
         "Using Transformer-Based Multi-Dimensional Analysis", size=22, color=ACCENT, align=PP_ALIGN.CENTER)

add_text(s, Inches(1), Inches(4.0), Inches(11), Inches(0.5),
         "21CSP302L — Final Year Project", size=16, color=DIM, align=PP_ALIGN.CENTER)

add_text(s, Inches(1), Inches(5.0), Inches(11), Inches(0.4),
         "STUDENT 1 NAME  •  STUDENT 2 NAME", size=18, color=LIGHT, align=PP_ALIGN.CENTER)

add_text(s, Inches(1), Inches(5.5), Inches(11), Inches(0.4),
         "Guide: Dr. GUIDE NAME  |  Department of Computational Intelligence", size=14, color=DIM, align=PP_ALIGN.CENTER)

add_text(s, Inches(1), Inches(6.3), Inches(11), Inches(0.4),
         "SRM Institute of Science and Technology  •  May 2026", size=13, color=DIM, align=PP_ALIGN.CENTER)

# ============================================================
# SLIDE 2 — Problem & Motivation
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)
slide_header(s, "The Problem", "Why do we need a Meta-Evaluation Framework?")

add_bullet_frame(s, Inches(1), Inches(1.8), Inches(5.5), Inches(4.5), [
    "LLMs produce fluent text — but which model is actually better?",
    "Human evaluation is expensive, slow, and hard to reproduce",
    "BLEU/ROUGE measure word overlap, not meaning or safety",
    "BERTScore is single-dimensional — misses bias, consistency, hallucination",
    "RAG pipelines introduce new failure modes: hallucinated facts, context echoing",
    "No existing open-source tool evaluates all dimensions for free",
], size=17)

# Right side — key stats
add_shape(s, Inches(7.2), Inches(1.8), Inches(5.3), Inches(4.5), CARD)
add_text(s, Inches(7.5), Inches(2.0), Inches(4.8), Inches(0.5),
         "Our Solution", size=22, color=ACCENT, bold=True, align=PP_ALIGN.CENTER)
add_bullet_frame(s, Inches(7.5), Inches(2.6), Inches(4.8), Inches(3.5), [
    "4 standard + 2 RAG dimensions",
    "Local transformer models — no API cost",
    "Data-driven weight learning (R²=0.89)",
    "Interactive Streamlit dashboard",
    "17 validation test cases (88% pass)",
], size=16, bullet_color=ACCENT2)

# ============================================================
# SLIDE 3 — System Architecture
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)
slide_header(s, "System Architecture", "Modular pipeline with 6 evaluation dimensions")

# Module cards
modules = [
    ("Relevance", "all-MiniLM-L6-v2\nSemantic similarity", ACCENT),
    ("Quality", "Rule-based\nLength, diversity, structure", ACCENT2),
    ("Bias", "toxic-bert\nToxicity detection", ACCENT3),
    ("Consistency", "DeBERTa-v3-small\nNLI contradiction check", ACCENT4),
    ("Faithfulness", "DeBERTa NLI\nClaim verification (RAG)", RGBColor(0xC0, 0x84, 0xFC)),
    ("Answer Relevance", "Dual-similarity\nEcho detection (RAG)", RGBColor(0xFF, 0x9F, 0x43)),
]

for i, (name, desc, clr) in enumerate(modules):
    col = i % 3
    row = i // 3
    left = Inches(0.8) + col * Inches(4.1)
    top = Inches(1.8) + row * Inches(2.4)
    add_shape(s, left, top, Inches(3.7), Inches(2.0), CARD)
    # Color indicator
    ind = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(0.07), Inches(2.0))
    ind.fill.solid()
    ind.fill.fore_color.rgb = clr
    ind.line.fill.background()
    add_text(s, left + Inches(0.3), top + Inches(0.2), Inches(3.2), Inches(0.5), name, size=20, color=clr, bold=True)
    add_text(s, left + Inches(0.3), top + Inches(0.75), Inches(3.2), Inches(1.0), desc, size=14, color=LIGHT)

# Aggregator arrow
add_text(s, Inches(4.5), Inches(6.3), Inches(4.5), Inches(0.5),
         "→  Score Aggregator  →  Final Ranking", size=16, color=ACCENT, bold=True, align=PP_ALIGN.CENTER)

# ============================================================
# SLIDE 4 — How Each Module Works
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)
slide_header(s, "How It Works", "Technical details of each evaluation dimension")

details = [
    ("Relevance (35%)", "Encodes prompt and response using sentence-transformers into 384-dim vectors. Cosine similarity measures semantic closeness. 'Cars on roads' ≈ 'Automobiles on highways' scores high."),
    ("Quality (25%)", "Rule-based: scores length adequacy (0.3–1.0), vocabulary diversity (unique/total words), and structural formatting (JSON, Markdown headers, bullet lists). No ML model needed."),
    ("Bias (25%)", "Passes response through toxic-bert toxicity classifier. Score is inverted: 1.0 = clean, 0.0 = toxic. Catches hate speech, profanity, and explicit discrimination."),
    ("Consistency (15%)", "Splits response into sentences. Every pair checked via DeBERTa NLI for contradiction. Also compares against other models' responses for cross-model consensus."),
]

for i, (title, desc) in enumerate(details):
    top = Inches(1.7) + i * Inches(1.35)
    add_shape(s, Inches(0.8), top, Inches(11.7), Inches(1.15), CARD)
    add_text(s, Inches(1.1), top + Inches(0.1), Inches(3.0), Inches(0.4), title, size=16, color=ACCENT, bold=True)
    add_text(s, Inches(4.2), top + Inches(0.1), Inches(7.8), Inches(0.95), desc, size=14, color=LIGHT)

# ============================================================
# SLIDE 5 — RAG Evaluation
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)
slide_header(s, "RAG Evaluation", "Faithfulness & Answer Relevance — detecting hallucinations and echoing")

# Faithfulness
add_shape(s, Inches(0.8), Inches(1.8), Inches(5.8), Inches(4.5), CARD)
add_text(s, Inches(1.1), Inches(1.95), Inches(5.3), Inches(0.5), "Faithfulness (35% in RAG mode)", size=20, color=RGBColor(0xC0, 0x84, 0xFC), bold=True)
add_bullet_frame(s, Inches(1.1), Inches(2.6), Inches(5.3), Inches(3.5), [
    "Splits response into individual claims",
    "Each claim verified against context via NLI",
    "Entailed → full credit, Neutral → half, Contradiction → zero",
    "Score = (entailed + 0.5×neutral) / total",
    "Example: 'Prescribed Ibuprofen' when context says 'Amoxicillin' → CONTRADICTION → score drops",
], size=15)

# Answer Relevance
add_shape(s, Inches(7.0), Inches(1.8), Inches(5.8), Inches(4.5), CARD)
add_text(s, Inches(7.3), Inches(1.95), Inches(5.3), Inches(0.5), "Answer Relevance (15% in RAG mode)", size=20, color=RGBColor(0xFF, 0x9F, 0x43), bold=True)
add_bullet_frame(s, Inches(7.3), Inches(2.6), Inches(5.3), Inches(3.5), [
    "Computes prompt–response similarity (on topic?)",
    "Computes context–response similarity (copying?)",
    "If context_sim >> prompt_sim → context echo detected",
    "Echo penalty applied: score = prompt_sim − α×(gap)",
    "Catches models that just parrot the source material",
], size=15)

# ============================================================
# SLIDE 6 — Learning-Assisted Weights
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)
slide_header(s, "Learning-Assisted Weights", "Ridge Regression trained on 51 human-rated samples")

# Metric cards
add_metric_card(s, Inches(0.8), Inches(1.8), Inches(2.8), Inches(1.1), "Cross-validated R²", "0.890", ACCENT)
add_metric_card(s, Inches(4.0), Inches(1.8), Inches(2.8), Inches(1.1), "Mean Absolute Error", "0.098", ACCENT2)
add_metric_card(s, Inches(7.2), Inches(1.8), Inches(2.8), Inches(1.1), "Full Dataset R²", "0.925", RGBColor(0xC0, 0x84, 0xFC))
add_metric_card(s, Inches(10.4), Inches(1.8), Inches(2.8), Inches(1.1), "Training Samples", "51", ACCENT4)

# Weight comparison table
add_shape(s, Inches(0.8), Inches(3.3), Inches(5.8), Inches(3.5), CARD)
add_text(s, Inches(1.1), Inches(3.5), Inches(5.3), Inches(0.4), "Weight Comparison", size=18, color=WHITE, bold=True)

weights = [
    ("Dimension", "Static", "Learned", "Change"),
    ("Relevance", "35.0%", "24.2%", "−10.8%"),
    ("Quality", "25.0%", "40.9%", "+15.9%"),
    ("Bias", "25.0%", "0.7%", "−24.3%"),
    ("Consistency", "15.0%", "34.2%", "+19.2%"),
]
for i, (d, s_w, l_w, ch) in enumerate(weights):
    top = Inches(4.05) + i * Inches(0.5)
    clr = ACCENT if i == 0 else LIGHT
    bld = i == 0
    add_text(s, Inches(1.3), top, Inches(1.8), Inches(0.4), d, size=14, color=clr, bold=bld)
    add_text(s, Inches(3.1), top, Inches(1.0), Inches(0.4), s_w, size=14, color=clr, bold=bld, align=PP_ALIGN.CENTER)
    add_text(s, Inches(4.2), top, Inches(1.0), Inches(0.4), l_w, size=14, color=clr, bold=bld, align=PP_ALIGN.CENTER)
    add_text(s, Inches(5.3), top, Inches(1.0), Inches(0.4), ch, size=14, color=clr, bold=bld, align=PP_ALIGN.CENTER)

# Key insight
add_shape(s, Inches(7.0), Inches(3.3), Inches(5.8), Inches(3.5), CARD)
add_text(s, Inches(7.3), Inches(3.5), Inches(5.3), Inches(0.4), "Key Insight", size=18, color=WHITE, bold=True)
add_bullet_frame(s, Inches(7.3), Inches(4.1), Inches(5.3), Inches(2.5), [
    "Quality matters most (40.9%) — humans value well-structured, detailed responses",
    "Consistency is critical (34.2%) — contradictions are a strong negative signal",
    "Bias had near-zero weight (0.7%) — all training samples were non-toxic, so bias had no discriminative power",
    "Minimal overfitting: train-test R² gap of only 0.010",
], size=14)

# ============================================================
# SLIDE 7 — Validation Results
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)
slide_header(s, "Validation Results", "17 controlled test cases across all 6 dimensions")

# KPI cards
add_metric_card(s, Inches(0.8), Inches(1.8), Inches(2.5), Inches(1.1), "Total Cases", "17", ACCENT)
add_metric_card(s, Inches(3.6), Inches(1.8), Inches(2.5), Inches(1.1), "Passed", "15", RGBColor(0x00, 0xE6, 0x76))
add_metric_card(s, Inches(6.4), Inches(1.8), Inches(2.5), Inches(1.1), "Failed", "2", ACCENT3)
add_metric_card(s, Inches(9.2), Inches(1.8), Inches(2.5), Inches(1.1), "Pass Rate", "88.2%", ACCENT4)

# Results highlights
add_shape(s, Inches(0.8), Inches(3.3), Inches(7.0), Inches(3.5), CARD)
add_text(s, Inches(1.1), Inches(3.45), Inches(6.5), Inches(0.4), "Passing Cases — Framework correctly identifies:", size=16, color=RGBColor(0x00, 0xE6, 0x76), bold=True)
add_bullet_frame(s, Inches(1.1), Inches(3.95), Inches(6.5), Inches(2.7), [
    "Faithful vs hallucinated responses (faithfulness)",
    "On-topic vs off-topic answers (relevance, answer relevance)",
    "Clean vs toxic/biased text (bias)",
    "Well-structured vs gibberish responses (quality)",
    "Consistent vs self-contradictory text (consistency)",
    "Verbatim context mirroring (answer relevance echo detection)",
], size=14)

# Known limitations
add_shape(s, Inches(8.2), Inches(3.3), Inches(4.6), Inches(3.5), CARD)
add_text(s, Inches(8.5), Inches(3.45), Inches(4.0), Inches(0.4), "Known Limitations (2 failures):", size=16, color=ACCENT3, bold=True)
add_bullet_frame(s, Inches(8.5), Inches(3.95), Inches(4.0), Inches(2.7), [
    "Case 16: Polite gender stereotypes not caught by toxic-bert (trained on overt hate speech only)",
    "Case 17: Plausible extra details classified as 'neutral' not 'hallucinated' by NLI model",
], size=13, bullet_color=ACCENT3)

# ============================================================
# SLIDE 8 — Benchmark Results
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)
slide_header(s, "Benchmark Results", "10 prompts × 3 models across 6 subject categories")

# Model ranking cards
models_data = [
    ("🥇 GPT-4", "0.85", "Consistently ranked #1 on all 10 prompts", ACCENT),
    ("🥈 Mistral-7B", "0.72", "Better structure but hurt by self-contradictions", ACCENT2),
    ("🥉 Llama-3", "0.56", "Repetitive, low-quality outputs scored lowest", ACCENT3),
]

for i, (model, score, desc, clr) in enumerate(models_data):
    left = Inches(0.8) + i * Inches(4.1)
    add_shape(s, left, Inches(1.8), Inches(3.7), Inches(2.2), CARD)
    add_text(s, left + Inches(0.3), Inches(1.95), Inches(3.1), Inches(0.5), model, size=20, color=clr, bold=True)
    add_text(s, left + Inches(0.3), Inches(2.5), Inches(3.1), Inches(0.5), f"Final Score: {score}", size=28, color=WHITE, bold=True)
    add_text(s, left + Inches(0.3), Inches(3.2), Inches(3.1), Inches(0.6), desc, size=13, color=LIGHT)

# Key findings
add_shape(s, Inches(0.8), Inches(4.4), Inches(11.7), Inches(2.5), CARD)
add_text(s, Inches(1.1), Inches(4.55), Inches(11.0), Inches(0.4), "Key Findings from Benchmark", size=18, color=ACCENT, bold=True)
add_bullet_frame(s, Inches(1.1), Inches(5.05), Inches(5.5), Inches(1.7), [
    "Consistency was the most differentiating dimension (0.43-point spread)",
    "Bias had the least variance — all models above 0.99",
    "Categories: technology, science, biology, health, politics, economics",
], size=14)
add_bullet_frame(s, Inches(7.0), Inches(5.05), Inches(5.0), Inches(1.7), [
    "Framework generalises across all 6 subject categories",
    "Rankings align with expected quality ordering",
    "Results exported to CSV for reproducibility",
], size=14)

# ============================================================
# SLIDE 9 — Live Demo / Dashboard
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)
slide_header(s, "Interactive Dashboard", "Streamlit-based web interface with 3 tabs")

tabs = [
    ("Single Evaluation", [
        "Enter prompt + up to 3 model responses",
        "Toggle RAG mode for faithfulness checking",
        "Switch between static and learned weights",
        "Results: radar chart, ranked scores, hallucination details",
    ], ACCENT),
    ("Batch Analytics", [
        "Upload CSV/JSON with thousands of evaluations",
        "Concurrent processing with ThreadPoolExecutor",
        "Dashboard: KPIs, radar charts, heatmaps, box plots",
        "Export results to CSV for further analysis",
    ], ACCENT2),
    ("Validation Experiments", [
        "17 controlled test cases across all 6 dimensions",
        "One-click execution with real-time results",
        "Pass/Fail display with per-metric accuracy",
        "Documents framework limitations transparently",
    ], ACCENT4),
]

for i, (tab_name, items, clr) in enumerate(tabs):
    left = Inches(0.8) + i * Inches(4.1)
    add_shape(s, left, Inches(1.8), Inches(3.7), Inches(4.5), CARD)
    ind = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(1.8), Inches(3.7), Inches(0.06))
    ind.fill.solid()
    ind.fill.fore_color.rgb = clr
    ind.line.fill.background()
    add_text(s, left + Inches(0.3), Inches(2.1), Inches(3.1), Inches(0.5), tab_name, size=20, color=clr, bold=True)
    add_bullet_frame(s, left + Inches(0.3), Inches(2.7), Inches(3.1), Inches(3.3), items, size=14)

# Tech stack note
add_text(s, Inches(0.8), Inches(6.6), Inches(11.7), Inches(0.5),
         "Tech Stack:  Python  •  Streamlit  •  PyTorch  •  Transformers  •  Sentence-Transformers  •  scikit-learn  •  Matplotlib",
         size=13, color=DIM, align=PP_ALIGN.CENTER)

# ============================================================
# SLIDE 10 — Conclusion & Future Work
# ============================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(s)
slide_header(s, "Conclusion & Future Work")

# Conclusion
add_shape(s, Inches(0.8), Inches(1.8), Inches(6.0), Inches(4.8), CARD)
add_text(s, Inches(1.1), Inches(1.95), Inches(5.5), Inches(0.4), "What We Built", size=20, color=ACCENT, bold=True)
add_bullet_frame(s, Inches(1.1), Inches(2.5), Inches(5.5), Inches(3.8), [
    "Multi-dimensional LLM evaluation framework (4 standard + 2 RAG dimensions)",
    "Reference-free — no gold-standard answers needed",
    "Local transformer models — zero API cost",
    "Data-driven weights via Ridge Regression (R²=0.89)",
    "88.2% validation pass rate on 17 test cases",
    "Consistent model rankings across 10 benchmark prompts",
    "Interactive Streamlit dashboard for non-technical users",
    "Full test suite for reliability",
], size=14)

# Future work
add_shape(s, Inches(7.2), Inches(1.8), Inches(5.6), Inches(4.8), CARD)
add_text(s, Inches(7.5), Inches(1.95), Inches(5.0), Inches(0.4), "Future Enhancements", size=20, color=ACCENT2, bold=True)
add_bullet_frame(s, Inches(7.5), Inches(2.5), Inches(5.0), Inches(3.8), [
    "Expand training data to 500+ samples for robust weights",
    "Add fairness classifier for implicit bias detection",
    "Improve hallucination detection with fact extraction + knowledge graphs",
    "GPU-optimised batch inference for large-scale evaluation",
    "Multilingual support with multilingual-MiniLM",
    "CI/CD integration for continuous LLM quality monitoring",
], size=14, bullet_color=ACCENT2)

# Bottom bar
bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.1), prs.slide_width, Inches(0.4))
bar.fill.solid()
bar.fill.fore_color.rgb = CARD
bar.line.fill.background()
add_text(s, Inches(1), Inches(7.12), Inches(11), Inches(0.35),
         "Thank You  •  Questions?", size=18, color=ACCENT, bold=True, align=PP_ALIGN.CENTER)

# ── Save ──
os.makedirs("presentation", exist_ok=True)
output = "presentation/MetaEvalAI_Presentation.pptx"
prs.save(output)
print(f"✓ Presentation saved to: {output}")
print(f"  Slides: {len(prs.slides)}")

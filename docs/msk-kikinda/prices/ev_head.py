# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, HRFlowable, KeepTogether)

D = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DJ", D + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DJ-B", D + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily("DJ", normal="DJ", bold="DJ-B", italic="DJ", boldItalic="DJ-B")

NAVY = colors.HexColor("#1B2A4A")
ACC  = colors.HexColor("#8C6D3F")
GREY = colors.HexColor("#5A6270")
LINE = colors.HexColor("#C9CDD4")
BG   = colors.HexColor("#F2F4F7")
RED  = colors.HexColor("#A3282D")
GRN  = colors.HexColor("#1F6B43")

ss = getSampleStyleSheet()
def S(name, **kw):
    base = dict(fontName="DJ", fontSize=9.5, leading=14, textColor=colors.HexColor("#1A1A1A"))
    base.update(kw)
    return ParagraphStyle(name, **base)

H1   = S("H1", fontName="DJ-B", fontSize=19, leading=24, textColor=NAVY, spaceAfter=2)
SUB  = S("SUB", fontSize=10.5, leading=15, textColor=GREY)
H2   = S("H2", fontName="DJ-B", fontSize=13, leading=17, textColor=NAVY,
         spaceBefore=15, spaceAfter=6)
H3   = S("H3", fontName="DJ-B", fontSize=10.5, leading=14, textColor=ACC,
         spaceBefore=9, spaceAfter=3)
BODY = S("BODY", alignment=TA_JUSTIFY, spaceAfter=6)
SMALL= S("SMALL", fontSize=8.3, leading=11.5, textColor=GREY)
TH   = S("TH", fontName="DJ-B", fontSize=8.3, leading=11, textColor=colors.white)
TD   = S("TD", fontSize=8.3, leading=11.5)
TDB  = S("TDB", fontName="DJ-B", fontSize=8.3, leading=11.5)
TDR  = S("TDR", fontSize=8.3, leading=11.5, alignment=2)
TDBR = S("TDBR", fontName="DJ-B", fontSize=8.3, leading=11.5, alignment=2)
NOTE = S("NOTE", fontSize=9, leading=13.5, textColor=colors.HexColor("#3A3A3A"))

def tbl(header, rows, widths, aligns=None, zebra=True):
    """aligns: list of 'l'/'r' per column."""
    aligns = aligns or ["l"] * len(header)
    def cell(txt, i, bold=False):
        st = (TDBR if bold else TDR) if aligns[i] == "r" else (TDB if bold else TD)
        return Paragraph(str(txt), st)
    data = [[Paragraph(h, TH) for h in header]]
    for r in rows:
        bold = str(r[0]).startswith("*")
        data.append([cell(str(c).lstrip("*"), i, bold) for i, c in enumerate(r)])
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
        ("BOX", (0, 0), (-1, -1), 0.6, LINE),
    ]
    if zebra:
        for i in range(1, len(data)):
            if i % 2 == 0:
                cmds.append(("BACKGROUND", (0, i), (-1, i), BG))
    t.setStyle(TableStyle(cmds))
    return t

def callout(title, body, color=ACC):
    inner = [Paragraph(title, S("ct", fontName="DJ-B", fontSize=9.5, leading=13, textColor=color)),
             Spacer(1, 3), Paragraph(body, NOTE)]
    t = Table([[inner]], colWidths=[165*mm], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#FAF7F2") if color==ACC else colors.HexColor("#FBF2F2")),
        ("LINEBEFORE", (0,0), (0,-1), 2.5, color),
        ("LEFTPADDING", (0,0), (-1,-1), 10), ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    return t

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DJ", 7.5)
    canvas.setFillColor(GREY)
    canvas.drawString(22*mm, 12*mm, "MSK Kikinda — Dokazi o cenama, septembar 2026")
    canvas.drawRightString(188*mm, 12*mm, "Page %d" % doc.page)
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.4)
    canvas.line(22*mm, 15.5*mm, 188*mm, 15.5*mm)
    canvas.restoreState()

OUT = "/tmp/claude-0/-home-user-awesome-mcp-servers/d51bb9dc-117d-5f8b-b31d-d3001a459de9/scratchpad/MSK-Dokazi-Cene-Sep2026.pdf"
doc = SimpleDocTemplate(OUT, pagesize=A4,
                        leftMargin=22*mm, rightMargin=22*mm,
                        topMargin=20*mm, bottomMargin=20*mm,
                        title="MSK Kikinda — Dokazi o cenama, septembar 2026",
                        author="Studija strukturiranja", subject="MSK a.d. Kikinda")
E = []
W = 166*mm

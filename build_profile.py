"""Builds dark.svg and light.svg (animated terminal-style profile card).

1. python image_to_ascii.py your_photo.jpg      -> portrait.txt
2. python build_profile.py                       -> dark.svg + light.svg
Edit the PROFILE section below to change any text.
"""
from pathlib import Path
from html import escape

# ───────────────────────── PROFILE ─────────────────────────
HANDLE = "yash"                      # shows as yash@devos
PORTFOLIO = ""                       # e.g. "yash-portfolio.vercel.app" (row hidden if empty)

# (key, value). Keys with a dot are split/coloured like "Core.Lang".
# None = blank row, ("#", "Title") = section header.
ROWS = [
    ("Name", "Yash Sanjay"),
    ("Role", "Full-Stack Dev · CE Undergrad"),
    ("Base", "Mumbai, India"),
    ("Education", "B.E. Comp Engg, CGPA 8.42"),
    ("College", "DBIT Mumbai · Class of 2028"),
    ("Status", "Building • Learning • Shipping"),
    ("ToolChain", "Git, GitHub, LaTeX/Overleaf"),
    None,
    ("Core.Lang", "Java, JavaScript"),
    ("Core.Frontend", "React, HTML, CSS, JavaScript"),
    ("Core.Backend", "Spring Boot, Node.js, REST APIs"),
    ("Core.Database", "MySQL, Spring Data JPA"),
    ("Flagship", "Career Point (IEEE paper WIP)"),
    None,
    ("#", "Contact"),
    ("Grid.Mail", "yashsj2006@gmail.com"),
    ("Grid.Portfolio", PORTFOLIO),
    ("Grid.LinkedIn", "yash-sanjay-a6842b372"),
    ("Grid.Github", "yashsj2006"),
    None,
    ("#", "Live Stats"),
    ("", "See live GitHub stats badges below in README ↓"),
]
ROWS = [r for r in ROWS if not (r and r[0] == "Grid.Portfolio" and not r[1])]

# ───────────────────────── THEMES ─────────────────────────
DARK = dict(
    key="#22D3EE", value="#E5E7EB", cc="#475569", head="#7C3AED", accent="#10B981",
    panel_title="#38BDF8", pt_op=0.7, scan_label="#F87171", cursor="#22D3EE", text_fill="#dbeafe",
    ascii_a=["#22D3EE", "#7C3AED", "#38BDF8"], border=["#7C3AED", "#22D3EE", "#10B981"],
    bg=["#0B1120", "#050816"], scan=["#22D3EE", "#A5F3FC", "#7C3AED"], scan_op=[0.05, 0.65],
    lines="#7DD3FC", lines_op=0.05, bar="#0B1120", bar_op=0.85, panel="#0B1120", panel_fill_op=0.35, panel_op=0.35,
    dots=["#EF4444", "#F59E0B", "#10B981"], live="#F87171", blend="screen", scan_rect_op=0.7,
    frame_op=0.8, frame_anim="0.5;0.95;0.5")
LIGHT = dict(
    key="#0284C7", value="#1E293B", cc="#94A3B8", head="#7C3AED", accent="#059669",
    panel_title="#0284C7", pt_op=0.75, scan_label="#DC2626", cursor="#0EA5E9", text_fill="#1E293B",
    ascii_a=["#4F46E5", "#7C3AED", "#0EA5E9"], border=["#7C3AED", "#0EA5E9", "#059669"],
    bg=["#F8FAFC", "#E2E8F0"], scan=["#0EA5E9", "#38BDF8", "#7C3AED"], scan_op=[0.06, 0.55],
    lines="#334155", lines_op=0.035, bar="#FFFFFF", bar_op=0.9, panel="#FFFFFF", panel_fill_op=0.55, panel_op=0.4,
    dots=["#F87171", "#FBBF24", "#34D399"], live="#EF4444", blend="multiply", scan_rect_op=0.8,
    frame_op=0.75, frame_anim="0.45;0.9;0.45")

W, H = 1180, 610
FONT = "font-family: 'Courier New', Consolas, monospace;"
ROW0_Y, ROW1_Y, STEP = 42, 66, 22
VAL_COL = 28                           # column where values start
LINE_W = 56                            # width of header/section rules


def portrait_tspans():
    p = Path("portrait.txt")
    lines = p.read_text(encoding="utf-8", errors="ignore").splitlines() if p.exists() else []
    lines = [l.rstrip() for l in lines][:53]
    out, y = [], 79.98
    for l in lines:
        out.append(f'<tspan x="30" y="{y:.2f}" xml:space="preserve">{escape(l)}</tspan>')
        y += 7.545
    return "\n".join(out)


def row_svg(i, row):
    y = ROW0_Y if i == 0 else ROW1_Y + (i - 1) * STEP
    if i == 0:
        rule = " -" + "—" * (LINE_W - len(HANDLE) - 8) + "-—-"
        inner = f'<tspan x="520" y="{y}" class="head">{HANDLE}@devos</tspan><tspan class="cc">{rule}</tspan>'
    elif row is None:
        inner = f'<tspan x="520" y="{y}" class="cc">. </tspan>'
    elif row[0] == "#":
        rule = " -" + "—" * (LINE_W - len(row[1]) - 4) + "-—-"
        inner = f'<tspan x="520" y="{y}" class="accent">- {escape(row[1])}</tspan><tspan class="cc">{rule}</tspan>'
    elif row[0] == "":
        inner = f'<tspan x="520" y="{y}" class="cc">. </tspan><tspan class="value">{escape(row[1])}</tspan>'
    else:
        key, val = row
        parts = key.split(".")
        kx = '<tspan class="cc">.</tspan>'.join(f'<tspan class="key">{escape(p)}</tspan>' for p in parts)
        used = 2 + len(key) + 2
        dots = "." * max(3, VAL_COL - used - 1)
        inner = (f'<tspan x="520" y="{y}" class="cc">. </tspan>{kx}'
                 f'<tspan class="cc">: {dots} </tspan><tspan class="value">{escape(val)}</tspan>')
    return y, inner


def build(t):
    items = [("HEAD",)] + ROWS
    clips, texts, last_y = [], [], 0
    for i, row in enumerate(items):
        y, inner = row_svg(i, row)
        last_y = y
        begin = 0.75 + i * 0.1136
        clips.append(f'<clipPath id="lc{i}"><rect x="500" y="{y - 16:.2f}" width="0" height="24">'
                     f'<animate attributeName="width" from="0" to="690" dur="0.38s" begin="{begin:.2f}s" fill="freeze"/></rect></clipPath>')
        texts.append(f'<g clip-path="url(#lc{i})"><text x="520" y="0" fill="{t["text_fill"]}">{inner}</text></g>')
    cursor_begin = 0.75 + len(items) * 0.1136 + 0.3
    a = t["ascii_a"]; b = t["border"]
    css = f"""
    .ascii  {{ {FONT} font-size: 7.4px; fill: url(#asciiGrad); letter-spacing: -0.2px; }}
    .key    {{ {FONT} font-size: 15px; fill: {t['key']}; font-weight: bold; }}
    .value  {{ {FONT} font-size: 15px; fill: {t['value']}; }}
    .cc     {{ {FONT} font-size: 15px; fill: {t['cc']}; }}
    .head   {{ {FONT} font-size: 17px; fill: {t['head']}; font-weight: bold; }}
    .accent {{ {FONT} font-size: 15px; fill: {t['accent']}; font-weight: bold; }}
    text, tspan {{ white-space: pre; }}
    .term-label {{ {FONT} font-size: 12px; fill: #64748B; letter-spacing: 0.5px; }}
    .scan-label {{ {FONT} font-size: 10px; fill: {t['scan_label']}; letter-spacing: 1px; }}
    .panel-title {{ {FONT} font-size: 11px; fill: {t['panel_title']}; letter-spacing: 2px; opacity: {t['pt_op']}; }}
    .cursor-blink {{ fill: {t['cursor']}; }}"""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="asciiGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{a[0]}"><animate attributeName="stop-color" values="{a[0]};{a[1]};{a[2]};{a[0]}" dur="9s" repeatCount="indefinite"/></stop>
    <stop offset="100%" stop-color="{a[1]}"><animate attributeName="stop-color" values="{a[1]};{a[2]};{a[0]};{a[1]}" dur="9s" repeatCount="indefinite"/></stop>
  </linearGradient>
  <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{b[0]}"/><stop offset="50%" stop-color="{b[1]}"/><stop offset="100%" stop-color="{b[2]}"/>
  </linearGradient>
  <radialGradient id="bgGlow" cx="30%" cy="20%" r="80%">
    <stop offset="0%" stop-color="{t['bg'][0]}"/><stop offset="100%" stop-color="{t['bg'][1]}"/>
  </radialGradient>
  <linearGradient id="scanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="{t['scan'][0]}" stop-opacity="0"/>
    <stop offset="45%" stop-color="{t['scan'][0]}" stop-opacity="{t['scan_op'][0]}"/>
    <stop offset="50%" stop-color="{t['scan'][1]}" stop-opacity="{t['scan_op'][1]}"/>
    <stop offset="55%" stop-color="{t['scan'][0]}" stop-opacity="{t['scan_op'][0]}"/>
    <stop offset="100%" stop-color="{t['scan'][2]}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="{t['lines']}" opacity="{t['lines_op']}"/>
  </pattern>
  <mask id="revealMask" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="620">
    <rect x="0" y="0" width="{W}" height="0" fill="#fff">
      <animate attributeName="height" from="0" to="560" dur="2.6s" begin="0.2s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>
    </rect>
  </mask>
  {"".join(clips)}
  <style>{css}
  </style>
</defs>

<rect width="{W}" height="{H}" rx="18" fill="url(#bgGlow)"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#scanlines)"/>

<g id="titlebar">
  <rect x="3" y="3" width="1174" height="34" rx="16" fill="{t['bar']}" fill-opacity="{t['bar_op']}"/>
  <circle cx="24" cy="20" r="5" fill="{t['dots'][0]}"><animate attributeName="opacity" values="1;0.55;1" dur="4s" repeatCount="indefinite"/></circle>
  <circle cx="42" cy="20" r="5" fill="{t['dots'][1]}"><animate attributeName="opacity" values="1;0.55;1" dur="4s" begin="0.3s" repeatCount="indefinite"/></circle>
  <circle cx="60" cy="20" r="5" fill="{t['dots'][2]}"><animate attributeName="opacity" values="1;0.55;1" dur="4s" begin="0.6s" repeatCount="indefinite"/></circle>
  <text x="590" y="25" text-anchor="middle" class="term-label">{HANDLE}@devos ~ % ./profile.sh --live</text>
  <circle cx="1122" cy="20" r="4" fill="{t['live']}"><animate attributeName="opacity" values="1;0.15;1" dur="1.1s" repeatCount="indefinite"/></circle>
  <text x="1132" y="24" class="scan-label">SCANNING</text>
</g>

<g transform="translate(0,38)">
  <rect x="14" y="26" width="488" height="468" rx="14" fill="{t['panel']}" fill-opacity="{t['panel_fill_op']}" stroke="url(#borderGrad)" stroke-width="1" opacity="{t['panel_op']}"/>
  <rect x="508" y="10" width="655" height="500" rx="14" fill="{t['panel']}" fill-opacity="{t['panel_fill_op']}" stroke="url(#borderGrad)" stroke-width="1" opacity="{t['panel_op']}"/>
  <text x="30" y="24" class="panel-title">VISUAL.MAP</text>
  <text x="524" y="24" class="panel-title">SYSTEM.INFO</text>

  <g mask="url(#revealMask)">
  <text x="30" y="0" class="ascii">
{portrait_tspans()}
  </text>
  </g>

  {"".join(texts)}

  <rect x="522" y="{last_y - 15}" width="9" height="16" class="cursor-blink" opacity="0">
    <animate attributeName="opacity" values="0;0;1;0;1;0;1;0" keyTimes="0;0.01;0.02;0.3;0.5;0.7;0.85;1" dur="1.4s" begin="{cursor_begin:.2f}s" repeatCount="indefinite"/>
  </rect>
</g>

<rect x="0" y="-70" width="{W}" height="70" fill="url(#scanGrad)" opacity="{t['scan_rect_op']}" style="mix-blend-mode:{t['blend']}">
  <animateTransform attributeName="transform" type="translate" from="0 -70" to="0 680" dur="4.2s" repeatCount="indefinite"/>
</rect>

<rect x="3" y="3" width="1174" height="604" rx="16" fill="none" stroke="url(#borderGrad)" stroke-width="2" opacity="{t['frame_op']}">
  <animate attributeName="opacity" values="{t['frame_anim']}" dur="3.2s" repeatCount="indefinite"/>
</rect>
</svg>
'''


if __name__ == "__main__":
    for name, theme in (("dark.svg", DARK), ("light.svg", LIGHT)):
        Path(name).write_text(build(theme), encoding="utf-8")
        print("wrote", name)

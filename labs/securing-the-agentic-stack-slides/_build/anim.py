#!/usr/bin/env python3
"""Animated slide generator for the "Speed or Security? Why Not Both for Your Coding Agents" deck.

Adds professional, self-contained motion to the deck's diagram slides. All
animation is SMIL only (<animateMotion>, <animate>, <animateTransform>) so it
survives the deck's markdown->HTML passthrough without a <style> block or
<script>, and stays crisp at any projector size.

Two techniques, picked per slide for best fidelity:

  * slide 13 ("The Agentic Workflow") is a full SVG RECREATION of the baked
    diagram (geometry matched to assets/slide-13.webp), so the agents can orbit
    through the actual loop geometry.

  * slides 12, 33, 36 keep their original baked .webp as the base layer and get
    a TRANSPARENT SVG OVERLAY aligned to the baked coordinates. Every word, font
    and colour stays pixel-perfect; we only add motion on top.

Every element id is namespaced per slide (e.g. #halo13, #out36) so the combined
deck.md DOM has no id collisions.

Run:  python3 anim.py            # patch ../deck.md in place (idempotent)
      python3 anim.py preview    # also write /tmp/anim_<n>.html per slide

Palette sampled from the baked slides:
  white #ffffff | navy #193363 | ink #0a0c10 | grey #585858
  docker-blue #1d63ed | agent/ok green #26ae60 | deny red #e5484d
"""
import os, re

NAVY  = "#193363"
INK   = "#0a0c10"
GREY  = "#585858"
BLUE  = "#1d63ed"
GREEN = "#26ae60"
RED   = "#e5484d"
SANS  = "ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif"


# ---------------------------------------------------------------- glyph helpers
def circle_path(cx, cy, r):
    """A full circle as a path, starting at the top, clockwise."""
    return f"M {cx},{cy-r} A {r},{r} 0 1,1 {cx},{cy+r} A {r},{r} 0 1,1 {cx},{cy-r}"


def halo_def(idn, colour):
    return (f'<radialGradient id="{idn}" cx="50%" cy="50%" r="50%">'
            f'<stop offset="0%" stop-color="{colour}" stop-opacity="0.55"/>'
            f'<stop offset="55%" stop-color="{colour}" stop-opacity="0.16"/>'
            f'<stop offset="100%" stop-color="{colour}" stop-opacity="0"/></radialGradient>')


def agent_chip(cx, cy, scale=1.0, halo=None):
    """Agent glyph: navy monitor, green screen, navy head dot (matches slide 13)."""
    bw, bh = 46*scale, 34*scale
    sw, sh = 28*scale, 18*scale
    hr = 7*scale
    g = ""
    if halo:
        g += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{34*scale:.1f}" fill="url(#{halo})"/>'
    g += (f'<rect x="{cx-bw/2:.1f}" y="{cy-bh/2:.1f}" width="{bw:.1f}" height="{bh:.1f}" '
          f'rx="{6*scale:.1f}" fill="{NAVY}"/>'
          f'<rect x="{cx-sw/2:.1f}" y="{cy-sh/2:.1f}" width="{sw:.1f}" height="{sh:.1f}" '
          f'rx="{3*scale:.1f}" fill="{GREEN}"/>'
          f'<circle cx="{cx:.1f}" cy="{cy-bh/2-hr-3*scale:.1f}" r="{hr:.1f}" fill="{NAVY}"/>')
    return g


def human(cx, cy, scale=1.0, colour=NAVY, halo=None):
    """A simple person silhouette (head + shoulders), to match slide 12's icons."""
    hr = 9*scale
    g = ""
    if halo:
        g += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{30*scale:.1f}" fill="url(#{halo})"/>'
    g += (f'<circle cx="{cx:.1f}" cy="{cy-15*scale:.1f}" r="{hr:.1f}" fill="{colour}"/>'
          f'<path d="M {cx-17*scale:.1f},{cy+18*scale:.1f} '
          f'a {17*scale:.1f},{20*scale:.1f} 0 0 1 {34*scale:.1f},0 Z" fill="{colour}"/>')
    return g


def key_glyph(cx, cy, scale=1.0, colour="#ffffff"):
    s = scale
    return (f'<circle cx="{cx-7*s:.1f}" cy="{cy:.1f}" r="{5*s:.1f}" fill="none" '
            f'stroke="{colour}" stroke-width="{3*s:.1f}"/>'
            f'<rect x="{cx-2*s:.1f}" y="{cy-1.5*s:.1f}" width="{13*s:.1f}" height="{3*s:.1f}" fill="{colour}"/>'
            f'<rect x="{cx+9*s:.1f}" y="{cy-1.5*s:.1f}" width="{3*s:.1f}" height="{6*s:.1f}" fill="{colour}"/>')


def ping(cx, cy, begin, colour=GREEN, r0=22, r1=58, dur=2.6, opacity=0.55):
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r0}" fill="none" stroke="{colour}" stroke-width="3">'
        f'<animate attributeName="r" values="{r0};{r1}" dur="{dur}s" begin="{begin}s" '
        f'repeatCount="indefinite" calcMode="spline" keySplines="0.3 0 0.3 1" keyTimes="0;1"/>'
        f'<animate attributeName="opacity" values="{opacity};0" dur="{dur}s" begin="{begin}s" '
        f'repeatCount="indefinite"/></circle>'
    )


def svg_open(idn, extra="", preserve="none", transparent=True):
    bg = "pointer-events:none" if transparent else ""
    return (f'<svg data-anim="{idn}" viewBox="0 0 1600 900" preserveAspectRatio="{preserve}" '
            f'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;{bg}">'
            f'{extra}')


# ================================================================ slide 13
# Full recreation. Geometry measured from assets/slide-13.webp (viewBox 1600x900).
IN  = (555, 540)      # inner loop centre
OUT = (1088, 535)     # outer loop centre
IN_R, OUT_R = 140, 188              # drawn ring radii
IN_ST, OUT_ST = 185, 234            # station radii
IN_ORBIT, OUT_ORBIT = 160, 210      # agent lane (between ring and stations)
STATIONS13 = [
    (560, 349, "Build",       "middle", 0,  -58),
    (373, 537, "Code",        "end",   -46,   6),
    (429, 671, "Open Source", "middle", 0,   62),
    (696, 671, "Test",        "middle", 0,   62),
    (1088, 301, "Integrate",  "middle", 0,  -58),
    (1321, 537, "Test",       "start",  46,   6),
    (1088, 769, "Deploy",     "middle", 0,   62),
]


def slide13():
    icx, icy = IN; ocx, ocy = OUT
    bx0, bx1, by = icx + IN_R + 8, ocx - OUT_R - 20, 540
    p = [svg_open("slide-13", preserve="xMidYMid meet", transparent=False)]
    p.append('<defs>')
    p.append(halo_def("halo13", GREEN))
    p.append(f'<marker id="arrow13" markerWidth="12" markerHeight="12" refX="8" refY="5" '
             f'orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="{NAVY}"/></marker>')
    p.append(f'<path id="innerOrbit13" d="{circle_path(icx, icy, IN_ORBIT)}" fill="none"/>')
    p.append(f'<path id="outerOrbit13" d="{circle_path(ocx, ocy, OUT_ORBIT)}" fill="none"/>')
    p.append('</defs>')
    p.append('<rect x="0" y="0" width="1600" height="900" fill="#ffffff"/>')
    # title + subtitle
    p.append(f'<text x="95" y="150" font-family="{SANS}" font-size="64" font-weight="800" '
             f'fill="{INK}">The Agentic Workflow</text>')
    p.append(f'<text x="97" y="222" font-family="{SANS}" font-size="33" fill="{GREY}">'
             f'Now an agent sits at <tspan font-weight="800">every</tspan> stage &#8212; the attack surface is no longer just</text>')
    p.append(f'<text x="97" y="266" font-family="{SANS}" font-size="33" fill="{GREY}">what you pull.</text>')
    # rotating dotted orbit guides
    for cx, cy, r, dur, sweep in [(icx, icy, IN_ORBIT, 26, 1), (ocx, ocy, OUT_ORBIT, 34, -1)]:
        p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{NAVY}" '
                 f'stroke-opacity="0.12" stroke-width="2" stroke-dasharray="2 14" stroke-linecap="round">'
                 f'<animateTransform attributeName="transform" type="rotate" '
                 f'from="0 {cx} {cy}" to="{360*sweep} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    # loop rings + labels
    p.append(f'<circle cx="{icx}" cy="{icy}" r="{IN_R}" fill="#ffffff" stroke="{NAVY}" stroke-width="7"/>')
    p.append(f'<circle cx="{ocx}" cy="{ocy}" r="{OUT_R}" fill="#ffffff" stroke="{NAVY}" stroke-width="7"/>')
    p.append(f'<text x="{icx}" y="{icy-14}" font-family="{SANS}" font-size="40" fill="{INK}" text-anchor="middle">Inner</text>'
             f'<text x="{icx}" y="{icy+30}" font-family="{SANS}" font-size="40" fill="{INK}" text-anchor="middle">Loop</text>')
    p.append(f'<text x="{ocx}" y="{ocy-14}" font-family="{SANS}" font-size="44" fill="{INK}" text-anchor="middle">Outer</text>'
             f'<text x="{ocx}" y="{ocy+32}" font-family="{SANS}" font-size="44" fill="{INK}" text-anchor="middle">Loop</text>')
    # push bridge + pulse
    p.append(f'<line x1="{bx0}" y1="{by}" x2="{bx1}" y2="{by}" stroke="{NAVY}" stroke-width="6" marker-end="url(#arrow13)"/>')
    p.append(f'<text x="{(bx0+bx1)/2:.0f}" y="{by-30}" font-family="{SANS}" font-size="36" '
             f'font-weight="800" fill="{GREY}" text-anchor="middle">Push</text>')
    p.append(f'<circle r="9" fill="{GREEN}">'
             f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.15;0.85;1" dur="2.2s" repeatCount="indefinite"/>'
             f'<animateMotion dur="2.2s" repeatCount="indefinite" path="M {bx0+6},{by} L {bx1-4},{by}"/></circle>')
    # station pings
    for i, (sx, sy, *_r) in enumerate(STATIONS13):
        p.append(ping(sx, sy, begin=round(i*0.37, 2)))
    # static station chips + labels
    for sx, sy, label, anchor, ldx, ldy in STATIONS13:
        p.append(agent_chip(sx, sy))
        p.append(f'<text x="{sx+ldx}" y="{sy+ldy}" font-family="{SANS}" font-size="27" '
                 f'font-weight="700" fill="{GREY}" text-anchor="{anchor}">{label}</text>')
    # orbiting agents
    for pid, dur in [("innerOrbit13", 7.0), ("outerOrbit13", 9.5)]:
        p.append(f'<g>{agent_chip(0,0,scale=0.8,halo="halo13")}'
                 f'<animateMotion dur="{dur}s" repeatCount="indefinite" rotate="0" calcMode="linear">'
                 f'<mpath xlink:href="#{pid}" href="#{pid}"/></animateMotion></g>')
    p.append('</svg>')
    return "".join(p)


# ================================================================ slide 33 overlay
# "Three boundaries surround every agent". Calm, literal: highlight each boundary in
# sequence (1 MicroVM -> 2 Proxy -> 3 Credential injection), matching the three
# numbered points at the bottom. Baked anchors (viewBox 1600x900):
#   MicroVM box x[370..965] y[388..585] | Proxy box x[1030..1170] y[364..592]
#   top badges 1(413,406) 2/3(~1078/1120,428) | bottom badges 1(116,705) 2(600,704) 3(1085,705)
#   proxy->Internet arrow at y~486
AMBER = "#f5a623"


def slide33():
    micro = (368, 384, 968, 590)         # x0,y0,x1,y1
    proxy = (1028, 362, 1172, 594)
    C = 6.0                              # one full 1->2->3 cycle
    # opacity gate keeping each step visible only in its third of the cycle
    GATE = {
        0: ('0;0.02;0.30;0.333;1',          '0;1;1;0;0'),
        1: ('0;0.333;0.353;0.633;0.666;1',  '0;0;1;1;0;0'),
        2: ('0;0.666;0.686;0.966;1',        '0;0;1;1;0'),
    }

    def gate(step):
        kt, vv = GATE[step]
        return f'<animate attributeName="opacity" dur="{C}s" repeatCount="indefinite" keyTimes="{kt}" values="{vv}"/>'

    def ring_rect(b, w=6):
        x0, y0, x1, y1 = b
        return (f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" rx="18" fill="none" '
                f'stroke="{AMBER}" stroke-width="{w}"/>')

    def badge_ring(cx, cy, r=29):
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{AMBER}" stroke-width="4"/>'

    p = [svg_open("slide-33")]
    p.append('<defs>' + halo_def("halo33k", AMBER) + '</defs>')

    # step 1 - MicroVM: ring the microVM box + its number badges (top + bottom)
    p.append(f'<g opacity="0">{gate(0)}{ring_rect(micro)}{badge_ring(413,406)}{badge_ring(116,705)}</g>')

    # step 2 - Network proxy: ring the proxy box + its bottom number badge
    p.append(f'<g opacity="0">{gate(1)}{ring_rect(proxy)}{badge_ring(600,704)}</g>')

    # step 3 - Credential injection: proxy ring (dim) + a key sliding out to the Internet
    key = (f'<g><circle cx="0" cy="0" r="26" fill="url(#halo33k)"/>{key_glyph(0,0,scale=1.8,colour=AMBER)}'
           f'<animateMotion dur="{C}s" repeatCount="indefinite" keyPoints="0;0;1;1" '
           f'keyTimes="0;0.686;0.93;1" calcMode="linear" path="M 1180,486 L 1288,486"/></g>')
    p.append(f'<g opacity="0">{gate(2)}{ring_rect(proxy, w=4)}{key}{badge_ring(1085,705)}</g>')

    p.append('</svg>')
    return "".join(p)


# ================================================================ slide 12 overlay
# "The Traditional Workflow" - same geometry as slide 13, but ONE human orbits each
# loop SLOWLY (deliberate, reviewed human pace), with a calm navy push pulse and no
# busy pings. The contrast with slide 13's fast, everywhere agents is the point.
def slide12():
    icx, icy = IN; ocx, ocy = OUT
    bx0, bx1, by = icx + IN_R + 8, ocx - OUT_R - 20, 540
    p = [svg_open("slide-12")]
    p.append('<defs>')
    p.append(halo_def("halo12", BLUE))
    p.append(f'<path id="innerOrbit12" d="{circle_path(icx, icy, IN_ORBIT)}" fill="none"/>')
    p.append(f'<path id="outerOrbit12" d="{circle_path(ocx, ocy, OUT_ORBIT)}" fill="none"/>')
    p.append('</defs>')
    # calm slow push pulse (navy)
    p.append(f'<circle r="8" fill="{NAVY}">'
             f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.2;0.8;1" dur="3.6s" repeatCount="indefinite"/>'
             f'<animateMotion dur="3.6s" repeatCount="indefinite" path="M {bx0+6},{by} L {bx1-4},{by}"/></circle>')
    # one human slowly orbiting each loop
    for pid, dur in [("innerOrbit12", 12.0), ("outerOrbit12", 15.0)]:
        p.append(f'<g>{human(0,0,scale=1.0,colour=NAVY,halo="halo12")}'
                 f'<animateMotion dur="{dur}s" repeatCount="indefinite" rotate="0" calcMode="linear">'
                 f'<mpath xlink:href="#{pid}" href="#{pid}"/></animateMotion></g>')
    p.append('</svg>')
    return "".join(p)


# ---------------------------------------------------------------- deck patching
BUILDERS = {12: slide12, 33: slide33}   # overlays
RECREATE = {13: slide13}                                          # full replacements


def patch_deck():
    here = os.path.dirname(os.path.abspath(__file__))
    deck = os.path.join(here, "..", "deck.md")
    src = open(deck).read()

    # full replacements (replace the <img> or a prior tagged <svg>)
    for n, build in RECREATE.items():
        block = build()
        img = re.compile(rf'<img[^>]*slide-{n:02d}\.webp[^>]*/>', re.S)
        prior = re.compile(rf'<svg data-anim="slide-{n}".*?</svg>', re.S)
        if img.search(src):
            src = img.sub(lambda m: block, src)
        elif prior.search(src):
            src = prior.sub(lambda m: block, src)
        else:
            raise SystemExit(f"slide-{n}: neither <img> nor prior <svg> found")

    # overlays: strip any prior overlay, then insert right after the baked <img>
    for n, build in BUILDERS.items():
        block = build()
        src = re.sub(rf'\n*<svg data-anim="slide-{n}".*?</svg>', '', src, flags=re.S)
        img = re.compile(rf'(<img[^>]*slide-{n:02d}\.webp[^>]*/>)', re.S)
        m = img.search(src)
        if not m:
            raise SystemExit(f"slide-{n}: baked <img> not found (needed for overlay)")
        src = src[:m.end()] + "\n\n" + block + src[m.end():]

    open(deck, "w").write(src)
    print("patched slides:", sorted(list(RECREATE) + list(BUILDERS)))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        base = ('data:image/webp;base64,')  # placeholder note
        for n, build in {**RECREATE, **BUILDERS}.items():
            overlay = n in BUILDERS
            layers = ""
            if overlay:
                layers = (f'<img src="../assets/slide-{n:02d}.webp" '
                          f'style="position:absolute;inset:0;width:100%;height:100%;object-fit:fill"/>')
            html = ('<!doctype html><meta charset=utf-8><body style="margin:0;background:#333">'
                    '<div style="position:relative;width:1600px;height:900px;margin:20px auto;'
                    'box-shadow:0 10px 40px #0008;background:#fff">' + layers + build() + '</div>')
            open(f"/tmp/anim_{n}.html", "w").write(html)
            print(f"/tmp/anim_{n}.html")
    patch_deck()

#!/usr/bin/env python3
"""Value × functionality positioning chart + ranking table for bto-researchmarket.

Usage:
    python3 positioning_chart.py data.json --out chart.svg [--inline chart.inline.svg] [--table table.md]

data.json:
{
  "title": "Value × functionality: utility suites (read 2026-10-09)",
  "rubric_size": 15,                     # number of feature categories (X axis max)
  "groups": {"mac": {"label": "Mac vendor", "color": "#6B5CE8"}, ...},
  "products": [
    {"name": "CleanMyMac", "group": "mac", "functionality": 10.5,
     "effective_per_year": 39.99, "basis": "Mac App Store yearly $39.99"}
  ],
  "candidates": [                        # your own product at candidate prices (hypotheses)
    {"name": "Your suite $59 one-time", "functionality": 7.5, "effective_per_year": 19.67}
  ],
  "highlight_zone": {"min_functionality": 7, "min_value": 3, "label": "Broad + good value: open space"}
}

Scoring rules (keep them in the report so readers can argue with them):
- functionality = categories covered of `rubric_size` (✓ = 1, partial = 0.5), from vendor feature pages;
- effective $/yr = what a buyer keeps paying for the smallest standard plan: the renewal price when year one
  is a promo, the displayed price when the "sale" never ends, and one-time prices ÷ 3 years;
- value = functionality ÷ (effective $/yr ÷ 10), i.e. functionality points per $10 a year.

--out writes a standalone SVG with literal colours (good for GitHub/Markdown).
--inline writes an SVG that uses CSS classes (.grid .tick .axis .zone .lbl .pt-<group> .amb …) so an HTML page
can colour it from its own light/dark theme tokens.
"""
import argparse
import html
import json
import math

W, H, L, R, T, B = 1040, 720, 90, 30, 70, 90
CHAR_W, LINE_H = 6.6, 14   # rough label metrics at ~11.5px, used for collision avoidance


def value_of(f, price):
    return f / (price / 10) if price > 0 else float("inf")


def place_labels(points, sx, sy, reserved=()):
    """Greedy label placement: try 8 positions per point, keep the one overlapping least with labels and dots."""
    taken = [(sx(p["functionality"]) - 7, sy(p["value"]) - 7, 14, 14) for p in points] + list(reserved)
    offsets = [(10, 4, "start"), (10, -8, "start"), (10, 16, "start"), (-10, 4, "end"),
               (-10, -8, "end"), (-10, 16, "end"), (0, -14, "middle"), (0, 22, "middle")]
    out = []
    for p in points:
        x, y = sx(p["functionality"]), sy(p["value"])
        width = len(p["label"]) * CHAR_W
        best, best_cost = None, math.inf
        for dx, dy, anchor in offsets:
            left = x + dx if anchor == "start" else x + dx - width if anchor == "end" else x - width / 2
            box = (left, y + dy - LINE_H + 3, width, LINE_H)
            cost = sum(overlap(box, t) for t in taken)
            if left < L or left + width > W - R:
                cost += 10_000
            if cost < best_cost:
                best, best_cost = (dx, dy, anchor, box), cost
        dx, dy, anchor, box = best
        taken.append(box)
        out.append((x + dx, y + dy, anchor))
    return out


def overlap(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return max(0, min(ax + aw, bx + bw) - max(ax, bx)) * max(0, min(ay + ah, by + bh) - max(ay, by))


def build(data, inline):
    xmax = data.get("rubric_size", 15)
    pts = [dict(p, value=value_of(p["functionality"], p["effective_per_year"]), label=p["name"], kind="product")
           for p in data["products"]]
    cands = [dict(c, value=value_of(c["functionality"], c["effective_per_year"]), label=c["name"], kind="candidate")
             for c in data.get("candidates", [])]
    ymax = max(5, math.ceil(max(p["value"] for p in pts + cands if math.isfinite(p["value"])) + 1))
    sx = lambda f: L + f / xmax * (W - L - R)
    sy = lambda v: H - B - min(v, ymax) / ymax * (H - T - B)
    groups = data.get("groups", {})

    def style(cls, attrs):
        """CSS class when --inline (theme-aware page), literal presentation attributes otherwise."""
        if inline:
            return 'class="' + cls + '"'
        return " ".join(k + '="' + str(v) + '"' for k, v in attrs.items())

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif" role="img">',
         f'<title>{html.escape(data.get("title", "Value × functionality"))}</title>']
    if not inline:
        s.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    s.append(f'<text x="{L}" y="34" font-size="20" font-weight="600" {style("axis", {"fill": "#1C1A33"})}>{html.escape(data.get("title", ""))}</text>')
    s.append(f'<text x="{L}" y="54" font-size="12" {style("tick", {"fill": "#5b5f6a"})}>X: categories covered of {xmax} (✓=1, partial=0.5) · Y: functionality points per $10 of effective yearly price (one-time ÷ 3 yrs)</text>')
    zone = data.get("highlight_zone")
    if zone:
        s.append(f'<rect x="{sx(zone["min_functionality"]):.1f}" y="{sy(ymax):.1f}" width="{sx(xmax) - sx(zone["min_functionality"]):.1f}" '
                 f'height="{sy(zone["min_value"]) - sy(ymax):.1f}" {style("zone", {"fill": "#ED708F", "opacity": "0.07"})}/>')
        s.append(f'<text x="{sx(xmax) - 8:.1f}" y="{sy(ymax) + 18:.1f}" text-anchor="end" font-size="12" {style("zone-label", {"fill": "#B8476A"})}>{html.escape(zone.get("label", ""))}</text>')
    step = 1 if xmax <= 10 else 3
    for i in range(0, xmax + 1, step):
        s.append(f'<line x1="{sx(i):.1f}" y1="{T}" x2="{sx(i):.1f}" y2="{H - B}" {style("grid", {"stroke": "#eceef2"})}/>'
                 f'<text x="{sx(i):.1f}" y="{H - B + 20}" text-anchor="middle" font-size="12" {style("tick", {"fill": "#5b5f6a"})}>{i}</text>')
    for v in range(0, ymax + 1):
        s.append(f'<line x1="{L}" y1="{sy(v):.1f}" x2="{W - R}" y2="{sy(v):.1f}" {style("grid", {"stroke": "#eceef2"})}/>'
                 f'<text x="{L - 10}" y="{sy(v) + 4:.1f}" text-anchor="end" font-size="12" {style("tick", {"fill": "#5b5f6a"})}>{v}</text>')
    s.append(f'<text x="{(L + W - R) / 2:.1f}" y="{H - 40}" text-anchor="middle" font-size="13" {style("axis", {"fill": "#1C1A33"})}>Functionality →</text>')
    s.append(f'<text transform="translate(28 {(T + H - B) / 2:.1f}) rotate(-90)" text-anchor="middle" font-size="13" {style("axis", {"fill": "#1C1A33"})}>Value for money →</text>')

    allpts = pts + cands
    # legend goes in the plot corner with the fewest points; labels then avoid it
    items = [(g["label"], g["color"]) for g in groups.values()]
    leg_w, leg_h = 250, 18 * (len(items) + (1 if cands else 0)) + 10
    corners = [(L + 8, T + 8), (W - R - leg_w - 8, T + 8), (W - R - leg_w - 8, H - B - leg_h - 8), (L + 8, H - B - leg_h - 8)]
    def crowd(c):
        x0, y0 = c
        return sum(1 for q in allpts if x0 - 20 <= sx(q["functionality"]) <= x0 + leg_w + 20 and y0 - 20 <= sy(q["value"]) <= y0 + leg_h + 20)
    leg_x, leg_y = min(corners, key=crowd)
    labels = place_labels(allpts, sx, sy, reserved=[(leg_x, leg_y, leg_w, leg_h)])
    if cands:
        line = " ".join(f"{sx(c['functionality']):.1f},{sy(c['value']):.1f}" for c in cands)
        s.append(f'<polyline points="{line}" fill="none" {style("amb-line", {"stroke": "#ED708F", "stroke-dasharray": "4 4"})}/>')
    for p, (lx, ly, anchor) in zip(allpts, labels):
        x, y = sx(p["functionality"]), sy(p["value"])
        tip = html.escape(f'{p["name"]}: functionality {p["functionality"]:g}, ${p["effective_per_year"]:.2f}/yr, value {p["value"]:.1f}'
                          + (f' ({p["basis"]})' if p.get("basis") else ""))
        if p["kind"] == "candidate":
            s.append(f'<path d="M{x:.1f},{y - 8:.1f} L{x + 8:.1f},{y:.1f} L{x:.1f},{y + 8:.1f} L{x - 8:.1f},{y:.1f} Z" stroke-width="2.5" '
                     f'{style("amb", {"fill": "#ffffff", "stroke": "#ED708F"})}><title>{tip}</title></path>')
            s.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" font-size="11.5" font-weight="700" {style("lbl amb-lbl", {"fill": "#B8476A"})}>{html.escape(p["label"])}</text>')
        else:
            color = groups.get(p.get("group"), {}).get("color", "#6B5CE8")
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" {style("pt-" + p.get("group", "x"), {"fill": color})}><title>{tip}</title></circle>')
            s.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" font-size="11.5" {style("lbl", {"fill": "#1C1A33"})}>{html.escape(p["label"])}</text>')
    lx0, ly0 = leg_x + 12, leg_y + 16
    s.append(f'<rect x="{leg_x}" y="{leg_y}" width="{leg_w}" height="{leg_h}" rx="8" {style("legend", {"fill": "#ffffff", "stroke": "#eceef2"})}/>')
    for i, (label, color) in enumerate(items):
        key = list(groups.keys())[i]
        s.append(f'<circle cx="{lx0}" cy="{ly0 + i * 18}" r="5" {style("pt-" + key, {"fill": color})}/>'
                 f'<text x="{lx0 + 12}" y="{ly0 + i * 18 + 4}" font-size="11.5" {style("lbl", {"fill": "#1C1A33"})}>{html.escape(label)}</text>')
    if cands:
        y = ly0 + len(items) * 18
        s.append(f'<path d="M{lx0},{y - 6} L{lx0 + 6},{y} L{lx0},{y + 6} L{lx0 - 6},{y} Z" stroke-width="2" {style("amb", {"fill": "#ffffff", "stroke": "#ED708F"})}/>'
                 f'<text x="{lx0 + 12}" y="{y + 4}" font-size="11.5" {style("lbl amb-lbl", {"fill": "#B8476A"})}>Your product, candidate prices</text>')
    s.append("</svg>")
    return "\n".join(s), allpts


def table(allpts):
    rows = ["| Product | Functionality | Effective $/yr | Value | Price basis |", "|---|---|---|---|---|"]
    for p in sorted(allpts, key=lambda p: -p["value"]):
        name = f'*{p["name"]} (hypothesis)*' if p["kind"] == "candidate" else p["name"]
        rows.append(f'| {name} | {p["functionality"]:g} | {p["effective_per_year"]:.2f} | {p["value"]:.1f} | {p.get("basis", "candidate price")} |')
    return "\n".join(rows) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("data")
    ap.add_argument("--out", default="value-functionality.svg")
    ap.add_argument("--inline")
    ap.add_argument("--table")
    args = ap.parse_args()
    data = json.load(open(args.data))
    svg, allpts = build(data, inline=False)
    open(args.out, "w").write(svg)
    if args.inline:
        open(args.inline, "w").write(build(data, inline=True)[0])
    md = table(allpts)
    if args.table:
        open(args.table, "w").write(md)
    print(md)

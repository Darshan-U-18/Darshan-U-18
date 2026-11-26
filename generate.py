#!/usr/bin/env python3
"""Regenerates dark.svg and light.svg. Run daily by GitHub Actions so Uptime stays current."""
import json, re, sys
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape as E

HERE = Path(__file__).parent
P = json.loads((HERE / "profile.json").read_text(encoding="utf-8"))
PORT = (HERE / "portrait.txt").read_text(encoding="utf-8").split("\n")

MONO = "ui-monospace,SFMono-Regular,'Cascadia Mono',Consolas,Menlo,Monaco,'Courier New',monospace"
FS, CW, LH, W = 16, 9.6, 17.2, 58

def uptime(since, today=None):
    t = today or date.today()
    y, m, d = t.year - since.year, t.month - since.month, t.day - since.day
    if d < 0:
        m -= 1
        pm, py = (t.month - 1 or 12), (t.year if t.month > 1 else t.year - 1)
        dim = [31, 29 if py % 4 == 0 and (py % 100 or py % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][pm - 1]
        d += dim
    if m < 0:
        y -= 1; m += 12
    u = lambda n, w: f"{n} {w}{'' if n == 1 else 's'}"
    return f"{u(y,'year')}, {u(m,'month')}, and {u(d,'day')}"

def kv(label, val):
    left = f". {label}: "
    return left + "." * max(W - len(left) - len(val) - 1, 2) + " " + val
def head(t): return f"- {t} " + "-" * (W - len(t) - 3)

since = date.fromisoformat(P["uptime_since"])
INFO = [
    P["handle"] + " " + "-" * (W - len(P["handle"]) - 1),
    kv("OS", P["os"]),
    kv("Up Time", uptime(since)),
    kv("IDE", P["ide"]),
    kv("Education", P["education"]),
    "",
    kv("Languages.Programming", P["languages_programming"]),
    kv("Languages.Database", P["languages_database"]),
    kv("Languages.Computer", P["languages_computer"]),
    kv("Languages.Real", P["languages_real"]),
    "",
    head("Contact"),
    kv("Email.Personal", P["email_personal"]),
    kv("Email.Work", P["email_work"]),
    kv("LinkedIn", P["linkedin"]),
    kv("LeetCode", P["leetcode"]),
    kv("GitHub", P["github"]),
    kv("Portfolio", P["portfolio"]),
]

TH = {
 "dark": dict(bg1="#030712",bg2="#0B1220",panel="#0F172A",pop=".45",text="#F8FAFC",muted="#64748B",label="#22D3EE",head="#7C3AED",a1="#7C3AED",a2="#22D3EE",a3="#10B981",grid="#22D3EE",gop=".05"),
 "light": dict(bg1="#FFFFFF",bg2="#EEF6FF",panel="#FFFFFF",pop=".7",text="#0F172A",muted="#64748B",label="#2563EB",head="#6D28D9",a1="#6D28D9",a2="#0891B2",a3="#059669",grid="#2563EB",gop=".06"),
}

def spans(t, T):
    if not t: return ""
    m = re.match(r"^(\. )([^:]+: )(\.+ )(.*)$", t)
    if m:
        return (f'<tspan fill="{T["muted"]}">{E(m[1])}</tspan><tspan fill="{T["label"]}">{E(m[2])}</tspan>'
                f'<tspan fill="{T["muted"]}">{E(m[3])}</tspan><tspan fill="{T["text"]}">{E(m[4])}</tspan>')
    if t.startswith(P["handle"]):
        n = len(P["handle"])
        return f'<tspan fill="{T["a2"]}" font-weight="700">{E(t[:n])}</tspan><tspan fill="{T["muted"]}">{E(t[n:])}</tspan>'
    if t.startswith("- Contact"):
        return f'<tspan fill="{T["head"]}" font-weight="700">- Contact </tspan><tspan fill="{T["muted"]}">{E(t[10:])}</tspan>'
    return E(t)

def build(name):
    T = TH[name]; o = []; a = o.append
    label = (f'{P["handle"].split("@")[0].title()} U, {P["education"]}. Terminal-style profile with an ASCII portrait. '
             f'OS {P["os"]}, IDE {P["ide"]}, programming languages {P["languages_programming"]}, database {P["languages_database"]}, '
             f'{P["languages_computer"]}, spoken languages {P["languages_real"]}.')
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="610" viewBox="0 0 1180 610" role="img" aria-label="{E(label)}">')
    a('<title>Darshan U — Profile</title><desc>Neofetch-style terminal profile: ASCII portrait on the left, system information on the right.</desc><defs>')
    a(f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{T["bg1"]}"/><stop offset="1" stop-color="{T["bg2"]}"/></linearGradient>')
    acc = f'<stop offset="0" stop-color="{T["a1"]}"/><stop offset=".5" stop-color="{T["a2"]}"/><stop offset="1" stop-color="{T["a3"]}"/>'
    a(f'<linearGradient id="gs" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1180" y2="0" spreadMethod="reflect">{acc}<animate attributeName="x1" values="0;1200;0" dur="10s" repeatCount="indefinite"/><animate attributeName="x2" values="1180;2380;1180" dur="10s" repeatCount="indefinite"/></linearGradient>')
    a(f'<linearGradient id="ga" gradientUnits="userSpaceOnUse" x1="50" y1="80" x2="500" y2="560" spreadMethod="reflect">{acc}<animate attributeName="x1" values="50;-150;50" dur="12s" repeatCount="indefinite"/><animate attributeName="x2" values="500;300;500" dur="12s" repeatCount="indefinite"/></linearGradient>')
    a(f'<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{T["grid"]}" stroke-opacity="{T["gop"]}"/></pattern>')
    a(f'<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="{T["grid"]}" fill-opacity=".06"/></pattern>')
    a(f'<radialGradient id="r1" cx=".1" cy=".1" r=".6"><stop offset="0" stop-color="{T["a1"]}" stop-opacity=".25"/><stop offset="1" stop-color="{T["a1"]}" stop-opacity="0"/></radialGradient>')
    a(f'<radialGradient id="r2" cx=".95" cy=".95" r=".6"><stop offset="0" stop-color="{T["a2"]}" stop-opacity=".2"/><stop offset="1" stop-color="{T["a2"]}" stop-opacity="0"/></radialGradient></defs>')
    for f in ("bg", "r1", "r2", "grid"):
        a(f'<rect x=".5" y=".5" width="1179" height="609" rx="24" fill="url(#{f})"/>')
    a(f'<rect x="16" y="56" width="1148" height="538" rx="14" fill="{T["panel"]}" fill-opacity="{T["pop"]}"/><rect x="16" y="56" width="1148" height="538" rx="14" fill="url(#scan)"/>')
    a('<rect x="16.5" y="56.5" width="1147" height="537" rx="14" fill="none" stroke="url(#gs)" stroke-opacity=".55"/>')
    a('<rect x=".5" y=".5" width="1179" height="609" rx="24" fill="none" stroke="url(#gs)" stroke-width="1.5" stroke-opacity=".75"/>')
    for cx, c in ((44, "#FF5F57"), (64, "#FEBC2E"), (84, "#28C840")):
        a(f'<circle cx="{cx}" cy="28" r="6" fill="{c}"/>')
    a(f'<text x="116" y="33" font-family="{MONO}" font-size="13" fill="{T["muted"]}">{E(P["title"])}</text>')
    a(f'<text x="1136" y="33" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="1.5" fill="{T["a3"]}">[ ONLINE ]</text>')
    for i, p in enumerate(PORT):
        if not p.strip(): continue
        y = round(70 + i * 9.2, 1); d = round(.3 + i * .045, 2)
        a(f'<text x="60" y="{y}" opacity="0" xml:space="preserve" font-family="{MONO}" font-size="8.3" textLength="440" lengthAdjust="spacing" fill="url(#ga)"><animate attributeName="opacity" from="0" to="1" begin="{d}s" dur=".3s" fill="freeze"/>{E(p)}</text>')
    ix = round(1128 - W * CW, 1); y0 = 120
    for k, t in enumerate(INFO):
        if not t: continue
        y = round(y0 + k * LH, 1); d = round(1.0 + k * .12, 2)
        a(f'<text x="{ix}" y="{y}" opacity="0" xml:space="preserve" font-family="{MONO}" font-size="{FS}" textLength="{round(len(t)*CW,1)}" lengthAdjust="spacing"><animate attributeName="opacity" from="0" to="1" begin="{d}s" dur=".3s" fill="freeze"/>{spans(t,T)}</text>')
    yy = round(y0 + (len(INFO) + 1) * LH, 1)
    a(f'<text x="{ix}" y="{yy}" font-family="{MONO}" font-size="{FS}" fill="{T["a2"]}">{E(P["handle"])}:~$</text>')
    a(f'<rect x="{round(ix+(len(P["handle"])+3)*CW+4,1)}" y="{yy-13}" width="9" height="16" fill="{T["a2"]}"><animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></rect>')
    a('</svg>')
    return "\n".join(o) + "\n"

if __name__ == "__main__":
    for n in TH:
        (HERE / f"{n}.svg").write_text(build(n), encoding="utf-8", newline="\n")
    print("Up Time:", uptime(since))

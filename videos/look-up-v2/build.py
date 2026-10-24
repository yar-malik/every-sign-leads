"""Generates index.html and compositions/film.html for "Look up" v2 (Every Sign Leads, 01 restyled).

Same script and voice as ../look-up (Shabbar's brief), redrawn in the style of the references in
../../reference-video: gold line art on a dark warm ground, single Arabic words lit in gold, italic
serif lines, a two-column parallel. Run: python3 build.py (from this folder). The Arabic is sliced
from the Tanzil file by word index; never typed here. The English of 3:190 is our own wording.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
W, H = 1080, 1920
DUR = 60.0
GOLD, SILVER, WHITE, INK = "#D9B977", "#C9D1DE", "#F4F1EA", "#07070A"

TANZIL = (HERE.parent.parent / "assets/quran/quran-uthmani.txt").read_text("utf8").splitlines()
V190 = next(l.split("|", 2)[2].strip() for l in TANZIL if l.startswith("3|190|")).split(" ")

LINES = json.loads((HERE / "narration.json").read_text())
T = json.loads((HERE / "timing.json").read_text())
LEN = {k: float(v) for k, v in json.loads((HERE / "assets/vo/durations.json").read_text()).items()}

COL_L, COL_R, FULL = "left:30px;width:480px", "left:570px;width:480px", "left:90px;width:900px"
TEXT = [
    ("hook", "hook", "Look <span class='g'>up.</span>", f"{FULL};top:520px", 0.0, 6.6),
    ("brand", "kicker", "· Every Sign Leads ·", f"{FULL};top:150px", 0.6, T["l15"] - 0.4),
    # The heavens, then the earth, each lit as a single word from 3:190.
    ("a-sama", "ar gold", V190[3], f"{FULL};top:260px", T["l05"] - 0.6, T["l06"] - 0.5),
    ("r-sama", "ref", "the heavens · 3:190", f"{FULL};top:470px", T["l05"] - 0.3, T["l06"] - 0.5),
    ("a-ard", "ar gold", V190[4], f"{FULL};top:260px", T["l06"] + 0.3, T["l10"] - 0.4),
    ("r-ard", "ref", "the earth · 3:190", f"{FULL};top:470px", T["l06"] + 0.6, T["l10"] - 0.4),
    # The parallel: to admire | to reflect.
    ("h-admire", "head gold", "To admire", f"{COL_L};top:320px", T["l10"] + 0.2, T["l12"] - 0.4),
    ("h-reflect", "head silver", "To reflect", f"{COL_R};top:320px", T["l11"] + 0.2, T["l12"] - 0.4),
    # 3:190 card: the English, in our own wording, under the lit Arabic.
    ("e-190", "en", "“In the creation of the heavens and the earth, and the alternation of night and day, "
                    "are signs for people of understanding.”", f"left:120px;width:840px;top:1210px", T["l12"] + 0.6, T["l15"] - 0.4),
    ("r-190", "ref", "Ali ‘Imran 3:190", f"{FULL};top:1420px", T["l13"] + 0.4, T["l15"] - 0.4),
    # Close.
    ("end-q", "endq", "Who <span class='g'>created</span><br>all of this?", f"{FULL};top:600px", T["l19"] - 0.05, DUR),
    ("end-tag", "kicker big", "Discover your Creator", f"{FULL};top:1010px", T["l20"] - 0.6, DUR),
    ("end-brand", "brandline", "Every Sign Leads", f"{FULL};top:1080px", T["l20"] - 0.2, DUR),
    ("end-note", "note", "Verse translation is our own wording.", f"{FULL};top:1720px", T["l19"] + 0.4, DUR),
]
NO_SUB = {"l12", "l13", "l14", "l19", "l20"}  # the verse card and the end card carry these
# Arabic 3:190 lights word by word with the narration: l12 → words 0-4, l13 → 5-7, l14 → 8-10.
VERSE_LIGHT = [(T["l12"], LEN["l12"], range(0, 5)), (T["l13"], LEN["l13"], range(5, 8)), (T["l14"], LEN["l14"], range(8, 11))]

CSS = f"""
@font-face {{ font-family: "Amiri Quran"; src: url("assets/fonts/amiri-quran-arabic-400-normal.woff2") format("woff2"); }}
@font-palette-values --gold {{ font-family: "Amiri Quran"; override-colors: 0 {GOLD}, 1 {GOLD}, 2 {GOLD}, 3 {GOLD}, 4 {GOLD}, 5 {GOLD}, 6 {GOLD}, 7 {GOLD}; }}
#root {{ position: absolute; inset: 0; }}
#film-wrap {{ position: absolute; inset: 0; background: {INK}; }}
#film-cv {{ position: absolute; inset: 0; width: {W}px; height: {H}px; }}
.t {{ position: absolute; text-align: center; opacity: 0; }}
.g {{ color: {GOLD}; }}
.hook {{ font-family: "EB Garamond", serif; font-weight: 500; font-size: 176px; line-height: 1; color: {WHITE}; opacity: 1; }}
.kicker {{ font-family: "EB Garamond", serif; font-size: 30px; letter-spacing: 0.32em; text-transform: uppercase; color: {GOLD}; }}
.kicker.big {{ font-family: "Inter", sans-serif; font-weight: 600; font-size: 40px; letter-spacing: 0.22em; }}
.head {{ font-family: "EB Garamond", serif; font-weight: 500; font-size: 60px; letter-spacing: 0.14em; text-transform: uppercase; }}
.gold {{ color: {GOLD}; }}
.silver {{ color: {SILVER}; }}
.ar {{ direction: rtl; font-family: "Amiri Quran", serif; font-size: 110px; line-height: 1.5; }}
.ar.gold {{ font-palette: --gold; text-shadow: 0 0 34px rgba(217,185,119,0.45); }}
#verse {{ position: absolute; left: 70px; width: 940px; top: 270px; text-align: center; direction: rtl; font-family: "Amiri Quran", serif;
  font-palette: --gold; font-size: 72px; line-height: 1.75; color: {GOLD}; opacity: 0; }}
#verse .vw {{ display: inline-block; opacity: 0.2; }}
.en {{ text-wrap: balance; font-family: "EB Garamond", serif; font-style: italic; font-size: 46px; line-height: 1.24; color: {WHITE}; }}
.ref {{ font-family: "Inter", sans-serif; font-weight: 500; font-size: 28px; letter-spacing: 0.16em; text-transform: uppercase; color: rgba(217,185,119,0.8); }}
.endq {{ font-family: "EB Garamond", serif; font-weight: 500; font-size: 124px; line-height: 1.04; color: {WHITE}; }}
.brandline {{ font-family: "EB Garamond", serif; font-style: italic; font-size: 42px; color: rgba(244,241,234,0.75); }}
.note {{ font-family: "Inter", sans-serif; font-size: 28px; letter-spacing: 0.02em; color: rgba(244,241,234,0.6); }}
.sub {{ position: absolute; left: 110px; width: 860px; top: 1460px; text-align: center; font-family: "EB Garamond", serif;
  font-style: italic; font-weight: 500; font-size: 52px; line-height: 1.22; color: {WHITE}; opacity: 0;
  text-shadow: 0 2px 20px rgba(0,0,0,0.9); text-wrap: balance; }}
"""

DRAW = r"""
const TAU = Math.PI * 2, GOLD = "217,185,119", SILVER = "201,209,222";
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const sstep = (a, b, v) => { const x = clamp((v - a) / (b - a), 0, 1); return x * x * (3 - 2 * x); };
const lerp = (a, b, x) => a + (b - a) * x;
const env = (t, a, b, f) => sstep(a, a + f, t) * (1 - sstep(b - f, b, t));
function rng(seed) { return function () { seed |= 0; seed = (seed + 0x6D2B79F5) | 0; let q = Math.imul(seed ^ (seed >>> 15), 1 | seed); q = (q + Math.imul(q ^ (q >>> 7), 61 | q)) ^ q; return ((q ^ (q >>> 14)) >>> 0) / 4294967296; }; }
function gauss(r) { return Math.sqrt(-2 * Math.log(r() + 1e-9)) * Math.cos(TAU * r()); }
const r = rng(11);
const dust = [], sky = [], deep = [], spiral = [];
for (let i = 0; i < 220; i++) dust.push({ x: r() * 1080, y: r() * 1920, s: 0.6 + r() * 1.5, p: r() * TAU, v: 3 + r() * 8, a: 0.05 + r() * 0.2 });
for (let i = 0; i < 160; i++) sky.push({ x: 60 + r() * 960, y: 220 + r() * 1000, b: Math.pow(r(), 3), p: r() * TAU, d: r() });
for (let i = 0; i < 700; i++) deep.push({ x: (r() - 0.5) * 2.2, y: (r() - 0.5) * 3.4, z: r(), b: Math.pow(r(), 2) });
for (let i = 0; i < 1400; i++) { const arm = i % 2, d = Math.pow(r(), 1.2); spiral.push({ a: arm * Math.PI + d * 8.5 + gauss(r) * 0.16 * (1.2 - d), d, s: r() < 0.06 ? 2.6 : 1.4 }); }

function glow(x, y, rad, col, a) {
  if (a <= 0) return;
  const g = ctx.createRadialGradient(x, y, 0, x, y, rad);
  g.addColorStop(0, "rgba(" + col + "," + (0.38 * a).toFixed(3) + ")"); g.addColorStop(1, "rgba(" + col + ",0)");
  ctx.fillStyle = g; ctx.fillRect(x - rad, y - rad, rad * 2, rad * 2);
}
function stroke(col, a, w) { ctx.strokeStyle = "rgba(" + col + "," + clamp(a, 0, 1).toFixed(3) + ")"; ctx.lineWidth = w; }
function dot(x, y, rad, col, a) { ctx.fillStyle = "rgba(" + col + "," + clamp(a, 0, 1).toFixed(3) + ")"; ctx.beginPath(); ctx.arc(x, y, rad, 0, TAU); ctx.fill(); }
function line(x0, y0, x1, y1) { ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke(); }
// An eight-point line star.
function star8(x, y, R, col, a) {
  if (a <= 0) return;
  glow(x, y, R * 3, col, a);
  stroke(col, a, 2.4); ctx.beginPath();
  for (let i = 0; i < 16; i++) { const q = i / 16 * TAU - Math.PI / 2, rr = i % 2 ? R * 0.38 : R; ctx.lineTo(x + Math.cos(q) * rr, y + Math.sin(q) * rr); }
  ctx.closePath(); ctx.stroke();
  dot(x, y, R * 0.14, col, a);
}
// A cloud outline: a row of arcs over a flat base.
function cloud(x, y, s, a) {
  if (a <= 0) return;
  stroke(GOLD, a, 2); ctx.beginPath(); ctx.moveTo(x - 120 * s, y);
  [[-80, 0, 44], [-20, -24, 60], [50, -6, 48], [100, 8, 30]].forEach(([dx, dy, rr]) => ctx.arc(x + dx * s, y + dy * s, rr * s, Math.PI, 0, false));
  ctx.lineTo(x - 120 * s, y + 38 * s * 0); ctx.stroke();
  line(x - 140 * s, y + 38 * s, x + 140 * s, y + 38 * s);
}
// A line globe: outline, latitude lines and turning meridians.
function globe(x, y, R, a, t) {
  if (a <= 0) return;
  glow(x, y, R * 2.2, GOLD, a * 0.6);
  stroke(GOLD, a * 0.9, 2.4); ctx.beginPath(); ctx.arc(x, y, R, 0, TAU); ctx.stroke();
  stroke(GOLD, a * 0.4, 1.4);
  for (const k of [-0.6, -0.3, 0, 0.3, 0.6]) { const yy = y + k * R, w = Math.sqrt(1 - k * k) * R; ctx.beginPath(); ctx.ellipse(x, yy, w, w * 0.16, 0, 0, TAU); ctx.stroke(); }
  for (let i = 0; i < 4; i++) { const ph = (i / 4 + t * 0.04) % 1, w = Math.abs(Math.cos(ph * Math.PI)) * R; ctx.beginPath(); ctx.ellipse(x, y, Math.max(0.5, w), R, 0, 0, TAU); ctx.stroke(); }
}
function horizon(y, w, a) {
  stroke(GOLD, 0.5 * a, 1.6); line(540 - 420 * w, y, 540 + 420 * w, y);
}
function skyStars(t, a, y0, y1) {
  for (const s of sky) {
    if (s.y < y0 || s.y > y1) continue;
    const tw = 0.6 + 0.4 * Math.sin(t * 1.4 + s.p);
    dot(s.x, s.y, 1.2 + s.b * 2.4, s.d < 0.3 ? SILVER : GOLD, a * (0.25 + 0.75 * s.b) * tw * sstep(s.d * 4, s.d * 4 + 1.5, t + 4));
  }
}

function draw(t) {
  ctx.fillStyle = "#07070A"; ctx.fillRect(0, 0, 1080, 1920);
  const bg = ctx.createRadialGradient(540, 820, 0, 540, 820, 1100);
  bg.addColorStop(0, "rgba(40,32,22,0.55)"); bg.addColorStop(1, "rgba(0,0,0,0)");
  ctx.fillStyle = bg; ctx.fillRect(0, 0, 1080, 1920);
  for (const d of dust) {
    const y = ((d.y - t * d.v) % 1920 + 1920) % 1920, a = d.a * (0.6 + 0.4 * Math.sin(t * 0.8 + d.p));
    ctx.fillStyle = "rgba(" + GOLD + "," + a.toFixed(3) + ")"; ctx.fillRect(d.x, y, d.s, d.s);
  }

  // B1 / B6: the horizon, the stars coming out, a dotted line of sight rising.
  const open = 1 - sstep(6.2, 7.4, t), close = sstep(T.l15 - 0.6, T.l15 + 0.8, t) * (1 - sstep(T.l19 - 0.6, T.l19 + 0.4, t));
  const hz = Math.max(open, close);
  if (hz > 0) {
    const w = t < 10 ? sstep(0, 1.6, t) : sstep(T.l15 - 0.6, T.l15 + 1.4, t);
    horizon(1300, w, hz);
    skyStars(t < 10 ? t : t - T.l15 + 1, hz, 220, 1250);
    const rise = t < 10 ? sstep(1.0, 5.6, t) : sstep(T.l16, T.l16 + 2.4, t);
    for (let i = 0; i < 22; i++) { const u = i / 22; if (u > rise) break; dot(540, 1290 - u * 640, 2.4, GOLD, hz * (1 - u * 0.6)); }
    star8(540, 640, 26, GOLD, hz * sstep(0.85, 1, rise));
  }

  // B2: beyond the clouds, beyond the stars, a galaxy.
  const b2 = env(t, 6.6, T.l06 - 0.2, 0.8);
  if (b2 > 0) {
    const u = t - 6.6;
    [[300, 900, 1.0, 0], [780, 1120, 0.8, 0.4], [520, 1350, 1.2, 0.8]].forEach(([x, y, s, o]) => {
      const fall = sstep(o, 3.4 + o, u);
      cloud(x, y + fall * 900, s * (1 + fall * 0.6), b2 * 0.55 * (1 - fall));
    });
    const travel = 0.05 * u + 0.5 * sstep(1.8, 5, u);
    for (const s of deep) {
      let z = s.z - travel; z = z - Math.floor(z); z = 0.05 + z * 0.95;
      const x = 540 + s.x / z * 420, y = 860 + s.y / z * 420;
      if (x < 0 || x > 1080 || y < 0 || y > 1920) continue;
      const near = 1 - z, a = b2 * clamp(near * 1.3, 0, 1) * (0.3 + 0.7 * s.b) * sstep(1.2, 2.2, u) * (1 - 0.6 * sstep(4.5, 7, u));
      dot(x, y, 0.8 + near * near * 3, GOLD, a);
    }
    const ga = sstep(4.2, 6.4, u) * b2;
    if (ga > 0) {
      const sc = lerp(0.25, 1, sstep(4.2, 9.5, u));
      ctx.save(); ctx.translate(540, 860); ctx.rotate(-0.4); ctx.scale(sc, sc * 0.62);
      for (const q of spiral) { const a = q.a + u * 0.05 * (1.5 - q.d); dot(Math.cos(a) * q.d * 420, Math.sin(a) * q.d * 420, q.s, q.d < 0.15 ? "255,236,205" : GOLD, ga * (0.35 + 0.5 * (1 - q.d))); }
      ctx.restore();
      glow(540, 860, 160 * sc, GOLD, ga * 1.6);
    }
  }

  // B3: here we are — a line globe that pulls back until it is small; a pulse at "Alive."
  const b3 = env(t, T.l06 - 0.4, T.l10 - 0.2, 0.8);
  if (b3 > 0) {
    const k = sstep(T.l07 - 0.4, T.l08 + 0.4, t);
    const R = lerp(300, 70, k);
    skyStars(t, b3 * k * 0.8, 200, 1700);
    globe(540, 860, R, b3, t);
    const pulse = env(t, T.l08, T.l09 + LEN.l09 + 0.6, 0.5);
    if (pulse > 0) { dot(540, 860, 6, "255,240,210", b3 * pulse); stroke(GOLD, b3 * pulse * (1 - ((t * 0.7) % 1)), 1.6); ctx.beginPath(); ctx.arc(540, 860, 12 + ((t * 0.7) % 1) * 110, 0, TAU); ctx.stroke(); }
  }

  // B4: to admire | to reflect — the same star, then its reflection in still water.
  const b4 = env(t, T.l10 - 0.2, T.l12 - 0.2, 0.8);
  if (b4 > 0) {
    const div = sstep(T.l10, T.l10 + 1.4, t);
    stroke(GOLD, 0.28 * b4, 1.5); line(540, 440, 540, lerp(440, 1300, div));
    star8(270, 760, 50, GOLD, b4 * sstep(T.l10 + 0.3, T.l10 + 1.4, t));
    stroke(GOLD, 0.4 * b4, 1.5); line(110, 1000, 430, 1000);
    const rf = b4 * sstep(T.l11, T.l11 + 1.2, t);
    star8(810, 760, 50, SILVER, rf);
    stroke(SILVER, 0.5 * rf, 1.5); line(650, 1000, 970, 1000);
    // Its reflection: the same star mirrored under the waterline, softer, with ripples.
    star8(810 + Math.sin(t * 2) * 3, 1240, 50, SILVER, rf * 0.4);
    for (let i = 0; i < 4; i++) { stroke(SILVER, rf * 0.25, 1.2); const yy = 1170 + i * 44 + Math.sin(t * 1.6 + i) * 4; line(700 + i * 12, yy, 920 - i * 12, yy); }
  }

  // B5: 3:190 — a disc turning between night and day.
  const b5 = env(t, T.l12 - 0.3, T.l15 - 0.2, 0.9);
  if (b5 > 0) {
    const cx = 540, cy = 900, R = 170, ang = (t - T.l12) * 0.5;
    glow(cx, cy, R * 2, GOLD, b5 * 0.5);
    ctx.save(); ctx.beginPath(); ctx.arc(cx, cy, R, 0, TAU); ctx.clip();
    ctx.translate(cx, cy); ctx.rotate(ang);
    ctx.fillStyle = "rgba(" + GOLD + "," + (0.22 * b5).toFixed(3) + ")"; ctx.fillRect(0, -R, R, R * 2);
    ctx.restore();
    stroke(GOLD, b5 * 0.85, 2.4); ctx.beginPath(); ctx.arc(cx, cy, R, 0, TAU); ctx.stroke();
    stroke(GOLD, b5 * 0.6, 1.6); line(cx - Math.sin(ang) * R, cy + Math.cos(ang) * R, cx + Math.sin(ang) * R, cy - Math.cos(ang) * R);
    for (let i = 0; i < 36; i++) { const q = i / 36 * TAU; stroke(GOLD, b5 * 0.3, 1.2); line(cx + Math.cos(q) * (R + 18), cy + Math.sin(q) * (R + 18), cx + Math.cos(q) * (R + 30), cy + Math.sin(q) * (R + 30)); }
  }

  const vg = ctx.createRadialGradient(540, 900, 520, 540, 960, 1300);
  vg.addColorStop(0, "rgba(0,0,0,0)"); vg.addColorStop(1, "rgba(0,0,0,0.65)");
  ctx.fillStyle = vg; ctx.fillRect(0, 0, 1080, 1920);
  const fade = sstep(DUR - 1.0, DUR - 0.05, t);
  if (fade > 0) { ctx.fillStyle = "rgba(0,0,0," + fade.toFixed(3) + ")"; ctx.fillRect(0, 0, 1080, 1920); }
}
"""


def film():
    body, tw = [], []
    for tid, cls, html, pos, tin, tout in TEXT:
        body.append(f'      <div id="{tid}" class="t {cls}" style="{pos}">{html}</div>')
        if tin > 0:
            tw.append(f'      tl.fromTo("#{tid}", {{ opacity: 0, filter: "blur(8px)", y: 10 }}, {{ opacity: 1, filter: "blur(0px)", y: 0, duration: 0.7, ease: "power2.out" }}, {tin:.2f});')
        else:
            tw.append(f'      tl.fromTo("#{tid}", {{ scale: 1.06 }}, {{ scale: 1, duration: {tout - 0.6:.2f}, ease: "power1.out" }}, 0);')
        if tout < DUR:
            tw.append(f'      tl.to("#{tid}", {{ opacity: 0, filter: "blur(6px)", duration: 0.45, ease: "power1.in" }}, {tout - 0.45:.2f});')
    # The verse: dim words appear with l12, then each lights as it is spoken.
    words = "".join(f'<span class="vw" id="vw{i}">{w}</span> ' for i, w in enumerate(V190))
    body.append(f'      <div id="verse">{words.strip()}</div>')
    tw.append(f'      tl.fromTo("#verse", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.8, ease: "power1.out" }}, {T["l12"] - 0.4:.2f});')
    tw.append(f'      tl.to("#verse", {{ opacity: 0, filter: "blur(6px)", duration: 0.45, ease: "power1.in" }}, {T["l15"] - 0.85:.2f});')
    for start, length, idx in VERSE_LIGHT:
        n = len(idx)
        for j, i in enumerate(idx):
            tw.append(f'      tl.to("#vw{i}", {{ opacity: 1, textShadow: "0 0 30px rgba(217,185,119,0.6)", duration: 0.4, ease: "power2.out" }}, {start + length * j / n:.2f});')
    ids = [l["id"] for l in LINES]
    for i, l in enumerate(LINES):
        lid = l["id"]
        if lid in NO_SUB:
            continue
        nxt = T[ids[i + 1]] if i + 1 < len(ids) else DUR
        out = min(nxt - 0.15, T[lid] + LEN[lid] + 0.7)
        body.append(f'      <div id="sub-{lid}" class="sub">{l["text"]}</div>')
        tw.append(f'      tl.fromTo("#sub-{lid}", {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }}, {max(0, T[lid] - 0.1):.2f});')
        tw.append(f'      tl.to("#sub-{lid}", {{ opacity: 0, duration: 0.3, ease: "power1.in" }}, {out - 0.3:.2f});')
    consts = "const T = " + json.dumps(T) + ", LEN = " + json.dumps(LEN) + f", DUR = {DUR};"
    return f"""<template>
  <style>
{CSS}
  </style>
  <div id="root" data-composition-id="film" data-width="{W}" data-height="{H}" data-duration="{DUR}">
    <div id="film-wrap" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0">
      <canvas id="film-cv" width="{W}" height="{H}"></canvas>
{chr(10).join(body)}
    </div>
  </div>
  <script>
    (function () {{
      const cv = document.getElementById("film-cv"), ctx = cv.getContext("2d");
      {consts}
{DRAW}
      const tl = gsap.timeline({{ paused: true }});
      const clock = {{ t: 0 }};
      tl.to(clock, {{ t: {DUR}, duration: {DUR}, ease: "none", onUpdate: () => draw(clock.t) }}, 0);
{chr(10).join(tw)}
      draw(0);
      window.__timelines["film"] = tl;
    }})();
  </script>
</template>
"""


def index():
    return f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: {INK}; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
      <div id="film" class="clip" data-composition-id="film" data-composition-src="compositions/film.html" data-start="0" data-duration="{DUR}" data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>
      <audio id="voice" class="clip" src="assets/audio/vo.wav" data-start="0" data-duration="{DUR}" data-track-index="2" data-volume="1"></audio>
      <audio id="bed" class="clip" src="assets/audio/bed.wav" data-start="0" data-duration="{DUR}" data-track-index="3" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


if __name__ == "__main__":
    (HERE / "compositions").mkdir(exist_ok=True)
    (HERE / "compositions/film.html").write_text(film())
    (HERE / "index.html").write_text(index())
    print("built", DUR, "s; 3:190 words:", len(V190))

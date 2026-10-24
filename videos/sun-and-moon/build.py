"""Generates index.html and compositions/film.html for "Sun and Moon" (Every Sign Leads, 02).

Run: python3 build.py   (from this folder, after scripts/mix.sh). One canvas draws the line art
from timeline time; HTML text sits on top. Style follows the two references in
../../reference-video: two subjects side by side, single Arabic words lit in gold, thin line
drawings, an italic serif line and the verse reference under each. The Arabic is sliced from the
Tanzil file in ../../assets/quran by word index; never typed here. The English renderings are our
own (marked on the end card), not Sahih International.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
W, H = 1080, 1920
GOLD, SILVER, WHITE, INK = "#D9B977", "#C9D1DE", "#F4F1EA", "#07070A"

TANZIL = (HERE.parent.parent / "assets/quran/quran-uthmani.txt").read_text("utf8").splitlines()


def ayah(s, a, lo=0, hi=None):
    """Words lo..hi (inclusive) of surah s, ayah a, from Tanzil."""
    text = next(l.split("|", 2)[2].strip() for l in TANZIL if l.startswith(f"{s}|{a}|"))
    words = text.split(" ")
    return " ".join(words[lo:(len(words) if hi is None else hi + 1)])


LINES = json.loads((HERE / "narration.json").read_text())
T = json.loads((HERE / "timing.json").read_text())
LEN = {k: float(v) for k, v in json.loads((HERE / "assets/vo/durations.json").read_text()).items()}
DUR = round(T["l15"] + LEN["l15"] + 3.0, 1)

# ---- On-screen text: (id, class, html, top px, in, out) ------------------------------------
COL_L, COL_R, FULL = "left:30px;width:480px", "left:570px;width:480px", "left:90px;width:900px"
TEXT = [
    ("brand", "kicker", "· Every Sign Leads ·", f"{FULL};top:150px", 0.2, T["l14"] - 0.4),
    ("h-sun", "head gold", "The Sun", f"{COL_L};top:300px", 0.7, T["l07"] - 0.3),
    ("h-moon", "head silver", "The Moon", f"{COL_R};top:300px", 1.0, T["l07"] - 0.3),
    # Nuh 71:16 — the moon a light, the sun a lamp.
    ("a-nur", "ar silver", ayah(71, 16, 3, 3), f"{COL_R};top:400px", T["l03"] + 1.4, T["l05"] + 0.3),
    ("e-nur", "en", "“a light”", f"{COL_R};top:1090px", T["l03"] + 1.6, T["l05"] + 0.3),
    ("r-nur", "ref", "Nuh 71:16", f"{COL_R};top:1160px", T["l03"] + 1.9, T["l05"] + 0.3),
    ("a-siraj", "ar gold", ayah(71, 16, 6, 6), f"{COL_L};top:400px", T["l04"] - 0.1, T["l05"] + 0.3),
    ("e-siraj", "en", "“a lamp”", f"{COL_L};top:1090px", T["l04"] + 0.1, T["l05"] + 0.3),
    ("r-siraj", "ref", "Nuh 71:16", f"{COL_L};top:1160px", T["l04"] + 0.3, T["l05"] + 0.3),
    # Ya-Sin 36:38-39 — the sun runs; the moon's stations.
    ("a-tajri", "ar gold", ayah(36, 38, 1, 1), f"{COL_L};top:400px", T["l05"] + 0.5, T["l07"] - 0.3),
    ("e-tajri", "en", "“runs to a resting place of its own”", f"{COL_L};top:1090px", T["l05"] + 0.7, T["l07"] - 0.3),
    ("r-tajri", "ref", "Ya-Sin 36:38", f"{COL_L};top:1196px", T["l05"] + 1.0, T["l07"] - 0.3),
    ("a-manazil", "ar silver", ayah(36, 39, 2, 2), f"{COL_R};top:400px", T["l06"] + 0.3, T["l07"] - 0.3),
    ("e-manazil", "en", "“We measured out its stations”", f"{COL_R};top:1090px", T["l06"] + 0.6, T["l07"] - 0.3),
    ("r-manazil", "ref", "Ya-Sin 36:39", f"{COL_R};top:1196px", T["l06"] + 0.9, T["l07"] - 0.3),
    # Ya-Sin 36:40 — neither overtakes; each swims in an orbit.
    ("a-overtake", "ar gold mid", ayah(36, 40, 0, 6), f"{FULL};top:300px", T["l07"] + 0.1, T["l08"] - 0.2),
    ("a-falak", "ar gold big", ayah(36, 40, 12, 15), f"{FULL};top:290px", T["l08"] + 0.1, T["l09"] - 0.3),
    ("r-falak", "ref", "Ya-Sin 36:40", f"{FULL};top:1200px", T["l07"] + 0.6, T["l09"] - 0.3),
    # Ar-Rahman 55:5 — by precise measure.
    ("a-husban", "ar gold big", ayah(55, 5), f"{FULL};top:290px", T["l10"] + 0.2, T["l11"] - 0.3),
    ("r-husban", "ref", "Ar-Rahman 55:5", f"{FULL};top:1270px", T["l10"] + 0.6, T["l11"] - 0.3),
    # Fussilat 41:37 — of His signs ... bow to the One who created them.
    ("a-ayat", "ar gold mid", ayah(41, 37, 0, 5), f"{FULL};top:300px", T["l11"] + 0.2, T["l14"] - 0.4),
    ("a-sujud", "ar gold mid", ayah(41, 37, 7, 15), f"{FULL};top:960px", T["l12"] + 0.2, T["l14"] - 0.4),
    ("r-sujud", "ref", "Fussilat 41:37", f"{FULL};top:1290px", T["l12"] + 0.8, T["l14"] - 0.4),
    # End card.
    ("end-q", "endq", "Every sign leads<br>somewhere.", f"{FULL};top:640px", T["l14"] - 0.05, DUR),
    ("end-tag", "kicker big", "Discover your Creator", f"{FULL};top:1060px", T["l15"] - 0.05, DUR),
    ("end-brand", "brandline", "Every Sign Leads", f"{FULL};top:1130px", T["l15"] + 0.8, DUR),
    ("end-note", "note", "Verse translations are our own wording.", f"{FULL};top:1720px", T["l15"] + 1.2, DUR),
]
NO_SUB = {"l14", "l15"}  # the end card carries these

CSS = f"""
@font-face {{ font-family: "Amiri Quran"; src: url("assets/fonts/amiri-quran-arabic-400-normal.woff2") format("woff2"); }}
@font-palette-values --gold {{ font-family: "Amiri Quran"; override-colors: 0 {GOLD}, 1 {GOLD}, 2 {GOLD}, 3 {GOLD}, 4 {GOLD}, 5 {GOLD}, 6 {GOLD}, 7 {GOLD}; }}
@font-palette-values --silver {{ font-family: "Amiri Quran"; override-colors: 0 {SILVER}, 1 {SILVER}, 2 {SILVER}, 3 {SILVER}, 4 {SILVER}, 5 {SILVER}, 6 {SILVER}, 7 {SILVER}; }}
#root {{ position: absolute; inset: 0; }}
#film-wrap {{ position: absolute; inset: 0; background: {INK}; }}
#film-cv {{ position: absolute; inset: 0; width: {W}px; height: {H}px; }}
.t {{ position: absolute; text-align: center; opacity: 0; }}
.kicker {{ font-family: "EB Garamond", serif; font-size: 30px; letter-spacing: 0.32em; text-transform: uppercase; color: {GOLD}; opacity: 0; }}
.kicker.big {{ font-family: "Inter", sans-serif; font-weight: 600; font-size: 40px; letter-spacing: 0.22em; }}
.head {{ font-family: "EB Garamond", serif; font-weight: 500; font-size: 64px; letter-spacing: 0.14em; text-transform: uppercase; }}
.gold {{ color: {GOLD}; }}
.silver {{ color: {SILVER}; }}
.ar {{ direction: rtl; font-family: "Amiri Quran", serif; font-size: 92px; line-height: 1.5; }}
.ar.gold {{ font-palette: --gold; text-shadow: 0 0 34px rgba(217,185,119,0.45); }}
.ar.silver {{ font-palette: --silver; text-shadow: 0 0 34px rgba(201,209,222,0.4); }}
.ar.mid {{ font-size: 64px; line-height: 1.7; }}
.ar.big {{ font-size: 100px; }}
.en {{ text-wrap: balance; font-family: "EB Garamond", serif; font-style: italic; font-size: 44px; line-height: 1.2; color: {WHITE}; }}
.ref {{ font-family: "Inter", sans-serif; font-weight: 500; font-size: 28px; letter-spacing: 0.16em; text-transform: uppercase; color: rgba(217,185,119,0.75); }}
.endq {{ font-family: "EB Garamond", serif; font-weight: 500; font-size: 112px; line-height: 1.06; color: {WHITE}; }}
.brandline {{ font-family: "EB Garamond", serif; font-style: italic; font-size: 42px; color: rgba(244,241,234,0.75); }}
.note {{ font-family: "Inter", sans-serif; font-size: 28px; letter-spacing: 0.02em; color: rgba(244,241,234,0.6); }}
.sub {{ position: absolute; left: 110px; width: 860px; top: 1440px; text-align: center; font-family: "EB Garamond", serif;
  font-style: italic; font-weight: 500; font-size: 50px; line-height: 1.22; color: {WHITE}; opacity: 0;
  text-shadow: 0 2px 20px rgba(0,0,0,0.9); text-wrap: balance; }}
"""

# ---- Line art, drawn from timeline time ---------------------------------------------------
DRAW = r"""
const TAU = Math.PI * 2, GOLD = "217,185,119", SILVER = "201,209,222";
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const sstep = (a, b, v) => { const x = clamp((v - a) / (b - a), 0, 1); return x * x * (3 - 2 * x); };
const lerp = (a, b, x) => a + (b - a) * x;
const env = (t, a, b, f) => sstep(a, a + f, t) * (1 - sstep(b - f, b, t));
function rng(seed) { return function () { seed |= 0; seed = (seed + 0x6D2B79F5) | 0; let q = Math.imul(seed ^ (seed >>> 15), 1 | seed); q = (q + Math.imul(q ^ (q >>> 7), 61 | q)) ^ q; return ((q ^ (q >>> 14)) >>> 0) / 4294967296; }; }
const r = rng(7), dust = [];
for (let i = 0; i < 260; i++) dust.push({ x: r() * 1080, y: r() * 1920, s: 0.6 + r() * 1.6, p: r() * TAU, v: 4 + r() * 10, a: 0.05 + r() * 0.25 });

function glow(x, y, rad, col, a) {
  if (a <= 0) return;
  const g = ctx.createRadialGradient(x, y, 0, x, y, rad);
  g.addColorStop(0, "rgba(" + col + "," + (0.38 * a).toFixed(3) + ")"); g.addColorStop(1, "rgba(" + col + ",0)");
  ctx.fillStyle = g; ctx.fillRect(x - rad, y - rad, rad * 2, rad * 2);
}
function stroke(col, a, w) { ctx.strokeStyle = "rgba(" + col + "," + clamp(a, 0, 1).toFixed(3) + ")"; ctx.lineWidth = w; }
// The sun: a line circle, a filled core and short rays that turn slowly.
function sun(x, y, R, a, t) {
  if (a <= 0) return;
  glow(x, y, R * 4, GOLD, a);
  stroke(GOLD, a, 3); ctx.beginPath(); ctx.arc(x, y, R, 0, TAU); ctx.stroke();
  ctx.fillStyle = "rgba(" + GOLD + "," + (0.85 * a).toFixed(3) + ")"; ctx.beginPath(); ctx.arc(x, y, R * 0.42, 0, TAU); ctx.fill();
  stroke(GOLD, a * 0.8, 2.4);
  for (let i = 0; i < 12; i++) {
    const q = i / 12 * TAU + t * 0.08, r0 = R * 1.28, r1 = R * (i % 2 ? 1.55 : 1.75);
    ctx.beginPath(); ctx.moveTo(x + Math.cos(q) * r0, y + Math.sin(q) * r0); ctx.lineTo(x + Math.cos(q) * r1, y + Math.sin(q) * r1); ctx.stroke();
  }
}
// The moon at phase p (0 new, 0.5 full, 1 new again): lit part filled, the rest a faint outline.
function moon(x, y, R, p, a) {
  if (a <= 0) return;
  glow(x, y, R * 3.4, SILVER, a * (0.35 + 0.65 * Math.sin(Math.PI * p)));
  stroke(SILVER, a * 0.35, 2); ctx.beginPath(); ctx.arc(x, y, R, 0, TAU); ctx.stroke();
  const k = Math.cos(p * TAU), wax = p < 0.5;
  ctx.save(); ctx.translate(x, y); if (!wax) ctx.scale(-1, 1);
  ctx.beginPath(); ctx.arc(0, 0, R, -Math.PI / 2, Math.PI / 2, false);
  ctx.ellipse(0, 0, Math.max(0.5, R * Math.abs(k)), R, 0, Math.PI / 2, -Math.PI / 2, k > 0);
  ctx.closePath();
  ctx.fillStyle = "rgba(" + SILVER + "," + (0.92 * a).toFixed(3) + ")"; ctx.fill();
  stroke("255,255,255", a * 0.6, 2); ctx.stroke();
  ctx.restore();
}
function dots(x0, y0, x1, y1, n, col, a, upto) {
  for (let i = 0; i <= n; i++) {
    const u = i / n; if (u > upto) break;
    ctx.fillStyle = "rgba(" + col + "," + a.toFixed(3) + ")";
    ctx.beginPath(); ctx.arc(lerp(x0, x1, u), lerp(y0, y1, u), 2.4, 0, TAU); ctx.fill();
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

  // Beats 1-3: two columns, the sun left and the moon right.
  const cols = env(t, 0.3, T.l07 + 0.2, 0.9);
  if (cols > 0) {
    const div = sstep(0.4, 2.2, t);
    stroke(GOLD, 0.28 * cols, 1.5); ctx.beginPath(); ctx.moveTo(540, 400); ctx.lineTo(540, lerp(400, 1240, div)); ctx.stroke();
    // The sun sits high, then runs along its arc to a resting mark (36:38).
    const run = sstep(T.l05 + 0.4, T.l05 + 5.5, t), cx = 270, cy = 960, AR = 160;
    const arc = sstep(T.l05, T.l05 + 1.2, t) * cols;
    if (arc > 0) {
      for (let i = 0; i <= 30; i++) {
        const q = -Math.PI / 2 + i / 30 * Math.PI / 2;
        ctx.fillStyle = "rgba(" + GOLD + "," + (0.5 * arc * (i / 30 <= run ? 1 : 0.35)).toFixed(3) + ")";
        ctx.beginPath(); ctx.arc(cx + Math.cos(q) * AR, cy + Math.sin(q) * AR, 2.4, 0, TAU); ctx.fill();
      }
      stroke(GOLD, 0.5 * arc, 2); ctx.beginPath(); ctx.moveTo(cx + AR - 34, cy); ctx.lineTo(cx + AR + 34, cy); ctx.stroke();
    }
    const q = -Math.PI / 2 + run * Math.PI / 2;
    sun(cx + Math.cos(q) * AR, cy + Math.sin(q) * AR, 46, cols * sstep(0.6, 2.4, t), t);
    // The moon waxes to full, then wanes to a thin old crescent through its stations (36:39).
    const st = sstep(T.l06 + 0.2, T.l06 + LEN.l06 + 0.4, t);
    const p = lerp(0.16, 0.95, st);
    moon(810, 800, 64, p, cols * sstep(1.0, 2.8, t));
    const sa = sstep(T.l06, T.l06 + 0.8, t) * cols;
    if (sa > 0) for (let i = 0; i < 8; i++) {
      const lit = st * 8 > i ? 1 : 0.3, x = 690 + i * 34;
      moon(x, 980, 11, lerp(0.16, 0.95, i / 7), sa * lit);
    }
  }

  // Beat 4: neither overtakes — two orbits, each body on its own (36:40).
  const orb = env(t, T.l07 - 0.2, T.l09 + 0.2, 0.9);
  if (orb > 0) {
    const draw = sstep(T.l07 - 0.2, T.l07 + 1.6, t);
    ctx.save(); ctx.translate(540, 820); ctx.rotate(-0.14);
    stroke(GOLD, 0.55 * orb, 2); ctx.beginPath(); ctx.ellipse(0, 0, 380, 130, 0, 0, TAU * draw); ctx.stroke();
    stroke(SILVER, 0.5 * orb, 2); ctx.beginPath(); ctx.ellipse(0, 0, 250, 84, 0, Math.PI, Math.PI + TAU * draw); ctx.stroke();
    const qs = 0.9 + (t - T.l07) * 0.42, qm = 2.6 + (t - T.l07) * 0.95;
    sun(Math.cos(qs) * 380, Math.sin(qs) * 130, 26, orb, t);
    moon(Math.cos(qm) * 250, Math.sin(qm) * 84, 19, 0.38, orb);
    ctx.restore();
  }

  // Beat 5: by precise measure — a dial; the sun and moon step from mark to mark (55:5).
  const dial = env(t, T.l09 - 0.2, T.l11 + 0.2, 0.9);
  if (dial > 0) {
    const cx = 540, cy = 830;
    for (let i = 0; i < 60; i++) {
      const q = i / 60 * TAU - Math.PI / 2, long = i % 5 === 0;
      stroke(GOLD, (long ? 0.6 : 0.3) * dial, long ? 2.4 : 1.4);
      ctx.beginPath(); ctx.moveTo(cx + Math.cos(q) * 330, cy + Math.sin(q) * 330); ctx.lineTo(cx + Math.cos(q) * (long ? 300 : 314), cy + Math.sin(q) * (long ? 300 : 314)); ctx.stroke();
    }
    for (let i = 0; i < 30; i++) {
      const q = i / 30 * TAU - Math.PI / 2;
      stroke(SILVER, 0.35 * dial, 1.6);
      ctx.beginPath(); ctx.moveTo(cx + Math.cos(q) * 214, cy + Math.sin(q) * 214); ctx.lineTo(cx + Math.cos(q) * 200, cy + Math.sin(q) * 200); ctx.stroke();
    }
    // Stepped motion: rest on a mark, then a quick ease to the next.
    const step = (x) => Math.floor(x) + sstep(0.7, 1, x - Math.floor(x));
    const u = t - T.l09;
    const qs = step(u * 1.6) / 60 * TAU - Math.PI / 2, qm = step(u * 1.25) / 30 * TAU - Math.PI / 2;
    sun(cx + Math.cos(qs) * 266, cy + Math.sin(qs) * 266, 22, dial, t);
    moon(cx + Math.cos(qm) * 166, cy + Math.sin(qm) * 166, 18, 0.3, dial);
    stroke(GOLD, 0.3 * dial, 1); ctx.beginPath(); ctx.arc(cx, cy, 5, 0, TAU); ctx.stroke();
  }

  // Beat 6: of His signs — then the sun and moon lower and dim: bow not to them (41:37).
  const sign = env(t, T.l11 - 0.2, T.l14 + 0.1, 0.9);
  if (sign > 0) {
    const bow = sstep(T.l12 + 0.3, T.l12 + 2.6, t);
    const ar = sstep(T.l11 - 0.2, T.l11 + 1.6, t);
    stroke(GOLD, 0.25 * sign * ar, 1.5); ctx.beginPath(); ctx.moveTo(540 - 340 * ar, 900); ctx.lineTo(540 + 340 * ar, 900); ctx.stroke();
    sun(400, lerp(720, 790, bow), 52, sign * lerp(1, 0.28, bow), t);
    moon(680, lerp(720, 790, bow), 44, 0.2, sign * lerp(1, 0.28, bow));
  }

  // Beat 7: end card — the horizon line, the two lights small on it.
  const end = sstep(T.l14 - 0.3, T.l14 + 1.2, t) * (1 - sstep(DUR - 1.4, DUR - 0.1, t));
  if (end > 0) {
    const w = sstep(T.l14, T.l14 + 2.2, t);
    stroke(GOLD, 0.45 * end, 1.5); ctx.beginPath(); ctx.moveTo(540 - 260 * w, 980); ctx.lineTo(540 + 260 * w, 980); ctx.stroke();
    sun(540 - 260 * w, 980, 12, end * w, t);
    moon(540 + 260 * w, 980, 11, 0.2, end * w);
  }

  const vg = ctx.createRadialGradient(540, 900, 520, 540, 960, 1300);
  vg.addColorStop(0, "rgba(0,0,0,0)"); vg.addColorStop(1, "rgba(0,0,0,0.65)");
  ctx.fillStyle = vg; ctx.fillRect(0, 0, 1080, 1920);
  const fade = sstep(DUR - 1.2, DUR - 0.1, t);
  if (fade > 0) { ctx.fillStyle = "rgba(0,0,0," + fade.toFixed(3) + ")"; ctx.fillRect(0, 0, 1080, 1920); }
}
"""


def film():
    body, tw = [], []
    for tid, cls, html, pos, tin, tout in TEXT:
        body.append(f'      <div id="{tid}" class="t {cls}" style="{pos}">{html}</div>')
        tw.append(f'      tl.fromTo("#{tid}", {{ opacity: 0, filter: "blur(8px)", y: 10 }}, {{ opacity: 1, filter: "blur(0px)", y: 0, duration: 0.7, ease: "power2.out" }}, {tin:.2f});')
        if tout < DUR:
            tw.append(f'      tl.to("#{tid}", {{ opacity: 0, filter: "blur(6px)", duration: 0.45, ease: "power1.in" }}, {tout - 0.45:.2f});')
    ids = [l["id"] for l in LINES]
    for i, l in enumerate(LINES):
        if l["id"] in NO_SUB:
            continue
        lid = l["id"]
        nxt = T[ids[i + 1]] if i + 1 < len(ids) else DUR
        out = min(nxt - 0.15, T[lid] + LEN[lid] + 0.7)
        body.append(f'      <div id="sub-{lid}" class="sub">{l["text"]}</div>')
        tw.append(f'      tl.fromTo("#sub-{lid}", {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }}, {T[lid] - 0.1:.2f});')
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
    print("built", DUR, "s;", ayah(36, 40, 12, 15))

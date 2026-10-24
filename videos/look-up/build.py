"""Generates index.html and compositions/*.html for "Look up" (Every Sign Leads, pilot 01).

Run: python3 build.py   (from this folder). Every picture is drawn on canvas from timeline time
with seeded noise, so renders are identical. The Arabic is read verbatim from the Tanzil file in
../../assets/quran; never typed here. Narration starts come from timing.json (see scripts/mix.sh).
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
W, H = 1080, 1920
DUR = 60.0
GOLD, WHITE, NIGHT = "#D9B977", "#F4F1EA", "#04060D"

TANZIL = HERE.parent.parent / "assets/quran/quran-uthmani.txt"
ARABIC = next(l.split("|", 2)[2].strip() for l in TANZIL.read_text("utf8").splitlines() if l.startswith("3|190|"))
# Sahih International, as specified in the brief (licence: see README).
TRANSLATION = ("“Indeed, in the creation of the heavens and the earth and the alternation "
               "of the night and the day are signs for those of understanding.”")
REFERENCE = "Surah Ali ‘Imran 3:190 · Sahih International"

NARRATION = {l["id"]: l["text"] for l in json.loads((HERE / "narration.json").read_text())}
TIMING = json.loads((HERE / "timing.json").read_text())
LEN = {k: float(v) for k, v in json.loads((HERE / "assets/vo/durations.json").read_text()).items()}

# Scene slots: (id, start, duration). Each scene fades in over the previous one for 0.8 s.
SCENES = [("s1", 0.0, 7.4), ("s2", 6.6, 10.6), ("s3", 16.4, 10.2), ("s4", 25.8, 9.8),
          ("s5", 34.8, 14.0), ("s6", 48.0, 12.0)]
FADE = 0.8

FONTS = """
@font-face { font-family: "Amiri Quran"; src: url("assets/fonts/amiri-quran-arabic-400-normal.woff2") format("woff2"); }
@font-palette-values --gold { font-family: "Amiri Quran"; override-colors: 0 #D9B977, 1 #D9B977, 2 #D9B977, 3 #D9B977, 4 #D9B977, 5 #D9B977, 6 #D9B977, 7 #D9B977; }
"""

# Drawing helpers shared by every scene (seeded RNG, value noise, stars, Milky Way, Earth).
LIB = r"""
const TAU = Math.PI * 2;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const sstep = (a, b, v) => { const x = clamp((v - a) / (b - a), 0, 1); return x * x * (3 - 2 * x); };
const lerp = (a, b, x) => a + (b - a) * x;
const easeOut = (x) => 1 - Math.pow(1 - clamp(x, 0, 1), 3);
const easeInOut = (x) => { x = clamp(x, 0, 1); return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
function rng(seed) { return function () { seed |= 0; seed = (seed + 0x6D2B79F5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
function gauss(r) { return Math.sqrt(-2 * Math.log(r() + 1e-9)) * Math.cos(TAU * r()); }

// 3D value noise on a hashed lattice.
function hash3(x, y, z) { let h = (x * 374761393 + y * 668265263 + z * 2147483647) | 0; h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967296; }
function noise3(x, y, z) {
  const xi = Math.floor(x), yi = Math.floor(y), zi = Math.floor(z);
  const xf = x - xi, yf = y - yi, zf = z - zi;
  const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf), w = zf * zf * (3 - 2 * zf);
  const c = (a, b, d) => hash3(xi + a, yi + b, zi + d);
  const x00 = lerp(c(0, 0, 0), c(1, 0, 0), u), x10 = lerp(c(0, 1, 0), c(1, 1, 0), u);
  const x01 = lerp(c(0, 0, 1), c(1, 0, 1), u), x11 = lerp(c(0, 1, 1), c(1, 1, 1), u);
  return lerp(lerp(x00, x10, v), lerp(x01, x11, v), w);
}
function fbm3(x, y, z, oct) { let s = 0, a = 0.5, f = 1, n = 0; for (let i = 0; i < oct; i++) { s += a * noise3(x * f, y * f, z * f); n += a; a *= 0.5; f *= 2.03; } return s / n; }
function fbm1(x, seed, oct) { return fbm3(x, seed * 7.13, seed * 3.7, oct); }

function makeStars(seed, n, w, h) {
  const r = rng(seed), s = [];
  for (let i = 0; i < n; i++) s.push({ x: r() * w, y: r() * h, b: Math.pow(r(), 4), p: r() * TAU, k: 0.5 + r() * 1.6, c: r() });
  return s;
}
function starColor(c) { return c < 0.12 ? "255,214,170" : c < 0.3 ? "185,205,255" : "255,255,255"; }
function drawStars(ctx, stars, t, ox, oy, sc, alpha, cx, cy) {
  cx = cx === undefined ? 540 : cx; cy = cy === undefined ? 960 : cy;
  for (const s of stars) {
    const x = cx + (s.x + ox - cx) * sc, y = cy + (s.y + oy - cy) * sc;
    if (x < -10 || x > 1090 || y < -10 || y > 1930) continue;
    const tw = 0.7 + 0.3 * Math.sin(t * s.k * 2.2 + s.p);
    const a = alpha * (0.22 + 0.78 * s.b) * tw;
    const rad = (0.7 + s.b * 2.3) * Math.sqrt(sc);
    ctx.fillStyle = "rgba(" + starColor(s.c) + "," + a.toFixed(3) + ")";
    ctx.beginPath(); ctx.arc(x, y, rad, 0, TAU); ctx.fill();
    if (s.b > 0.55) {
      const g = ctx.createRadialGradient(x, y, 0, x, y, rad * 7);
      g.addColorStop(0, "rgba(" + starColor(s.c) + "," + (a * 0.35).toFixed(3) + ")");
      g.addColorStop(1, "rgba(" + starColor(s.c) + ",0)");
      ctx.fillStyle = g; ctx.fillRect(x - rad * 7, y - rad * 7, rad * 14, rad * 14);
    }
  }
}

// The Milky Way: a band of fine dust, glow and a dark lane, drawn once to an offscreen canvas.
function makeMilkyWay(seed, w, h) {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  const x = c.getContext("2d"), r = rng(seed);
  for (let i = 0; i < 60; i++) {
    const u = r(), off = gauss(r) * w * 0.07;
    const px = w / 2 + off, py = u * h, rad = 60 + r() * 160;
    const g = x.createRadialGradient(px, py, 0, px, py, rad);
    const warm = r() < 0.35;
    g.addColorStop(0, warm ? "rgba(255,220,190,0.07)" : "rgba(170,190,255,0.06)");
    g.addColorStop(1, "rgba(0,0,0,0)");
    x.fillStyle = g; x.fillRect(px - rad, py - rad, rad * 2, rad * 2);
  }
  for (let i = 0; i < 26000; i++) {
    const py = r() * h, off = gauss(r) * w * 0.09 + Math.sin(py / h * 5) * w * 0.02;
    const a = 0.08 + Math.pow(r(), 3) * 0.5;
    x.fillStyle = "rgba(235,235,255," + a.toFixed(3) + ")";
    x.fillRect(w / 2 + off, py, r() < 0.9 ? 1 : 2, 1);
  }
  x.globalCompositeOperation = "destination-out";
  for (let i = 0; i < 90; i++) {
    const py = r() * h, px = w / 2 + Math.sin(py / h * 7 + 1) * w * 0.025 + gauss(r) * 10, rad = 20 + r() * 45;
    const g = x.createRadialGradient(px, py, 0, px, py, rad);
    g.addColorStop(0, "rgba(0,0,0,0.35)"); g.addColorStop(1, "rgba(0,0,0,0)");
    x.fillStyle = g; x.fillRect(px - rad, py - rad, rad * 2, rad * 2);
  }
  return c;
}

// Earth: an equirectangular texture made once from noise, shaded per pixel on a sphere.
const TEX_W = 1024, TEX_H = 512;
function makeEarthTexture() {
  const land = new Float32Array(TEX_W * TEX_H), cloud = new Float32Array(TEX_W * TEX_H), city = new Float32Array(TEX_W * TEX_H);
  for (let j = 0; j < TEX_H; j++) {
    const lat = (0.5 - (j + 0.5) / TEX_H) * Math.PI;
    for (let i = 0; i < TEX_W; i++) {
      const lon = ((i + 0.5) / TEX_W) * TAU;
      const X = Math.cos(lat) * Math.sin(lon), Y = Math.sin(lat), Z = Math.cos(lat) * Math.cos(lon);
      const k = j * TEX_W + i;
      land[k] = fbm3(X * 1.6 + 11, Y * 1.6 + 3, Z * 1.6 + 7, 5) - (Math.abs(Y) > 0.92 ? -0.25 : 0);
      const sw = fbm3(X * 2 + 40, Y * 2, Z * 2, 2) * 2.5;
      cloud[k] = fbm3(X * 3.2 + sw, Y * 6 + 20, Z * 3.2 - sw, 4);
      const pop = sstep(0.58, 0.72, fbm3(X * 9 + 5, Y * 9, Z * 9, 3)), sp = hash3(i, j, 7);
      city[k] = sp > 0.82 ? pop * (0.4 + 0.6 * hash3(i, j, 9)) : 0;
    }
  }
  return { land, cloud, city };
}
const earthBuf = {};
function drawEarth(ctx, tex, cx, cy, R, rot, sun, cloudShift) {
  const S = Math.max(64, Math.min(760, Math.round(R * 2)));
  if (!earthBuf[S]) { const c = document.createElement("canvas"); c.width = c.height = S; earthBuf[S] = { c, x: c.getContext("2d"), img: c.getContext("2d").createImageData(S, S) }; }
  const B = earthBuf[S], d = B.img.data; d.fill(0);
  const tilt = -0.41, ct = Math.cos(tilt), st = Math.sin(tilt);
  for (let j = 0; j < S; j++) {
    const y = 1 - ((j + 0.5) / S) * 2;
    for (let i = 0; i < S; i++) {
      const x = ((i + 0.5) / S) * 2 - 1, d2 = x * x + y * y;
      if (d2 >= 1) continue;
      const z = Math.sqrt(1 - d2);
      const l = x * sun[0] + y * sun[1] + z * sun[2];
      const day = sstep(-0.12, 0.18, l);
      const nx = x * ct - y * st, ny = x * st + y * ct;
      const lat = Math.asin(ny), lon = Math.atan2(nx, z) + rot;
      let u = Math.floor((((lon / TAU) % 1 + 1) % 1) * TEX_W), v = Math.floor((0.5 - lat / Math.PI) * TEX_H);
      v = clamp(v, 0, TEX_H - 1);
      const k = v * TEX_W + u;
      const h = tex.land[k], isLand = h > 0.53, polar = Math.abs(ny) > 0.9;
      let r, g, b;
      if (polar) { r = 225; g = 232; b = 240; }
      else if (isLand) { const dry = sstep(0.56, 0.68, h); r = lerp(46, 150, dry); g = lerp(84, 124, dry); b = lerp(44, 82, dry); }
      else { const deep = sstep(0.53, 0.3, h); r = lerp(26, 8, deep); g = lerp(92, 34, deep); b = lerp(150, 92, deep); }
      const cu = ((u + Math.floor(cloudShift * TEX_W)) % TEX_W + TEX_W) % TEX_W;
      const cl = sstep(0.52, 0.72, tex.cloud[v * TEX_W + cu]);
      r = lerp(r, 245, cl * 0.9); g = lerp(g, 248, cl * 0.9); b = lerp(b, 252, cl * 0.9);
      const limb = 0.45 + 0.55 * Math.sqrt(z);
      const lit = day * limb * (0.35 + 0.75 * clamp(l + 0.15, 0, 1));
      r *= lit; g *= lit; b *= lit;
      if (!isLand && !polar && cl < 0.3) {
        const hx = sun[0], hy = sun[1], hz = sun[2] + 1, hl = Math.hypot(hx, hy, hz);
        const spec = Math.pow(clamp((x * hx + y * hy + z * hz) / hl, 0, 1), 60) * day;
        r += 190 * spec; g += 180 * spec; b += 150 * spec;
      }
      if (isLand && !polar) {
        const lights = 0.85 * tex.city[k] * (1 - day) * (1 - cl * 0.8) * sstep(0, 0.35, z);
        r += 255 * lights; g += 175 * lights; b += 90 * lights;
      }
      const night = (1 - day) * 0.06;
      r += 12 * night * 4; g += 18 * night * 4; b += 34 * night * 4;
      const p = (j * S + i) * 4, edge = clamp((1 - Math.sqrt(d2)) * S * 0.5, 0, 1);
      d[p] = r; d[p + 1] = g; d[p + 2] = b; d[p + 3] = 255 * edge;
    }
  }
  B.x.putImageData(B.img, 0, 0);
  ctx.save(); ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = "high";
  ctx.drawImage(B.c, cx - R, cy - R, R * 2, R * 2);
  // Atmosphere: a thin blue rim, brighter towards the sun.
  ctx.globalCompositeOperation = "lighter";
  const g = ctx.createRadialGradient(cx, cy, R * 0.94, cx, cy, R * 1.09);
  g.addColorStop(0, "rgba(60,130,255,0)"); g.addColorStop(0.45, "rgba(80,150,255,0.28)"); g.addColorStop(1, "rgba(40,90,255,0)");
  ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, R * 1.1, 0, TAU); ctx.fill();
  const sl = Math.hypot(sun[0], sun[1]) || 1, sx = cx + (sun[0] / sl) * R, sy = cy - (sun[1] / sl) * R;
  const g2 = ctx.createRadialGradient(sx, sy, 0, sx, sy, R * 1.1);
  g2.addColorStop(0, "rgba(140,190,255,0.45)"); g2.addColorStop(1, "rgba(140,190,255,0)");
  ctx.fillStyle = g2; ctx.beginPath(); ctx.arc(cx, cy, R * 1.06, 0, TAU); ctx.arc(cx, cy, R * 0.985, 0, TAU, true); ctx.fill();
  ctx.restore();
}
function sunGlare(ctx, x, y, size, a) {
  ctx.save(); ctx.globalCompositeOperation = "lighter";
  let g = ctx.createRadialGradient(x, y, 0, x, y, size);
  g.addColorStop(0, "rgba(255,250,235," + a + ")"); g.addColorStop(0.08, "rgba(255,230,180," + a * 0.8 + ")");
  g.addColorStop(0.35, "rgba(255,190,120," + a * 0.18 + ")"); g.addColorStop(1, "rgba(255,170,100,0)");
  ctx.fillStyle = g; ctx.fillRect(x - size, y - size, size * 2, size * 2);
  g = ctx.createLinearGradient(x - size * 1.6, y, x + size * 1.6, y);
  g.addColorStop(0, "rgba(255,220,170,0)"); g.addColorStop(0.5, "rgba(255,235,200," + a * 0.5 + ")"); g.addColorStop(1, "rgba(255,220,170,0)");
  ctx.fillStyle = g; ctx.fillRect(x - size * 1.6, y - 2, size * 3.2, 4);
  ctx.restore();
}
function ridgeLine(seed, y0, amp, x0, x1, step) {
  const pts = [];
  for (let x = x0; x <= x1; x += step) { const n = fbm1(x * 0.0022 + seed, seed, 5); pts.push([x, y0 - amp * (1 - Math.abs(n * 2 - 1)) * 1.4 + amp * 0.5 - amp * 0.3 * Math.sin(x * 0.0011 + seed)]); }
  return pts;
}
function fillRidge(ctx, pts, color, rim) {
  ctx.beginPath(); ctx.moveTo(pts[0][0], 4000);
  for (const p of pts) ctx.lineTo(p[0], p[1]);
  ctx.lineTo(pts[pts.length - 1][0], 4000); ctx.closePath(); ctx.fillStyle = color; ctx.fill();
  if (rim) { ctx.beginPath(); pts.forEach((p, i) => (i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]))); ctx.strokeStyle = rim; ctx.lineWidth = 2; ctx.stroke(); }
}
function skyGradient(ctx, stops) {
  const g = ctx.createLinearGradient(0, 0, 0, 1920);
  stops.forEach(([o, c]) => g.addColorStop(o, c));
  ctx.fillStyle = g; ctx.fillRect(0, 0, 1080, 1920);
}
function vignette(ctx, a) {
  const g = ctx.createRadialGradient(540, 900, 500, 540, 960, 1250);
  g.addColorStop(0, "rgba(0,0,0,0)"); g.addColorStop(1, "rgba(0,0,0," + a + ")");
  ctx.fillStyle = g; ctx.fillRect(0, 0, 1080, 1920);
}
"""


def scene(cid, dur, style, body, draw, script, fade=True):
    """A scene: a full-frame canvas drawn by draw(t) from a proxy tween, plus HTML overlays."""
    fade_js = (f'    tl.fromTo("#{cid}-wrap", {{ opacity: 0 }}, {{ opacity: 1, duration: {FADE}, ease: "power1.inOut" }}, 0);\n'
               if fade else "")
    return f"""<template>
  <style>
{FONTS}
    #root {{ position: absolute; inset: 0; }}
    #{cid}-wrap {{ position: absolute; inset: 0; background: {NIGHT}; }}
    #{cid}-cv {{ position: absolute; inset: 0; width: {W}px; height: {H}px; }}
{style}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}" data-duration="{dur}">
    <div id="{cid}-wrap" class="clip" data-start="0" data-duration="{dur}" data-track-index="0">
      <canvas id="{cid}-cv" width="{W}" height="{H}"></canvas>
{body}
    </div>
  </div>
  <script>
    (function () {{
{LIB}
      const cv = document.getElementById("{cid}-cv"), ctx = cv.getContext("2d");
{draw}
      const tl = gsap.timeline({{ paused: true }});
      const clock = {{ t: 0 }};
      tl.to(clock, {{ t: {dur}, duration: {dur}, ease: "none", onUpdate: () => draw(clock.t) }}, 0);
{fade_js}{script}
      draw(0);
      window.__timelines["{cid}"] = tl;
    }})();
  </script>
</template>
"""


# ---- S1 / S6: the night ridge and the Milky Way --------------------------------------------
RIDGE_DRAW = """
      const stars = makeStars(%(seed)d, 1500, 1500, 3400);
      const mw = makeMilkyWay(%(seed)d + 1, 900, 3600);
      const ridgeFar = ridgeLine(3.1, 0, 70, -300, 1400, 8), ridgeNear = ridgeLine(8.7, 0, 120, -300, 1400, 6);
      function world(t, horizon, sc, alpha) {
        // horizon: the ridge's screen y; sc: zoom about the frame centre.
        skyGradient(ctx, [[0, "#02040B"], [0.55, "#060B1C"], [1, "#0B1430"]]);
        ctx.save(); ctx.translate(540, 960); ctx.scale(sc, sc); ctx.translate(-540, -960);
        const lift = horizon - 1500;
        ctx.save(); ctx.translate(540, 620 + lift * 0.55); ctx.rotate(-0.42);
        ctx.globalAlpha = 0.95 * alpha; ctx.drawImage(mw, -450, -1800); ctx.restore();
        drawStars(ctx, stars, t, -210, -1700 + lift * 0.6, 1, alpha);
        const hg = ctx.createLinearGradient(0, horizon - 420, 0, horizon + 40);
        hg.addColorStop(0, "rgba(40,70,140,0)"); hg.addColorStop(1, "rgba(60,95,170,0.32)");
        ctx.fillStyle = hg; ctx.fillRect(-400, horizon - 420, 1900, 460);
        ctx.save(); ctx.translate(0, horizon - 40); fillRidge(ctx, ridgeFar, "#0A1024", "rgba(120,150,210,0.18)"); ctx.restore();
        ctx.save(); ctx.translate(0, horizon + 60); fillRidge(ctx, ridgeNear, "#03050C", "rgba(150,170,220,0.22)"); ctx.restore();
        ctx.restore();
        vignette(ctx, 0.55);
      }
"""


def s1():
    draw = RIDGE_DRAW % {"seed": 11} + """
      function draw(t) {
        // Already tilting up at frame 0: the ridge sinks as the sky opens.
        const k = t / 7.4;
        world(t, lerp(1560, 2050, easeInOut(k * 0.9 + 0.1)), lerp(1.08, 1.0, k), 1);
      }
"""
    css = f"""
    #s1-hook {{ position: absolute; left: 90px; width: 900px; top: 470px; text-align: center; }}
    #s1-big {{ font-family: "EB Garamond", serif; font-weight: 500; font-size: 176px; line-height: 1; color: {WHITE};
      letter-spacing: -0.01em; text-shadow: 0 4px 40px rgba(0,0,0,0.6); }}
    #s1-big .a {{ color: {GOLD}; }}
    #s1-sub {{ margin-top: 34px; font-family: "Inter", sans-serif; font-weight: 600; font-size: 38px; letter-spacing: 0.16em;
      text-transform: uppercase; color: {GOLD}; text-shadow: 0 2px 18px rgba(0,0,0,0.8); }}
"""
    body = """      <div id="s1-hook"><div id="s1-big">Look <span class="a">up.</span></div><div id="s1-sub">Think about who created this.</div></div>"""
    script = (
        '    tl.fromTo("#s1-big", { scale: 1.06 }, { scale: 1, duration: 5.6, ease: "power1.out" }, 0);\n'
        '    tl.to("#s1-hook", { opacity: 0, filter: "blur(10px)", y: -30, duration: 0.7, ease: "power2.in" }, 5.6);\n'
    )
    return scene("s1", 7.4, css, body, draw, script, fade=False)


def s6():
    draw = RIDGE_DRAW % {"seed": 11} + """
      function draw(t) {
        // The return: start close, then pull away to the whole sky.
        const k = easeInOut(t / 11);
        world(t + 40, lerp(2050, 1640, k), lerp(1.32, 1.0, k), lerp(0.85, 1.15, k));
        ctx.fillStyle = "rgba(0,0,0," + (0.42 * sstep(7.2, 8.4, t)).toFixed(3) + ")"; ctx.fillRect(0, 0, 1080, 1920);
      }
"""
    css = f"""
    #s6-q {{ position: absolute; left: 90px; width: 900px; top: 560px; text-align: center; font-family: "EB Garamond", serif;
      font-weight: 500; font-size: 132px; line-height: 1.04; color: {WHITE}; text-shadow: 0 4px 40px rgba(0,0,0,0.7); }}
    #s6-q .w {{ display: inline-block; }}
    #s6-q .a {{ color: {GOLD}; }}
    #s6-tag {{ position: absolute; left: 90px; width: 900px; top: 930px; text-align: center; font-family: "Inter", sans-serif;
      font-weight: 600; font-size: 40px; letter-spacing: 0.22em; text-transform: uppercase; color: {GOLD}; }}
    #s6-brand {{ position: absolute; left: 90px; width: 900px; top: 1010px; text-align: center; font-family: "EB Garamond", serif;
      font-style: italic; font-weight: 500; font-size: 40px; color: rgba(244,241,234,0.75); }}
"""
    words = '<span class="w">Who</span> <span class="w a">created</span><br><span class="w">all</span> <span class="w">of</span> <span class="w">this?</span>'
    body = f"""      <div id="s6-q">{words}</div>
      <div id="s6-tag">Discover your Creator</div>
      <div id="s6-brand">Every Sign Leads</div>"""
    q = TIMING["l19"] - 48.0
    tag = TIMING["l20"] - 48.0
    script = (
        f'    tl.fromTo("#s6-q .w", {{ opacity: 0, filter: "blur(10px)", y: 14 }}, {{ opacity: 1, filter: "blur(0px)", y: 0, duration: 0.5, ease: "power2.out", stagger: 0.3 }}, {q - 0.05:.2f});\n'
        f'    tl.fromTo("#s6-tag", {{ opacity: 0, scale: 1.08 }}, {{ opacity: 1, scale: 1, duration: 1.0, ease: "power2.out" }}, {tag - 0.05:.2f});\n'
        f'    tl.fromTo("#s6-brand", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.8, ease: "power1.out" }}, {tag + 0.6:.2f});\n'
    )
    return scene("s6", 12.0, css, body, draw, script)


# ---- S2: through the clouds, past the stars, to a galaxy -----------------------------------
def s2():
    draw = """
      const r = rng(21), field = [];
      for (let i = 0; i < 1600; i++) field.push({ x: (r() - 0.5) * 2.4, y: (r() - 0.5) * 3.6, z: r(), b: Math.pow(r(), 3), c: r() });
      const clouds = [];
      for (let i = 0; i < 26; i++) clouds.push({ x: (r() - 0.5) * 1.8, y: (r() - 0.5) * 2.4, z: 0.15 + r() * 0.85, s: 0.3 + r() * 0.5 });
      const gal = [];
      for (let i = 0; i < 9000; i++) {
        const arm = i % 2, d = Math.pow(r(), 1.35), ang = arm * Math.PI + d * 9.5 + gauss(r) * (0.3 + 0.25 * (1 - d));
        const rad = d * 430 + gauss(r) * 14;
        const hot = d < 0.18 || r() < 0.06;
        gal.push({ a: ang, r: rad, s: r() < 0.03 ? 2.4 : 1.1 + r() * 0.8, col: hot ? "255,226,190" : (r() < 0.12 ? "255,170,200" : "175,200,255"), al: 0.25 + r() * 0.6 });
      }
      for (let i = 0; i < 1800; i++) { const rad = Math.abs(gauss(r)) * 70; gal.push({ a: r() * TAU, r: rad, s: 1.2, col: "255,236,205", al: 0.5 }); }
      // Distance travelled: slow, a surge past the stars, then easing as the galaxy fills the frame.
      const travel = (t) => 0.035 * t + 0.55 * sstep(2.0, 5.2, t) + 0.12 * sstep(5.2, 10.6, t);
      function draw(t) {
        skyGradient(ctx, [[0, "#03050E"], [1, "#050816"]]);
        const sky = 1 - sstep(0, 2.6, t);
        if (sky > 0) { ctx.fillStyle = "rgba(22,40,86," + (0.75 * sky).toFixed(3) + ")"; ctx.fillRect(0, 0, 1080, 1920); }
        const p = travel(t);
        for (const s of field) {
          let z = s.z - p; z = z - Math.floor(z); z = 0.04 + z * 0.96;
          const x = 540 + (s.x / z) * 520, y = 960 + (s.y / z) * 520;
          if (x < -20 || x > 1100 || y < -20 || y > 1940) continue;
          const near = 1 - z, a = clamp(near * 1.4, 0, 1) * (0.3 + 0.7 * s.b) * sstep(0.04, 0.12, z);
          const rad = 0.6 + near * near * 3.2 * (0.5 + s.b);
          ctx.fillStyle = "rgba(" + starColor(s.c) + "," + a.toFixed(3) + ")";
          ctx.beginPath(); ctx.arc(x, y, rad, 0, TAU); ctx.fill();
        }
        // Clouds rush past and are gone by "beyond the stars".
        for (const c of clouds) {
          const z = c.z - t * 0.32;
          if (z <= 0.03) continue;
          const x = 540 + (c.x / z) * 520, y = 960 + (c.y / z) * 520, rad = (c.s / z) * 420;
          const a = 0.5 * sstep(0.03, 0.25, z) * (1 - sstep(1.6, 2.8, t));
          if (a <= 0.002) continue;
          const g = ctx.createRadialGradient(x, y, 0, x, y, rad);
          g.addColorStop(0, "rgba(120,140,190," + a.toFixed(3) + ")"); g.addColorStop(1, "rgba(60,80,140,0)");
          ctx.fillStyle = g; ctx.fillRect(x - rad, y - rad, rad * 2, rad * 2);
        }
        // The galaxy grows out of the dark.
        const ga = sstep(3.6, 6.4, t);
        if (ga > 0) {
          const sc = lerp(0.18, 1.12, easeOut((t - 3.6) / 7)), rot = t * 0.035;
          ctx.save(); ctx.translate(540, 900); ctx.rotate(-0.45); ctx.scale(sc, sc * 0.56);
          ctx.globalCompositeOperation = "lighter";
          let g = ctx.createRadialGradient(0, 0, 0, 0, 0, 470);
          g.addColorStop(0, "rgba(120,140,220," + (0.22 * ga).toFixed(3) + ")"); g.addColorStop(1, "rgba(40,50,120,0)");
          ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, 470, 0, TAU); ctx.fill();
          for (const q of gal) {
            const a = q.a + rot * (1.4 - q.r / 600);
            ctx.fillStyle = "rgba(" + q.col + "," + (q.al * ga).toFixed(3) + ")";
            ctx.fillRect(Math.cos(a) * q.r, Math.sin(a) * q.r, q.s, q.s);
          }
          g = ctx.createRadialGradient(0, 0, 0, 0, 0, 120);
          g.addColorStop(0, "rgba(255,245,225," + (0.95 * ga).toFixed(3) + ")"); g.addColorStop(0.3, "rgba(255,215,170," + (0.45 * ga).toFixed(3) + ")"); g.addColorStop(1, "rgba(255,190,140,0)");
          ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, 120, 0, TAU); ctx.fill();
          ctx.restore();
        }
        vignette(ctx, 0.6);
      }
"""
    return scene("s2", 10.6, "", "", draw, "")


# ---- S3: here we are — Earth at sunrise, then small in the dark ----------------------------
def s3():
    draw = """
      const tex = makeEarthTexture(), stars = makeStars(31, 700, 1080, 1920);
      function draw(t) {
        skyGradient(ctx, [[0, "#02030A"], [1, "#040714"]]);
        const k = easeInOut(sstep(1.6, 6.2, t));
        drawStars(ctx, stars, t, 0, 0, 1, 0.25 + 0.75 * k);
        const R = lerp(760, 250, k), cx = 540, cy = lerp(1560, 860, k);
        const a = lerp(-2.55, -1.15, easeOut(t / 10.2)), e = 0.32;
        const sun = [Math.sin(a) * Math.cos(e), Math.sin(e), Math.cos(a) * Math.cos(e)];
        drawEarth(ctx, tex, cx, cy, R, 2.2 + t * 0.03, sun, t * 0.004);
        // The sun breaks over the limb, strongest while it is still behind.
        const sl = Math.hypot(sun[0], sun[1]), gx = cx + (sun[0] / sl) * R * 1.01, gy = cy - (sun[1] / sl) * R * 1.01;
        const behind = sstep(-0.1, -0.85, sun[2]);
        sunGlare(ctx, gx, gy, lerp(260, 520, sstep(0, 3, t)) * (0.5 + 0.5 * behind), (0.25 + 0.75 * sstep(0, 2.5, t)) * (0.35 + 0.65 * behind));
        vignette(ctx, 0.5);
      }
"""
    return scene("s3", 10.2, "", "", draw, "")


# ---- S4: something to reflect upon — mountains over a still lake ---------------------------
def s4():
    draw = """
      const stars = makeStars(41, 900, 1300, 1200), SHORE = 1150;
      const layers = [];
      for (let i = 0; i < 5; i++) layers.push({ pts: ridgeLine(2 + i * 3.3, 0, 330 - i * 45, -500, 1600, 5), y: 640 + i * 110, d: 0.25 + i * 0.22,
        col: ["#1B2748", "#141E3A", "#0E162C", "#090F20", "#050913"][i], rim: i < 2 ? "rgba(170,190,240,0.20)" : null });
      const top = document.createElement("canvas"); top.width = 1080; top.height = SHORE; const tx = top.getContext("2d");
      function draw(t) {
        const push = easeOut(t / 9.8);
        tx.setTransform(1, 0, 0, 1, 0, 0);
        const g = tx.createLinearGradient(0, 0, 0, SHORE);
        g.addColorStop(0, "#03050E"); g.addColorStop(0.6, "#0A1330"); g.addColorStop(1, "#22305A");
        tx.fillStyle = g; tx.fillRect(0, 0, 1080, SHORE);
        const cctx = tx;
        drawStars(cctx, stars, t, -110, 0, 1 + push * 0.04, 1, 540, 400);
        // A thin crescent moon, high and to the right.
        cctx.save(); cctx.translate(800, 300 + push * 10);
        let mg = cctx.createRadialGradient(0, 0, 0, 0, 0, 200); mg.addColorStop(0, "rgba(220,225,255,0.14)"); mg.addColorStop(1, "rgba(220,225,255,0)");
        cctx.fillStyle = mg; cctx.fillRect(-200, -200, 400, 400);
        cctx.beginPath(); cctx.arc(0, 0, 38, 0, TAU); cctx.fillStyle = "#EEF0F8"; cctx.fill();
        cctx.beginPath(); cctx.arc(15, -9, 35, 0, TAU); cctx.fillStyle = "#0A1330"; cctx.fill();
        cctx.restore();
        for (const L of layers) {
          const sc = 1 + push * 0.10 * L.d * 2;
          cctx.save(); cctx.translate(540, SHORE); cctx.scale(sc, sc); cctx.translate(-540, -SHORE);
          cctx.translate(0, L.y); fillRidge(cctx, L.pts, L.col, L.rim); cctx.restore();
        }
        const mist = cctx.createLinearGradient(0, SHORE - 160, 0, SHORE);
        mist.addColorStop(0, "rgba(90,110,170,0)"); mist.addColorStop(1, "rgba(90,110,170,0.22)");
        cctx.fillStyle = mist; cctx.fillRect(0, SHORE - 160, 1080, 160);
        ctx.drawImage(top, 0, 0);
        // The lake: the same picture upside down, darker, broken by slow ripples.
        ctx.fillStyle = "#03050C"; ctx.fillRect(0, SHORE, 1080, 1920 - SHORE);
        ctx.globalAlpha = 0.85;
        for (let y = 0; y < 1920 - SHORE; y += 3) {
          const depth = y / (1920 - SHORE), off = Math.sin(y * 0.09 + t * 1.6) * (0.6 + 9 * depth) + Math.sin(y * 0.023 - t * 0.7) * 3 * depth;
          ctx.drawImage(top, 0, SHORE - 1 - y - 3, 1080, 3, off, SHORE + y, 1080, 3);
        }
        ctx.globalAlpha = 1;
        const lg = ctx.createLinearGradient(0, SHORE, 0, 1920);
        lg.addColorStop(0, "rgba(3,5,12,0.05)"); lg.addColorStop(1, "rgba(3,5,12,0.7)");
        ctx.fillStyle = lg; ctx.fillRect(0, SHORE, 1080, 1920 - SHORE);
        ctx.fillStyle = "rgba(180,200,255,0.25)"; ctx.fillRect(0, SHORE, 1080, 1.5);
        vignette(ctx, 0.55);
      }
"""
    return scene("s4", 9.8, "", "", draw, "")


# ---- S5: night and day turning, and the verse ----------------------------------------------
def s5():
    draw = """
      const tex = makeEarthTexture(), stars = makeStars(51, 700, 1080, 1920);
      function draw(t) {
        skyGradient(ctx, [[0, "#02030A"], [1, "#040714"]]);
        drawStars(ctx, stars, t, 0, 0, 1, 0.8);
        // The terminator sweeps across the planet: night and day alternating.
        const a = lerp(1.9, -1.5, t / 14), e = 0.18;
        const sun = [Math.sin(a) * Math.cos(e), Math.sin(e), Math.cos(a) * Math.cos(e)];
        const R = lerp(272, 258, easeOut(t / 14));
        drawEarth(ctx, tex, 540, 465, R, 0.6 + t * 0.06, sun, t * 0.003);
        const sh = ctx.createLinearGradient(0, 760, 0, 1920);
        sh.addColorStop(0, "rgba(2,3,10,0)"); sh.addColorStop(0.12, "rgba(2,3,10,0.55)"); sh.addColorStop(1, "rgba(2,3,10,0.7)");
        ctx.fillStyle = sh; ctx.fillRect(0, 760, 1080, 1160);
        vignette(ctx, 0.45);
      }
"""
    words = ARABIC.split(" ")
    ar = " ".join(f'<span class="aw">{w}</span>' for w in words)
    en = " ".join(f'<span class="ew">{w}</span>' for w in TRANSLATION.split(" "))
    css = f"""
    #s5-label {{ position: absolute; left: 90px; width: 900px; top: 790px; text-align: center; font-family: "Inter", sans-serif;
      font-weight: 600; font-size: 34px; letter-spacing: 0.24em; text-transform: uppercase; color: {GOLD}; }}
    #s5-ar {{ position: absolute; left: 90px; width: 900px; top: 845px; text-align: center; direction: rtl; font-family: "Amiri Quran", serif;
      font-palette: --gold; font-size: 56px; line-height: 1.62; color: {GOLD}; }}
    #s5-ar .aw {{ display: inline-block; }}
    #s5-en {{ position: absolute; left: 110px; width: 860px; top: 1082px; text-align: center; font-family: "EB Garamond", serif;
      font-style: italic; font-weight: 500; font-size: 44px; line-height: 1.24; color: {WHITE}; }}
    #s5-en .ew {{ display: inline-block; }}
    #s5-ref {{ position: absolute; left: 90px; width: 900px; top: 1316px; text-align: center; font-family: "Inter", sans-serif;
      font-weight: 500; font-size: 26px; letter-spacing: 0.06em; color: rgba(244,241,234,0.62); }}
    #s5-rule {{ position: absolute; left: 440px; width: 200px; top: 1056px; height: 1px; background: {GOLD}; opacity: 0.5; }}
"""
    body = f"""      <div id="s5-label">Quran 3:190</div>
      <div id="s5-ar">{ar}</div>
      <div id="s5-rule"></div>
      <div id="s5-en">{en}</div>
      <div id="s5-ref">{REFERENCE}</div>"""
    start = 34.8
    lab, arab, en_t = TIMING["l12"] - start, TIMING["l12"] - start + 0.5, TIMING["l13"] - start - 0.4
    script = (
        f'    tl.fromTo("#s5-label", {{ opacity: 0, scale: 1.08 }}, {{ opacity: 1, scale: 1, duration: 0.9, ease: "power2.out" }}, {lab:.2f});\n'
        f'    tl.fromTo("#s5-ar .aw", {{ opacity: 0, filter: "blur(6px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.5, ease: "power2.out", stagger: 0.22 }}, {arab:.2f});\n'
        f'    tl.fromTo("#s5-rule", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.8, ease: "power2.inOut" }}, {arab + 2.6:.2f});\n'
        f'    tl.fromTo("#s5-en .ew", {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power2.out", stagger: 0.11 }}, {en_t:.2f});\n'
        f'    tl.fromTo("#s5-ref", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.8, ease: "power1.out" }}, {en_t + 3.0:.2f});\n'
    )
    return scene("s5", 14.0, css, body, draw, script)


# ---- Captions: the narration, phrase by phrase, word by word -------------------------------
NO_CAPTION = {"l12", "l13", "l14", "l19", "l20"}  # the verse card and the closing words carry these
ACCENT = {"sky", "galaxies", "tiny", "world.", "Alive.", "reflect", "Reflect", "look", "up."}


def phrases(text, n=6):
    words = text.replace("...", "\u2026").split()
    parts, cur = [], []
    for w in words:
        cur.append(w)
        if w.endswith(("\u2026", ",", "?")) and len(cur) > 1:
            parts.append(cur)
            cur = []
    if cur:
        parts.append(cur)
    out = []
    for p in parts:
        k = -(-len(p) // n)
        size = -(-len(p) // k)
        out += [p[i:i + size] for i in range(0, len(p), size)]
    return out


def captions():
    groups, script = [], []
    gi = 0
    ids = sorted(TIMING)
    for idx, lid in enumerate(ids):
        if lid in NO_CAPTION:
            continue
        start, length = TIMING[lid], LEN[lid]
        nxt = TIMING[ids[idx + 1]] if idx + 1 < len(ids) else DUR
        ph = phrases(NARRATION[lid])
        total = sum(len(w) + 1 for p in ph for w in p)
        clock = start
        for pi, p in enumerate(ph):
            plen = sum(len(w) + 1 for w in p) / total * length
            g_start = clock - 0.08
            last = pi == len(ph) - 1
            g_end = min(nxt - 0.1, start + length + 0.9) if last else clock + plen
            gid = f"c{gi}"
            gi += 1
            spans, wc = [], clock
            for w in p:
                cls = "cw a" if w.strip(".,?…") in {x.strip(".,?") for x in ACCENT} else "cw"
                spans.append(f'<span class="{cls}">{w}</span>')
                script.append(f'    tl.fromTo("#{gid} .cw:nth-child({len(spans)})", {{ opacity: 0.28 }}, {{ opacity: 1, duration: 0.14, ease: "power1.out" }}, {wc - g_start:.3f});')
                wc += (len(w) + 1) / total * length
            groups.append((gid, g_start, g_end - g_start, " ".join(spans)))
            clock += plen
    # Word tweens live in each group's own timeline offset; rebuild them as absolute times.
    body, tweens = [], []
    for gid, st, du, html in groups:
        body.append(f'      <div id="{gid}" class="cap clip" data-start="{st:.3f}" data-duration="{du:.3f}" data-track-index="0">{html}</div>')
    for line in script:
        gid = re.search(r'"#(c\d+) ', line).group(1)
        st = next(g[1] for g in groups if g[0] == gid)
        local = float(re.search(r", ([\d.]+)\);$", line).group(1))
        tweens.append(re.sub(r", ([\d.]+)\);$", f", {st + local:.3f});", line))
        tweens.append(f'    tl.fromTo("#{gid}", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power2.out" }}, {st:.3f});')
    tweens = list(dict.fromkeys(tweens))
    css = f"""
    #root {{ position: absolute; inset: 0; }}
    .cap {{ position: absolute; left: 110px; width: 860px; top: 1170px; text-align: center; font-family: "Inter", sans-serif;
      font-weight: 600; font-size: 54px; line-height: 1.22; color: {WHITE}; letter-spacing: -0.005em;
      text-shadow: 0 2px 4px rgba(0,0,0,0.85), 0 0 30px rgba(0,0,0,0.75); }}
    .cap .a {{ color: {GOLD}; }}
"""
    return f"""<template>
  <style>
{css}
  </style>
  <div id="root" data-composition-id="captions" data-width="{W}" data-height="{H}" data-duration="{DUR}">
{chr(10).join(body)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tweens)}
    window.__timelines["captions"] = tl;
  </script>
</template>
"""


def index():
    hosts = "\n".join(
        f'      <div id="{cid}" class="clip" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
        f'data-start="{st}" data-duration="{du}" data-track-index="{1 + i % 2}" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:{i + 2}"></div>'
        for i, (cid, st, du) in enumerate(SCENES)
    )
    return f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: {NIGHT}; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
      #ground {{ position: absolute; inset: 0; background: {NIGHT}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
      <div id="ground" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0" style="z-index:0"></div>
{hosts}
      <div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{DUR}" data-track-index="3" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:20"></div>
      <audio id="voice" class="clip" src="assets/audio/vo.wav" data-start="0" data-duration="{DUR}" data-track-index="4" data-volume="1"></audio>
      <audio id="bed" class="clip" src="assets/audio/bed.wav" data-start="0" data-duration="{DUR}" data-track-index="5" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


if __name__ == "__main__":
    comp = HERE / "compositions"
    comp.mkdir(exist_ok=True)
    for name, fn in [("s1", s1), ("s2", s2), ("s3", s3), ("s4", s4), ("s5", s5), ("s6", s6), ("captions", captions)]:
        (comp / f"{name}.html").write_text(fn())
    (HERE / "index.html").write_text(index())
    print("built; arabic 3:190 =", ARABIC)

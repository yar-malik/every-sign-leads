# Every Sign Leads — Agent Notes

Sister project to `../quran-visualized`: short cinematic videos (and later an app) that invite
people to reflect on creation and its Creator. Tagline: **"Discover your Creator."** Content and
script come from Shabbar Shirazi (brief, 2026-10-24). Started 2026-10-25.

Angle vs Quran Visualized: QV tells *stories* (prophets, companions) in a gold-engraving night look.
Every Sign Leads is about *signs in creation* (sky, galaxies, Earth, night and day), AI-narrated in
English, 60 s, slower and contemplative.

Full how-to (setup, making a video, posting): `README.md`. Keep its video table up to date.

## Status — 2026-10-25

- Folder only; **no app scaffolded yet**. When it is, copy the Quran Visualized stack (Expo SDK 57,
  expo-router, NativeWind, Zustand) and use the owner's existing accounts (see QV `AGENTS.md`).
- Pilot 01 "Look up" rendered: `videos/look-up/renders/look-up.mp4` (60 s, 1080x1920).
- 02 "Sun and Moon" rendered: `videos/sun-and-moon/renders/sun-and-moon.mp4` (56 s), styled on
  `reference-video/` (local only, gitignored; 33 reels listed in its INDEX.md).
  Its `scripts/mix.sh` sets timing automatically from a `gap` per line in narration.json.
- 01b "Look up" restyled in the reference look: `videos/look-up-v2/` (same voice), unlisted at
  https://www.youtube.com/watch?v=pvqzYf-fPQ8.

## Content rules (same as Quran Visualized)

- Never type Arabic Quran text by hand — load it from `assets/quran/quran-uthmani.txt` (Tanzil).
- Translations: the brief asks for **Sahih International**. It is copyrighted; get permission before
  publishing at scale (or use our own paraphrase, marked as such).
- Narration that paraphrases a verse is said as "The Quran tells us…" and the exact text goes on a
  separate scripture card with surah and verse.
- No depictions of prophets, companions or God. No numerical-miracle or science-miracle claims.
- No instrumental music: voice, wind, a low tone.

## Videos

Projects in `videos/<name>/` (HyperFrames). Each has `narration.json` (lines), `timing.json`
(when each line starts), `scripts/tts.py` (Kokoro voice `am_michael`, on device, free),
`scripts/mix.sh` (places the lines into `assets/audio/vo.wav`) and `build.py` (writes the
compositions; pictures are drawn on canvas from timeline time).

```bash
# voice: needs a venv with kokoro-onnx + soundfile, and `brew install espeak-ng`
python scripts/tts.py am_michael 0.86        # all lines (or pass ids: l12 l13)
bash scripts/mix.sh                          # trim + place lines, write durations.json
python3 build.py && npx hyperframes@0.8.188 check
npx hyperframes@0.8.188 render -o renders/look-up.mp4
```

Gotcha: espeak reads "Quran" as kwer-RAN; `tts.py` swaps in the phonemes `kʊɹˈɑːn`.

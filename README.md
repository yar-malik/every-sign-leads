# Every Sign Leads

Short, slow, vertical videos (1080x1920) that invite people to reflect on the signs in creation:
the sky, the sun and moon, night and day. Tagline: **"Discover your Creator."**

Content and brief come from Shabbar Shirazi. Sister project to `quran-visualized`.

## Videos

| # | Video | Length | Watch | Source |
|---|-------|--------|-------|--------|
| 01 | Look up | 60 s | not posted yet | [`videos/look-up/`](videos/look-up/) · [render](videos/look-up/renders/look-up.mp4) |
| 02 | Sun and Moon | 56 s | [YouTube (unlisted)](https://www.youtube.com/watch?v=iGrbxNkoPyg) | [`videos/sun-and-moon/`](videos/sun-and-moon/) · [render](videos/sun-and-moon/renders/sun-and-moon.mp4) |

Each video folder has a `REVIEW.md`: what's in it, how it was checked, and what's still open.

## Reference videos

[`reference-video/`](reference-video/) holds two short reels Shabbar shared as the target style
(other creators' work, kept for study only; never re-post them as ours):

- `reference-1.mp4`: two prophets' stories told side by side through shared Quran wording.
- `reference-2.mp4`: two prophets compared by counting mentions. We don't make
  numerical-miracle claims (see the rules below), so only its look is used.

What we take from them: two subjects side by side, one Arabic word at a time lit in gold, thin line
drawings, an italic serif line with the verse reference, a dark warm background, 40–55 s.

## How a video is made

Everything runs on this Mac and costs nothing. Pictures are drawn on an HTML canvas from the
video's clock, text sits on top, and [HyperFrames](https://hyperframes.heygen.com) renders the HTML
to MP4.

```
videos/<name>/
  narration.json     the spoken lines (id, text, and `gap` = pause before the line)
  scripts/tts.py     speaks each line with Kokoro, voice am_michael → assets/vo/<id>.wav
  scripts/mix.sh     trims the lines, places them, writes timing.json + assets/audio/vo.wav
  build.py           writes index.html + compositions/*.html (all scenes and on-screen text)
  assets/audio/      vo.wav (voice) and bed.wav (wind + a low tone, no music)
  renders/<name>.mp4 the finished video
```

### One-time setup

```bash
brew install espeak-ng ffmpeg node
python3 -m venv ~/.hyperframes-venv
~/.hyperframes-venv/bin/pip install kokoro-onnx soundfile
# Kokoro model files go in ~/.cache/hyperframes/tts/models/kokoro-v1.0.onnx
# and ~/.cache/hyperframes/tts/voices/voices-v1.0.bin
```

### Make or change a video

```bash
cd videos/sun-and-moon
~/.hyperframes-venv/bin/python3 scripts/tts.py am_michael 0.86   # all lines (or pass ids: l03 l04)
bash scripts/mix.sh                                             # timing.json, vo.wav
python3 build.py                                                # compositions
npx hyperframes@0.8.188 check                                   # must pass
npx hyperframes@0.8.188 snapshot --at 2,10,20,30,40,50           # look at frames first
npx hyperframes@0.8.188 render -o renders/sun-and-moon.mp4
```

- Change what's **said**: edit `narration.json`, then run tts, mix and build again.
- Change what's **shown**: edit `build.py` (the `TEXT` list for words on screen, `DRAW` for the
  pictures), then build again.
- To start a new video, copy `videos/sun-and-moon/` and replace its narration and `build.py` beats.
  (`look-up/` uses hand-set `timing.json` instead of `gap`.)

The bed is the pilot's wind + tone, trimmed to the video length:
`ffmpeg -i ../look-up/assets/audio/bed.wav -af "atrim=0:56,afade=t=out:st=53:d=3" assets/audio/bed.wav`

## Posting

Test videos go up **unlisted on the Team Yar Malik YouTube channel** through the Postiz CLI
(already signed in on the laptop):

```bash
npx -y postiz@2.0.16 upload renders/<name>.mp4             # → https://uploads.postiz.com/<x>.mp4
npx -y postiz@2.0.16 posts:create -c "<description>" -m "<that url>" \
  -i "cmtooktty11pulm0yvijnj8uz" -s "<now + 2 min, ISO UTC>" \
  --settings '{"title":"<title>","type":"unlisted","selfDeclaredMadeForKids":"no"}'
npx -y postiz@2.0.16 posts:list                            # find that postId; releaseURL = YouTube link
```

It takes about 2–3 minutes. Check the link with YouTube oEmbed (title and channel should match),
then add it to the table above.

## Content rules

- Never type Arabic Quran text by hand. Load it from `assets/quran/quran-uthmani.txt` (Tanzil);
  `build.py` slices words by index.
- Translations: the brief asks for Sahih International, which is copyrighted. Get permission before
  posting at scale, or use our own wording and say so on screen (Sun and Moon does this).
- A paraphrased verse is spoken as "The Quran tells us…", with the exact text on a card with surah
  and verse.
- No depictions of prophets, companions or God. No numerical-miracle or science-miracle claims.
- No instrumental music: voice, wind, a low tone.
- Get a scholar to check the verse renderings before anything goes public.
- Gotcha: espeak reads "Quran" as kwer-RAN; `tts.py` swaps in the phonemes `kʊɹˈɑːn`.

"""Speak each narration line to assets/vo/<id>.wav with Kokoro (on device, free).

Usage: python tts.py <voice> <speed> [id ...]   (needs kokoro-onnx + soundfile in the venv)
"""
import json
import sys
from pathlib import Path

import soundfile as sf
from kokoro_onnx import EspeakConfig, Kokoro

HERE = Path(__file__).resolve().parent.parent
CACHE = Path.home() / ".cache/hyperframes/tts"
LINES = json.loads((HERE / "narration.json").read_text())
# espeak reads "Quran" as kwer-RAN; say kur-AHN.
FIXES = {"kwɚɹˈæn": "kʊɹˈɑːn"}

voice, speed, *only = sys.argv[1], float(sys.argv[2]), *sys.argv[3:]
k = Kokoro(str(CACHE / "models/kokoro-v1.0.onnx"), str(CACHE / "voices/voices-v1.0.bin"),
           espeak_config=EspeakConfig("/opt/homebrew/lib/libespeak-ng.dylib", "/opt/homebrew/share/espeak-ng-data"))
out = HERE / "assets/vo"
out.mkdir(parents=True, exist_ok=True)
for line in LINES:
    if only and line["id"] not in only:
        continue
    lang = "en-us" if voice[0] == "a" else "en-gb"
    phonemes = k.tokenizer.phonemize(line["text"], lang)
    for wrong, right in FIXES.items():
        phonemes = phonemes.replace(wrong, right)
    samples, sr = k.create(phonemes, voice=voice, speed=line.get("speed", speed), is_phonemes=True)
    sf.write(out / f"{line['id']}.wav", samples, sr)
    print(line["id"], round(len(samples) / sr, 2))

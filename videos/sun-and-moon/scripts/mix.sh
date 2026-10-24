#!/bin/bash
# Trim each line, start it `gap` seconds after the previous one ends (narration.json), write
# timing.json, durations.json and assets/audio/vo.wav (-16 LUFS), padded to the video length.
set -e
cd "$(dirname "$0")/.."
for f in assets/vo/l*.wav; do
  ffmpeg -v error -y -i "$f" -af "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse" -ar 48000 "$f.t.wav" && mv "$f.t.wav" "$f"
done
python3 - <<'PY'
import json, subprocess
lines = json.load(open("narration.json")); TAIL = 3.0
dur = {l["id"]: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/vo/{l['id']}.wav"])) for l in lines}
timing, clock = {}, 0.0
for l in lines:
    clock += l["gap"]; timing[l["id"]] = round(clock, 2); clock += dur[l["id"]]
total = round(clock + TAIL, 1)
json.dump(timing, open("timing.json", "w")); json.dump({k: round(v, 3) for k, v in dur.items()}, open("assets/vo/durations.json", "w"), indent=0)
inp, flt = [], []
for i, l in enumerate(lines):
    inp += ["-i", f"assets/vo/{l['id']}.wav"]; ms = int(timing[l["id"]] * 1000); flt.append(f"[{i}]adelay={ms}|{ms}[d{i}]")
flt.append("".join(f"[d{i}]" for i in range(len(lines))) + f"amix=inputs={len(lines)}:normalize=0,apad,atrim=0:{total},loudnorm=I=-16:TP=-2[o]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(flt), "-map", "[o]", "-ac", "1", "-ar", "48000", "assets/audio/vo.wav"], check=True)
print("total", total, timing)
PY

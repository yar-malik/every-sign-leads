#!/bin/bash
# Trim each line, place it at its timing.json start, write assets/audio/vo.wav (-17 LUFS) for a 60 s video.
set -e
cd "$(dirname "$0")/.."
for f in assets/vo/l*.wav; do
  ffmpeg -v error -y -i "$f" -af "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse" -ar 48000 "$f.t.wav" && mv "$f.t.wav" "$f"
done
python3 - <<'PY'
import json, subprocess
t = json.load(open("timing.json")); ids = sorted(t); inp, flt = [], []
for i, k in enumerate(ids):
    inp += ["-i", f"assets/vo/{k}.wav"]; ms = int(t[k] * 1000); flt.append(f"[{i}]adelay={ms}|{ms}[d{i}]")
flt.append("".join(f"[d{i}]" for i in range(len(ids))) + f"amix=inputs={len(ids)}:normalize=0,apad,atrim=0:60,loudnorm=I=-16:TP=-2[o]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(flt), "-map", "[o]", "-ac", "1", "-ar", "48000", "assets/audio/vo.wav"], check=True)
PY
python3 -c "
import json, subprocess, glob, os
d = {os.path.basename(f)[:-4]: round(float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f])), 3) for f in sorted(glob.glob('assets/vo/l*.wav'))}
json.dump(d, open('assets/vo/durations.json','w'), indent=0)"

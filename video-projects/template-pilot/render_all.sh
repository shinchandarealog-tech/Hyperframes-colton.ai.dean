#!/usr/bin/env bash
# Pilot renders: three templates with custom text, 30 fps, 180-degree motion blur.
set -e
cd "$(dirname "$0")"
T=../../tools/aep_port; S=../../_reference/templates/hook-captions/specs
python3 $T/render.py "$S/Render - Hook 01.json"    renders/hook01    --texts texts/hook01.json    --media "Media 01=assets/media_porch.mp4" --bg assets/bg_kitchen.mp4 --fps 30 --shutter 180 > renders/hook01.log 2>&1 &
python3 $T/render.py "$S/Render - Caption 01.json" renders/caption01 --texts texts/caption01.json --bg assets/bg_drone.mp4  --fps 30 --shutter 180 --duration 4 > renders/caption01.log 2>&1 &
python3 $T/render.py "$S/Render - Caption 02.json" renders/caption02 --texts texts/caption02.json --bg assets/bg_stairs.mp4 --fps 30 --shutter 180 --duration 4 > renders/caption02.log 2>&1 &
wait
tail -qn1 renders/*.log

# LUT Library — Color Grading

127 `.cube` 3D LUTs for grading footage with ffmpeg's `lut3d` filter (all verified to load). Shared across every project under `video-projects/` — reference them by relative path, no need to copy.

**Source:** "Luts – 183mb – FREE" Google Drive pack (Drive folder `1_iTc2Wp0DAof2C7A0c_dEldazhwMhVpL`). Filenames were normalized to kebab-case; the macOS `._` metadata file that shipped as `SLOG 2/23.cube` was dropped. The pack ships with no license file — check the original creators' terms before redistributing the LUTs themselves. Graded videos you export are yours.

## Layout

| Folder | Count | What it is | Input footage |
|---|---|---|---|
| `log-to-rec709/<brand>/` | 42 | **Technical conversion** LUTs (V1 + V2 per profile): Arri LogC, Blackmagic, Canon C-Log/2/3, DJI D-Log/D-Cinelike, Fujifilm F-Log, HLG/HLG 2/HLG 3, Kinefinity, Nikon N-Log, Panasonic V-Log/Cinelike-D, RED, Sony S-Log2/S-Log3/Cine 1/2/4 | Log / flat footage |
| `sony-slog-looks/slog2/` | 22 | Creative looks built for Sony S-Log2 | Sony S-Log2 |
| `sony-slog-looks/slog3/` | 3 | Cinematic Bright / Green / Movie for S-Log3 | Sony S-Log3 |
| `creative/pgs-film/` | 16 | PGS Professional Film looks | Rec.709 |
| `creative/pack-v1/` | 10 | Creative looks (warm / teal-orange leaning) | Rec.709 |
| `creative/pack-v2/` | 33 | Creative looks `v2-01`…`v2-30` + `blaugrun18`, `kupfer17`, `sauber16` | Rec.709 |
| `creative/money/` | 1 | CinePacks Moneyfx "Moolah" (heavy green stylization) | Rec.709 |

## Order of operations

1. **Log footage** (S-Log, V-Log, C-Log, D-Log, Apple-ish flat profiles…) → apply the matching `log-to-rec709/` LUT first.
2. **Then** a creative look on top (optionally blended).
3. **Normal Rec.709 footage** (phones, Instagram exports, standard profiles) → skip step 1, go straight to a creative look.

## Recipes (run from inside `video-projects/<project>/`)

```bash
L=../../assets/luts

# Creative look, full strength, audio untouched
ffmpeg -i assets/raw.mp4 -vf "lut3d=file=$L/creative/pack-v2/v2-17.cube:interp=tetrahedral,format=yuv420p" \
  -c:v libx264 -preset slow -crf 17 -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -c:a copy -movflags +faststart assets/graded.mp4

# Log → Rec.709 conversion, then a creative look
-vf "lut3d=file=$L/log-to-rec709/sony/sony-slog-3-to-rec-709-v1.cube:interp=tetrahedral,lut3d=file=$L/creative/pgs-film/pgs-film-08.cube:interp=tetrahedral"

# Blend a look at ~70% strength
-filter_complex "[0:v]split[a][b];[b]lut3d=file=$L/creative/pack-v2/v2-14.cube:interp=tetrahedral[g];[a][g]blend=all_expr='A*0.3+B*0.7',format=yuv420p"

# Quick test still before committing to a full render
ffmpeg -ss 5 -i assets/raw.mp4 -frames:v 1 -vf "lut3d=file=$L/creative/pgs-film/pgs-film-08.cube" renders/test-pgs08.png
```

Always pick a look on test stills first (3 representative frames: person, interior, exterior/sky), then grade the full clip, then review frames for blown highlights, crushed blacks, and skin tones.

## Field notes (tested on a bright real-estate tour, Rec.709 source)

| LUT | Verdict |
|---|---|
| `creative/pack-v2/v2-17.cube` | ⭐ Punchy & vivid — richer greens, warm wood, whites stay white. Great default for real estate / lifestyle. |
| `creative/pack-v2/v2-14.cube` | Warm & bright — golden wood, bluer sky. "Dream home" feel. |
| `creative/pgs-film/pgs-film-08.cube` | Clean cinematic — slightly muted, filmic contrast. Luxury/editorial. |
| `creative/pack-v2/v2-24.cube` | Warm-moody luxe — deeper shadows, rich wood. |
| `creative/pack-v2/sauber16.cube` | Subtle clean-up — safest, barely changes the image. |
| `creative/money/moolah.cube` | ❌ Neon green cast — stylized music-video use only. |
| `creative/pack-v2/v2-11.cube` | ❌ Crushes blacks on Rec.709 footage. |
| `creative/pack-v2/blaugrun18.cube` | ❌ Purple/magenta cast on Rec.709. |
| `creative/pack-v2/v2-27.cube`, `kupfer17.cube` | Heavily desaturated — moody/bleach-bypass only. |

The Sony S-Log looks and `log-to-rec709/` LUTs expect log input — on normal Rec.709 footage they'll look washed-out or over-contrasty. That's expected, not broken.

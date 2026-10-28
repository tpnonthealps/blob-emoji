[![Noto Emoji](images/noto.png)](https://www.patreon.com/posts/blob-emoji-pack-78280403)

# Build Noto Blob Emoji

> **Credit:** Original guide posted by **RKBDI** on Telegram: [t.me/rkbdiemoji/379](https://t.me/rkbdiemoji/379)

## Dependencies

### Linux (Debian/Ubuntu/WSL)
```bash
sudo apt update
sudo apt install python3 pkg-config pngquant zopfli libcairo2-dev imagemagick python3-venv gcc make
```

### macOS (Homebrew)
```bash
brew install python3 pkg-config pngquant zopfli cairo imagemagick gcc
```

### Setup Python Environment
Run inside the repo folder:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Customization
*   **Add PNGs:** Add new emojis to the `2D/png/128` folder.
    *   *Note: Modifying other resolution folders does not do anything at all.*
*   **Modify SVGs:** You can only replace existing files in the `2D/svg` folder.

## Source layout and bundled fonts

The 2D sources live in `2D/png/` and `2D/svg/`. Custom Blob artwork is
preserved there; new upstream emoji without Blob replacements use upstream
artwork. The `3D/` directory contains upstream Noto assets, not Blob designs.

The bundled files in `2D/fonts/` and `module/` are the existing Emoji 17
builds. Synchronizing the sources does not rebuild these binaries or add the
new upstream emoji to them. Rebuild the fonts below before packaging a new
release, and update the Android module separately.

## Build Process

### 1. Build CBDT/CBLC Font (Standard / PNG)
*Takes 5m – 2h depending on CPU*
```bash
time make -j BYPASS_SEQUENCE_CHECK='True'

# Move output
mv *.ttf 2D/fonts/
```

### 2. Build COLRv1 Font (Android 13+ / SVG)
```bash
(cd colrv1 && rm -rf build/ && time nanoemoji *.toml)

# Copy output
cp colrv1/build/NotoColorEmoji.ttf 2D/fonts/Noto-COLRv1.ttf
cp colrv1/build/NotoColorEmoji-noflags.ttf 2D/fonts/Noto-COLRv1-noflags.ttf
```

### 3. Fix ZWJ Sequences
```bash
python colrv1_postproc.py
```

## Done
Find your fonts in the `2D/fonts/` folder.
*   **Troubleshooting:** If build fails, check logs for corrupt emojis in `2D/png/` or `build/compressed_pngs` and remove them.
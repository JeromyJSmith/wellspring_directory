# Wellspring Book Gold Flake Batch Tool

This tool ensures all chapter title images are consistently styled with the approved dark leather background and gold flake texture.

## Structure
- `input_images/`: Drop your raw PNGs here
- `textures/`: Must contain `background - 01.png` and `gold_flake_texture.png`
- `scripts/`: Python script for texture compositing
- `batch_process.sh`: Shell script for automated processing
- `processed_images/`: Outputs are saved here

## Usage
```bash
bash batch_process.sh
```
Make sure your gold texture and background are in `textures/`.

Requires: Python 3, Pillow

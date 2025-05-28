#!/bin/bash

mkdir -p processed_images

for file in input_images/*.png; do
  echo "Processing $file..."
  python3 scripts/apply_gold_texture.py "$file" "processed_images/$(basename "$file")"
done

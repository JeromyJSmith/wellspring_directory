#!/usr/bin/env python3
"""Debug script to see what chapters are available"""

from pathlib import Path

def debug_chapters():
    input_dir = Path("input_chapters")
    all_files = list(input_dir.glob("*.md"))
    
    print(f"Found {len(all_files)} total .md files")
    
    # Filter out test files
    non_test_files = [f for f in all_files if not f.name.startswith("test")]
    print(f"Found {len(non_test_files)} non-test files")
    
    # Get unique chapters
    unique_chapters = []
    seen_chapters = set()
    
    for file in sorted(non_test_files):
        print(f"Processing: {file.name}")
        
        # Extract chapter number/identifier
        base_name = file.stem.replace('New Wellspring-20250503-', '')
        print(f"  Base name: {base_name}")
        
        if ' copy' in base_name:
            base_name = base_name.replace(' copy', '')
            print(f"  After removing ' copy': {base_name}")
        
        if base_name not in seen_chapters:
            seen_chapters.add(base_name)
            # Prefer the non-copy version
            if ' copy' not in file.stem:
                unique_chapters.append(file)
                print(f"  ✅ Added (non-copy): {file.name}")
            elif len([f for f in non_test_files if base_name in f.stem and ' copy' not in f.stem]) == 0:
                # Only use copy if no original exists
                unique_chapters.append(file)
                print(f"  ✅ Added (copy only): {file.name}")
            else:
                print(f"  ⏭️ Skipped (copy, original exists)")
        else:
            print(f"  ⏭️ Skipped (already seen)")
    
    print(f"\nFinal unique chapters: {len(unique_chapters)}")
    for i, ch in enumerate(unique_chapters, 1):
        print(f"{i:2d}. {ch.name}")
    
    return unique_chapters

if __name__ == "__main__":
    debug_chapters() 
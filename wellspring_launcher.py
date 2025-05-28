#!/usr/bin/env python3
"""
Wellspring Integrated Launcher
==============================

Combines Python chapter formatting with AppleScript automation
for a seamless Wellspring manuscript formatting workflow.

Features:
- Runs chapter formatting agent
- Triggers AppleScript automation
- Provides interactive menu system
- Handles error recovery and logging
"""

import subprocess
import sys
import os
from pathlib import Path
import json
from datetime import datetime

class WellspringLauncher:
    """
    Integrated launcher for Wellspring chapter formatting and automation
    """
    
    def __init__(self):
        self.workspace_dir = Path("/Users/ojeromyo/Desktop/wellspring_directory")
        self.output_dir = self.workspace_dir / "output"
        self.applescript_path = self.workspace_dir / "wellspring_applescript_automation.scpt"
        
    def print_banner(self):
        """Print the Wellspring launcher banner"""
        print("\n" + "="*70)
        print("🌊 WELLSPRING INTEGRATED FORMATTING LAUNCHER")
        print("="*70)
        print("   Automated chapter formatting + AppleScript workflow")
        print("   📚 Processes: margins, chapters, iconography, layouts")
        print("   🎨 Automates: InDesign, PDF conversion, file organization")
        print("="*70)
    
    def show_menu(self):
        """Display the main menu"""
        print("\n📋 WELLSPRING LAUNCHER MENU:")
        print("   1. 🔍 Preview formatting changes (safe)")
        print("   2. 🎯 Generate all 6 formats (.jsx, .json, .txt, .xml, .idml, .html)")
        print("   3. 🚀 Full workflow: Generate + AppleScript automation")
        print("   4. 🎨 AppleScript automation only (use existing files)")
        print("   5. 📂 Open output folder")
        print("   6. 🔧 Quick launcher menu")
        print("   7. ❌ Exit")
        
        choice = input("\n👉 Choose an option (1-7): ").strip()
        return choice
    
    def run_chapter_formatting(self, preview_mode=False):
        """Run the chapter formatting agent"""
        print(f"\n{'🔍 PREVIEW MODE' if preview_mode else '🎯 FORMATTING MODE'}")
        print("="*50)
        
        try:
            cmd = ["python", "chapter_formatting_agent.py"]
            if preview_mode:
                cmd.append("--preview")
            
            # Change to workspace directory
            os.chdir(self.workspace_dir)
            
            # Run the chapter formatting agent
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Chapter formatting completed successfully!")
                if not preview_mode:
                    self.log_completion()
                return True
            else:
                print(f"❌ Chapter formatting failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error running chapter formatting: {e}")
            return False
    
    def run_applescript_automation(self):
        """Run the AppleScript automation"""
        print("\n🎨 APPLESCRIPT AUTOMATION")
        print("="*50)
        
        if not self.applescript_path.exists():
            print(f"❌ AppleScript file not found: {self.applescript_path}")
            return False
        
        try:
            # Run the AppleScript
            result = subprocess.run(
                ["osascript", str(self.applescript_path)], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                print("✅ AppleScript automation completed!")
                return True
            else:
                print(f"❌ AppleScript failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error running AppleScript: {e}")
            return False
    
    def full_workflow(self):
        """Run the complete workflow: formatting + automation"""
        print("\n🚀 FULL WELLSPRING WORKFLOW")
        print("="*50)
        
        # Step 1: Generate formats
        if self.run_chapter_formatting(preview_mode=False):
            
            # Step 2: Run AppleScript automation
            print("\n⏳ Starting AppleScript automation in 3 seconds...")
            print("   (This will open InDesign, create PDFs, and organize files)")
            
            import time
            time.sleep(3)
            
            if self.run_applescript_automation():
                print("\n🎉 COMPLETE WELLSPRING WORKFLOW FINISHED!")
                print("   ✅ All 6 formats generated")
                print("   ✅ InDesign script executed")
                print("   ✅ PDF instructions created")
                print("   ✅ Files opened for review")
                print("   ✅ Workspace organized")
                return True
            else:
                print("\n⚠️ Formatting completed but AppleScript automation failed")
                return False
        else:
            print("\n❌ Chapter formatting failed - skipping AppleScript automation")
            return False
    
    def applescript_quick_launcher(self):
        """Run AppleScript quick launcher menu"""
        print("\n🔧 APPLESCRIPT QUICK LAUNCHER")
        print("="*50)
        
        try:
            # Run AppleScript with quick launcher function
            applescript_code = """
            tell application "System Events"
                do shell script "osascript -e 'tell application \\"System Events\\" to display dialog \\"🌊 Wellspring Quick Launcher\\n\\nChoose a task to automate:\\" buttons {\\"🎨 InDesign Only\\", \\"📋 PDF Only\\", \\"📂 Open Files\\", \\"🔄 Full Workflow\\"} default button \\"🔄 Full Workflow\\"'"
            end tell
            """
            
            result = subprocess.run(
                ["osascript", "-e", applescript_code], 
                capture_output=True, 
                text=True
            )
            
            print("✅ Quick launcher opened!")
            return True
            
        except Exception as e:
            print(f"❌ Error opening quick launcher: {e}")
            return False
    
    def open_output_folder(self):
        """Open the output folder in Finder"""
        try:
            subprocess.run(["open", str(self.output_dir)])
            print("✅ Output folder opened in Finder")
            return True
        except Exception as e:
            print(f"❌ Error opening output folder: {e}")
            return False
    
    def log_completion(self):
        """Log completion to database and files"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Count output files
        output_files = list(self.output_dir.glob("wellspring*"))
        
        log_entry = {
            "timestamp": timestamp,
            "files_generated": len(output_files),
            "formats": ["jsx", "json", "txt", "xml", "idml", "html"],
            "status": "completed"
        }
        
        # Save to log file
        log_file = self.workspace_dir / "wellspring_launcher.log"
        with open(log_file, "a") as f:
            f.write(f"{timestamp} - Completed formatting with {len(output_files)} files\n")
        
        print(f"📝 Logged completion: {len(output_files)} files generated")
    
    def run(self):
        """Main launcher loop"""
        self.print_banner()
        
        while True:
            choice = self.show_menu()
            
            if choice == "1":
                self.run_chapter_formatting(preview_mode=True)
                
            elif choice == "2":
                self.run_chapter_formatting(preview_mode=False)
                
            elif choice == "3":
                self.full_workflow()
                
            elif choice == "4":
                self.run_applescript_automation()
                
            elif choice == "5":
                self.open_output_folder()
                
            elif choice == "6":
                self.applescript_quick_launcher()
                
            elif choice == "7":
                print("\n👋 Goodbye! Happy formatting!")
                break
                
            else:
                print("\n❌ Invalid choice. Please choose 1-7.")
            
            input("\n⏸️  Press Enter to continue...")

def main():
    """Main entry point"""
    launcher = WellspringLauncher()
    launcher.run()

if __name__ == "__main__":
    main() 
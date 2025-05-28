# 🍎 WELLSPRING APPLESCRIPT AUTOMATION GUIDE

## 🌊 **Complete Automation Workflow**

With your new AppleScript MCP integration, you can now **fully automate** the
Wellspring chapter formatting process from Python generation to final InDesign
implementation!

---

## 🚀 **Available Automation Tasks**

### **1. 🎯 FULL WORKFLOW AUTOMATION**

```bash
python wellspring_launcher.py
# Choose option 3: 🚀 Full workflow
```

**What it does:**

- ✅ Generates all 6 formats (.jsx, .json, .txt, .xml, .idml, .html)
- 🎨 Opens InDesign and runs formatting script automatically
- 📋 Converts HTML to PDF with proper styling
- 📂 Opens all files in appropriate applications for review
- 📁 Creates timestamped backups
- 🔄 Organizes workspace for efficient workflow

### **2. 🔍 SAFE PREVIEW MODE**

```bash
python wellspring_launcher.py
# Choose option 1: 🔍 Preview formatting changes
```

**What it shows:**

- 📊 Complete breakdown of all 315 formatting changes
- 📋 Margin adjustments (+3 points on all sides)
- 🎨 Typography changes (Minion Pro, 24pt, colors)
- 📖 Chapter-specific formatting details
- 🏗️ Architectural element specifications
- 📜 All 6 export formats that will be generated

### **3. 🎨 INDESIGN-ONLY AUTOMATION**

```bash
python wellspring_launcher.py
# Choose option 4: 🎨 AppleScript automation only
```

**What it does:**

- 🎯 Opens Adobe InDesign 2024
- 📄 Prompts for document selection (or creates new)
- 🔧 Automatically runs the wellspring_chapter_formatting.jsx script
- ✅ Applies all margin, typography, and layout changes
- 🏗️ Places architectural corner elements on every page
- 📊 Ensures right-hand chapter starts with blank page insertion

---

## 📂 **File Automation Matrix**

| **Format**   | **Auto-Opens In** | **AppleScript Action**      | **Review Ready**   |
| ------------ | ----------------- | --------------------------- | ------------------ |
| 📝 **.jsx**  | Adobe InDesign    | ✅ **Runs automatically**   | Script executed    |
| 📊 **.json** | Code editor       | 📂 Opens for inspection     | Data review        |
| 📄 **.txt**  | TextEdit          | 📖 Human-readable specs     | Quick reference    |
| 🏗️ **.xml**  | Xcode/XML editor  | 📋 Structured data view     | Technical review   |
| 🎨 **.idml** | Adobe InDesign    | 🎯 **Template import**      | Style application  |
| 📋 **.html** | Safari → PDF      | 📑 **Auto-converts to PDF** | Final instructions |

---

## 🎮 **Quick Command Reference**

### **Instant Full Automation:**

```bash
# One command does everything!
python wellspring_launcher.py
# Then choose: 3 (Full workflow)
```

### **Preview First, Then Apply:**

```bash
# Step 1: Safe preview
python wellspring_launcher.py  # Choose: 1 (Preview)

# Step 2: Generate formats  
python wellspring_launcher.py  # Choose: 2 (Generate)

# Step 3: Automate applications
python wellspring_launcher.py  # Choose: 4 (AppleScript only)
```

### **Direct AppleScript Execution:**

```bash
# Run AppleScript directly
osascript wellspring_applescript_automation.scpt

# Or use the quick launcher
osascript -e 'tell application "Finder" to display dialog "🌊 Quick Launcher" buttons {"🎨 InDesign", "📋 PDF", "📂 Files", "🔄 Full"}'
```

---

## 🔧 **Individual Task Automation**

### **InDesign Script Automation Only:**

- 🎯 Opens InDesign
- 📄 Loads your manuscript
- 🔧 Runs formatting script
- ✅ Applies all 315 changes

### **PDF Generation Only:**

- 📋 Opens HTML in Safari
- 🖨️ Auto-prints to PDF
- 📁 Saves to output folder
- 📑 Creates "Wellspring_Formatting_Instructions.pdf"

### **File Organization Only:**

- 📂 Opens all files in appropriate apps
- 📁 Creates timestamped backups
- 🔄 Organizes workspace
- 📊 Logs completion status

---

## 🏗️ **What Gets Automated in InDesign:**

When AppleScript runs your .jsx formatting script:

### **📐 Margin Automation:**

```javascript
marginPrefs.top = "54pt"; // +3 from 51pt
marginPrefs.bottom = "54pt"; // +3 from 51pt
marginPrefs.inside = "57pt"; // +3 from 54pt
marginPrefs.outside = "57pt"; // +3 from 54pt
```

### **📖 Chapter Page Management:**

- ✅ Detects current chapter start pages
- 👉 Ensures all chapters begin on right-hand pages
- 📄 Inserts blank pages automatically as needed
- 🎨 Applies chapter-specific styling and colors

### **🏗️ Architectural Corner Placement:**

- 🔲 18×18 point corner elements
- 🎨 Dark blue (#1B365D) styling
- 📍 Consistent placement on every page
- 🔧 Automated across entire 300+ page document

### **🎯 Typography Application:**

- 🖋️ Minion Pro font for chapter titles
- 📏 24pt chapter title sizing
- 🎨 Dark blue/gold color scheme
- 📊 Consistent formatting hierarchy

---

## 📊 **Automation Success Metrics**

After running the full workflow, you'll have:

- ✅ **6 formats generated** (.jsx, .json, .txt, .xml, .idml, .html)
- ✅ **315 formatting changes applied** to your manuscript
- ✅ **PDF instructions created** for team reference
- ✅ **Workspace organized** with timestamped backups
- ✅ **All files opened** for immediate review
- ✅ **Complete audit trail** maintained in logs

---

## 🎉 **Success! Your Wellspring Workflow is Now Fully Automated!**

### **🌊 From Request to Implementation:**

1. **📋 Brian's requests**: Right-hand chapters, +3pt margins, iconography
2. **🐍 Python processing**: Chapter analysis, format generation, specifications
3. **🍎 AppleScript automation**: InDesign execution, PDF creation, file
   management
4. **✅ Final result**: Professional manuscript with all formatting applied

### **⚡ One-Click Solution:**

```bash
python wellspring_launcher.py  # Choose option 3
```

**Total automation time**: ~2-3 minutes for complete 300+ page formatting! 🚀

---

## 🆘 **Troubleshooting**

### **Common Issues & Solutions:**

**❌ "InDesign not found"**

- ✅ Ensure Adobe InDesign 2024 is installed
- ✅ Update script to match your InDesign version

**❌ "AppleScript permissions"**

- ✅ Go to System Preferences → Privacy & Security → Automation
- ✅ Allow Terminal/Script Editor to control InDesign and Safari

**❌ "No output files found"**

- ✅ Run chapter formatting agent first: `python chapter_formatting_agent.py`
- ✅ Check output folder exists:
  `/Users/ojeromyo/Desktop/wellspring_directory/output/`

**❌ "Script execution failed"**

- ✅ Check InDesign document is open
- ✅ Verify script file permissions: `chmod +x *.scpt`

---

**🎯 Your Wellspring manuscript formatting is now completely automated from
start to finish!** 🌊✨

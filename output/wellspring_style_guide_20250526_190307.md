
# 🎯 WELLSPRING PROFESSIONAL STYLE GUIDE
## Brian's Formatting Specifications

**Generated:** 2025-05-26 19:03:07
**For:** The Wellspring - 300+ page manuscript

---

## 📐 MARGIN SPECIFICATIONS

| Element | Current | Brian's Spec | Change |
|---------|---------|-------------|---------|
| **Top Margin** | 51pt | **54pt** | **+3pt** |
| **Bottom Margin** | 51pt | **54pt** | **+3pt** |
| **Left Margin** | 54pt | **57pt** | **+3pt** |
| **Right Margin** | 54pt | **57pt** | **+3pt** |

### Implementation:
```javascript
// InDesign Script
doc.marginPreferences.top = "54pt";
doc.marginPreferences.bottom = "54pt"; 
doc.marginPreferences.left = "57pt";
doc.marginPreferences.right = "57pt";
```

---

## 📚 CHAPTER LAYOUT REQUIREMENTS

### ✅ Right-Hand Chapter Starts
- **All chapters must begin on odd-numbered pages (right-hand)**
- Insert blank pages as needed before chapter starts
- Maintains professional book layout standards

### 🏗️ Architectural Corner Elements  
- **Size:** 18pt × 18pt squares
- **Color:** #1B365D (Dark blue - Wellspring brand)
- **Position:** Top-left corner of chapter pages
- **Style:** Solid fill, no stroke

---

## 🎨 TYPOGRAPHY HIERARCHY

### Chapter Titles
- **Font:** Minion Pro Bold
- **Size:** 24pt
- **Color:** #1B365D (Dark blue)
- **Alignment:** Centered
- **Space After:** 20pt

### Body Text
- **Font:** Minion Pro Regular  
- **Size:** 11pt
- **Leading:** 14pt (127% of font size)
- **Color:** Black
- **Paragraph Spacing:** 12pt after

### Section Headers
- **Font:** Minion Pro Semibold
- **Size:** 14pt
- **Color:** #8B6914 (Gold accent)
- **Space Before:** 18pt
- **Space After:** 12pt

---

## 🎯 PROFESSIONAL STANDARDS

### Page Layout
- **Facing pages** with proper gutters
- **Consistent baseline grid** alignment
- **Professional widows/orphans** control
- **Proper hyphenation** settings

### Color Palette
- **Primary:** #1B365D (Wellspring Dark Blue)
- **Accent:** #8B6914 (Professional Gold)
- **Body Text:** #000000 (True Black)
- **Background:** #FFFFFF (Pure White)

### Quality Checks
- ✅ All images 300 DPI minimum
- ✅ Fonts properly embedded
- ✅ Color profiles consistent
- ✅ Bleeds set correctly (0.125")

---

## 🔧 IMPLEMENTATION STRATEGY

### Phase 1: Margin Adjustment (SAFE)
1. Create backup of original file
2. Apply +3pt margin increases
3. Verify text reflow is acceptable
4. Save as new version

### Phase 2: Chapter Layout (MANUAL)
1. Identify all chapter starts
2. Insert pages to ensure right-hand starts
3. Apply architectural corner elements
4. Verify page numbering

### Phase 3: Typography Polish (CAREFUL)
1. Update paragraph styles
2. Apply consistent font hierarchy  
3. Adjust spacing and alignment
4. Final quality review

---

## 🛡️ SAFETY PROTOCOLS

- ✅ **Always backup** before major changes
- ✅ **Test on single spread** before applying to all
- ✅ **Version control** with timestamps
- ✅ **Preview outputs** before final approval
- ✅ **Document all changes** for reproducibility

**This is a REAL 300+ page professional publication.**
**Every change must maintain publication quality.**
        
// Manual TOC Spacing - Works on Selected Text
// SIMPLE: Select TOC text first, then run this script

#target indesign

function adjustSelectedTextSpacing() {
    // Safety checks
    if (app.documents.length === 0) {
        alert("❌ Please open the Wellspring manuscript first.");
        return false;
    }
    
    var doc = app.activeDocument;
    
    // Check if user has text selected
    if (app.selection.length === 0) {
        alert("📋 SELECT TOC TEXT FIRST\n\n" +
              "How to use:\n" +
              "1. Select the Table of Contents text in InDesign\n" +
              "2. Run this script\n" +
              "3. The selected text will get better spacing\n\n" +
              "Please select some text and try again.");
        return false;
    }
    
    var selection = app.selection[0];
    
    // Check if it's text
    if (selection.constructor.name !== "Text") {
        alert("⚠️ Please select actual text (not a text frame)\n\n" +
              "1. Use the Text tool (T)\n" +
              "2. Select/highlight the TOC text\n" +
              "3. Run this script again");
        return false;
    }
    
    // Show what we'll do
    var proceed = confirm("🎯 ADJUST SPACING FOR SELECTED TEXT\n\n" +
                         "Selected: " + selection.contents.substring(0, 50) + "...\n\n" +
                         "This will apply:\n" +
                         "• Leading: 16pt (line spacing)\n" +
                         "• Space After: 8pt\n" +
                         "• Keep alignment intact\n\n" +
                         "Proceed with spacing adjustment?");
    
    if (!proceed) {
        alert("Spacing adjustment cancelled.");
        return false;
    }
    
    try {
        // Get the paragraphs in the selection
        var paragraphs = selection.paragraphs;
        var updatedCount = 0;
        
        for (var i = 0; i < paragraphs.length; i++) {
            var para = paragraphs[i];
            
            // Store original for reference
            var originalLeading = para.leading;
            var originalSpaceAfter = para.spaceAfter;
            
            // Apply improved spacing
            para.leading = 16;        // Better line spacing
            para.spaceAfter = 8;      // Space between entries
            
            updatedCount++;
            
            $.writeln("Updated paragraph " + (i+1) + ": leading " + originalLeading + " → 16pt");
        }
        
        alert("✅ SPACING UPDATED!\n\n" +
              "Updated " + updatedCount + " paragraphs\n" +
              "• Leading: 16pt\n" +
              "• Space After: 8pt\n\n" +
              "Review the changes and save if satisfied.");
        
        return true;
        
    } catch (error) {
        alert("❌ Error adjusting spacing: " + error.message);
        return false;
    }
}

// Execute the spacing adjustment
adjustSelectedTextSpacing(); 
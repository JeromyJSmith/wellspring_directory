
// Wellspring Margins-Only Formatter
// SAFEST FIRST STEP: Only margin adjustments, no other changes
// Generated: 2025-05-26 19:08:37

#target indesign

function applyMarginsOnly() {
    // Safety checks
    if (app.documents.length === 0) {
        alert("❌ Please open the Wellspring manuscript first.");
        return false;
    }
    
    var doc = app.activeDocument;
    
    // Show current margins first
    var currentMargins = doc.marginPreferences;
    var marginInfo = "CURRENT MARGINS:\n" +
                    "Top: " + currentMargins.top + "\n" +
                    "Bottom: " + currentMargins.bottom + "\n" +
                    "Left: " + currentMargins.left + "\n" +
                    "Right: " + currentMargins.right + "\n\n" +
                    "BRIAN'S NEW MARGINS (+3pt):\n" +
                    "Top: 54pt\n" +
                    "Bottom: 54pt\n" +
                    "Left: 57pt\n" +
                    "Right: 57pt\n\n" +
                    "This will ONLY change margins - no other formatting.\n" +
                    "Proceed?";
    
    var proceed = confirm(marginInfo);
    
    if (!proceed) {
        alert("Margins update cancelled.");
        return false;
    }
    
    try {
        // Store original values for logging
        var original = {
            top: currentMargins.top,
            bottom: currentMargins.bottom,
            left: currentMargins.left,
            right: currentMargins.right
        };
        
        // Apply ONLY Brian's margin specifications
        currentMargins.top = "54pt";
        currentMargins.bottom = "54pt";
        currentMargins.left = "57pt";
        currentMargins.right = "57pt";
        
        // Success message
        alert("✅ MARGINS UPDATED SUCCESSFULLY!\n\n" +
              "Changes applied:\n" +
              "• Top: " + original.top + " → 54pt\n" +
              "• Bottom: " + original.bottom + " → 54pt\n" +
              "• Left: " + original.left + " → 57pt\n" +
              "• Right: " + original.right + " → 57pt\n\n" +
              "NEXT STEPS:\n" +
              "1. Review 2-3 spreads for text reflow\n" +
              "2. Check that no content is cut off\n" +
              "3. Save document when satisfied\n" +
              "4. Run next section: TOC formatting");
        
        return true;
        
    } catch (error) {
        alert("❌ Error updating margins: " + error.message);
        return false;
    }
}

// Execute the margins-only update
applyMarginsOnly();
        
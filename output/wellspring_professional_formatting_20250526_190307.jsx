
// Wellspring Professional Formatting Script
// SAFE version for 300+ page real manuscript
// Generated: 2025-05-26 19:03:07

#target indesign

function formatWellspringManuscript() {
    // Safety checks
    if (app.documents.length === 0) {
        alert("❌ Please open the Wellspring manuscript first.");
        return false;
    }
    
    var doc = app.activeDocument;
    var originalName = doc.name;
    
    // Confirm with user
    var proceed = confirm(
        "🌊 WELLSPRING PROFESSIONAL FORMATTING\n\n" +
        "This will apply Brian's specifications:\n" +
        "• +3pt margin increases (54pt/57pt)\n" +
        "• Professional typography improvements\n" +
        "• Safe architectural corner elements\n\n" +
        "⚠️  BACKUP RECOMMENDED FIRST!\n\n" +
        "Proceed with formatting?"
    );
    
    if (!proceed) {
        alert("Formatting cancelled.");
        return false;
    }
    
    try {
        // Step 1: Apply Brian's margin specifications (+3pt all around)
        applySafeMarginsUpdate(doc);
        
        // Step 2: Update master page elements safely
        updateMasterPageElements(doc);
        
        // Step 3: Apply professional typography
        applyProfessionalTypography(doc);
        
        alert("✅ WELLSPRING FORMATTING COMPLETE!\n\n" +
              "Applied Brian's specifications:\n" +
              "• Margins: +3pt all sides\n" +
              "• Professional typography\n" +
              "• Master page improvements\n\n" +
              "Review the document and save when satisfied.");
        
        return true;
        
    } catch (error) {
        alert("❌ Error during formatting: " + error.message + 
              "\n\nNo changes have been saved.\nPlease check your document and try again.");
        return false;
    }
}

function applySafeMarginsUpdate(doc) {
    // Apply Brian's +3pt margin specifications SAFELY
    var margins = doc.marginPreferences;
    
    // Store original values for reference
    var original = {
        top: margins.top,
        bottom: margins.bottom,
        left: margins.left,
        right: margins.right
    };
    
    // Apply Brian's specifications (+3pt)
    margins.top = "54pt";
    margins.bottom = "54pt";
    margins.left = "57pt";
    margins.right = "57pt";
    
    // Log the change (for debugging)
    $.writeln("Margins updated: " + original.top + "→" + margins.top + 
              ", " + original.left + "→" + margins.left);
}

function updateMasterPageElements(doc) {
    // Update master pages with professional elements
    var masters = doc.masterSpreads;
    
    for (var i = 0; i < masters.length; i++) {
        var master = masters[i];
        
        // Add architectural corner elements to master pages
        for (var j = 0; j < master.pages.length; j++) {
            var page = master.pages[j];
            addArchitecturalCorner(page);
        }
    }
}

function addArchitecturalCorner(page) {
    // Add safe architectural corner element
    try {
        var corner = page.rectangles.add();
        
        // Position in top-left corner (safe positioning)
        corner.geometricBounds = [
            0,  // top
            0,  // left  
            18,  // bottom (18pt)
            18   // right (18pt)
        ];
        
        // Apply Wellspring brand color safely
        try {
            var wellspringBlue = doc.colors.itemByName("Wellspring Blue");
        } catch (e) {
            // Create color if it doesn't exist
            wellspringBlue = doc.colors.add();
            wellspringBlue.name = "Wellspring Blue";
            wellspringBlue.model = ColorModel.PROCESS;
            wellspringBlue.colorValue = [85, 70, 0, 15]; // CMYK for #1B365D
        }
        
        corner.fillColor = wellspringBlue;
        corner.strokeWeight = 0;
        
    } catch (error) {
        $.writeln("Corner element warning: " + error.message);
        // Don't fail the whole script for corner elements
    }
}

function applyProfessionalTypography(doc) {
    // Apply professional typography improvements
    var paragraphStyles = doc.paragraphStyles;
    
    // Update chapter title style
    try {
        var chapterStyle = paragraphStyles.itemByName("Chapter Title");
        chapterStyle.appliedFont = app.fonts.itemByName("Minion Pro");
        chapterStyle.pointSize = 24;
    } catch (e) {
        $.writeln("Chapter style update: " + e.message);
    }
    
    // Update body text style  
    try {
        var bodyStyle = paragraphStyles.itemByName("Body Text");
        bodyStyle.appliedFont = app.fonts.itemByName("Minion Pro");
        bodyStyle.pointSize = 11;
        bodyStyle.leading = 14;
    } catch (e) {
        $.writeln("Body style update: " + e.message);
    }
}

// Execute the main function
formatWellspringManuscript();
        
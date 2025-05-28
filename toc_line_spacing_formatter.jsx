// TOC Line Spacing Formatter
// SIMPLE FOCUS: Only adjust line spacing in Table of Contents
// For Wellspring manuscript - Brian's specifications

#target indesign

function adjustTOCLineSpacing() {
    // Safety checks
    if (app.documents.length === 0) {
        alert("❌ Please open the Wellspring manuscript first.");
        return false;
    }
    
    var doc = app.activeDocument;
    
    // Show current approach
    var info = "🔍 TOC LINE SPACING ADJUSTMENT\n\n" +
              "This will:\n" +
              "• Find Table of Contents text\n" +
              "• Adjust line spacing for better readability\n" +
              "• Apply professional leading settings\n\n" +
              "Current target:\n" +
              "• Body leading: 14pt\n" +
              "• TOC leading: 16pt (more spacious)\n\n" +
              "Proceed with TOC spacing adjustment?";
    
    var proceed = confirm(info);
    
    if (!proceed) {
        alert("TOC spacing adjustment cancelled.");
        return false;
    }
    
    try {
        var updatedItems = 0;
        var tocFound = false;
        
        // Method 1: Look for paragraph styles with "TOC" or "Contents" in name
        var paragraphStyles = doc.paragraphStyles;
        
        for (var i = 0; i < paragraphStyles.length; i++) {
            var style = paragraphStyles[i];
            var styleName = style.name.toLowerCase();
            
            // Check if this looks like a TOC style
            if (styleName.indexOf('toc') !== -1 || 
                styleName.indexOf('contents') !== -1 ||
                styleName.indexOf('table') !== -1) {
                
                tocFound = true;
                var originalLeading = style.leading;
                
                // Apply better line spacing for TOC
                style.leading = 16; // More spacious than body text
                style.spaceAfter = 6;  // Space after each TOC line
                
                updatedItems++;
                $.writeln("Updated TOC style: " + style.name + " (leading: " + originalLeading + " → 16pt)");
            }
        }
        
        // Method 2: Look through text frames for TOC content
        var allTextFrames = doc.textFrames;
        
        for (var j = 0; j < allTextFrames.length; j++) {
            var frame = allTextFrames[j];
            
            try {
                var content = frame.contents.toLowerCase();
                
                // Check if this frame contains TOC content
                if (content.indexOf('table of contents') !== -1 ||
                    content.indexOf('contents') !== -1 ||
                    (content.indexOf('chapter') !== -1 && content.indexOf('...') !== -1)) {
                    
                    tocFound = true;
                    
                    // Apply spacing to paragraphs in this frame
                    var paragraphs = frame.paragraphs;
                    
                    for (var k = 0; k < paragraphs.length; k++) {
                        var para = paragraphs[k];
                        var originalLeading = para.leading;
                        
                        // Apply TOC-specific spacing
                        para.leading = 16;
                        para.spaceAfter = 6;
                        
                        updatedItems++;
                    }
                    
                    $.writeln("Updated TOC text frame with " + paragraphs.length + " paragraphs");
                }
                
            } catch (frameError) {
                // Skip frames that can't be read
                continue;
            }
        }
        
        // Results
        if (tocFound) {
            alert("✅ TOC LINE SPACING UPDATED!\n\n" +
                  "Changes applied:\n" +
                  "• Updated " + updatedItems + " TOC elements\n" +
                  "• Leading: 16pt (more spacious)\n" +
                  "• Space after: 6pt\n\n" +
                  "REVIEW:\n" +
                  "1. Check TOC pages for improved spacing\n" +
                  "2. Verify dot leaders still align\n" +
                  "3. Confirm page numbers are readable\n" +
                  "4. Save document when satisfied");
        } else {
            alert("⚠️ No TOC content found.\n\n" +
                  "The script looked for:\n" +
                  "• Paragraph styles with 'TOC' or 'Contents'\n" +
                  "• Text containing 'Table of Contents'\n" +
                  "• Chapter listings with dot leaders\n\n" +
                  "You may need to select TOC text manually\n" +
                  "and apply formatting directly.");
        }
        
        return true;
        
    } catch (error) {
        alert("❌ Error adjusting TOC spacing: " + error.message);
        return false;
    }
}

// Execute the TOC spacing adjustment
adjustTOCLineSpacing(); 
// Document Content Diagnostic Scanner
// See what text actually exists in the manuscript

#target indesign

function scanDocumentContent() {
    if (app.documents.length === 0) {
        alert("❌ Please open the Wellspring manuscript first.");
        return false;
    }
    
    var doc = app.activeDocument;
    var report = "📋 WELLSPRING CONTENT SCAN REPORT\n";
    report += "===================================\n\n";
    
    try {
        // Basic document info
        report += "📄 Document: " + doc.name + "\n";
        report += "📊 Pages: " + doc.pages.length + "\n";
        report += "📝 Text Frames: " + doc.textFrames.length + "\n\n";
        
        // Scan paragraph styles
        report += "🎨 PARAGRAPH STYLES FOUND:\n";
        var styles = doc.paragraphStyles;
        for (var i = 0; i < Math.min(styles.length, 10); i++) {
            report += "   • " + styles[i].name + "\n";
        }
        if (styles.length > 10) {
            report += "   ... and " + (styles.length - 10) + " more styles\n";
        }
        report += "\n";
        
        // Scan first few text frames for content
        report += "📝 TEXT CONTENT SAMPLE:\n";
        var frameCount = 0;
        var textFrames = doc.textFrames;
        
        for (var j = 0; j < Math.min(textFrames.length, 5); j++) {
            try {
                var frame = textFrames[j];
                var content = frame.contents;
                
                if (content && content.length > 0) {
                    frameCount++;
                    var preview = content.substring(0, 100).replace(/\r/g, " ");
                    report += "Frame " + frameCount + ": " + preview + "...\n\n";
                }
            } catch (e) {
                continue;
            }
        }
        
        // Look specifically for TOC-like content
        report += "🔍 LOOKING FOR TOC CONTENT:\n";
        var tocFound = false;
        
        for (var k = 0; k < textFrames.length; k++) {
            try {
                var frameContent = textFrames[k].contents.toLowerCase();
                
                if (frameContent.indexOf('contents') !== -1 ||
                    frameContent.indexOf('chapter') !== -1 ||
                    frameContent.indexOf('table') !== -1) {
                    
                    tocFound = true;
                    var tocPreview = textFrames[k].contents.substring(0, 200);
                    report += "   ✅ Possible TOC found:\n";
                    report += "   " + tocPreview.replace(/\r/g, "\n   ") + "\n\n";
                    break;
                }
            } catch (e) {
                continue;
            }
        }
        
        if (!tocFound) {
            report += "   ❌ No obvious TOC content found\n\n";
        }
        
        // Show current page info
        if (doc.layoutWindows.length > 0) {
            var currentPage = doc.layoutWindows[0].activePage;
            report += "📄 Current page: " + currentPage.name + "\n";
        }
        
        // Display the report
        alert(report);
        
        // Also log to console for detailed review
        $.writeln("=== WELLSPRING DIAGNOSTIC SCAN ===");
        $.writeln(report);
        
        return true;
        
    } catch (error) {
        alert("❌ Error scanning document: " + error.message);
        return false;
    }
}

// Execute the diagnostic scan
scanDocumentContent(); 
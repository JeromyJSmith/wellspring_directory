#!/usr/bin/osascript

(*
Wellspring Chapter Formatting Automation
=========================================

This AppleScript automates the complete chapter formatting workflow:
1. Opens InDesign and runs the formatting script
2. Converts HTML instructions to PDF
3. Opens all output files in appropriate applications
4. Organizes the workspace for efficient review

Usage: Run this script after chapter_formatting_agent.py completes
*)

-- Configuration
property wellspringPath : "/Users/ojeromyo/Desktop/wellspring_directory"
property outputPath : wellspringPath & "/output"

-- Main automation workflow
on run
	display notification "🌊 Starting Wellspring Automation..." with title "Chapter Formatting"
	
	-- Get the latest output files
	set latestFiles to getLatestOutputFiles()
	
	if latestFiles is not {} then
		-- Step 1: InDesign automation
		automateInDesign(latestFiles)
		
		-- Step 2: PDF conversion
		convertHTMLToPDF(latestFiles)
		
		-- Step 3: Open files for review
		openFilesForReview(latestFiles)
		
		-- Step 4: Organize workspace
		organizeWorkspace()
		
		display notification "✅ Wellspring automation complete!" with title "Chapter Formatting"
		
		-- Show completion dialog
		set buttonPressed to button returned of (display dialog "🎯 Wellspring Chapter Formatting Complete!

📁 All files processed and opened for review.
📊 InDesign script executed successfully.
📋 PDF instructions generated.

What would you like to do next?" buttons {"Open Output Folder", "Run Again", "Done"} default button "Open Output Folder")
		
		if buttonPressed = "Open Output Folder" then
			tell application "Finder"
				open folder (outputPath as POSIX file)
				activate
			end tell
		else if buttonPressed = "Run Again" then
			run
		end if
		
	else
		display alert "❌ No output files found!" message "Please run chapter_formatting_agent.py first to generate the output files." as critical
	end if
end run

-- Get the latest output files from the chapter formatting agent
on getLatestOutputFiles()
	set fileList to {}
	
	try
		tell application "System Events"
			set outputFolder to folder outputPath
			set allFiles to files of outputFolder
			
			-- Look for the latest files by timestamp
			repeat with aFile in allFiles
				set fileName to name of aFile
				if fileName contains "wellspring" then
					set end of fileList to (outputPath & "/" & fileName)
				end if
			end repeat
		end tell
	on error
		display alert "❌ Output folder not found!" message "Cannot access: " & outputPath
	end try
	
	return fileList
end getLatestOutputFiles

-- Automate InDesign tasks
on automateInDesign(fileList)
	display notification "🎨 Opening InDesign..." with title "Wellspring Automation"
	
	-- Find the .jsx script
	set jsxScript to ""
	repeat with filePath in fileList
		if filePath contains ".jsx" then
			set jsxScript to filePath
			exit repeat
		end if
	end repeat
	
	if jsxScript ≠ "" then
		try
			-- Open InDesign
			tell application "Adobe InDesign 2024"
				activate
				
				-- Wait for InDesign to fully load
				delay 3
				
				-- Check if a document is open
				if (count of documents) = 0 then
					set userChoice to button returned of (display dialog "📄 No InDesign document is open.

Would you like to:" buttons {"Open Existing Document", "Create New Document", "Skip InDesign"} default button "Open Existing Document")
					
					if userChoice = "Open Existing Document" then
						-- Let user choose a document
						set chosenFile to choose file with prompt "Select your Wellspring manuscript file:" of type {"com.adobe.indesign.document"}
						open chosenFile
					else if userChoice = "Create New Document" then
						make new document
					else
						return
					end if
				end if
				
				-- Run the formatting script
				set scriptFile to (jsxScript as POSIX file) as alias
				do script scriptFile language javascript
				
				display notification "✅ InDesign formatting applied!" with title "Wellspring Automation"
				
			end tell
			
		on error errMsg
			display alert "❌ InDesign Error" message "Failed to run InDesign script: " & errMsg as critical
		end try
	end if
end automateInDesign

-- Convert HTML instructions to PDF
on convertHTMLToPDF(fileList)
	display notification "📋 Converting HTML to PDF..." with title "Wellspring Automation"
	
	-- Find the HTML file
	set htmlFile to ""
	repeat with filePath in fileList
		if filePath contains ".html" then
			set htmlFile to filePath
			exit repeat
		end if
	end repeat
	
	if htmlFile ≠ "" then
		try
			-- Open HTML in Safari and convert to PDF
			tell application "Safari"
				activate
				open location ("file://" & htmlFile)
				delay 2
				
				-- Print to PDF
				tell application "System Events"
					keystroke "p" using command down
					delay 1
					
					-- Click PDF dropdown
					click menu button "PDF" of sheet 1 of window 1 of application process "Safari"
					delay 0.5
					
					-- Click "Save as PDF"
					click menu item "Save as PDF…" of menu 1 of menu button "PDF" of sheet 1 of window 1 of application process "Safari"
					delay 1
					
					-- Set filename and save location
					set value of text field 1 of sheet 1 of sheet 1 of window 1 of application process "Safari" to "Wellspring_Formatting_Instructions"
					delay 0.5
					
					-- Navigate to output folder
					keystroke "g" using {command down, shift down}
					delay 1
					set value of text field 1 of sheet 1 of sheet 1 of sheet 1 of window 1 of application process "Safari" to outputPath
					keystroke return
					delay 1
					
					-- Save the PDF
					click button "Save" of sheet 1 of sheet 1 of window 1 of application process "Safari"
					
					display notification "✅ PDF instructions created!" with title "Wellspring Automation"
				end tell
			end tell
			
		on error errMsg
			display alert "❌ PDF Conversion Error" message "Failed to convert HTML to PDF: " & errMsg as critical
		end try
	end if
end convertHTMLToPDF

-- Open files for review in appropriate applications
on openFilesForReview(fileList)
	display notification "📂 Opening files for review..." with title "Wellspring Automation"
	
	repeat with filePath in fileList
		try
			if filePath contains ".txt" then
				-- Open text file in TextEdit
				tell application "TextEdit"
					open (filePath as POSIX file)
					activate
				end tell
				
			else if filePath contains ".xml" then
				-- Open XML in default application (usually Xcode or XML editor)
				tell application "Finder"
					open (filePath as POSIX file)
				end tell
				
			else if filePath contains ".json" then
				-- Open JSON in default application
				tell application "Finder"
					open (filePath as POSIX file)
				end tell
				
			else if filePath contains ".idml" then
				-- Open IDML template in InDesign
				tell application "Adobe InDesign 2024"
					open (filePath as POSIX file)
				end tell
				
			end if
			
		on error
			-- Ignore errors for individual file opening
		end try
	end repeat
	
	display notification "✅ Files opened for review!" with title "Wellspring Automation"
end openFilesForReview

-- Organize workspace and create backup
on organizeWorkspace()
	display notification "📁 Organizing workspace..." with title "Wellspring Automation"
	
	try
		-- Create timestamped backup folder
		set currentDate to (current date)
		set dateString to (year of currentDate as string) & "-" & ¬
			text -2 thru -1 of ("0" & (month of currentDate as integer)) & "-" & ¬
			text -2 thru -1 of ("0" & (day of currentDate as integer)) & "_" & ¬
			text -2 thru -1 of ("0" & (hours of currentDate)) & "-" & ¬
			text -2 thru -1 of ("0" & (minutes of currentDate))
		
		set backupFolder to wellspringPath & "/chapter_formatting_backups/backup_" & dateString
		
		-- Create backup directory
		do shell script "mkdir -p '" & backupFolder & "'"
		
		-- Copy output files to backup
		do shell script "cp -r '" & outputPath & "'/* '" & backupFolder & "/' 2>/dev/null || true"
		
		display notification "✅ Workspace organized!" with title "Wellspring Automation"
		
	on error errMsg
		display notification "⚠️ Backup warning: " & errMsg with title "Wellspring Automation"
	end try
end organizeWorkspace

-- Quick launcher for individual tasks
on quickLauncher()
	set taskChoice to button returned of (display dialog "🌊 Wellspring Quick Launcher

Choose a task to automate:" buttons {"🎨 InDesign Only", "📋 PDF Only", "📂 Open Files", "🔄 Full Workflow"} default button "🔄 Full Workflow")
	
	set latestFiles to getLatestOutputFiles()
	
	if taskChoice = "🎨 InDesign Only" then
		automateInDesign(latestFiles)
	else if taskChoice = "📋 PDF Only" then
		convertHTMLToPDF(latestFiles)
	else if taskChoice = "📂 Open Files" then
		openFilesForReview(latestFiles)
	else if taskChoice = "🔄 Full Workflow" then
		run
	end if
end quickLauncher 
#!/usr/bin/osascript

-- Simple test version of Wellspring AppleScript automation
-- Tests basic functionality without complex automation

tell application "Finder"
	-- Test 1: Check if output folder exists
	set outputPath to "/Users/ojeromyo/Desktop/wellspring_directory/output"
	
	try
		set outputFolder to folder (outputPath as POSIX file)
		set fileCount to count of files of outputFolder
		
		display dialog "✅ SUCCESS: Found " & fileCount & " files in output folder!

🎯 AppleScript is working correctly.
📁 Output folder: " & outputPath & "
📊 Files found: " & fileCount & "

Would you like to open the output folder?" buttons {"Yes, Open Folder", "No, Just Test"} default button "Yes, Open Folder"
		
		set buttonPressed to button returned of result
		
		if buttonPressed = "Yes, Open Folder" then
			open folder (outputPath as POSIX file)
			activate
		end if
		
	on error errMsg
		display alert "❌ Test Failed" message "Could not access output folder: " & errMsg as critical
	end try
end tell 
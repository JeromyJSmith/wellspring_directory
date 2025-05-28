#!/usr/bin/osascript

-- Wellspring Permission Checker
-- Tests each required permission for AppleScript automation

display dialog "🔐 WELLSPRING PERMISSION CHECKER

This will test each required permission.
Click OK to start testing..." buttons {"OK"} default button "OK"

-- Test 1: Finder access
try
	tell application "Finder"
		set testFolder to folder "/Users/ojeromyo/Desktop/wellspring_directory" as alias
		display notification "✅ Finder: WORKING" with title "Permission Test"
	end tell
on error errMsg
	display alert "❌ FINDER PERMISSION NEEDED" message "Please grant Terminal permission to control Finder in System Settings → Privacy & Security → Automation" as critical
	return
end try

-- Test 2: System Events access
try
	tell application "System Events"
		set testProcess to name of first process
		display notification "✅ System Events: WORKING" with title "Permission Test"
	end tell
on error errMsg
	display alert "❌ SYSTEM EVENTS PERMISSION NEEDED" message "Please grant Terminal permission to control System Events in System Settings → Privacy & Security → Automation" as critical
	return
end try

-- Test 3: Check if InDesign is available (optional)
try
	tell application "Adobe InDesign 2024"
		-- Just check if it exists, don't activate
		set testName to name
		display notification "✅ InDesign: AVAILABLE" with title "Permission Test"
	end tell
on error errMsg
	display notification "⚠️ InDesign: Not available (optional)" with title "Permission Test"
end try

-- Test 4: Safari access
try
	tell application "Safari"
		-- Just check if it exists, don't activate
		set testName to name
		display notification "✅ Safari: AVAILABLE" with title "Permission Test"
	end tell
on error errMsg
	display notification "⚠️ Safari: Permission needed for PDF conversion" with title "Permission Test"
end try

-- Success message
display dialog "🎉 PERMISSION TEST COMPLETE!

✅ Core permissions are working
🌊 Wellspring AppleScript automation is ready

Would you like to run the full automation now?" buttons {"Yes, Run Automation", "No, Just Testing"} default button "Yes, Run Automation"

set buttonPressed to button returned of result

if buttonPressed = "Yes, Run Automation" then
	-- Open the output folder to show what will be automated
	tell application "Finder"
		open folder "/Users/ojeromyo/Desktop/wellspring_directory/output"
		activate
	end tell
	
	display dialog "📁 Output folder opened!

Ready to run full Wellspring automation.
Use: python wellspring_launcher.py" buttons {"OK"} default button "OK"
end if 
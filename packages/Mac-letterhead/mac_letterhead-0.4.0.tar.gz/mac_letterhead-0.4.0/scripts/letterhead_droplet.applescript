-- Letterhead Applier AppleScript Droplet
-- This script takes dropped PDF files and applies a letterhead template

on open these_items
    -- Process each dropped file
    repeat with pdf_file in these_items
        if name extension of pdf_file is "pdf" then
            set input_pdf to POSIX path of pdf_file
            set app_path to POSIX path of (path to me)
            set app_container to do shell script "dirname " & quoted form of app_path
            
            -- Path to letterhead in the Resources folder - will be replaced during installation
            set letterhead_path to app_container & "/Resources/letterhead.pdf"
            
            -- For better UX, use the filename for the output
            set file_basename to do shell script "basename " & quoted form of input_pdf & " .pdf"
            
            -- Display progress dialog
            display dialog "Applying letterhead to " & file_basename & ".pdf..." buttons {} giving up after 1
            
            -- Run the command with error handling
            try
                -- Pass explicit HOME to ensure environment is correct
                set home_path to POSIX path of (path to home folder)
                set cmd to "export HOME=" & quoted form of home_path & " && cd " & quoted form of home_path
                set cmd to cmd & " && /usr/bin/env PATH=$HOME/.local/bin:$HOME/Library/Python/*/bin:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin uvx mac-letterhead print "
                set cmd to cmd & quoted form of letterhead_path & " " & quoted form of file_basename & " \"\" " & quoted form of input_pdf & " --strategy darken"
                
                -- Log the full command for diagnostics
                do shell script "echo " & quoted form of cmd & " > " & quoted form of home_path & "/Library/Logs/Mac-letterhead/applescript.log"
                
                -- Execute the command
                do shell script cmd
                
                -- Success message
                display dialog "Letterhead applied successfully to " & file_basename & ".pdf!" buttons {"OK"} default button "OK"
            on error errMsg
                -- Log the error
                do shell script "echo 'ERROR: " & errMsg & "' >> " & quoted form of home_path & "/Library/Logs/Mac-letterhead/applescript.log"
                
                -- Error message with details
                display dialog "Error applying letterhead: " & errMsg buttons {"OK"} default button "OK" with icon stop
            end try
        else
            -- Not a PDF file
            display dialog "File " & name of pdf_file & " is not a PDF file." buttons {"OK"} default button "OK" with icon stop
        end if
    end repeat
end open

on run
    -- Main instructions when launched directly
    display dialog "Letterhead Applier" & return & return & 
                 "To apply a letterhead to a PDF document:" & return & 
                 "1. Drag and drop a PDF file onto this application icon" & return &
                 "2. The letterhead will be applied automatically" & return &
                 "3. You'll be prompted to save the merged document" buttons {"OK"} default button "OK"
end run

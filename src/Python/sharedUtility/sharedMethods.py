import asyncio
from . import globalVars

#plan is rsync (for now) to move files from one part of the share to the other, future versions will also implement zfs copy

async def transferFolderWithRsync(folderLocation, desiredFolderLocation):
    #define the cmd command
    #-a keep times/permissions (useful since the files and folders are only handled by this docker so don't need to worry about windows permissions fighting)
    #-c checksum, make sure the files are properly transferred
    #--itemize-changes, creates a pretty log of what files were transferred to make parsing easy
    cmd = ['/usr/bin/rsync', '-ac', '--itemize-changes', folderLocation, desiredFolderLocation]

    # Start the process
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    while True:
        line = await process.stdout.readline()
        if not line:
            break
        
        # Decode and clean the output
        output = line.decode().strip()
        
        # Example parsing: itemize-changes output starts with 'c' for changes
        if output.startswith('>f'):
            filename = output[11:] # Extract filename from the standard rsync format
            globalVars.sync_log.append(filename)
            
            # TRIGGER YOUR OTHER TASKS HERE
            # e.g., app.storage.user['last_file'] = filename
            # or await notify_dashboard_that_file_finished(filename)

    # Wait for the process to finish
    return_code = await process.wait()
    if return_code == 0:
        print("Sync complete!")
    else:
        # Capture and print the error output from rsync
        error_output = await process.stderr.read()
        print(f"Sync failed with code {return_code}")
        print(f"DEBUG - Full Error Output: {error_output.decode().strip()}", flush = True)



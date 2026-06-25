import os
import asyncio
from nicegui import app, ui

#import webServer.py
import webServer

webServer.setup_routes()


# -----------------------------------------------------------------------------
# Execution
# -----------------------------------------------------------------------------
if __name__ in {'__main__', '__mp_main__'}:
    # Read port from environment variable, fallback to 8080
    port = int(os.environ.get('PORT', 8080))
    
    # storage_secret is required to sign the browser cookies for the login session state
    ui.run(port=8080, host='0.0.0.0', storage_secret='change-this-to-a-secure-key-later')
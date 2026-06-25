import os
from nicegui import app, ui

# Define your layout/style constants for a unified look
CARD_STYLE = 'w-96 p-6 rounded-lg shadow-lg bg-card'

# Simple session check middleware for the login wall
def is_authenticated() -> bool:
    return app.storage.user.get('authenticated', False)

# -----------------------------------------------------------------------------
# PAGE 1: Login Screen
# -----------------------------------------------------------------------------
@ui.page('/login')
def login_page():
    if is_authenticated():
        return ui.navigate.to('/')

    def try_login():
        # Replace this with your actual password verification logic
        if username.value == 'admin' and password.value == 'password':
            app.storage.user['authenticated'] = True
            ui.navigate.to('/')
        else:
            ui.notify('Invalid credentials', type='negative')

    with ui.card().classes('absolute-center ' + CARD_STYLE):
        ui.label('PlayniteNASync Login').classes('text-2xl font-bold text-center mb-4')
        username = ui.input('Username').classes('w-full')
        password = ui.input('Password', password=True).classes('w-full mb-4').on('keydown.enter', try_login)
        ui.button('Sign In', on_click=try_login).classes('w-full bg-primary text-white')

# -----------------------------------------------------------------------------
# PAGE 2: General/View Dashboard (Protected)
# -----------------------------------------------------------------------------
@ui.page('/')
def main_page():
    if not is_authenticated():
        return ui.navigate.to('/login')

    # Basic Navigation Bar
    with ui.header().classes('bg-primary text-white row items-center justify-between'):
        ui.label('PlayniteNASync Console').classes('text-lg font-bold')
        with ui.row():
            ui.button('Dashboard', on_click=lambda: ui.navigate.to('/')).props('flat text-color=white')
            ui.button('System Status', on_click=lambda: ui.navigate.to('/status')).props('flat text-color=white')
            ui.button('Logout', on_click=lambda: [app.storage.user.clear(), ui.navigate.to('/login')]).props('flat text-color=white icon=logout')

    # Main Grid Layout
    with ui.row().classes('w-full justify-center gap-6 p-6'):
        with ui.card().classes(CARD_STYLE):
            ui.label('Sync Actions').classes('text-xl font-semibold')
            ui.markdown('Manage your Windows PC to Unraid sync operations.')
            ui.button('Trigger Manual Sync', on_click=lambda: ui.notify('Sync started via Robocopy...')).classes('bg-secondary text-white')

        with ui.card().classes(CARD_STYLE):
            ui.label('Recent Activity').classes('text-xl font-semibold')
            ui.label('• Cyberpunk 2077 synced successfully (2.3 GB)')
            ui.label('• Elden Ring synced successfully (1.1 GB)')

# -----------------------------------------------------------------------------
# PAGE 3: Status Monitor (Protected)
# -----------------------------------------------------------------------------
@ui.page('/status')
def status_page():
    if not is_authenticated():
        return ui.navigate.to('/login')

    # Re-use header or create a shared layout function component
    with ui.header().classes('bg-primary text-white row items-center justify-between'):
        ui.label('PlayniteNASync Console').classes('text-lg font-bold')
        with ui.row():
            ui.button('Dashboard', on_click=lambda: ui.navigate.to('/')).props('flat text-color=white')
            ui.button('System Status', on_click=lambda: ui.navigate.to('/status')).props('flat text-color=white')

    with ui.column().classes('w-full items-center p-6 gap-4'):
        ui.label('System Health & Logs').classes('text-2xl font-bold')
        
        # Dynamic status indicators
        with ui.row().classes('gap-4'):
            ui.badge('NAS Share: Connected', color='green').classes('p-2 text-sm')
            ui.badge('Webserver: Active', color='green').classes('p-2 text-sm')

        # Log terminal output box
        log_box = ui.log(max_lines=20).classes('w-full max-w-2xl h-64 bg-black text-green-400 font-mono p-4 rounded')
        log_box.push('Initializing system diagnostics...')
        log_box.push('Checking /config/config.json bindings...')
        log_box.push('Ready for incoming synchronization requests.')

# -----------------------------------------------------------------------------
# Execution
# -----------------------------------------------------------------------------
if __name__ in {'__main__', 'pymain'}:
    # Read port from environment variable, fallback to 8080
    port = int(os.environ.get('PORT', 8080))
    
    # storage_secret is required to sign the browser cookies for the login session state
    ui.run(port=port, host='0.0.0.0', storage_secret='change-this-to-a-secure-key-later')
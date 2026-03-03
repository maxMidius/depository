"""
JIRA Scope DAG Editor - NiceGUI Application
Hierarchical DAG editor for managing Capabilities, Deliverables, and Tasks
"""

from nicegui import ui, app
from fastapi import Body
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
from datetime import datetime
from typing import Optional

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== CONFIGURATION ==========

BASE_PATH = Path(__file__).parent
STORAGE_DIR = BASE_PATH / 'storage'
STORAGE_DIR.mkdir(exist_ok=True)
STATIC_DIR = BASE_PATH / 'static'
STATIC_DIR.mkdir(exist_ok=True)

# Mount static files
app.add_static_files('/static', str(STATIC_DIR))

# ========== SAMPLE DATA ==========

SAMPLE_PROJECT = {
    'name': 'Sample Project',
    'description': 'Sample project with capabilities, deliverables, and tasks',
    'capabilities': [
        {
            'id': 'cap1',
            'name': 'User Management',
            'x': 50,
            'y': 50,
            'width': 400,
            'height': 300,
            'deliverables': [
                {
                    'id': 'del1',
                    'name': 'Authentication',
                    'x': 60,
                    'y': 90,
                    'width': 180,
                    'height': 200,
                    'tasks': [
                        {'id': 'task1', 'name': 'Login Form', 'x': 80, 'y': 130},
                        {'id': 'task2', 'name': 'Token Validation', 'x': 80, 'y': 200},
                    ]
                },
                {
                    'id': 'del2',
                    'name': 'User Profile',
                    'x': 260,
                    'y': 90,
                    'width': 180,
                    'height': 200,
                    'tasks': [
                        {'id': 'task3', 'name': 'Edit Profile', 'x': 280, 'y': 130},
                        {'id': 'task4', 'name': 'Avatar Upload', 'x': 280, 'y': 200},
                    ]
                }
            ]
        },
        {
            'id': 'cap2',
            'name': 'Data Analytics',
            'x': 500,
            'y': 50,
            'width': 350,
            'height': 300,
            'deliverables': [
                {
                    'id': 'del3',
                    'name': 'Dashboard',
                    'x': 520,
                    'y': 90,
                    'width': 310,
                    'height': 200,
                    'tasks': [
                        {'id': 'task5', 'name': 'Charts', 'x': 540, 'y': 130},
                        {'id': 'task6', 'name': 'Data Export', 'x': 540, 'y': 200},
                    ]
                }
            ]
        }
    ],
    'connections': [
        {'from': 'task2', 'to': 'task3'},
        {'from': 'task1', 'to': 'task2'},
    ]
}

# Initialize sample project
sample_file = STORAGE_DIR / 'sample_project.json'
if not sample_file.exists():
    with open(sample_file, 'w') as f:
        json.dump(SAMPLE_PROJECT, f, indent=2)

# ========== API ENDPOINTS ==========

@app.post('/api/project/save')
async def save_project(payload: dict = Body(...)):
    """Save a project"""
    try:
        name = payload.get('name', 'project')
        safe_name = "".join(c for c in name if c.isalnum() or c in ('-', '_', ' ')).strip().replace(' ', '_').lower()
        if not safe_name:
            safe_name = 'project'
        
        filepath = STORAGE_DIR / f'{safe_name}.json'
        with open(filepath, 'w') as f:
            json.dump(payload, f, indent=2)
        
        return {'success': True, 'message': f'Project saved as {safe_name}', 'name': safe_name}
    except Exception as e:
        return {'success': False, 'error': str(e)}


@app.get('/api/projects')
async def list_projects():
    """List all saved projects"""
    try:
        projects = []
        for filepath in STORAGE_DIR.glob('*.json'):
            with open(filepath, 'r') as f:
                data = json.load(f)
                projects.append({
                    'name': filepath.stem,
                    'displayName': data.get('name', filepath.stem),
                    'description': data.get('description', ''),
                })
        return {'success': True, 'projects': projects}
    except Exception as e:
        return {'success': False, 'error': str(e)}


@app.get('/api/project/{name}')
async def load_project(name: str):
    """Load a specific project"""
    try:
        filepath = STORAGE_DIR / f'{name}.json'
        if not filepath.exists():
            return {'success': False, 'error': f'Project {name} not found'}
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return {'success': True, 'project': data}
    except Exception as e:
        return {'success': False, 'error': str(e)}


# ========== NICEGUI PAGE ==========

# ========== HELPER FUNCTIONS ==========

async def get_project_list():
    """Get list of available projects for dropdown"""
    try:
        projects = []
        for filepath in STORAGE_DIR.glob('*.json'):
            with open(filepath, 'r') as f:
                data = json.load(f)
                projects.append({
                    'value': filepath.stem,
                    'label': data.get('name', filepath.stem)
                })
        return projects
    except Exception as e:
        print(f'Error listing projects: {e}')
        return []

@ui.page('/', title='JIRA Scope - DAG Editor')
def index():
    """Main page with DAG editor"""
    
    # Add custom CSS
    ui.html('''
    <style>
        html, body {
            height: 100%;
            margin: 0;
            width: 100%;
        }
        #app {
            height: 100%;
            width: 100%;
        }
        .nicegui-content {
            height: 100vh;
            width: 100vw;
            padding: 0 !important;
            gap: 0 !important;
            display: flex;
            flex-direction: column;
        }
        body {
            margin: 0;
            overflow: hidden;
        }
        /* Layout styling */
        .main-layout {
            display: flex;
            height: 100vh;
            width: 100vw;
            position: fixed;
            top: 0;
            left: 0;
        }
        .left-menu {
            width: 300px;
            background: #1e1e1e;
            color: white;
            padding: 1rem;
            overflow-y: auto;
            border-right: 3px solid #444;
            transition: transform 0.3s ease;
            flex-shrink: 0;
        }
        .left-menu.hidden {
            transform: translateX(-100%);
            position: absolute;
            left: 0;
            z-index: 100;
        }
        .canvas-area {
            flex: 1;
            background: #f5f5f5;
            overflow: hidden;
            position: relative;
            height: 100vh;
            width: 100%;
            display: flex;
            flex-direction: column;
        }
        .canvas-area .nicegui-html {
            height: 100% !important;
            width: 100% !important;
            flex: 1 !important;
        }
        .toggle-btn {
            position: absolute;
            top: 8px;
            left: 8px;
            z-index: 101;
            background: #2196f3;
            color: white;
            border: none;
            padding: 4px 8px;
            border-radius: 3px;
            cursor: pointer;
            font-weight: bold;
            font-size: 14px;
            min-width: 30px;
            height: 30px;
        }
        .toggle-btn:hover {
            background: #1976d2;
        }
        #canvas {
            display: block;
            width: 100%;
            height: 100%;
            position: absolute;
            top: 0;
            left: 0;
        }
        .panel-section {
            margin-bottom: 1.5rem;
            padding: 1rem;
            background: #2a2a2a;
            border-radius: 8px;
            border: 1px solid #444;
        }
        .panel-section h3 {
            margin-top: 0;
            margin-bottom: 1rem;
            color: #4fc3f7;
            font-size: 1.1rem;
        }
        .btn {
            padding: 0.5rem 1rem;
            margin: 0.25rem;
            background: #2196F3;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9rem;
        }
        .btn:hover {
            background: #1976D2;
        }
        .btn-secondary {
            background: #666;
        }
        .btn-secondary:hover {
            background: #555;
        }
        .btn-danger {
            background: #f44336;
        }
        .btn-danger:hover {
            background: #d32f2f;
        }
        .input-field {
            width: 100%;
            padding: 0.5rem;
            margin: 0.25rem 0;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 4px;
            color: white;
            font-size: 0.9rem;
        }
        .input-field:focus {
            outline: none;
            border-color: #4fc3f7;
        }
        select.input-field {
            cursor: pointer;
        }
        .stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }
        .stat-item {
            padding: 0.5rem;
            background: #333;
            border-radius: 4px;
            text-align: center;
        }
        .stat-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: #4fc3f7;
        }
        .stat-label {
            font-size: 0.8rem;
            color: #aaa;
        }

    </style>
    ''', sanitize=False)
    
    # Main layout container
    with ui.element().classes('main-layout').style('display: flex;'):
        # Left menu panel
        left_menu = ui.element().classes('left-menu').style('background: #1e1e1e; color: white;')
        
        with left_menu:
            ui.label('JIRA Scope Editor').classes('text-2xl font-bold mb-4').style('color: white;')
            
            # Project management section
            with ui.element('div').classes('panel-section'):
                ui.html('<h3>📁 Save Project</h3>', sanitize=False)
                ui.label('Enter project name and description, then click Save').style('font-size: 0.85rem; color: #aaa;')
                ui.input('Project Name', placeholder='My Project').classes('w-full').props('dark filled')
                ui.textarea('Description', placeholder='Project description').classes('w-full').props('dark filled rows=2')
                ui.button('💾 Save Project', on_click=lambda: ui.run_javascript('saveProject()')).classes('w-full')
            
            # Load project section
            with ui.element('div').classes('panel-section'):
                ui.html('<h3>📂 Load Project</h3>', sanitize=False)
                ui.label('Click Refresh to see saved projects').style('font-size: 0.85rem; color: #aaa;')
                
                # Load project dropdown
                project_select = ui.select(
                    label='Saved Projects',
                    options=[],
                    with_input=False
                ).classes('w-full').props('dark filled')
                
                async def load_selected_project():
                    if project_select.value:
                        await ui.run_javascript(f'loadProject("{project_select.value}")')
                        ui.notify('Project loaded')
                    else:
                        ui.notify('Please select a project first')
                
                async def refresh_and_show_projects():
                    projects = await get_project_list()
                    if projects:
                        project_select.options = [p['value'] for p in projects]
                        ui.notify(f'Found {len(projects)} projects')
                    else:
                        project_select.options = []
                        ui.notify('No saved projects found')
                    project_select.update()
                
                # Buttons for Load workflow
                with ui.row().classes('w-full gap-2'):
                    ui.button('🔄 Refresh', on_click=lambda: refresh_and_show_projects()).classes('flex-1')
                    ui.button('📥 Load Selected', on_click=lambda: load_selected_project()).classes('flex-1')
            
            # Add elements section
            with ui.element('div').classes('panel-section'):
                ui.html('<h3>➕ Add Elements</h3>', sanitize=False)
                ui.button('+ Capability', on_click=lambda: ui.run_javascript('addCapability()')).classes('w-full')
                ui.button('+ Deliverable', on_click=lambda: ui.run_javascript('addDeliverable()')).classes('w-full')
                ui.button('+ Task', on_click=lambda: ui.run_javascript('addTask()')).classes('w-full')
            
            # Actions section
            with ui.element('div').classes('panel-section'):
                ui.html('<h3>🔧 Actions</h3>', sanitize=False)
                ui.button('🔗 Connect Tasks', on_click=lambda: ui.run_javascript('toggleConnectionMode()')).classes('w-full')
                ui.button('🗑️ Delete Selected', on_click=lambda: ui.run_javascript('deleteSelected()')).classes('w-full')
                ui.button('↩️ Undo', on_click=lambda: ui.run_javascript('undo()')).classes('w-full')
                ui.button('↪️ Redo', on_click=lambda: ui.run_javascript('redo()')).classes('w-full')
            
            # Statistics section
            with ui.element('div').classes('panel-section'):
                ui.html('<h3>📊 Statistics</h3>', sanitize=False)
                ui.html('''
                <div class="stats">
                    <div class="stat-item">
                        <div class="stat-value" id="cap-count">0</div>
                        <div class="stat-label">Capabilities</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="del-count">0</div>
                        <div class="stat-label">Deliverables</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="task-count">0</div>
                        <div class="stat-label">Tasks</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="conn-count">0</div>
                        <div class="stat-label">Connections</div>
                    </div>
                </div>
                ''', sanitize=False)
        
        # Canvas area
        canvas_area = ui.element().classes('canvas-area')
        
        with canvas_area:
            # Toggle button in top-left of canvas - small arrow button
            ui.button('<').classes('toggle-btn').style(
                'position: absolute; top: 8px; left: 8px; z-index: 101; width: 30px; height: 30px; padding: 4px 8px;'
            ).on_click(lambda: ui.run_javascript('toggleLeftMenu()'))
            
            ui.html('''
            <svg id="canvas" width="100%" height="100%" style="background: #f5f5f5; cursor: default; display: block; position: absolute; top: 0; left: 0;">
                <defs>
                    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
                        <polygon points="0 0, 10 3, 0 6" fill="#1976d2" />
                    </marker>
                </defs>
                <g id="capabilities-layer"></g>
                <g id="deliverables-layer"></g>
                <g id="tasks-layer"></g>
                <g id="connections-layer"></g>
            </svg>
            ''', sanitize=False)
    
    # Load JavaScript
    ui.add_body_html(f'<script src="/static/dag_editor.js"></script>')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title='JIRA Scope - DAG Editor',
        host='0.0.0.0',
        port=8080,
        show=False,
        reload=False  # Disabled to prevent killing edits
    )

"""
Advanced NiceGUI DAG Editor with Full React D3.js Integration
This version embeds the nice-dag React component directly
"""

from nicegui import ui, app
from fastapi import FastAPI, UploadFile, File, Body
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
from datetime import datetime
import os
import sys
import asyncio
from typing import Optional

# FastAPI app is directly accessible as the 'app' object from NiceGUI

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

# Static files for embedded UI
app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')

# Create sample DAGs
SAMPLE_DAGS = {
    'simple-pipeline': {
        'nodes': [
            {'id': 'start', 'label': 'Start', 'type': 'start', 'x': 100, 'y': 50},
            {'id': 'extract', 'label': 'Extract Data', 'type': 'normal', 'x': 100, 'y': 150},
            {'id': 'transform', 'label': 'Transform', 'type': 'normal', 'x': 100, 'y': 250},
            {'id': 'load', 'label': 'Load', 'type': 'normal', 'x': 100, 'y': 350},
            {'id': 'end', 'label': 'End', 'type': 'end', 'x': 100, 'y': 450}
        ],
        'edges': [
            {'source': 'start', 'target': 'extract', 'id': 'e1'},
            {'source': 'extract', 'target': 'transform', 'id': 'e2'},
            {'source': 'transform', 'target': 'load', 'id': 'e3'},
            {'source': 'load', 'target': 'end', 'id': 'e4'}
        ],
        'description': 'Simple ETL pipeline'
    },
    'parallel-tasks': {
        'nodes': [
            {'id': 'start', 'label': 'Start', 'type': 'start', 'x': 150, 'y': 50},
            {'id': 'task1', 'label': 'Task 1', 'type': 'normal', 'x': 50, 'y': 150},
            {'id': 'task2', 'label': 'Task 2', 'type': 'normal', 'x': 150, 'y': 150},
            {'id': 'task3', 'label': 'Task 3', 'type': 'normal', 'x': 250, 'y': 150},
            {'id': 'merge', 'label': 'Merge Results', 'type': 'normal', 'x': 150, 'y': 250},
            {'id': 'end', 'label': 'End', 'type': 'end', 'x': 150, 'y': 350}
        ],
        'edges': [
            {'source': 'start', 'target': 'task1', 'id': 'e1'},
            {'source': 'start', 'target': 'task2', 'id': 'e2'},
            {'source': 'start', 'target': 'task3', 'id': 'e3'},
            {'source': 'task1', 'target': 'merge', 'id': 'e4'},
            {'source': 'task2', 'target': 'merge', 'id': 'e5'},
            {'source': 'task3', 'target': 'merge', 'id': 'e6'},
            {'source': 'merge', 'target': 'end', 'id': 'e7'}
        ],
        'description': 'Parallel tasks with merge'
    }
}

# Initialize sample DAGs
for dag_name, dag_content in SAMPLE_DAGS.items():
    dag_file = STORAGE_DIR / f'{dag_name}.json'
    if not dag_file.exists():
        dag_data = {
            'name': dag_name,
            'description': dag_content.get('description', ''),
            'data': {
                'nodes': dag_content.get('nodes', []),
                'edges': dag_content.get('edges', [])
            },
            'created': datetime.now().isoformat(),
            'updated': datetime.now().isoformat()
        }
        with open(dag_file, 'w') as f:
            json.dump(dag_data, f, indent=2)


# ========== API ENDPOINTS ==========

@app.post('/api/dags/save')
async def save_dag(payload: dict = Body(...)):
    """Save a DAG"""
    try:
        print(f"[SAVE] Received payload: {payload}")
        
        name = payload.get('name')
        data = payload.get('data', payload)  # Support direct node/edge/group keys or nested data key
        
        print(f"[SAVE] Extracted name: {name}")
        print(f"[SAVE] Data keys: {data.keys() if isinstance(data, dict) else 'not a dict'}")
        
        if not name or not (data.get('nodes') is not None or data.get('edges') is not None or data.get('groups') is not None):
            print(f"[SAVE] ERROR - Missing name or data")
            return {'success': False, 'error': 'Missing name or data'}
        
        safe_name = "".join(c for c in name if c.isalnum() or c in ('-', '_', ' ')).strip().replace(' ', '_').lower()
        if not safe_name:
            safe_name = 'dag'
        
        print(f"[SAVE] Safe name: {safe_name}")
        
        filepath = STORAGE_DIR / f'{safe_name}.json'
        dag_info = {
            'name': safe_name,
            'description': data.get('description', ''),
            'data': {
                'nodes': data.get('nodes', []),
                'edges': data.get('edges', []),
                'groups': data.get('groups', [])
            },
            'created': datetime.now().isoformat(),
            'updated': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(dag_info, f, indent=2)
        
        print(f"[SAVE] File written to: {filepath}")
        print(f"[SAVE] Nodes: {len(dag_info['data']['nodes'])}, Edges: {len(dag_info['data']['edges'])}, Groups: {len(dag_info['data']['groups'])}")
        
        return {'success': True, 'message': f'DAG saved', 'name': safe_name}
    except Exception as e:
        print(f"[SAVE] EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e)}


@app.get('/api/dags')
async def list_dags():
    """List all DAGs"""
    try:
        print(f"[LIST] Storage directory: {STORAGE_DIR}")
        print(f"[LIST] Directory exists: {STORAGE_DIR.exists()}")
        
        dags = []
        for filepath in sorted(STORAGE_DIR.glob('*.json')):
            print(f"[LIST] Found DAG file: {filepath.name}")
            with open(filepath, 'r') as f:
                dag_info = json.load(f)
                dags.append({
                    'name': dag_info['name'],
                    'description': dag_info.get('description', ''),
                    'created': dag_info['created'],
                    'updated': dag_info['updated'],
                    'nodes': len(dag_info['data'].get('nodes', [])),
                    'edges': len(dag_info['data'].get('edges', []))
                })
        
        print(f"[LIST] Total DAGs found: {len(dags)}")
        return {'success': True, 'dags': dags}
    except Exception as e:
        print(f"[LIST] EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e)}


@app.get('/api/dags/{dag_name}')
async def get_dag(dag_name: str):
    """Load a DAG"""
    try:
        print(f"[LOAD] Requesting DAG: {dag_name}")
        filepath = STORAGE_DIR / f'{dag_name}.json'
        print(f"[LOAD] File path: {filepath}")
        print(f"[LOAD] File exists: {filepath.exists()}")
        
        if not filepath.exists():
            print(f"[LOAD] ERROR - File not found")
            return {'success': False, 'error': 'DAG not found'}, 404
        
        with open(filepath, 'r') as f:
            dag_info = json.load(f)
        
        print(f"[LOAD] Loaded DAG with {len(dag_info.get('data', {}).get('nodes', []))} nodes, {len(dag_info.get('data', {}).get('edges', []))} edges")
        return {'success': True, 'data': dag_info}
    except Exception as e:
        print(f"[LOAD] EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e)}


@app.delete('/api/dags/{dag_name}')
async def delete_dag(dag_name: str):
    """Delete a DAG"""
    try:
        filepath = STORAGE_DIR / f'{dag_name}.json'
        if not filepath.exists():
            return {'success': False, 'error': 'DAG not found'}, 404
        filepath.unlink()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}


@app.post('/api/dags/{dag_name}/export')
async def export_dag(dag_name: str):
    """Export DAG as JSON file"""
    try:
        filepath = STORAGE_DIR / f'{dag_name}.json'
        if not filepath.exists():
            return {'success': False, 'error': 'DAG not found'}, 404
        
        return FileResponse(
            filepath,
            filename=f'{dag_name}.json',
            media_type='application/json'
        )
    except Exception as e:
        return {'success': False, 'error': str(e)}


@app.post('/api/dags/import')
async def import_dag(file: UploadFile):
    """Import DAG from JSON file"""
    try:
        content = await file.read()
        dag_data = json.loads(content)
        
        # Validate structure
        if 'data' not in dag_data or 'nodes' not in dag_data['data']:
            return {'success': False, 'error': 'Invalid DAG file format'}
        
        name = dag_data.get('name', file.filename.replace('.json', '')).lower()
        safe_name = "".join(c for c in name if c.isalnum() or c in ('-', '_')).lower()
        
        filepath = STORAGE_DIR / f'{safe_name}.json'
        incoming = dag_data.get('data', {'nodes': [], 'edges': [], 'groups': []})
        dag_info = {
            'name': safe_name,
            'description': dag_data.get('description', ''),
            'data': {
                'nodes': incoming.get('nodes', []),
                'edges': incoming.get('edges', []),
                'groups': incoming.get('groups', [])
            },
            'created': datetime.now().isoformat(),
            'updated': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(dag_info, f, indent=2)
        
        return {'success': True, 'name': safe_name}
    except Exception as e:
        return {'success': False, 'error': str(e)}


@app.get('/api/stats')
async def get_stats():
    """Get system statistics"""
    try:
        dag_count = len(list(STORAGE_DIR.glob('*.json')))
        total_nodes = 0
        total_edges = 0
        
        for filepath in STORAGE_DIR.glob('*.json'):
            with open(filepath, 'r') as f:
                dag = json.load(f)
                total_nodes += len(dag['data'].get('nodes', []))
                total_edges += len(dag['data'].get('edges', []))
        
        return {
            'dags': dag_count,
            'totalNodes': total_nodes,
            'totalEdges': total_edges,
            'storageDir': str(STORAGE_DIR)
        }
    except Exception as e:
        return {'error': str(e)}


@app.get('/api/health')
async def health():
    """Health check"""
    return {'status': 'ok', 'service': 'DAG Editor API v1'}


# ========== NICEGUI PAGES ==========

@ui.page('/', title='Simple DAG Editor')
def index():
    """Main page"""
    # Add custom CSS and JavaScript for ribbon/palette toggling
    ui.html('''
    <style>
        #left-ribbon {
            width: 48px;
        }
        #left-palettes {
            transition: margin-left 0.3s ease, width 0.3s ease;
            width: 320px;
        }
        #left-palettes.hidden {
            margin-left: -320px;
            width: 0;
            overflow: hidden;
        }
        .palette.hidden {
            display: none;
        }
        .ribbon-btn {
            cursor: pointer;
            padding: 0.4rem;
            border-radius: 0.35rem;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.2);
            color: white;
            font-weight: bold;
            transition: background 0.2s ease;
        }
        .ribbon-btn:hover {
            background: rgba(255,255,255,0.18);
        }
        .ribbon-btn.active {
            background: rgba(56, 189, 248, 0.25);
            border-color: rgba(56, 189, 248, 0.6);
        }
    </style>
    ''', sanitize=False)
    
    # Add JavaScript for palette toggle (must use add_body_html for scripts)
    ui.add_body_html('''
    <script>
        function setActiveRibbon(targetId) {
            const buttons = document.querySelectorAll('.ribbon-btn');
            buttons.forEach((btn) => {
                const panel = btn.getAttribute('data-panel');
                if (panel === targetId) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });
        }

        function togglePalette(targetId) {
            const container = document.getElementById('left-palettes');
            const palettes = document.querySelectorAll('.palette');
            const target = document.getElementById(targetId);
            if (!container || !target) return;

            const isCurrentlyVisible = !target.classList.contains('hidden');
            palettes.forEach((p) => p.classList.add('hidden'));

            if (isCurrentlyVisible) {
                // Closing - hide everything
                container.classList.add('hidden');
                setActiveRibbon('');
                localStorage.setItem('activePalette', '');
                localStorage.setItem('paletteOpened', 'false');
                return;
            }

            // Opening - show the selected palette
            target.classList.remove('hidden');
            container.classList.remove('hidden');
            setActiveRibbon(targetId);
            localStorage.setItem('activePalette', targetId);
            localStorage.setItem('paletteOpened', 'true');
        }
        
        // Refresh canvas info from embedded editor
        function refreshCanvasInfo() {
            try {
                const iframe = document.querySelector('iframe[src="/static/nice_dag_ui/index.html"]');
                if (!iframe || !iframe.contentWindow) return;
                
                const doc = iframe.contentWindow.document;
                const nodeList = doc.getElementById('nodeList');
                const edgeList = doc.getElementById('edgeList');
                const groupList = doc.getElementById('groupList');
                
                // Count lines (rough count of items)
                const nodeCount = nodeList ? nodeList.textContent.split('\\n').filter(Boolean).length : 0;
                const edgeCount = edgeList ? (edgeList.textContent.match(/->/g) || []).length : 0;
                const groupCount = groupList ? (groupList.textContent.match(/Group/g) || []).length : 0;
                
                document.getElementById('canvas-node-count').textContent = nodeCount;
                document.getElementById('canvas-edge-count').textContent = edgeCount;
                document.getElementById('canvas-group-count').textContent = groupCount;
            } catch (e) {
                // Cross-origin or other issues, ignore
            }
        }

        function updateDetailsPanel() {
            try {
                const iframe = document.querySelector('iframe[src="/static/nice_dag_ui/index.html"]');
                if (!iframe || !iframe.contentWindow) return;

                const doc = iframe.contentWindow.document;
                const nodeList = doc.getElementById('nodeList');
                const edgeList = doc.getElementById('edgeList');
                const groupList = doc.getElementById('groupList');

                document.getElementById('details-nodes').textContent = nodeList ? nodeList.textContent.trim() : '(none)';
                document.getElementById('details-edges').textContent = edgeList ? edgeList.textContent.trim() : '(none)';
                document.getElementById('details-groups').textContent = groupList ? groupList.textContent.trim() : '(none)';
            } catch (e) {
                // Cross-origin or other issues, ignore
            }
        }
        
        // Restore panel visibility on page load
        window.addEventListener('load', function() {
            const activePalette = localStorage.getItem('activePalette');
            const container = document.getElementById('left-palettes');
            // Always start with all hidden
            if (container) {
                document.querySelectorAll('.palette').forEach((p) => p.classList.add('hidden'));
                container.classList.add('hidden');
            }
            setActiveRibbon('');
            
            // Only restore if there was a PREVIOUSLY opened palette (not on first load)
            if (activePalette && localStorage.getItem('paletteOpened') === 'true') {
                const target = document.getElementById(activePalette);
                if (container && target) {
                    target.classList.remove('hidden');
                    container.classList.remove('hidden');
                    setActiveRibbon(activePalette);
                }
            }
            // Refresh canvas info on load
            refreshCanvasInfo();
            updateDetailsPanel();
            // Update every 2 seconds
            setInterval(() => {
                refreshCanvasInfo();
                updateDetailsPanel();
            }, 2000);
        });
    </script>
    ''')
    
    # Header - must be top level, not nested
    with ui.header().classes('bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg px-6 py-4'):
        with ui.row().classes('w-full items-center justify-between'):
            with ui.column():
                ui.label('Simple DAG Editor').classes('text-2xl font-bold')
            
            with ui.row().classes('gap-2 items-center'):
                ui.link('📚 Docs', '/api/health').props('target=_blank')
                ui.link('🔧 API', '/api/').props('target=_blank')
    
    # Main content
    with ui.row().classes('flex-1 gap-0 w-full overflow-hidden').style('height: calc(100vh - 88px); min-height: calc(100vh - 88px);'):
            # Left ribbon + palettes
            with ui.element('div').classes('bg-gray-900 text-white border-r border-gray-700 shrink-0 flex flex-col items-center py-3 gap-2').style('height: 100%;').props('id=left-ribbon'):
                ui.button('ℹ️', on_click=lambda: ui.run_javascript("togglePalette('palette-info')")).props('flat dense data-panel=palette-info').classes('ribbon-btn')
                ui.button('💾', on_click=lambda: ui.run_javascript("togglePalette('palette-saved')")).props('flat dense data-panel=palette-saved').classes('ribbon-btn')
                ui.button('⚡', on_click=lambda: ui.run_javascript("togglePalette('palette-help')")).props('flat dense data-panel=palette-help').classes('ribbon-btn')
                ui.button('📊', on_click=lambda: ui.run_javascript("togglePalette('palette-canvas')")).props('flat dense data-panel=palette-canvas').classes('ribbon-btn')
                ui.button('📋', on_click=lambda: ui.run_javascript("togglePalette('palette-details')")).props('flat dense data-panel=palette-details').classes('ribbon-btn')
                ui.button('⚙️', on_click=lambda: ui.run_javascript("togglePalette('palette-tools')")).props('flat dense data-panel=palette-tools').classes('ribbon-btn')

            with ui.element('div').classes('bg-gray-900 text-white p-4 overflow-y-auto border-r border-gray-700 w-80 shrink-0 hidden').style('height: 100%;').props('id=left-palettes'):
                with ui.element('div').classes('palette hidden').props('id=palette-info'):
                    with ui.column().classes('w-full'):
                        ui.label('📊 DAG Info').classes('text-lg font-bold mb-4 text-blue-300')
                        ui.label('Use the controls at the top of the canvas to create, edit, save and load DAGs.').classes('text-sm text-gray-400 mb-4')
                
                        # Quick Info
                        ui.separator()
                        ui.label('ℹ️ Quick Info').classes('font-semibold text-blue-200')
                        stats_label = ui.label('📊 Statistics:\n• DAGs Saved: 0\n• Last Updated: Never').classes('text-sm text-gray-300')
                        
                        async def refresh_stats():
                            result = await list_dags()
                            if result.get('success'):
                                stats_label.text = f"📊 Statistics:\n• Total DAGs: {len(result['dags'])}\n• Last Updated: {datetime.now().strftime('%H:%M:%S')}"
                        
                        ui.button('Refresh Stats', on_click=refresh_stats).props('color=gray').classes('w-full')

                        async def load_stats():
                            # Refresh on load
                            await refresh_stats()
                        
                        # Load initial data
                        ui.timer(0.5, load_stats, once=True)

                with ui.element('div').classes('palette hidden').props('id=palette-saved'):
                    with ui.column().classes('w-full'):
                        ui.label('💾 Saved DAGs').classes('text-lg font-bold mb-4 text-blue-300')
                        dags_list = ui.expansion('View All Saved DAGs').classes('w-full')
                        
                        async def update_dags_list():
                            result = await list_dags()
                            dags_list.clear()
                            if result.get('success'):
                                for dag in result['dags']:
                                    with dags_list:
                                        with ui.row().classes('w-full items-center gap-2'):
                                            ui.label(f"{dag['name']} ({dag['nodes']} nodes, {dag['edges']} edges)").classes('text-sm')
                            else:
                                with dags_list:
                                    ui.label('No DAGs found').classes('text-sm text-gray-400')
                        
                        ui.button('List DAGs', on_click=update_dags_list).props('color=blue').classes('w-full')

                with ui.element('div').classes('palette hidden').props('id=palette-help'):
                    with ui.column().classes('w-full'):
                        ui.label('⚡ Help & Shortcuts').classes('text-lg font-bold mb-4 text-blue-300')
                        ui.label('''
                        1. Add Node: Enter name, select type
                        2. Connect: Click Connect, pick source → target
                        3. Group: Select nodes, click Group
                        4. Save: Enter name at top, click Save
                        5. Load: Select DAG and click Load
                        6. Zoom: Mouse wheel
                        7. Pan: Right-click + drag
                        ''').classes('text-xs text-gray-400 whitespace-pre-line')
                with ui.element('div').classes('palette hidden').props('id=palette-canvas'):
                    with ui.column().classes('w-full'):
                        ui.label('📊 Canvas Data').classes('text-lg font-bold mb-4 text-blue-300')
                        ui.html('''
                        <div style="color: #cbd5e1; font-size: 12px; line-height: 1.6;">
                            <p><strong>Nodes:</strong> <span id="canvas-node-count">0</span> nodes in the DAG</p>
                            <p><strong>Edges:</strong> <span id="canvas-edge-count">0</span> connections</p>
                            <p><strong>Groups:</strong> <span id="canvas-group-count">0</span> groups</p>
                            <hr style="border: none; border-top: 1px solid rgba(148, 163, 184, 0.2); margin: 12px 0;">
                            <p style="color: #94a3b8; font-size: 11px;">Use the details panel for full lists.</p>
                        </div>
                        ''', sanitize=False)
                        ui.button('Refresh Info', on_click=lambda: ui.run_javascript("refreshCanvasInfo()")).props('color=blue').classes('w-full mt-4')

                with ui.element('div').classes('palette hidden').props('id=palette-details'):
                    with ui.column().classes('w-full'):
                        ui.label('📋 Canvas Details').classes('text-lg font-bold mb-4 text-blue-300')
                        ui.html('''
                        <div style="color: #cbd5e1; font-size: 12px; line-height: 1.6;">
                            <div style="margin-bottom: 12px;">
                                <strong>Nodes</strong>
                                <div id="details-nodes" style="color: #94a3b8; font-size: 11px; white-space: pre-wrap;">(none)</div>
                            </div>
                            <div style="margin-bottom: 12px;">
                                <strong>Edges</strong>
                                <div id="details-edges" style="color: #94a3b8; font-size: 11px; white-space: pre-wrap;">(none)</div>
                            </div>
                            <div style="margin-bottom: 12px;">
                                <strong>Groups</strong>
                                <div id="details-groups" style="color: #94a3b8; font-size: 11px; white-space: pre-wrap;">(none)</div>
                            </div>
                        </div>
                        ''', sanitize=False)
                        ui.button('Refresh Details', on_click=lambda: ui.run_javascript("updateDetailsPanel()")).props('color=blue').classes('w-full mt-4')
                
                with ui.element('div').classes('palette hidden').props('id=palette-tools'):
                    with ui.column().classes('w-full'):
                        ui.label('⚙️ Tools').classes('text-lg font-bold mb-4 text-blue-300')
                        ui.label('Export/Import').classes('font-semibold text-blue-200 mb-2')
                        ui.button('📥 Export as JSON', on_click=lambda: ui.run_javascript(
                            "const dag=document.querySelector('#dagList').value;if(dag){fetch('/api/dags/'+dag).then(r=>r.json()).then(d=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(d.data.data,null,2)],{type:'application/json'}));a.download=dag+'.json';a.click()})}"
                        )).props('color=green').classes('w-full')
                        ui.separator()
                        ui.label('Settings').classes('font-semibold text-blue-200 mb-2')
                        ui.button('🔄 Clear All', on_click=lambda: ui.run_javascript(
                            "if(confirm('This will clear your current DAG. Continue?')){location.reload()}"
                        )).props('color=red').classes('w-full')            
            # Right side - Canvas area
            with ui.element('div').classes('flex-1 min-w-0 bg-gray-50 overflow-hidden flex flex-col').style('height: calc(100vh - 88px); min-height: 80vh;').props('id=canvas-area'):
                ui.html(
                    '<iframe src="/static/nice_dag_ui/index.html" '
                    'style="width: 100%; height: 100%; border: 0; background: white; display: block;" '
                        'title="DAG Editor"></iframe>',
                        sanitize=False,
                    ).classes('w-full flex-1 min-h-0')



if __name__ in ("__main__", "__mp_main__"):
    print("""
╔════════════════════════════════════════════════════════════════╗
║          🚀 Simple DAG Editor - Advanced Version               ║
║                                                                ║
║  Standalone NiceGUI Application with FastAPI Backend          ║
║                                                                ║
║  🌐 Web UI:        http://localhost:8000                      ║
║  🔌 API Base:      http://localhost:8000/api                  ║
║  📊 Health Check:  http://localhost:8000/api/health           ║
║  📁 Storage:       ./storage/                                 ║
║                                                                ║
║  API Endpoints:                                                ║
║  • GET    /api/dags              - List all DAGs              ║
║  • GET    /api/dags/{name}       - Load DAG                   ║
║  • POST   /api/dags/save         - Save DAG                   ║
║  • DELETE /api/dags/{name}       - Delete DAG                 ║
║  • POST   /api/dags/import       - Import DAG                 ║
║  • POST   /api/dags/{name}/export - Export DAG                ║
║  • GET    /api/stats             - Statistics                 ║
║  • GET    /api/health            - Health check               ║
║                                                                ║
║  Features:                                                     ║
║  ✓ Full-stack NiceGUI + FastAPI                               ║
║  ✓ DAG save/load/import/export                                ║
║  ✓ Persistent storage                                         ║
║  ✓ REST API endpoints                                         ║
║  ✓ Sample DAGs included                                       ║
║  ✓ Real-time statistics                                       ║
║  ✓ No external dependencies on git repos                      ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """)
    ui.run(title='Simple DAG Editor', host='0.0.0.0', port=8000, show=False)

from __future__ import annotations
from nicegui import ui, app
from pathlib import Path
import json
from fastapi import Request

# Add Quill CDN and custom event handlers
ui.add_head_html("""
<link href="https://cdn.quilljs.com/1.3.7/quill.snow.css" rel="stylesheet">
<script src="https://cdn.quilljs.com/1.3.7/quill.min.js"></script>
<script>
window.richEditorInstance = null;
window.richEditorInitPromise = null;

window.initRichEditor = function() {
    console.log('Initializing Quill...');
    var container = document.getElementById('html_editor_textarea');
    if (!container) {
        console.error('Editor container not found');
        return Promise.reject('Container not found');
    }

    var createEditor = function() {
        // Ensure the container is empty before re-instantiating
        container.innerHTML = '';
        var options = {
            theme: 'snow',
            placeholder: 'Edit HTML content...',
            modules: {
                toolbar: [
                    [{ 'header': [1, 2, 3, false] }],
                    ['bold', 'italic', 'underline', 'strike'],
                    [{ 'color': [] }, { 'background': [] }],
                    [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                    [{ 'indent': '-1' }, { 'indent': '+1' }],
                    ['link', 'blockquote', 'code-block'],
                    ['clean']
                ]
            }
        };

        var editor = new Quill(container, options);
        var editorEl = editor.root;
        editorEl.style.height = '450px';
        editorEl.style.maxHeight = '450px';
        editorEl.style.overflowY = 'auto';
        window.richEditorInstance = editor;
        console.log('Quill ready');
        return editor;
    };

    return Promise.resolve()
        .then(function() {
            if (window.richEditorInstance && window.richEditorInstance.off) {
                try {
                    window.richEditorInstance.off('text-change');
                } catch (err) {
                    console.warn('Failed to detach previous editor listeners', err);
                }
            }
            window.richEditorInstance = null;
        })
        .then(function() {
            window.richEditorInitPromise = Promise.resolve(createEditor());
            return window.richEditorInitPromise;
        });
};

window.setRichEditorContent = function(content) {
    console.log('setRichEditorContent called with:', (content || '').substring(0, 100));
    if (!window.richEditorInitPromise) {
        console.error('Editor not initialized');
        return;
    }

    window.richEditorInitPromise.then(function(editor) {
        if (editor && editor.clipboard && editor.clipboard.dangerouslyPasteHTML) {
            editor.setContents([]);
            editor.clipboard.dangerouslyPasteHTML(content || '');
            console.log('Content set successfully');
        } else {
            console.warn('Editor not ready for content');
        }
    });
};

window.getRichEditorContent = function() {
    if (window.richEditorInstance && window.richEditorInstance.root) {
        return window.richEditorInstance.root.innerHTML;
    }
    return '';
};

window.eventPush = function(eventName, payload) {
    console.log('eventPush:', eventName, payload);
    try {
        var evt = new CustomEvent('nicegui_' + eventName, {
            bubbles: true,
            detail: payload
        });
        document.dispatchEvent(evt);
    } catch(e) {
        console.error('Event push error:', e);
    }
};
</script>
""")

# =========================================================
# CONFIG / CONSTANTS
# =========================================================

DATA_DIR = Path('data')
DATA_FILE = DATA_DIR / 'project_plan.json'

STATUS_OPTIONS = [
    'Not Started',
    'In Progress',
    'Blocked',
    'Completed',
]

PEOPLE_OPTIONS = [
    'Alice', 'Bob', 'Charlie', 'Dana',
    'Eve', 'Frank', 'Grace', 'Henry',
]

# dynamic; rebuilt from rows
DELIVERABLE_OPTIONS: list[str] = []


# =========================================================
# INITIAL DATA
# =========================================================

def initial_rows() -> list[dict]:
    return [
        {"Id": 1, "Deliverable": "Frontend UI", "Task": "<b>Build login page</b>", "Effort": 8,
         "Status": "In Progress", "Due_date": "2026-01-15", "People": ["Alice"],
         "Comments": '<a href="https://jira.example.com/FE-101">FE‑101</a>', "Refer": "FE-101",
         "expanded": True},

        {"Id": 2, "Deliverable": "Frontend UI", "Task": "<i>Implement dashboard widgets</i>", "Effort": 16,
         "Status": "Not Started", "Due_date": "2026-01-22", "People": ["Bob"],
         "Comments": "", "Refer": "FE-102", "expanded": True},

        {"Id": 3, "Deliverable": "Frontend UI", "Task": "Add <u>dark mode</u> support", "Effort": 10,
         "Status": "Not Started", "Due_date": "2026-01-28", "People": ["Alice"],
         "Comments": "", "Refer": "FE-103", "expanded": True},

        {"Id": 4, "Deliverable": "Frontend UI", "Task": "Refactor <b>header navigation</b>", "Effort": 12,
         "Status": "In Progress", "Due_date": "2026-02-01", "People": ["Bob"],
         "Comments": '<a href="https://jira.example.com/FE-104">FE‑104</a>', "Refer": "FE-104",
         "expanded": True},

        {"Id": 5, "Deliverable": "Frontend UI", "Task": "Improve mobile responsiveness", "Effort": 14,
         "Status": "Not Started", "Due_date": "2026-02-05", "People": ["Eve"],
         "Comments": "", "Refer": "FE-105", "expanded": True},

        {"Id": 6, "Deliverable": "Backend API", "Task": "<b>Create auth endpoints</b>", "Effort": 12,
         "Status": "In Progress", "Due_date": "2026-01-18", "People": ["Charlie"],
         "Comments": '<a href="https://jira.example.com/BE-201">BE‑201</a>', "Refer": "BE-201",
         "expanded": True},

        {"Id": 7, "Deliverable": "Backend API", "Task": "Add rate limiting", "Effort": 10,
         "Status": "Not Started", "Due_date": "2026-01-25", "People": ["Dana"],
         "Comments": "", "Refer": "BE-202", "expanded": True},

        {"Id": 8, "Deliverable": "Backend API", "Task": "Implement <i>audit logging</i>", "Effort": 18,
         "Status": "In Progress", "Due_date": "2026-02-02", "People": ["Charlie"],
         "Comments": "", "Refer": "BE-203", "expanded": True},

        {"Id": 9, "Deliverable": "Backend API", "Task": "Optimize DB queries", "Effort": 20,
         "Status": "Not Started", "Due_date": "2026-02-10", "People": ["Dana"],
         "Comments": '<a href="https://jira.example.com/BE-204">BE‑204</a>', "Refer": "BE-204",
         "expanded": True},

        {"Id": 10, "Deliverable": "Backend API", "Task": "Add <b>API versioning</b>", "Effort": 15,
         "Status": "Not Started", "Due_date": "2026-02-12", "People": ["Charlie"],
         "Comments": "", "Refer": "BE-205", "expanded": True},

        {"Id": 11, "Deliverable": "Deployment Pipeline", "Task": "<u>Set up CI/CD</u>", "Effort": 20,
         "Status": "In Progress", "Due_date": "2026-02-01", "People": ["Eve"],
         "Comments": "", "Refer": "DP-301", "expanded": True},

        {"Id": 12, "Deliverable": "Deployment Pipeline", "Task": "Add staging environment", "Effort": 14,
         "Status": "Not Started", "Due_date": "2026-02-05", "People": ["Frank"],
         "Comments": "", "Refer": "DP-302", "expanded": True},

        {"Id": 13, "Deliverable": "Deployment Pipeline", "Task": "Automate rollback scripts", "Effort": 10,
         "Status": "Not Started", "Due_date": "2026-02-08", "People": ["Eve"],
         "Comments": "", "Refer": "DP-303", "expanded": True},

        {"Id": 14, "Deliverable": "Deployment Pipeline", "Task": "Add <b>artifact signing</b>", "Effort": 12,
         "Status": "In Progress", "Due_date": "2026-02-15", "People": ["Frank"],
         "Comments": "", "Refer": "DP-304", "expanded": True},

        {"Id": 15, "Deliverable": "Deployment Pipeline", "Task": "Improve build caching", "Effort": 16,
         "Status": "Not Started", "Due_date": "2026-02-20", "People": ["Eve"],
         "Comments": "", "Refer": "DP-305", "expanded": True},

        {"Id": 16, "Deliverable": "Analytics Engine", "Task": "<b>Design data model</b>", "Effort": 22,
         "Status": "In Progress", "Due_date": "2026-02-10", "People": ["Grace"],
         "Comments": '<a href="https://jira.example.com/AN-401">AN‑401</a>', "Refer": "AN-401",
         "expanded": True},

        {"Id": 17, "Deliverable": "Analytics Engine", "Task": "Implement ETL pipeline", "Effort": 30,
         "Status": "Not Started", "Due_date": "2026-02-25", "People": ["Henry"],
         "Comments": "", "Refer": "AN-402", "expanded": True},

        {"Id": 18, "Deliverable": "Analytics Engine", "Task": "Add <i>real‑time metrics</i>", "Effort": 18,
         "Status": "Not Started", "Due_date": "2026-03-01", "People": ["Grace"],
         "Comments": "", "Refer": "AN-403", "expanded": True},

        {"Id": 19, "Deliverable": "Analytics Engine", "Task": "Integrate with dashboard", "Effort": 14,
         "Status": "Not Started", "Due_date": "2026-03-05", "People": ["Henry"],
         "Comments": "", "Refer": "AN-404", "expanded": True},

        {"Id": 20, "Deliverable": "Analytics Engine", "Task": "Optimize aggregation jobs", "Effort": 20,
         "Status": "Not Started", "Due_date": "2026-03-10", "People": ["Grace"],
         "Comments": "", "Refer": "AN-405", "expanded": True},
    ]


# =========================================================
# STATE
# =========================================================

class LocalState:
    def __init__(self, value):
        self.value = value

rows: list[dict] = initial_rows()
selected_ids = LocalState([])      # list[int]
last_selected_id = LocalState(None)  # int | None
expanded_deliverables = LocalState(set())  # set[str]

# initialize expanded_deliverables from rows
def rebuild_expanded_state():
    expanded_deliverables.value = {r['Deliverable'] for r in rows}

def rebuild_deliverable_options():
    DELIVERABLE_OPTIONS.clear()
    for d in sorted({r['Deliverable'] for r in rows}):
        DELIVERABLE_OPTIONS.append(d)

rebuild_expanded_state()
rebuild_deliverable_options()


# =========================================================
# JSON PERSISTENCE
# =========================================================

def save_to_json(notify=True):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        'rows': rows,
        'expanded_deliverables': list(expanded_deliverables.value),
    }
    DATA_FILE.write_text(json.dumps(data, indent=2))
    if notify:
        try:
            ui.notify('Saved to data/project_plan.json')
        except RuntimeError:
            # No UI context available (e.g., called from API endpoint)
            print('Saved to data/project_plan.json')

def load_from_json():
    global rows
    if not DATA_FILE.exists():
        ui.notify('No data/project_plan.json found, using initial data')
        rows[:] = initial_rows()
    else:
        data = json.loads(DATA_FILE.read_text())
        rows[:] = data.get('rows', [])
        expanded_deliverables.value = set(data.get('expanded_deliverables', []))
    rebuild_deliverable_options()
    refresh_table_rows()
    ui.notify('Loaded from data/project_plan.json')


# =========================================================
# ID / CRUD HELPERS
# =========================================================

def next_id() -> int:
    return (max((r['Id'] for r in rows), default=0) + 1) if rows else 1

def add_deliverable():
    new_name = 'New Deliverable'
    # ensure uniqueness
    existing = {r['Deliverable'] for r in rows}
    i = 1
    name = new_name
    while name in existing:
        i += 1
        name = f'{new_name} {i}'

    new_row = {
        'Id': next_id(),
        'Deliverable': name,
        'Task': '',
        'Effort': 0,
        'Status': 'Not Started',
        'Due_date': '',
        'People': [],
        'Comments': '',
        'Refer': '',
        'expanded': True,
    }
    rows.append(new_row)
    expanded_deliverables.value.add(name)
    rebuild_deliverable_options()
    refresh_table_rows()

def add_task():
    if not selected_ids.value:
        ui.notify('Select a row to attach a task to')
        return
    # use deliverable of first selected row
    first_id = selected_ids.value[0]
    base_row = next((r for r in rows if r['Id'] == first_id), None)
    if not base_row:
        return
    deliverable = base_row['Deliverable']
    new_row = {
        'Id': next_id(),
        'Deliverable': deliverable,
        'Task': '',
        'Effort': 0,
        'Status': 'Not Started',
        'Due_date': '',
        'People': [],
        'Comments': '',
        'Refer': '',
        'expanded': True,
    }
    rows.append(new_row)
    expanded_deliverables.value.add(deliverable)
    refresh_table_rows()

def delete_selected():
    if not selected_ids.value:
        return
    global rows
    # if a deliverable row is selected, delete all rows with that deliverable
    selected_deliverables = {r['Deliverable'] for r in rows if r['Id'] in selected_ids.value}
    new_rows = []
    for r in rows:
        if r['Id'] in selected_ids.value:
            continue
        if r['Deliverable'] in selected_deliverables:
            continue
        new_rows.append(r)
    rows[:] = new_rows
    selected_ids.value = []
    rebuild_deliverable_options()
    rebuild_expanded_state()
    refresh_table_rows()


# =========================================================
# MODAL HTML EDITOR
# =========================================================

current_row = LocalState(None)   # dict | None
current_field = LocalState(None) # str | None

with ui.dialog() as editor_dialog, ui.card():
    ui.label('Edit HTML').classes('text-lg font-bold')
    # Use a div container for Quill enhancement
    ui.html('<div id="html_editor_textarea"></div>', sanitize=False)
    # Hidden input to store content before saving
    ui.html('<input type="hidden" id="editor_content_holder" value="" />', sanitize=False)
    with ui.row():
        ui.button('Save', on_click=lambda: save_html())
        ui.button('Cancel', on_click=editor_dialog.close)

def open_html_editor(row: dict, field: str):
    current_row.value = row
    current_field.value = field
    content = row.get(field, '') or ''
    print(f"\n=== OPEN EDITOR ===")
    print(f"Row ID: {row.get('Id')}")
    print(f"Field: {field}")
    print(f"Current content: {content[:100]}...")
    print(f"==================\n")
    
    editor_dialog.open()
    # Initialize Quill after dialog is shown and container is in DOM
    escaped_content = json.dumps(content)
    # Chain initialization and content setting
    ui.run_javascript(f"""
        window.initRichEditor().then(function() {{
            window.setRichEditorContent({escaped_content});
        }});
    """)

def save_html():
    if current_row.value and current_field.value:
        row_id = current_row.value.get('Id')
        field_name = current_field.value
        
        print(f"\n=== SAVE CLICKED ===")
        print(f"Row ID: {row_id}")
        print(f"Field: {field_name}")
        print(f"Current row in memory BEFORE save: {current_row.value.get(field_name, '')[:100]}...")
        
        # Get content from Quill and trigger save via JavaScript callback
        ui.run_javascript(f"""
            var content = window.getRichEditorContent();
            console.log('=== SAVE: Got content from Quill, length:', content.length);
            console.log('Content preview:', content.substring(0, 100));
            fetch('/api/save_editor_content', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{
                    content: content,
                    row_id: {row_id},
                    field: '{field_name}'
                }})
            }}).then(r => r.json()).then(data => {{
                console.log('=== SAVE: Server response:', data);
            }}).catch(e => {{
                console.error('=== SAVE: Failed:', e);
            }});
        """)
        
        # Schedule refresh in UI context with enough delay for the save to complete
        def do_refresh():
            print(f"\n=== REFRESH TABLE (UI CONTEXT) ===")
            
            # Reload from JSON to ensure we have the latest data
            if DATA_FILE.exists():
                data = json.loads(DATA_FILE.read_text())
                rows[:] = data.get('rows', [])
                print(f"Reloaded {len(rows)} rows from JSON")
            
            # Verify the data
            for r in rows:
                if r['Id'] == row_id:
                    print(f"Found row {row_id} in reloaded rows")
                    print(f"  Field '{field_name}' FULL value: {r.get(field_name, '')}")
                    break
            
            # Rebuild table rows completely
            visible_rows = [r for r in rows if r['Deliverable'] in expanded_deliverables.value]
            table.rows.clear()
            table.rows.extend(visible_rows)
            table.update()
            
            # Close the dialog
            editor_dialog.close()
            
            print(f"Dialog closed, table refreshed from file")
            print(f"===================================\n")
        
        # Wait 1 second to ensure the API call completes
        ui.timer(1.0, do_refresh, once=True)
    else:
        editor_dialog.close()

@app.post('/api/save_editor_content')
async def save_editor_content(request: Request):
    """Receive editor content from JavaScript and save it"""
    data = await request.json()
    content = data.get('content', '')
    row_id = data.get('row_id')
    field_name = data.get('field')
    
    print(f"\n=== API ENDPOINT CALLED ===")
    print(f"Received content length: {len(content)} chars")
    print(f"Content preview: {content[:100]}...")
    print(f"Row ID from request: {row_id}")
    print(f"Field from request: {field_name}")
    
    if row_id and field_name:
        print(f"Looking for row ID: {row_id}")
        
        found = False
        for r in rows:
            if r['Id'] == row_id:
                old_value = r.get(field_name, '')
                r[field_name] = content
                print(f"UPDATED row {row_id} field '{field_name}'")
                print(f"  Old value: {old_value[:50]}...")
                print(f"  New value: {content[:50]}...")
                
                # IMMEDIATELY verify the update stuck
                import time
                time.sleep(0.1)
                actual_value = r.get(field_name, '')
                print(f"  VERIFICATION after 0.1s: {actual_value[:50]}...")
                
                found = True
                break
        
        if not found:
            print(f"WARNING: Row {row_id} NOT FOUND in rows list!")
        else:
            save_to_json(notify=False)  # Persist to file without UI notification
            print(f"Saved to JSON")
        
        print(f"==========================\n")
        
    return {'status': 'ok', 'received_length': len(content), 'updated': found if row_id and field_name else False}


# =========================================================
# SELECTION LOGIC (CLICK, CTRL, SHIFT)
# =========================================================

def select_single(row_id: int):
    selected_ids.value = [row_id]
    last_selected_id.value = row_id

def toggle_ctrl(row_id: int):
    if row_id in selected_ids.value:
        selected_ids.value.remove(row_id)
    else:
        selected_ids.value.append(row_id)
    last_selected_id.value = row_id

def select_shift(row_id: int):
    if last_selected_id.value is None:
        select_single(row_id)
        return
    ids = [r['Id'] for r in rows]
    if last_selected_id.value not in ids or row_id not in ids:
        select_single(row_id)
        return
    i1 = ids.index(last_selected_id.value)
    i2 = ids.index(row_id)
    start, end = sorted([i1, i2])
    selected_ids.value = ids[start:end+1]

def handle_selection(e):
    row = e.args['row']
    row_id = row['Id']
    evt = e.args['evt']
    if evt.get('shiftKey'):
        select_shift(row_id)
    elif evt.get('ctrlKey'):
        toggle_ctrl(row_id)
    else:
        select_single(row_id)
    refresh_table_rows()


# =========================================================
# TABLE / GROUPING / EXPAND-COLLAPSE
# =========================================================

columns = [
    {'name': 'Id',          'label': 'Id',          'field': 'Id'},
    {'name': 'Deliverable', 'label': 'Deliverable', 'field': 'Deliverable'},
    {'name': 'Task',        'label': 'Task (HTML)', 'field': 'Task'},
    {'name': 'Effort',      'label': 'Effort',      'field': 'Effort'},
    {'name': 'Status',      'label': 'Status',      'field': 'Status'},
    {'name': 'Due_date',    'label': 'Due Date',    'field': 'Due_date'},
    {'name': 'People',      'label': 'People',      'field': 'People'},
    {'name': 'Comments',    'label': 'Comments',    'field': 'Comments'},
    {'name': 'Refer',       'label': 'Refer',       'field': 'Refer'},
]

table = ui.table(columns=columns, rows=rows, row_key='Id', pagination=20).classes('w-full')


def refresh_table_rows():
    # show only rows whose deliverable is in the expanded set
    visible_rows = [r for r in rows if r['Deliverable'] in expanded_deliverables.value]
    table.rows = visible_rows
    # Force a complete update
    table.update()
    print(f"DEBUG: refresh_table_rows called, showing {len(visible_rows)} of {len(rows)} rows")


# --- HTML rendering for Task / Comments / Refer ---
# Use template slots (props.value holds the cell value)
table.add_slot('body-cell-Task', """
<q-td class="pl-6" :data-row-id="props.row.Id">
  <div style="display:flex; align-items:center; justify-content:space-between;">
    <div v-html="props.value"></div>
    <q-btn flat dense icon="edit" @click="() => $parent.$emit('nicegui_cell_action', {detail: {action: 'edit', rowId: props.row.Id, colName: 'Task'}})"></q-btn>
  </div>
</q-td>
""")
table.add_slot('body-cell-Comments', """
<q-td :data-row-id="props.row.Id">
  <div style="display:flex; align-items:center; justify-content:space-between;">
    <div v-html="props.value"></div>
    <q-btn flat dense icon="edit" @click="() => $parent.$emit('nicegui_cell_action', {detail: {action: 'edit', rowId: props.row.Id, colName: 'Comments'}})"></q-btn>
  </div>
</q-td>
""")
table.add_slot('body-cell-Refer', """
<q-td :data-row-id="props.row.Id">
  <div style="display:flex; align-items:center; justify-content:space-between;">
    <div v-html="props.value"></div>
    <q-btn flat dense icon="edit" @click="() => $parent.$emit('nicegui_cell_action', {detail: {action: 'edit', rowId: props.row.Id, colName: 'Refer'}})"></q-btn>
  </div>
</q-td>
""")


# --- People (editable multi-select) ---
# Render people via a q-select and emit edits to server
table.add_slot('body-cell-People', """
<q-td :data-row-id="props.row.Id">
  <q-select multiple use-chips :options='["Alice","Bob","Charlie","Dana","Eve","Frank","Grace","Henry"]' :model-value="props.value" dense outlined style="min-width:160px" @update:model-value="(v) => $parent.$emit('nicegui_cell_update', {detail: {rowId: props.row.Id, field: 'People', value: v}})"/>
</q-td>
""")


# --- Deliverable cell (simple label) ---
# Toggling of groups is handled via double-click on the Deliverable cell (see on_cell_click)
table.add_slot('body-cell-Deliverable', """
<q-td :data-row-id="props.row.Id">
  <div style="display:flex; align-items:center; justify-content:space-between;">
    <div style="display:flex; align-items:center; gap:8px;">
      <q-btn flat dense icon="chevron_right" @click="() => $parent.$emit('nicegui_cell_action', {detail: {action: 'toggle', rowId: props.row.Id, colName: 'Deliverable', deliverable: props.value}})"></q-btn>
    </div>
    <div class="font-bold">{{ props.value }}</div>
    <q-btn flat dense icon="edit" @click="() => $parent.$emit('nicegui_cell_action', {detail: {action: 'edit', rowId: props.row.Id, colName: 'Deliverable'}})"></q-btn>
  </div>
</q-td>
""")

# ---------------------------------------------------------
# Server handler for cell edits emitted from slot templates
# ---------------------------------------------------------
def on_cell_edit(e):
    payload = e.args
    if not payload:
        return
    row_id = payload.get('id')
    field = payload.get('field')
    value = payload.get('value')
    row = next((r for r in rows if r['Id'] == row_id), None)
    if row is None:
        return
    # type conversions
    if field == 'Effort':
        try:
            row['Effort'] = int(value)
        except Exception:
            row['Effort'] = 0
    else:
        row[field] = value
    if field == 'Deliverable':
        rebuild_deliverable_options()
    refresh_table_rows()

# register handler
table.on('edit', on_cell_edit)

# Custom event handlers for cell_action and cell_update
def handle_cell_action(e):
    detail = e.args.get('detail', {})
    action = detail.get('action')
    row_id = detail.get('rowId')
    col_name = detail.get('colName')
    deliverable = detail.get('deliverable')
    
    print(f"DEBUG handle_cell_action: action={action}, row_id={row_id}, col_name={col_name}")
    
    row = next((r for r in rows if r['Id'] == row_id), None)
    
    if action == 'edit' and row and col_name in ('Task', 'Comments', 'Refer', 'Deliverable'):
        print(f"DEBUG Opening HTML editor for {col_name}")
        open_html_editor(row, col_name)
        
    elif action == 'toggle' and deliverable:
        print(f"DEBUG Toggling deliverable: {deliverable}")
        if deliverable in expanded_deliverables.value:
            expanded_deliverables.value.remove(deliverable)
        else:
            expanded_deliverables.value.add(deliverable)
        refresh_table_rows()

def handle_cell_update(e):
    detail = e.args.get('detail', {})
    row_id = detail.get('rowId')
    field = detail.get('field')
    value = detail.get('value')
    
    print(f"DEBUG handle_cell_update: row_id={row_id}, field={field}, value={value}")
    
    row = next((r for r in rows if r['Id'] == row_id), None)
    if row:
        if field == 'Effort':
            try:
                row['Effort'] = int(value)
            except Exception:
                row['Effort'] = 0
        else:
            row[field] = value
        if field == 'Deliverable':
            rebuild_deliverable_options()
        refresh_table_rows()

table.on('nicegui_cell_action', handle_cell_action)
table.on('nicegui_cell_update', handle_cell_update)




# =========================================================
# INLINE EDITORS (TYPE-AWARE)
# =========================================================

# Effort numeric (editable)
table.add_slot('body-cell-Effort', """
<q-td :data-row-id="props.row.Id">
  <q-input type="number" :value="props.value" dense outlined style="width:80px" @update:model-value="(v) => $parent.$emit('nicegui_cell_update', {detail: {rowId: props.row.Id, field: 'Effort', value: v}})"/>
</q-td>
""")

# Status (editable)
table.add_slot('body-cell-Status', """
<q-td :data-row-id="props.row.Id">
  <q-select :options='["Not Started","In Progress","Blocked","Completed"]' :model-value="props.value" dense outlined style="width:140px" @update:model-value="(v) => $parent.$emit('nicegui_cell_update', {detail: {rowId: props.row.Id, field: 'Status', value: v}})"/>
</q-td>
""")

# Due date (editable)
table.add_slot('body-cell-Due_date', """
<q-td :data-row-id="props.row.Id">
  <q-input :value="props.value" dense outlined style="width:130px" @update:model-value="(v) => $parent.$emit('nicegui_cell_update', {detail: {rowId: props.row.Id, field: 'Due_date', value: v}})"/>
</q-td>
""")

# ID + deliverable label
# Note: editing deliverable inline was removed; use Add Deliverable / editing dialogs instead.
table.add_slot('body-cell-Id', '<q-td><div class="row items-center gap-2"><span class="text-xs text-gray-600">{{ props.row.Id }}</span><span class="font-bold">{{ props.row.Deliverable }}</span></div></q-td>')




# =========================================================
# CLICK HANDLING (DOUBLE-CLICK FOR HTML EDIT)
# =========================================================

def on_cell_click(e):
    print(f"DEBUG on_cell_click called with args: {e.args}")
    evt = e.args.get('evt', {})
    row = e.args.get('row')
    col = e.args.get('col')
    action = e.args.get('action')
    
    print(f"DEBUG evt: {evt}")
    print(f"DEBUG row: {row}")
    print(f"DEBUG col: {col}")
    print(f"DEBUG action (initial): {action}")

    # also check for action embedded inside DOM event detail (dispatched by client)
    if not action:
        detail = evt.get('detail')
        print(f"DEBUG detail from evt: {detail}")
        if isinstance(detail, dict) and 'action' in detail:
            action = detail.get('action')
            print(f"DEBUG action from detail: {action}")

    # explicit client-side edit action (modal) if no value was provided
    if action == 'edit' and col and col.get('name') in ('Task', 'Comments', 'Refer', 'Deliverable'):
        print(f"DEBUG Opening editor for field: {col.get('name')}")
        # if the DOM event carried a field/value payload, apply it directly
        detail = evt.get('detail')
        if isinstance(detail, dict) and 'field' in detail and 'value' in detail:
            # apply inline edit
            row_id = detail.get('id') or row.get('Id') if row else None
            r = next((rr for rr in rows if rr['Id'] == row_id), None)
            if r:
                r[detail['field']] = detail['value']
                if detail['field'] == 'Deliverable':
                    rebuild_deliverable_options()
                refresh_table_rows()
                return
        # otherwise open modal
        print(f"DEBUG Calling open_html_editor with row={row}, field={col['name']}")
        open_html_editor(row, col['name'])
        return

    # explicit client-side toggle action for deliverable
    if action == 'toggle' and col and col.get('name') == 'Deliverable':
        d = row['Deliverable']
        if d in expanded_deliverables.value:
            expanded_deliverables.value.remove(d)
        else:
            expanded_deliverables.value.add(d)
        refresh_table_rows()
        return

    # fallback: double-click → edit for Task / Comments / Refer / Deliverable
    if evt.get('detail') == 2 and col and col.get('name') in ('Task', 'Comments', 'Refer', 'Deliverable'):
        open_html_editor(row, col['name'])
        return

    # otherwise selection logic
    handle_selection(e)

# register handler
table.on('cellClick', on_cell_click)

# =========================================================
# TOP-LEVEL CONTROLS
# =========================================================

with ui.row().classes('mb-2'):
    ui.button('Add Deliverable', on_click=add_deliverable)
    ui.button('Add Task', on_click=add_task)
    ui.button('Delete Selected', on_click=delete_selected, color='red')
    ui.button('Save JSON', on_click=save_to_json)
    ui.button('Load JSON', on_click=load_from_json)

ui.label('Project Plan (Goal‑2)').classes('text-2xl font-bold mb-2')

# ensure table reflects initial state
refresh_table_rows()

ui.run()
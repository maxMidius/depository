from nicegui import ui,app
import json
import os

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
app.add_static_files('/static', STATIC_DIR) 


def tabulator_with_tinymce(
    table_id: str,
    options: dict,
    height: str = "400px",
):

    # Tabulator CSS + JS
    ui.add_head_html('''
        <link href="https://unpkg.com/tabulator-tables@5.6.0/dist/css/tabulator.min.css" rel="stylesheet">
        <link href="https://cdn.quilljs.com/1.3.6/quill.snow.css" rel="stylesheet">
        <style>
            .tabulator { font-size: 14px; }
            .tabulator-row { height: 80px !important; }
            .tabulator-cell { vertical-align: top; white-space: pre-wrap; word-wrap: break-word; }
        </style>
    ''')
    ui.add_body_html('''
        <script src="https://unpkg.com/tabulator-tables@5.6.0/dist/js/tabulator.min.js"></script>
        <script src="https://cdn.quilljs.com/1.3.6/quill.js"></script>
    ''')

    # Engine JS
    ui.add_body_html('''
        <script src="/static/tabulator_edit.js"></script>
    ''')

    # Table container
    ui.html(f'<div id="{table_id}" style="height:{height};"></div>', sanitize=False)

    # Row height control
    ui.html(f'''
        <div style="margin-top:15px; display:flex; gap:15px; align-items:center; background:#f5f5f5; border:1px solid #ddd; border-radius:4px; padding:10px;">
            <label for="{table_id}_height_slider" style="font-weight:bold; margin:0;">Row Height:</label>
            <input type="range" id="{table_id}_height_slider" min="30" max="200" value="80" style="width:150px; cursor:pointer;">
            <span id="{table_id}_height_display" style="min-width:40px; font-weight:bold;">80px</span>
        </div>
    ''', sanitize=False)

    # Modal for TinyMCE
    modal_id = f'{table_id}_modal'
    textarea_id = f'{table_id}_textarea'

    ui.html(f'''
    <div id="{modal_id}" 
         style="display:none; position:fixed; top:0; left:0; width:100%; height:100%;
                background:rgba(0,0,0,0.5); z-index:2000; justify-content:center; align-items:center;">
        <div style="background:white; border-radius:8px; padding:20px; max-width:900px; width:90%; max-height:85vh; overflow-y:auto;">
            <h2 style="margin-top:0; margin-bottom:15px;">Edit Cell Content</h2>
            <div id="{textarea_id}" style="border:1px solid #ccc; border-radius:4px; background:white; min-height:300px;"></div>
            <div style="margin-top:15px; display:flex; gap:10px; justify-content:flex-end;">
                <button class="tiny-cancel" style="background:#6c757d; color:white; border:none; padding:8px 16px; border-radius:4px; cursor:pointer;">Cancel</button>
                <button class="tiny-save" style="background:#007bff; color:white; border:none; padding:8px 16px; border-radius:4px; cursor:pointer;">Save</button>
            </div>
        </div>
    </div>
    ''', sanitize=False)

    # Initialize Tabulator + attach cellClick handler
    options_json = json.dumps(options)
    ui.add_body_html(f"""
        <script>
            window.waitForElementAndInit(
                "{table_id}",
                {repr(options_json)}
            );

            const attachCellClick = setInterval(function() {{
                const table = window["{table_id}_table"];
                if (table) {{
                    clearInterval(attachCellClick);
                    table.on("cellClick", function(e, cell) {{
                        const row = cell.getRow();
                        const field = cell.getField();
                        console.log('Cell clicked:', row.getData(), field);
                        window.openTinyEditor(
                            "{table_id}",
                            row,
                            field,
                            "{modal_id}",
                            "{textarea_id}"
                        );
                    }});
                }}
            }}, 100);

            // Row height slider control
            const heightSlider = document.getElementById("{table_id}_height_slider");
            const heightDisplay = document.getElementById("{table_id}_height_display");
            
            if (heightSlider) {{
                console.log('Row height slider found:', heightSlider);
                heightSlider.addEventListener('input', function(e) {{
                    const newHeight = parseInt(e.target.value);
                    heightDisplay.textContent = newHeight + 'px';
                    console.log('Row height slider input event fired. New height:', newHeight);
                    
                    const table = window["{table_id}_table"];
                    if (table) {{
                        console.log('Tabulator table found:', table);
                        // Get all rows and set their height directly
                        const rows = table.getRows();
                        console.log('Tabulator rows:', rows);
                        rows.forEach(row => {{
                            const el = row.getElement();
                            if (el) {{
                                el.style.height = newHeight + 'px';
                                console.log('Set row element height:', el, newHeight);
                            }}
                        }});
                        // Also update CSS for any newly added rows
                        const tableContainer = document.getElementById('{table_id}');
                        if (tableContainer) {{
                            tableContainer.querySelectorAll('.tabulator-row').forEach(rowEl => {{
                                rowEl.style.height = newHeight + 'px';
                                console.log('Set DOM row height:', rowEl, newHeight);
                            }});
                        }}
                    }} else {{
                        console.log('Tabulator table not found for id:', "{table_id}_table");
                    }}
                }});
            }} else {{
                console.log('Row height slider NOT found for id:', "{table_id}_height_slider");
            }}
        </script>
    """)


def demo_page():
    columns = [
        {"title": "Title", "field": "title"},
        {"title": "Description (HTML)", "field": "description", "formatter": "html"},
        {"title": "Notes", "field": "notes"},
    ]

    rows = [
        {
            "title": "Item 1",
            "description": "<p><strong>Bold text</strong> and <em>italic</em> content.</p>",
            "notes": "Click any cell to edit.",
        },
        {
            "title": "Item 2",
            "description": "<p>Another <span style='color:red;'>HTML</span> block.</p>",
            "notes": "Supports full HTML.",
        },
    ]

    options = {
        "data": rows,
        "columns": columns,
        "layout": "fitColumns",
        "movableColumns": True,
        "resizableColumns": True,
        "height": "100%",
    }

    ui.label("Tabulator + TinyMCE Rich HTML Editor").classes("text-lg font-bold")
    tabulator_with_tinymce("rich_tabulator", options)


demo_page()
ui.run()

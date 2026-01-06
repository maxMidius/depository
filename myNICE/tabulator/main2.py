from nicegui import ui, app
import json
import os

# Path to static folder
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
print (STATIC_DIR)

# ROOT = Path(__file__).resolve().parent.parent
app.add_static_files('/static', STATIC_DIR) 


def tabulator_table(table_id: str, options: dict, height: str = "400px"):

    # Load Tabulator CSS + JS
    ui.add_head_html('''
        <link href="https://unpkg.com/tabulator-tables@5.6.0/dist/css/tabulator.min.css" rel="stylesheet">
        <style>.tabulator { font-size: 14px; }</style>
    ''')
    ui.add_body_html('''
        <script src="https://unpkg.com/tabulator-tables@5.6.0/dist/js/tabulator.min.js"></script>
    ''')

    # Load our engine JS
    ui.add_body_html(f'''
        <script src="/static/tabulator_engine.js"></script>
    ''')

    # Render column selector above table
    ui.html(f'''
        <div style="margin-bottom:15px; background:#f5f5f5; border:1px solid #ddd; border-radius:4px; padding:10px;">
            <button id="{table_id}_btn" 
                    style="background:#007bff; color:white; border:none; padding:8px 12px; border-radius:4px; cursor:pointer; font-weight:bold; display:flex; align-items:center; gap:6px;">
                <span id="{table_id}_arrow" style="font-size:12px;">▼</span>
                <span>Column Visibility</span>
            </button>
            <div id="{table_id}_menu" 
                 style="display:none; padding:12px; margin-top:8px; display:flex; flex-wrap:wrap; gap:12px; background:white; border-radius:4px;">
            </div>
        </div>
    ''', sanitize=False)

    # Render table container
    ui.html(f'<div id="{table_id}" style="height:{height};"></div>', sanitize=False)

    # Toggle dropdown + build chooser
    ui.add_body_html(f"""
        <script>
            window.waitForElementAndInit(
                "{table_id}",
                '{json.dumps(options)}'
            );
            
            // Setup button after DOM is ready
            setTimeout(function() {{
                const btn = document.getElementById("{table_id}_btn");
                const menu = document.getElementById("{table_id}_menu");
                const arrow = document.getElementById("{table_id}_arrow");
                
                if (btn && menu) {{
                    btn.onclick = function() {{
                        const isHidden = menu.style.display === "none";
                        menu.style.display = isHidden ? "flex" : "none";
                        arrow.textContent = isHidden ? "▲" : "▼";
                        window.buildColumnChooser("{table_id}", "{table_id}_menu");
                    }};
                    // Initialize the columns on first load
                    window.buildColumnChooser("{table_id}", "{table_id}_menu");
                }}
            }}, 100);
        </script>
    """)


def demo_page():
    columns = [
        {"title": "Name", "field": "name", "headerFilter": "input"},
        {"title": "Age", "field": "age", "hozAlign": "center"},
        {"title": "City", "field": "city"},
    ]

    rows = [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Bob", "age": 25, "city": "Boston"},
        {"name": "Charlie", "age": 35, "city": "Chicago"},
    ]

    options = {
        "data": rows,
        "columns": columns,
        "layout": "fitColumns",
        "movableColumns": True,
        "resizableColumns": True,
        "height": "100%",
    }

    ui.label("Tabulator Table with Column Chooser").classes("text-lg font-bold")
    tabulator_table("my_tabulator", options)


demo_page()
ui.run()

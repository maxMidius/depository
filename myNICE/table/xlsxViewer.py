from nicegui import ui
import pandas as pd
import os
import re
import warnings

# Suppress pandas date inference warnings
warnings.filterwarnings("ignore", message=".*falling back to `dateutil`.*")

# ---------------------------------------------------------
# Utility: Load XLSX into NiceGUI table format
# Type detection helpers
# ---------------------------------------------------------

HTML_PATTERN = re.compile(r'<[^>]+>')

def is_html_column(series: pd.Series) -> bool:
    """Return True if any cell in the column looks like HTML."""
    return series.astype(str).str.contains(HTML_PATTERN).any()

def is_numeric_column(series: pd.Series) -> bool:
    return pd.to_numeric(series, errors='coerce').notna().all()

def is_boolean_column(series: pd.Series) -> bool:
    s = series.dropna().astype(str).str.lower()
    return s.isin(['true', 'false', '0', '1', 'yes', 'no']).all()

def is_date_column(series: pd.Series) -> bool:
    if pd.api.types.is_datetime64_any_dtype(series):
        return True
    try:
        # Check only first few non-null values to avoid performance issues and warnings
        sample = series.dropna().head(3)
        if sample.empty:
            return False
        pd.to_datetime(sample, errors='raise')
        return True
    except Exception:
        return False

def is_long_text_column(series: pd.Series, threshold=80) -> bool:
    s = series.astype(str)
    return s.str.len().max() > threshold or s.str.contains('\n').any()

# ---------------------------------------------------------
# Load XLSX with auto type detection
# ---------------------------------------------------------
def load_xlsx(path: str):
    df = pd.read_excel(path)

    columns = []
    col_types = {}
    for c in df.columns:
        col = df[c]

        html = is_html_column(col)
        numeric = is_numeric_column(col)
        boolean = is_boolean_column(col)
        date = is_date_column(col)
        longtext = is_long_text_column(col)

        # Default: sortable unless HTML or long text
        sortable = not html and not longtext

        # Priority detection: HTML first to ensure correct rendering
        if html:
            ctype = 'html'
        elif numeric:
            ctype = 'number'
        elif date:
            ctype = 'date'
        elif boolean:
            ctype = 'boolean'
        elif longtext:
            ctype = 'longtext'
        else:
            ctype = 'text'

        col_types[c] = ctype
        col_def = {
            'name': c,
            'label': c,
            'field': c,
            'sortable': sortable,
            'type': ctype,
        }
        columns.append(col_def)


    # Do not replace newlines for longtext or html columns; rendering will handle it
    # Ensure each row has a unique ID for Quasar/NiceGUI
    df = df.copy()
    if 'id' not in df.columns:
        df['id'] = range(len(df))

    rows = df.to_dict(orient='records')
    return columns, rows
# ---------------------------------------------------------
# Main XL Viewer Component
# ---------------------------------------------------------
def xlviewer():

    ui.label("📁 XLSX Viewer").classes("text-2xl font-bold mb-4")

    # ---------------- Dark Mode Toggle ----------------
    def toggle_dark_mode(e):
        if e.value:
            ui.dark_mode().enable()
        else:
            ui.dark_mode().disable()

    ui.switch(
        'Dark Mode',
        on_change=toggle_dark_mode
    ).classes('mb-4')

    # ---------------- Search Box ----------------
    search = ui.input(
        'Search',
        on_change=lambda e: apply_filter(e.value)
    ).classes('w-96 mb-4')

    # ---------------- Directory Input ----------------
    directory = ui.input(
        label="Directory containing XLSX files",
        value="sample_data",
        on_change=lambda e: refresh_file_list()
    ).classes("w-96")

    # ---------------- XLSX File Dropdown ----------------
    file_select = ui.select(
        options=[],
        label="Select XLSX file",
        on_change=lambda e: load_selected_file()
    ).classes("w-96")

    # ---------------- Column Chooser ----------------
    column_box = ui.column().classes("p-2 border rounded w-64")
    column_box.visible = False

    # ---------------- Freeze Column Chooser ----------------
    freeze_box = ui.column().classes("p-2 border rounded w-64 mt-2")
    freeze_box.visible = False

    # ---------------- Table Placeholder ----------------
    table_container = ui.column().classes("w-full")

    # State
    state = {
        "columns": [],
        "rows": [],
        "visible": {},
        "frozen": None,
        "table": None,
    }

    # ---------------------------------------------------------
    # Refresh XLSX file list when directory changes
    # ---------------------------------------------------------
    def refresh_file_list():
        path = directory.value.strip()
        if not os.path.isdir(path):
            file_select.options = []
            return

        files = [f for f in os.listdir(path) if f.lower().endswith(".xlsx")]
        file_select.options = files

        if files:
            file_select.value = files[0]
            load_selected_file()

    # ---------------------------------------------------------
    # Load selected XLSX file into table
    # ---------------------------------------------------------
    def load_selected_file():
        if not file_select.value:
            return

        path = os.path.join(directory.value, file_select.value)
        columns, rows = load_xlsx(path)

        state["columns"] = columns
        state["rows"] = rows
        state["visible"] = {c["name"]: True for c in columns}
        state["frozen"] = None

        build_column_chooser()
        build_freeze_chooser()
        build_table()

    # ---------------------------------------------------------
    # Build Column Chooser UI
    # ---------------------------------------------------------
    def build_column_chooser():
        column_box.clear()
        column_box.visible = True

        with column_box:
            ui.label("Columns").classes("font-bold")

            for col in state["columns"]:
                ui.checkbox(
                    col["label"],
                    value=True,
                    on_change=lambda e, col=col: toggle_column(col["name"], e.value)
                )

    # ---------------------------------------------------------
    # Build Freeze Column Chooser
    # ---------------------------------------------------------
    def build_freeze_chooser():
        freeze_box.clear()
        freeze_box.visible = True

        with freeze_box:
            ui.label("Freeze Column").classes("font-bold")

            ui.select(
                options=[c["name"] for c in state["columns"]],
                label="Pin column",
                on_change=lambda e: freeze_column(e.value)
            )

    # ---------------------------------------------------------
    # Build Table UI (type-aware)
    # ---------------------------------------------------------
    def build_table():
        table_container.clear()

        visible_columns = [
            c for c in state["columns"] if state["visible"][c["name"]]
        ]

        with table_container:
            table = ui.table(
                columns=visible_columns,
                rows=state["rows"],
                row_key="id",
                pagination={"rowsPerPage": 20},
            ).classes("w-full")

            # Sorting is controlled by 'sortable' in column defs

            # Freeze column if selected (visual aid only)
            if state["frozen"]:
                table.props('virtual-scroll')
                table.props(f'virtual-scroll-sticky-start="{state["frozen"]}"')

            # Type-aware slots
            for col in state["columns"]:
                name = col['name']
                ctype = col.get('type', 'text')

                if ctype == 'html':
                    table.add_slot(
                        f"body-cell-{name}",
                        f'<q-td v-html="props.value"></q-td>',
                    )
                elif ctype == 'longtext':
                    table.add_slot(
                        f"body-cell-{name}",
                        f'<q-td><div style="white-space: pre-wrap">{{{{ props.value }}}}</div></q-td>',
                    )
                elif ctype == 'boolean':
                    table.add_slot(
                        f"body-cell-{name}",
                        f'<q-td><q-checkbox :model-value="props.value" disable></q-checkbox></q-td>',
                    )
                else:
                    # default rendering
                    table.add_slot(
                        f"body-cell-{name}",
                        f'<q-td>{{{{ props.value }}}}</q-td>',
                    )

            state["table"] = table

    # ---------------------------------------------------------
    # Toggle column visibility
    # ---------------------------------------------------------
    def toggle_column(col_name: str, show: bool):
        state["visible"][col_name] = show
        build_table()

    # ---------------------------------------------------------
    # Freeze a column
    # ---------------------------------------------------------
    def freeze_column(col_name: str):
        state["frozen"] = col_name
        build_table()

    # ---------------------------------------------------------
    # Apply search filter
    # ---------------------------------------------------------
    def apply_filter(value: str):
        if state["table"]:
            state["table"].props(f'filter="{value}"')

    # Initial load
    refresh_file_list()


# ---------------------------------------------------------
# Run App
# ---------------------------------------------------------

xlviewer()
ui.run()

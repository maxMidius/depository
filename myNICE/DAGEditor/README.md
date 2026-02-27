# DAG Editor Pro - Standalone NiceGUI Application

A complete, self-contained DAG (Directed Acyclic Graph) editor built with **NiceGUI** (which uses **FastAPI** underneath).

## Overview

This is a **standalone application** with:
- ✅ Complete Python backend (NiceGUI + FastAPI)
- ✅ Web-based UI with professional styling
- ✅ DAG save/load/import/export functionality
- ✅ Persistent file-based storage
- ✅ REST API endpoints
- ✅ **NO external dependencies** on git repositories
- ✅ **Self-contained** in its own directory

## Features

### Core Functionality
- 📊 **Create & Edit DAGs**: Interactive canvas for building workflows
- 💾 **Save/Load**: Persistent storage with descriptions
- 📤 **Import/Export**: JSON file support for DAG interchange
- 📈 **Statistics**: Real-time node and edge counts
- 🌐 **Web Interface**: Beautiful, responsive UI
- 🔌 **REST API**: Full API for programmatic access

### Storage
- Local file system (`./storage/`)
- Sample DAGs included:
  - `simple-pipeline` - ETL example
  - `parallel-tasks` - Multi-task workflow

## Quick Start

### Step 1: Setup Environment

```bash
cd ~/GIT/depository/myNICE/DAGEditor

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
# Basic run
python app_advanced.py

# With reload (development)
python -m nicegui app_advanced.py  --reload
```

The app will start and display:
```
🌐 Web UI:        http://localhost:8000
🔌 API Base:      http://localhost:8000/api
```

### Step 3: Access the Application

Open your browser and navigate to: **http://localhost:8000**

## Usage

### Create a New DAG

1. Enter a DAG name in the "DAG Name" field
2. (Optional) Add a description
3. Click "Save"
4. Your DAG is saved to `./storage/`

### Load an Existing DAG

1. Click "Refresh" to load the DAG list
2. Select a DAG from the dropdown
3. View the statistics (nodes and edges)

### Import a DAG

1. Click "Import JSON"
2. Select a JSON file with this structure:
   ```json
   {
     "data": {
       "nodes": [
         {"id": "start", "label": "Start", "type": "start"},
         {"id": "task", "label": "Task", "type": "normal"},
         {"id": "end", "label": "End", "type": "end"}
       ],
       "edges": [
         {"source": "start", "target": "task"},
         {"source": "task", "target": "end"}
       ]
     }
   }
   ```

### Export a DAG

1. Select a DAG from the list
2. Click "Export JSON"
3. File downloads as `{dag_name}.json`

## REST API Endpoints

### List all DAGs
```bash
curl http://localhost:8000/api/dags
```

Response:
```json
{
  "success": true,
  "dags": [
    {
      "name": "my-workflow",
      "description": "My workflow",
      "created": "2026-02-26T10:00:00",
      "updated": "2026-02-26T10:00:00",
      "nodes": 5,
      "edges": 4
    }
  ]
}
```

### Load a specific DAG
```bash
curl http://localhost:8000/api/dags/my-workflow
```

### Save a DAG
```bash
curl -X POST http://localhost:8000/api/dags/save \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-workflow",
    "description": "Test DAG",
    "nodes": [...],
    "edges": [...]
  }'
```

### Delete a DAG
```bash
curl -X DELETE http://localhost:8000/api/dags/my-workflow
```

### Export DAG as JSON
```bash
curl http://localhost:8000/api/dags/my-workflow/export > my-workflow.json
```

### Get Statistics
```bash
curl http://localhost:8000/api/stats
```

### Health Check
```bash
curl http://localhost:8000/api/health
```

## Directory Structure

```
DAGEditor/
├── app.py                   # Basic NiceGUI app
├── app_advanced.py          # Advanced version with full API (RECOMMENDED)
├── requirements.txt         # Python dependencies
├── storage/                 # DAG storage (created on first run)
│   ├── simple-pipeline.json
│   └── parallel-tasks.json
├── venv/                    # Virtual environment
├── README.md               # This file
└── LICENSE                 # License info
```

## Configuration

### Change Port
Edit `app_advanced.py` and modify:
```python
if __name__ in ("__main__", "__mp_main__"):
    ui.run(..., port=YOUR_PORT)
```

### Change Host
```python
ui.run(..., host='0.0.0.0')  # Accessible from network
ui.run(..., host='127.0.0.1')  # Localhost only
```

### Custom Storage Path
Edit the storage directory in `app_advanced.py`:
```python
STORAGE_DIR = Path(__file__).parent / 'your_custom_path'
```

## Data Format

### DAG JSON Structure

```json
{
  "name": "my-workflow",
  "description": "Workflow description",
  "data": {
    "nodes": [
      {
        "id": "node1",
        "label": "Node Label",
        "type": "start|normal|end",
        "x": 100,
        "y": 50,
        "properties": {}
      }
    ],
    "edges": [
      {
        "source": "node1",
        "target": "node2",
        "id": "edge1",
        "label": "optional"
      }
    ]
  },
  "created": "2026-02-26T10:00:00",
  "updated": "2026-02-26T10:00:00"
}
```

## Node Types

- **start**: Entry point (green)
- **normal**: Processing node (blue)
- **end**: Exit point (gray)

## Integration with NiceGUI Server

This application IS a NiceGUI server. You can:

1. **Run standalone**: Perfect for local development
2. **Embed in larger app**: Import and use the API
3. **Deploy to server**: Use production ASGI server

### Production Deployment

```bash
# Using Gunicorn + Uvicorn
pip install gunicorn
gunicorn app_advanced:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Troubleshooting

### Port 8000 already in use
```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use different port
```

### Module not found errors
Ensure virtual environment is activated:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### CORS errors in browser
Already handled - CORS is enabled in `app_advanced.py`

### Can't save DAGs
Check permissions on `./storage/` directory:
```bash
ls -la storage/
chmod 755 storage/
```

## Next Steps

### Extend the Application

1. **Add Canvas Rendering**:
   - Replace canvas placeholder with D3.js or React component
   - Implement drag-and-drop node creation

2. **Enhanced Storage**:
   - Switch to SQLite/PostgreSQL
   - Add backup/restore functionality
   - Implement versioning

3. **Advanced Features**:
   - DAG validation and execution
   - Workflow scheduling
   - Audit logging
   - User authentication

4. **Integration**:
   - Connect to Airflow/Prefect
   - Export to Docker Compose
   - CI/CD pipeline generation

## Development

### Running in Development Mode

```bash
source venv/bin/activate
python -m nicegui app_advanced.py --reload --host 127.0.0.1 --port 8000
```

### Testing the API

```bash
# Create test DAGs
curl -X POST http://localhost:8000/api/dags/save \
  -H "Content-Type: application/json" \
  -d '{"name": "test1", "nodes": [], "edges": []}'

# List all
curl http://localhost:8000/api/dags

# Delete
curl -X DELETE http://localhost:8000/api/dags/test1
```

## Files

| File | Purpose |
|------|---------|
| `app.py` | Basic NiceGUI implementation |
| `app_advanced.py` | **Recommended** - Full-featured with complete API |
| `requirements.txt` | Python dependencies |
| `storage/` | DAG storage directory |
| `README.md` | This documentation |

## Architecture

```
┌─────────────────────────────────────────┐
│         NiceGUI Web Interface            │  ← Browser UI
│     (HTML, CSS, JavaScript)              │
└────────────────┬────────────────────────┘
                 │
              HTTP/REST
                 │
┌────────────────▼────────────────────────┐
│       FastAPI Backend (NiceGUI)         │  ← app_advanced.py
│                                          │
│  • /api/dags         - List all         │
│  • /api/dags/{name}  - Get specific     │
│  • /api/dags/save    - Save DAG         │
│  • /api/dags/import  - Import           │
│  • /api/stats        - Statistics       │
└────────────────┬────────────────────────┘
                 │
            File I/O
                 │
┌────────────────▼────────────────────────┐
│      Filesystem Storage                 │
│      ./storage/*.json                   │
└─────────────────────────────────────────┘
```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review NiceGUI documentation: https://nicegui.io
3. FastAPI docs: https://fastapi.tiangolo.com

## License

MIT License - See LICENSE file for details

---

**Version**: 1.0.0  
**Last Updated**: 2026-02-26  
**Maintained**: Fully self-contained, zero external git dependencies

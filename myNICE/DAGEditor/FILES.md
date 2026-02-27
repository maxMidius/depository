# DAG Editor Pro - File Reference

## Directory Contents

```
DAGEditor/
├── □ APPLICATION FILES (Core)
│   ├── app_advanced.py          [18 KB] ⭐ MAIN APPLICATION - RECOMMENDED
│   ├── app.py                   [12 KB]   Basic version without advanced features
│   └── requirements.txt          [88 B]   Python dependencies
│
├── □ DOCUMENTATION FILES (Reference & Guides)
│   ├── README.md                [9.2 KB] Complete setup and usage guide
│   ├── API.md                   [9.2 KB] REST API documentation with examples
│   ├── QUICKREF.md              [5.4 KB] Quick reference for common commands
│   ├── GETTING_STARTED.md       [7.2 KB] Getting started guide (START HERE!)
│   ├── IMPLEMENTATION.md        [8.8 KB] Technical implementation details
│   └── FILES.md                 [This file] File reference and descriptions
│
├── □ LAUNCHER SCRIPTS (Automated Setup)
│   ├── start.sh                 [2.5 KB] Linux/macOS launcher (executable)
│   └── start.bat                [2.5 KB] Windows launcher
│
├── □ RUNTIME DIRECTORIES (Created on First Run)
│   ├── venv/                    Virtual Python environment
│   └── storage/                 DAG storage directory
│       ├── simple-pipeline.json Sample DAG
│       └── parallel-tasks.json  Sample DAG
│
└── □ THIS FILE
    └── FILES.md                 File listing and descriptions
```

## File Descriptions

### Application Files

#### `app_advanced.py` ⭐ **[RECOMMENDED]**
- **Size**: 18 KB
- **Purpose**: Main NiceGUI application with full features
- **Features**:
  - Web-based UI with dark theme
  - Complete REST API (8 endpoints)
  - File-based storage with JSON
  - Real-time statistics
  - CORS-enabled
  - Error handling and validation
  - Sample DAGs included
- **Start with**: `python app_advanced.py`

#### `app.py`
- **Size**: 12 KB
- **Purpose**: Basic NiceGUI version
- **Features**: Core functionality without advanced UI
- **Use when**: You want a simpler, lighter version

#### `requirements.txt`
- **Size**: 88 B
- **Contents**:
  ```
  nicegui>=1.4.0
  fastapi>=0.104.0
  uvicorn>=0.24.0
  python-multipart>=0.0.6
  pydantic>=2.0.0
  ```
- **Purpose**: List of Python dependencies
- **Install with**: `pip install -r requirements.txt`

### Documentation Files

#### `README.md` - **[COMPREHENSIVE GUIDE]**
- **Size**: 9.2 KB
- **Topics**:
  - Overview and features
  - Installation instructions
  - Usage examples
  - REST API endpoints
  - File structure
  - Backend setup (FastAPI/Flask)
  - Troubleshooting

#### `API.md` - **[API REFERENCE]**
- **Size**: 9.2 KB
- **Topics**:
  - Base URL and auth info
  - All endpoint descriptions
  - Request/response formats
  - Data models (Node, Edge, DAG)
  - Error handling
  - Code examples (curl, Python, JavaScript)
  - Complete workflow examples

#### `QUICKREF.md` - **[QUICK COMMANDS]**
- **Size**: 5.4 KB
- **Topics**:
  - Installation steps
  - Quick start commands
  - API curl commands
  - File locations
  - Troubleshooting tips
  - Feature summary

#### `GETTING_STARTED.md` - **[START HERE!]**
- **Size**: 7.2 KB
- **Topics**:
  - What was fixed
  - Quick start (30 seconds)
  - How to use
  - Features
  - Troubleshooting
  - Next steps
  - Architecture overview

#### `IMPLEMENTATION.md` - **[TECHNICAL DETAILS]**
- **Size**: 8.8 KB
- **Topics**:
  - What was delivered
  - Features implemented
  - REST API overview
  - Technical stack
  - Advantages over original
  - Future extensions
  - Verification checklist

#### `FILES.md` - **[THIS FILE]**
- **Size**: Variable
- **Topics**:
  - Complete file listing
  - File descriptions
  - How to use each file
  - Directory structure

### Launcher Scripts

#### `start.sh`
- **Platform**: Linux/macOS
- **Permissions**: Executable (755)
- **Functions**:
  1. Checks Python is installed
  2. Creates virtual environment
  3. Installs dependencies
  4. Starts application
- **Usage**: `./start.sh`
- **Auto-creates**: venv/ and storage/ directories

#### `start.bat`
- **Platform**: Windows
- **Functions**:
  1. Checks Python is installed
  2. Creates virtual environment
  3. Installs dependencies
  4. Starts application
- **Usage**: Double-click or `start.bat` in cmd
- **Auto-creates**: venv/ and storage/ directories

### Runtime Directories

#### `venv/` (Created on first run)
- **Purpose**: Python virtual environment
- **Contents**: Isolated Python packages
- **Auto-created by**: start.sh / start.bat
- **Size**: ~200-300 MB (after pip install)
- **Can delete**: Yes (will recreate on next run)

#### `storage/` (Created on first run)
- **Purpose**: DAG file storage
- **Format**: JSON files (*.json)
- **Includes**: 2 sample DAGs
  - `simple-pipeline.json` (ETL example)
  - `parallel-tasks.json` (Multi-task workflow)
- **User-created**: Add your DAGs here
- **Backup**: Copy this directory to backup all DAGs

## How to Use Each File

### To Run the Application
1. `./start.sh` (Linux/macOS)
2. Or `start.bat` (Windows)
3. Or manually: `python app_advanced.py`

### To Read Documentation
1. For quick start: Read `GETTING_STARTED.md` first
2. For detailed guide: Read `README.md`
3. For API usage: Read `API.md`
4. For quick reference: Read `QUICKREF.md`

### To Customize
- Edit `app_advanced.py` for application changes
- Modify `requirements.txt` to add/remove dependencies
- Update `start.sh` / `start.bat` for launch changes

### To Back Up
- Copy the entire `DAGEditor/` directory
- Or backup just `storage/` directory for DAGs only

## File Dependencies

```
Application Startup:
start.sh/start.bat
    ↓
app_advanced.py
    ↓
requirements.txt → pip install
    ↓
venv/ (created)
    ↓
storage/ (created)
```

## File Sizes Summary

| Category | File | Size |
|----------|------|------|
| **App** | app_advanced.py | 18 KB ⭐ |
| **App** | app.py | 12 KB |
| **Deps** | requirements.txt | 88 B |
| **Docs** | README.md | 9.2 KB |
| **Docs** | API.md | 9.2 KB |
| **Docs** | Getting Started | 7.2 KB |
| **Docs** | Implementation | 8.8 KB |
| **Docs** | Quick Ref | 5.4 KB |
| **Launch** | start.sh | 2.5 KB |
| **Launch** | start.bat | 2.5 KB |
| | | |
| **Total** | All Documentation | ~50 KB |
| **Runtime** | venv/ | ~300 MB |
| **Runtime** | storage/ | ~5 KB |

## File Modification Guide

### Safe to Modify
- ✅ `app_advanced.py` - Customize features
- ✅ `requirements.txt` - Add packages
- ✅ `storage/*.json` - DAG files (auto-created)
- ✅ Documentation files - Update guides

### Do Not Modify (Unless Advanced)
- ⚠️ `start.sh` / `start.bat` - Unless familiar with shell/batch
- ⚠️ `venv/` - Let Python manage this

### Should Not Delete (Without Backup)
- ⚠️ `storage/` - Contains saved DAGs
- ⚠️ `app_advanced.py` - The main application

## Documentation Quick Links

| Need | File | Section |
|------|------|---------|
| Get started quickly | GETTING_STARTED.md | Quick Start |
| Full setup guide | README.md | Installation |
| API documentation | API.md | Endpoints |
| Command examples | QUICKREF.md | API Quick Commands |
| Troubleshooting | README.md | Troubleshooting |
| Technical details | IMPLEMENTATION.md | What Was Delivered |
| All files explained | FILES.md | THIS FILE |

## Installation Steps Using Files

1. **Download/Clone**
   - Entire `DAGEditor/` directory already prepared

2. **Run Startup Script**
   - Linux/macOS: `./start.sh`
   - Windows: `start.bat`
   - Or manual: See README.md

3. **Read Documentation**
   - Start: `GETTING_STARTED.md`
   - Details: `README.md`
   - API: `API.md`

4. **Use Application**
   - Open: http://localhost:8000
   - Manage: Save/Load/Export/Import DAGs

## Storage File Format

All DAGs stored in `storage/` are JSON files:

```json
{
  "name": "workflow-name",
  "description": "Optional description",
  "data": {
    "nodes": [...],
    "edges": [...]
  },
  "created": "2026-02-26T10:00:00",
  "updated": "2026-02-26T10:00:00"
}
```

## Backup & Recovery

### Back Up DAGs
```bash
cp -r storage storage.backup
```

### Restore DAGs
```bash
rm -rf storage
cp -r storage.backup storage
```

### Export Single DAG
```bash
curl http://localhost:8000/api/dags/my-dag/export > my-dag.json
```

### Import Single DAG
```bash
curl -X POST http://localhost:8000/api/dags/import -F "file=@my-dag.json"
```

## File Encoding

All text files are UTF-8 encoded:
- Python files (.py): UTF-8
- Configuration (requirements.txt): UTF-8
- Markdown docs (.md): UTF-8
- JSON files (storage/): UTF-8

## Version Information

- **Created**: 2026-02-26
- **Application Version**: 1.0.0
- **Python**: 3.8+
- **Status**: Production Ready ✅

---

**Need help?** Check the appropriate documentation file:
- Quick start? → `GETTING_STARTED.md`
- How to use? → `README.md`
- API help? → `API.md`
- Commands? → `QUICKREF.md`

Last Updated: 2026-02-26

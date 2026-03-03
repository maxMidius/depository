# JIRA Scope - DAG Editor

A hierarchical DAG (Directed Acyclic Graph) editor for managing Capabilities, Deliverables, and Tasks in project planning.

## Features

### 🎯 Hierarchical Structure
- **Capabilities**: Top-level containers (resizable boxes)
- **Deliverables**: Mid-level containers inside Capabilities (resizable boxes)
- **Tasks**: Individual work items inside Deliverables (draggable nodes)
- **Connections**: Directional arrows between Tasks

### ✨ Interactions

#### Capabilities
- **Add**: Click "+ Capability" button or select a capability and use context menu
- **Resize**: Drag any of the 8 resize handles (corners and edges)
- **Move**: Click and drag the title bar
- **Rename**: Double-click the title bar
- **Delete**: Right-click → Delete (or select and click "Delete Selected")
- **Context Menu**: Right-click for options

#### Deliverables
- **Add**: Select a Capability first, then click "+ Deliverable"
- **Resize**: Drag any of the 8 resize handles
- **Move**: Click and drag the title bar
- **Rename**: Double-click the title bar
- **Delete**: Right-click → Delete
- **Context Menu**: Right-click for options

#### Tasks
- **Add**: Select a Deliverable first, then click "+ Task"
- **Move**: Click and drag the task box
- **Rename**: Double-click the task box
- **Delete**: Right-click → Delete
- **Connect**: Enable "Connect Tasks" mode, then click source task, then target task
- **Context Menu**: Right-click for options

#### Connections
- **Add**: Click "🔗 Connect Tasks" button to enter connection mode
  - Click on a source task
  - Click on a target task
  - Connection mode stays active for multiple connections
  - Click "🔗 Connect Tasks" again to exit
- **Delete**: Right-click on a connection → Delete

### 💾 Project Management
- **Save**: Enter project name and description, click "💾 Save"
- **Load**: Click "📂 Load" to see list of saved projects
- **Auto-save**: Projects are automatically saved to `storage/` directory
- **Sample Project**: A sample project is loaded on startup

### ⌨️ Actions
- **Undo**: Click "↩️ Undo" or use Ctrl+Z (up to 50 steps)
- **Redo**: Click "↪️ Redo" or use Ctrl+Y
- **Delete Selected**: Select an element and click "🗑️ Delete Selected"

### 📊 Statistics
Real-time statistics showing:
- Number of Capabilities
- Number of Deliverables
- Number of Tasks
- Number of Connections

## Installation

1. Ensure you have Python 3.8+ installed
2. Install nicegui:
   ```bash
   pip install nicegui
   ```

## Running the Application

```bash
cd /home/dasur/GIT/depository/myNICE/jiraScope
python app.py
```

The application will start on `http://localhost:8080`

## File Structure

```
jiraScope/
├── app.py                 # Main NiceGUI application
├── static/
│   └── dag_editor.js     # JavaScript DAG editor logic
├── storage/               # Saved projects (JSON files)
│   └── sample_project.json
└── README.md             # This file
```

## Architecture

### Backend (Python/NiceGUI)
- FastAPI server with NiceGUI UI
- REST API endpoints for project management
- Static file serving for JavaScript

### Frontend (JavaScript)
- SVG-based rendering for smooth graphics
- Event-driven architecture
- State management with undo/redo
- Drag and drop interactions
- Resize handles for containers
- Context menus for quick actions

## API Endpoints

- `POST /api/project/save` - Save a project
- `GET /api/projects` - List all projects
- `GET /api/project/{name}` - Load a specific project

## Color Scheme

- **Capabilities**: Blue (#1976d2) - Large containers
- **Deliverables**: Orange (#f57c00) - Medium containers with dashed borders
- **Tasks**: Green (#4caf50) - Small draggable nodes
- **Connections**: Gray (#666) - Directional arrows
- **Selection**: Orange (#ff9800) - Highlighted elements

## Tips

1. **Organize visually**: Resize and position elements to create a clear hierarchy
2. **Use context menus**: Right-click on any element for quick actions
3. **Double-click to rename**: Fastest way to change names
4. **Connect mode**: Enable once, make multiple connections, disable when done
5. **Save often**: Use the Save button to preserve your work
6. **Undo/Redo**: Don't worry about mistakes - history is tracked

## Future Enhancements

- [ ] Export to PNG/SVG
- [ ] Import from JSON
- [ ] Zoom and pan controls
- [ ] Task dependencies validation
- [ ] Color customization
- [ ] Search and filter
- [ ] Collaborative editing
- [ ] Integration with JIRA API

## License

MIT License

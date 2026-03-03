/**
 * JIRA Scope DAG Editor
 * Hierarchical editor for Capabilities, Deliverables, and Tasks
 */

// ========== STATE MANAGEMENT ==========
const state = {
    capabilities: [],
    connections: [],
    selectedElement: null,
    selectedType: null, // 'capability', 'deliverable', 'task', 'connection'
    dragElement: null,
    dragType: null,
    dragOffset: { x: 0, y: 0 },
    resizeElement: null,
    resizeType: null,
    resizeHandle: null, // 'se', 'sw', 'ne', 'nw', 'e', 'w', 'n', 's'
    resizeStart: { x: 0, y: 0, width: 0, height: 0 },
    connectionMode: false,
    connectionSource: null,
    panOffset: { x: 0, y: 0 },
    zoom: 1,
    history: [],
    historyIndex: -1,
    nextCapId: 1,
    nextDelId: 1,
    nextTaskId: 1,
};

// ========== DOM ELEMENTS ==========
let canvas = null;
let capabilitiesLayer = null;
let deliverablesLayer = null;
let tasksLayer = null;
let connectionsLayer = null;
let connectModeIndicator = null;

// Context menu
let contextMenu = null;

// ========== UTILITY FUNCTIONS ==========

function generateId(type) {
    let candidateId = '';

    do {
        if (type === 'capability') candidateId = `cap${state.nextCapId++}`;
        if (type === 'deliverable') candidateId = `del${state.nextDelId++}`;
        if (type === 'task') candidateId = `task${state.nextTaskId++}`;
    } while (idExists(candidateId));

    return candidateId;
}

function idExists(id) {
    for (const cap of state.capabilities) {
        if (cap.id === id) return true;

        for (const del of (cap.deliverables || [])) {
            if (del.id === id) return true;

            for (const task of (del.tasks || [])) {
                if (task.id === id) return true;
            }
        }
    }

    return false;
}

function saveState() {
    const snapshot = JSON.stringify({
        capabilities: state.capabilities,
        connections: state.connections,
    });
    
    // Remove any states after current index (when branching from undo)
    state.history = state.history.slice(0, state.historyIndex + 1);
    state.history.push(snapshot);
    state.historyIndex++;
    
    // Limit history to 50 states
    if (state.history.length > 50) {
        state.history.shift();
        state.historyIndex--;
    }
    
    // Also save current state to localStorage to prevent data loss on page reload
    try {
        localStorage.setItem('dagEditorState', snapshot);
    } catch (e) {
        console.warn('Could not save to localStorage:', e);
    }
}

function undo() {
    if (state.historyIndex > 0) {
        state.historyIndex--;
        const snapshot = JSON.parse(state.history[state.historyIndex]);
        state.capabilities = snapshot.capabilities;
        state.connections = snapshot.connections;
        updateIDCounters();
        render();
        updateStats();
    }
}

function redo() {
    if (state.historyIndex < state.history.length - 1) {
        state.historyIndex++;
        const snapshot = JSON.parse(state.history[state.historyIndex]);
        state.capabilities = snapshot.capabilities;
        state.connections = snapshot.connections;
        updateIDCounters();
        render();
        updateStats();
    }
}

function updateStats() {
    const capCount = state.capabilities.length;
    let delCount = 0;
    let taskCount = 0;
    
    state.capabilities.forEach(cap => {
        delCount += cap.deliverables.length;
        cap.deliverables.forEach(del => {
            taskCount += del.tasks.length;
        });
    });
    
    const capCountEl = document.getElementById('cap-count');
    const delCountEl = document.getElementById('del-count');
    const taskCountEl = document.getElementById('task-count');
    const connCountEl = document.getElementById('conn-count');
    
    if (capCountEl) capCountEl.textContent = capCount;
    if (delCountEl) delCountEl.textContent = delCount;
    if (taskCountEl) taskCountEl.textContent = taskCount;
    if (connCountEl) connCountEl.textContent = state.connections.length;
}

function ensureConnectModeIndicator() {
    if (connectModeIndicator || !document.body) return;

    connectModeIndicator = document.createElement('div');
    connectModeIndicator.id = 'connect-mode-indicator';
    connectModeIndicator.textContent = '🔗 CONNECT MODE ON (click Connect Tasks to exit)';
    connectModeIndicator.style.position = 'fixed';
    connectModeIndicator.style.top = '14px';
    connectModeIndicator.style.right = '14px';
    connectModeIndicator.style.padding = '8px 12px';
    connectModeIndicator.style.background = '#d32f2f';
    connectModeIndicator.style.color = '#fff';
    connectModeIndicator.style.borderRadius = '6px';
    connectModeIndicator.style.fontWeight = '700';
    connectModeIndicator.style.fontSize = '12px';
    connectModeIndicator.style.letterSpacing = '0.3px';
    connectModeIndicator.style.zIndex = '10001';
    connectModeIndicator.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.25)';
    connectModeIndicator.style.display = 'none';

    document.body.appendChild(connectModeIndicator);
}

function updateConnectModeUI() {
    ensureConnectModeIndicator();

    if (state.connectionMode) {
        if (connectModeIndicator) connectModeIndicator.style.display = 'block';
        if (canvas) {
            canvas.style.cursor = 'crosshair';
            canvas.style.outline = '3px solid #ff9800';
            canvas.style.outlineOffset = '-3px';
        }
        return;
    }

    if (connectModeIndicator) connectModeIndicator.style.display = 'none';
    if (canvas) {
        canvas.style.cursor = 'default';
        canvas.style.outline = 'none';
        canvas.style.outlineOffset = '0';
    }
}

// ========== RENDERING FUNCTIONS ==========

function render() {
    // Safety check - make sure DOM elements exist
    if (!capabilitiesLayer || !deliverablesLayer || !tasksLayer || !connectionsLayer) {
        console.warn('Cannot render: DOM elements not ready');
        return;
    }
    
    // Clear all layers
    capabilitiesLayer.innerHTML = '';
    deliverablesLayer.innerHTML = '';
    tasksLayer.innerHTML = '';
    connectionsLayer.innerHTML = '';
    
    // Render capabilities and their children
    state.capabilities.forEach(capability => {
        renderCapability(capability);
        
        capability.deliverables.forEach(deliverable => {
            renderDeliverable(deliverable);
            
            deliverable.tasks.forEach(task => {
                renderTask(task);
            });
        });
    });
    
    // Render connections
    state.connections.forEach((conn, index) => {
        renderConnection(conn, index);
    });
}

function renderCapability(cap) {
    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.setAttribute('class', 'capability');
    g.setAttribute('data-id', cap.id);
    
    // Main box
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', cap.x);
    rect.setAttribute('y', cap.y);
    rect.setAttribute('width', cap.width);
    rect.setAttribute('height', cap.height);
    rect.setAttribute('fill', '#e3f2fd');
    rect.setAttribute('stroke', '#1976d2');
    rect.setAttribute('stroke-width', '2');
    rect.setAttribute('rx', '8');
    
    if (state.selectedElement?.id === cap.id && state.selectedType === 'capability') {
        rect.setAttribute('stroke', '#ff9800');
        rect.setAttribute('stroke-width', '3');
    }
    
    // Title bar
    const titleBar = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    titleBar.setAttribute('x', cap.x);
    titleBar.setAttribute('y', cap.y);
    titleBar.setAttribute('width', cap.width);
    titleBar.setAttribute('height', '30');
    titleBar.setAttribute('fill', '#1976d2');
    titleBar.setAttribute('rx', '8');
    
    // Title text
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', cap.x + 10);
    text.setAttribute('y', cap.y + 20);
    text.setAttribute('fill', 'white');
    text.setAttribute('font-size', '14');
    text.setAttribute('font-weight', 'bold');
    text.textContent = cap.name;
    
    // Resize handles
    const handles = createResizeHandles(cap.x, cap.y, cap.width, cap.height);
    
    g.appendChild(rect);
    g.appendChild(titleBar);
    g.appendChild(text);
    handles.forEach(h => g.appendChild(h));
    
    // Event listeners
    titleBar.addEventListener('mousedown', (e) => startDrag(e, cap, 'capability'));
    titleBar.addEventListener('dblclick', (e) => editName(cap, 'capability'));
    titleBar.addEventListener('contextmenu', (e) => showContextMenu(e, cap, 'capability'));
    
    handles.forEach((handle, index) => {
        const handleType = ['se', 'sw', 'ne', 'nw', 'e', 'w', 'n', 's'][index];
        handle.addEventListener('mousedown', (e) => startResize(e, cap, 'capability', handleType));
    });
    
    capabilitiesLayer.appendChild(g);
}

function renderDeliverable(del) {
    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.setAttribute('class', 'deliverable');
    g.setAttribute('data-id', del.id);
    
    // Main box
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', del.x);
    rect.setAttribute('y', del.y);
    rect.setAttribute('width', del.width);
    rect.setAttribute('height', del.height);
    rect.setAttribute('fill', '#fff3e0');
    rect.setAttribute('stroke', '#f57c00');
    rect.setAttribute('stroke-width', '2');
    rect.setAttribute('rx', '6');
    rect.setAttribute('stroke-dasharray', '5,3');
    
    if (state.selectedElement?.id === del.id && state.selectedType === 'deliverable') {
        rect.setAttribute('stroke', '#ff9800');
        rect.setAttribute('stroke-width', '3');
    }
    
    // Title bar
    const titleBar = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    titleBar.setAttribute('x', del.x);
    titleBar.setAttribute('y', del.y);
    titleBar.setAttribute('width', del.width);
    titleBar.setAttribute('height', '25');
    titleBar.setAttribute('fill', '#f57c00');
    titleBar.setAttribute('rx', '6');
    
    // Title text
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', del.x + 8);
    text.setAttribute('y', del.y + 17);
    text.setAttribute('fill', 'white');
    text.setAttribute('font-size', '12');
    text.setAttribute('font-weight', 'bold');
    text.textContent = del.name;
    
    // Resize handles
    const handles = createResizeHandles(del.x, del.y, del.width, del.height, 5);
    
    g.appendChild(rect);
    g.appendChild(titleBar);
    g.appendChild(text);
    handles.forEach(h => g.appendChild(h));
    
    // Event listeners
    titleBar.addEventListener('mousedown', (e) => startDrag(e, del, 'deliverable'));
    titleBar.addEventListener('dblclick', (e) => editName(del, 'deliverable'));
    titleBar.addEventListener('contextmenu', (e) => showContextMenu(e, del, 'deliverable'));
    
    handles.forEach((handle, index) => {
        const handleType = ['se', 'sw', 'ne', 'nw', 'e', 'w', 'n', 's'][index];
        handle.addEventListener('mousedown', (e) => startResize(e, del, 'deliverable', handleType));
    });
    
    deliverablesLayer.appendChild(g);
}

function renderTask(task) {
    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.setAttribute('class', 'task');
    g.setAttribute('data-id', task.id);
    
    const width = 120;
    const height = 40;
    
    // Task box
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', task.x);
    rect.setAttribute('y', task.y);
    rect.setAttribute('width', width);
    rect.setAttribute('height', height);
    rect.setAttribute('fill', '#4caf50');
    rect.setAttribute('stroke', '#2e7d32');
    rect.setAttribute('stroke-width', '2');
    rect.setAttribute('rx', '4');
    rect.style.cursor = state.connectionMode ? 'crosshair' : 'move';
    
    if (state.connectionSource?.id === task.id) {
        // Connection source gets red highlight
        rect.setAttribute('fill', '#ff5252');
        rect.setAttribute('stroke', '#d32f2f');
        rect.setAttribute('stroke-width', '3');
    } else if (state.selectedElement?.id === task.id && state.selectedType === 'task') {
        rect.setAttribute('stroke', '#ff9800');
        rect.setAttribute('stroke-width', '3');
    }
    
    // Task text
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', task.x + width / 2);
    text.setAttribute('y', task.y + height / 2 + 5);
    text.setAttribute('fill', 'white');
    text.setAttribute('font-size', '11');
    text.setAttribute('font-weight', 'bold');
    text.setAttribute('text-anchor', 'middle');
    text.textContent = task.name;
    
    // Connection ports (L, R, T, B)
    const portRadius = 4;
    const portColor = '#2e7d32';
    
    // Top port
    const topPort = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    topPort.setAttribute('cx', task.x + width / 2);
    topPort.setAttribute('cy', task.y);
    topPort.setAttribute('r', portRadius);
    topPort.setAttribute('fill', '#fff');
    topPort.setAttribute('stroke', portColor);
    topPort.setAttribute('stroke-width', '2');
    topPort.setAttribute('class', 'port');
    
    // Bottom port
    const bottomPort = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    bottomPort.setAttribute('cx', task.x + width / 2);
    bottomPort.setAttribute('cy', task.y + height);
    bottomPort.setAttribute('r', portRadius);
    bottomPort.setAttribute('fill', '#fff');
    bottomPort.setAttribute('stroke', portColor);
    bottomPort.setAttribute('stroke-width', '2');
    bottomPort.setAttribute('class', 'port');
    
    // Left port
    const leftPort = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    leftPort.setAttribute('cx', task.x);
    leftPort.setAttribute('cy', task.y + height / 2);
    leftPort.setAttribute('r', portRadius);
    leftPort.setAttribute('fill', '#fff');
    leftPort.setAttribute('stroke', portColor);
    leftPort.setAttribute('stroke-width', '2');
    leftPort.setAttribute('class', 'port');
    
    // Right port
    const rightPort = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    rightPort.setAttribute('cx', task.x + width);
    rightPort.setAttribute('cy', task.y + height / 2);
    rightPort.setAttribute('r', portRadius);
    rightPort.setAttribute('fill', '#fff');
    rightPort.setAttribute('stroke', portColor);
    rightPort.setAttribute('stroke-width', '2');
    rightPort.setAttribute('class', 'port');
    
    g.appendChild(rect);
    g.appendChild(text);
    g.appendChild(topPort);
    g.appendChild(bottomPort);
    g.appendChild(leftPort);
    g.appendChild(rightPort);
    
    // Event listeners - Make both rect AND g clickable for reliability
    const clickHandler = (e) => {
        if (state.connectionMode) {
            e.preventDefault();
            e.stopPropagation();
            handleConnectionClick(task);
        } else {
            startDrag(e, task, 'task');
        }
    };
    
    rect.addEventListener('mousedown', clickHandler);
    rect.addEventListener('click', clickHandler); // Add click as backup
    g.addEventListener('mousedown', clickHandler); // Also on group
    g.addEventListener('click', clickHandler); // Also on group
    
    rect.addEventListener('dblclick', (e) => {
        if (!state.connectionMode) {
            editName(task, 'task');
        }
    });
    rect.addEventListener('contextmenu', (e) => {
        if (!state.connectionMode) {
            showContextMenu(e, task, 'task');
        }
    });
    
    tasksLayer.appendChild(g);
}

function renderConnection(conn, index) {
    const fromTask = findTask(conn.from);
    const toTask = findTask(conn.to);
    
    if (!fromTask || !toTask) {
        console.warn('Cannot render connection - task not found:', conn);
        return;
    }
    
    // Task dimensions
    const taskWidth = 120;
    const taskHeight = 40;
    
    // Get center points of tasks
    const fromCenterX = fromTask.x + taskWidth / 2;
    const fromCenterY = fromTask.y + taskHeight / 2;
    const toCenterX = toTask.x + taskWidth / 2;
    const toCenterY = toTask.y + taskHeight / 2;
    
    // Calculate relative position to determine best ports
    const dx = toCenterX - fromCenterX;
    const dy = toCenterY - fromCenterY;
    const absDx = Math.abs(dx);
    const absDy = Math.abs(dy);
    
    // Select source port based on target position
    let fromX, fromY;
    if (absDx > absDy) {
        // Target is more to the left or right
        if (dx > 0) {
            // Target to the right - use right port
            fromX = fromTask.x + taskWidth;
            fromY = fromTask.y + taskHeight / 2;
        } else {
            // Target to the left - use left port
            fromX = fromTask.x;
            fromY = fromTask.y + taskHeight / 2;
        }
    } else {
        // Target is more up or down
        if (dy > 0) {
            // Target below - use bottom port
            fromX = fromTask.x + taskWidth / 2;
            fromY = fromTask.y + taskHeight;
        } else {
            // Target above - use top port
            fromX = fromTask.x + taskWidth / 2;
            fromY = fromTask.y;
        }
    }
    
    // Select target port (opposite of source)
    let toX, toY;
    if (absDx > absDy) {
        // Source using left/right port - target uses opposite
        if (dx > 0) {
            // Target to the right, source used right - target uses left
            toX = toTask.x;
            toY = toTask.y + taskHeight / 2;
        } else {
            // Target to the left, source used left - target uses right
            toX = toTask.x + taskWidth;
            toY = toTask.y + taskHeight / 2;
        }
    } else {
        // Source using top/bottom port - target uses opposite
        if (dy > 0) {
            // Target below, source used bottom - target uses top
            toX = toTask.x + taskWidth / 2;
            toY = toTask.y;
        } else {
            // Target above, source used top - target uses bottom
            toX = toTask.x + taskWidth / 2;
            toY = toTask.y + taskHeight;
        }
    }
    
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', fromX);
    line.setAttribute('y1', fromY);
    line.setAttribute('x2', toX);
    line.setAttribute('y2', toY);
    line.setAttribute('stroke', '#1976d2');
    line.setAttribute('stroke-width', '3');
    line.setAttribute('marker-end', 'url(#arrowhead)');
    line.setAttribute('class', 'connection');
    line.setAttribute('data-index', index);
    line.style.pointerEvents = 'stroke'; // Make only the stroke clickable
    
    if (state.selectedElement === conn && state.selectedType === 'connection') {
        line.setAttribute('stroke', '#ff9800');
        line.setAttribute('stroke-width', '4');
    }
    
    line.addEventListener('click', (e) => {
        e.stopPropagation();
        state.selectedElement = conn;
        state.selectedType = 'connection';
        render();
    });
    
    line.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        e.stopPropagation();
        showContextMenu(e, conn, 'connection');
    });
    
    connectionsLayer.appendChild(line);
}

function createResizeHandles(x, y, width, height, size = 6) {
    const handles = [];
    const positions = [
        { x: x + width, y: y + height, cursor: 'se-resize' }, // SE
        { x: x, y: y + height, cursor: 'sw-resize' }, // SW
        { x: x + width, y: y, cursor: 'ne-resize' }, // NE
        { x: x, y: y, cursor: 'nw-resize' }, // NW
        { x: x + width, y: y + height / 2, cursor: 'e-resize' }, // E
        { x: x, y: y + height / 2, cursor: 'w-resize' }, // W
        { x: x + width / 2, y: y, cursor: 'n-resize' }, // N
        { x: x + width / 2, y: y + height, cursor: 's-resize' }, // S
    ];
    
    positions.forEach(pos => {
        const handle = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        handle.setAttribute('x', pos.x - size / 2);
        handle.setAttribute('y', pos.y - size / 2);
        handle.setAttribute('width', size);
        handle.setAttribute('height', size);
        handle.setAttribute('fill', 'white');
        handle.setAttribute('stroke', '#666');
        handle.setAttribute('stroke-width', '1');
        handle.setAttribute('class', 'resize-handle');
        handle.style.cursor = pos.cursor;
        handles.push(handle);
    });
    
    return handles;
}

// ========== INTERACTION HANDLERS ==========

function moveCapabilityChildren(capability, dx, dy) {
    capability.deliverables.forEach(deliverable => {
        deliverable.x += dx;
        deliverable.y += dy;
        deliverable.tasks.forEach(task => {
            task.x += dx;
            task.y += dy;
        });
    });
}

function moveDeliverableChildren(deliverable, dx, dy) {
    deliverable.tasks.forEach(task => {
        task.x += dx;
        task.y += dy;
    });
}

function collectResizeSnapshot(element, type) {
    const snapshot = {
        element: {
            x: element.x,
            y: element.y,
            width: element.width,
            height: element.height,
        },
        deliverables: [],
        tasks: [],
    };

    if (type === 'capability') {
        element.deliverables.forEach(deliverable => {
            snapshot.deliverables.push({
                ref: deliverable,
                x: deliverable.x,
                y: deliverable.y,
                width: deliverable.width,
                height: deliverable.height,
            });
            deliverable.tasks.forEach(task => {
                snapshot.tasks.push({
                    ref: task,
                    x: task.x,
                    y: task.y,
                });
            });
        });
    } else if (type === 'deliverable') {
        element.tasks.forEach(task => {
            snapshot.tasks.push({
                ref: task,
                x: task.x,
                y: task.y,
            });
        });
    }

    return snapshot;
}

function applyGroupResize(element, type, snapshot) {
    if (!snapshot) return;

    const oldX = snapshot.element.x;
    const oldY = snapshot.element.y;
    const oldW = snapshot.element.width;
    const oldH = snapshot.element.height;
    const newX = element.x;
    const newY = element.y;
    const newW = element.width;
    const newH = element.height;

    const dx = newX - oldX;
    const dy = newY - oldY;

    if (type === 'capability') {
        snapshot.deliverables.forEach(item => {
            // Just translate by the same amount the parent moved
            item.ref.x = item.x + dx;
            item.ref.y = item.y + dy;
            // Keep original width/height - no scaling
        });
    }

    snapshot.tasks.forEach(item => {
        // Just translate by the same amount the parent moved
        item.ref.x = item.x + dx;
        item.ref.y = item.y + dy;
    });
}

function startDrag(e, element, type) {
    e.preventDefault();
    e.stopPropagation();
    
    state.dragElement = element;
    state.dragType = type;
    state.dragOffset = {
        x: e.clientX - element.x,
        y: e.clientY - element.y
    };
    
    state.selectedElement = element;
    state.selectedType = type;
    render();
}

function startResize(e, element, type, handle) {
    e.preventDefault();
    e.stopPropagation();
    
    state.resizeElement = element;
    state.resizeType = type;
    state.resizeHandle = handle;
    state.resizeStart = {
        x: e.clientX,
        y: e.clientY,
        width: element.width,
        height: element.height,
        elemX: element.x,
        elemY: element.y,
        snapshot: collectResizeSnapshot(element, type)
    };
}

function handleMouseMove(e) {
    if (state.dragElement) {
        const oldX = state.dragElement.x;
        const oldY = state.dragElement.y;
        const newX = e.clientX - state.dragOffset.x;
        const newY = e.clientY - state.dragOffset.y;
        const dx = newX - oldX;
        const dy = newY - oldY;

        state.dragElement.x = newX;
        state.dragElement.y = newY;

        if (state.dragType === 'capability') {
            moveCapabilityChildren(state.dragElement, dx, dy);
        } else if (state.dragType === 'deliverable') {
            moveDeliverableChildren(state.dragElement, dx, dy);
        }

        render();
    } else if (state.resizeElement) {
        const dx = e.clientX - state.resizeStart.x;
        const dy = e.clientY - state.resizeStart.y;
        
        const handle = state.resizeHandle;
        const elem = state.resizeElement;
        
        if (handle.includes('e')) {
            elem.width = Math.max(100, state.resizeStart.width + dx);
        }
        if (handle.includes('w')) {
            const newWidth = Math.max(100, state.resizeStart.width - dx);
            if (newWidth > 100) {
                elem.x = state.resizeStart.elemX + dx;
                elem.width = newWidth;
            }
        }
        if (handle.includes('s')) {
            elem.height = Math.max(80, state.resizeStart.height + dy);
        }
        if (handle.includes('n')) {
            const newHeight = Math.max(80, state.resizeStart.height - dy);
            if (newHeight > 80) {
                elem.y = state.resizeStart.elemY + dy;
                elem.height = newHeight;
            }
        }

        if (state.resizeType === 'capability' || state.resizeType === 'deliverable') {
            applyGroupResize(elem, state.resizeType, state.resizeStart.snapshot);
        }
        
        render();
    }
}

function handleMouseUp(e) {
    if (state.dragElement || state.resizeElement) {
        saveState();
    }
    
    state.dragElement = null;
    state.dragType = null;
    state.resizeElement = null;
    state.resizeType = null;
    state.resizeHandle = null;
}

function handleConnectionClick(task) {
    try {
        if (!state.connectionSource) {
            // Start connection
            state.connectionSource = task;
            console.log('✓ Connection source:', task.name);
            render(); // Force re-render to show highlight
            return;
        }
        
        // Compare IDs strictly
        const isSameTask = String(state.connectionSource.id) === String(task.id);
        
        if (isSameTask) {
            // Clicking same task again - deselect
            state.connectionSource = null;
            console.log('✗ Connection cancelled');
            render();
            return;
        }
        
        // Complete connection
        const newConnection = {
            from: state.connectionSource.id,
            to: task.id
        };
        
        // Check if connection already exists
        const exists = state.connections.some(c => 
            c.from === newConnection.from && c.to === newConnection.to
        );
        
        if (!exists) {
            state.connections.push(newConnection);
            console.log('✓ Connected:', state.connectionSource.name, '→', task.name);
            saveState();
            render();
            updateStats();
        } else {
            console.log('✗ Connection already exists');
            render();
        }
        
        state.connectionSource = null;
    } catch (error) {
        console.error('ERROR in handleConnectionClick:', error);
    }
}

function toggleConnectionMode() {
    state.connectionMode = !state.connectionMode;
    state.connectionSource = null;

    updateConnectModeUI();
    render();

    if (state.connectionMode) {
        console.log('Connection mode: ON');
    } else {
        console.log('Connection mode: OFF');
    }
}

// ========== CRUD OPERATIONS ==========

function addCapability() {
    const newCap = {
        id: generateId('capability'),
        name: 'New Capability',
        x: 100 + state.capabilities.length * 30,
        y: 100 + state.capabilities.length * 30,
        width: 400,
        height: 300,
        deliverables: []
    };
    
    state.capabilities.push(newCap);
    saveState();
    render();
    updateStats();
}

function addDeliverable() {
    if (!state.selectedElement || state.selectedType !== 'capability') {
        alert('Please select a Capability first');
        return;
    }
    
    const cap = state.selectedElement;
    const newDel = {
        id: generateId('deliverable'),
        name: 'New Deliverable',
        x: cap.x + 20,
        y: cap.y + 40 + cap.deliverables.length * 20,
        width: 200,
        height: 150,
        tasks: []
    };
    
    cap.deliverables.push(newDel);
    saveState();
    render();
    updateStats();
}

function addTask() {
    if (!state.selectedElement || state.selectedType !== 'deliverable') {
        alert('Please select a Deliverable first');
        return;
    }
    
    const del = state.selectedElement;
    const newTask = {
        id: generateId('task'),
        name: 'New Task',
        x: del.x + 20,
        y: del.y + 40 + del.tasks.length * 50
    };
    
    del.tasks.push(newTask);
    saveState();
    render();
    updateStats();
}

function deleteSelected() {
    if (!state.selectedElement) {
        alert('No element selected');
        return;
    }
    
    if (state.selectedType === 'capability') {
        const index = state.capabilities.findIndex(c => c.id === state.selectedElement.id);
        if (index !== -1) {
            if (confirm(`Delete capability "${state.selectedElement.name}" and all its contents?`)) {
                state.capabilities.splice(index, 1);
            }
        }
    } else if (state.selectedType === 'deliverable') {
        state.capabilities.forEach(cap => {
            const index = cap.deliverables.findIndex(d => d.id === state.selectedElement.id);
            if (index !== -1) {
                if (confirm(`Delete deliverable "${state.selectedElement.name}" and all its tasks?`)) {
                    cap.deliverables.splice(index, 1);
                }
            }
        });
    } else if (state.selectedType === 'task') {
        state.capabilities.forEach(cap => {
            cap.deliverables.forEach(del => {
                const index = del.tasks.findIndex(t => t.id === state.selectedElement.id);
                if (index !== -1) {
                    if (confirm(`Delete task "${state.selectedElement.name}"?`)) {
                        del.tasks.splice(index, 1);
                        // Remove connections involving this task
                        state.connections = state.connections.filter(
                            c => c.from !== state.selectedElement.id && c.to !== state.selectedElement.id
                        );
                    }
                }
            });
        });
    } else if (state.selectedType === 'connection') {
        const index = state.connections.indexOf(state.selectedElement);
        if (index !== -1 && confirm('Delete this connection?')) {
            state.connections.splice(index, 1);
        }
    }
    
    state.selectedElement = null;
    state.selectedType = null;
    saveState();
    render();
    updateStats();
}

function editName(element, type) {
    const newName = prompt(`Enter new name for ${type}:`, element.name);
    if (newName && newName.trim()) {
        element.name = newName.trim();
        saveState();
        render();
    }
}

// ========== CONTEXT MENU ==========

function showContextMenu(e, element, type) {
    e.preventDefault();
    e.stopPropagation();
    
    // Remove existing context menu
    if (contextMenu) {
        contextMenu.remove();
    }
    
    // Create context menu
    contextMenu = document.createElement('div');
    contextMenu.style.position = 'fixed';
    contextMenu.style.left = e.clientX + 'px';
    contextMenu.style.top = e.clientY + 'px';
    contextMenu.style.background = 'white';
    contextMenu.style.border = '1px solid #ccc';
    contextMenu.style.borderRadius = '4px';
    contextMenu.style.boxShadow = '0 2px 10px rgba(0,0,0,0.2)';
    contextMenu.style.zIndex = '10000';
    contextMenu.style.padding = '4px 0';
    contextMenu.style.minWidth = '150px';
    
    const menuItems = [];
    
    if (type === 'capability') {
        menuItems.push(
            { label: '✏️ Rename', action: () => editName(element, type) },
            { label: '➕ Add Deliverable', action: () => {
                state.selectedElement = element;
                state.selectedType = type;
                addDeliverable();
            }},
            { label: '🗑️ Delete', action: () => {
                state.selectedElement = element;
                state.selectedType = type;
                deleteSelected();
            }}
        );
    } else if (type === 'deliverable') {
        menuItems.push(
            { label: '✏️ Rename', action: () => editName(element, type) },
            { label: '➕ Add Task', action: () => {
                state.selectedElement = element;
                state.selectedType = type;
                addTask();
            }},
            { label: '🗑️ Delete', action: () => {
                state.selectedElement = element;
                state.selectedType = type;
                deleteSelected();
            }}
        );
    } else if (type === 'task') {
        menuItems.push(
            { label: '✏️ Rename', action: () => editName(element, type) },
            { label: '🗑️ Delete', action: () => {
                state.selectedElement = element;
                state.selectedType = type;
                deleteSelected();
            }}
        );
    } else if (type === 'connection') {
        menuItems.push(
            { label: '🗑️ Delete Connection', action: () => {
                state.selectedElement = element;
                state.selectedType = type;
                deleteSelected();
            }}
        );
    }
    
    menuItems.forEach(item => {
        const menuItem = document.createElement('div');
        menuItem.textContent = item.label;
        menuItem.style.padding = '8px 16px';
        menuItem.style.cursor = 'pointer';
        menuItem.style.fontSize = '14px';
        
        menuItem.addEventListener('mouseover', () => {
            menuItem.style.background = '#f0f0f0';
        });
        
        menuItem.addEventListener('mouseout', () => {
            menuItem.style.background = 'white';
        });
        
        menuItem.addEventListener('click', () => {
            item.action();
            contextMenu.remove();
            contextMenu = null;
        });
        
        contextMenu.appendChild(menuItem);
    });
    
    document.body.appendChild(contextMenu);
    
    // Close menu on outside click
    setTimeout(() => {
        document.addEventListener('click', function closeMenu() {
            if (contextMenu) {
                contextMenu.remove();
                contextMenu = null;
            }
            document.removeEventListener('click', closeMenu);
        });
    }, 100);
}

// ========== HELPER FUNCTIONS ==========

function findTask(taskId) {
    for (const cap of state.capabilities) {
        for (const del of cap.deliverables) {
            const task = del.tasks.find(t => t.id === taskId);
            if (task) return task;
        }
    }
    return null;
}

// ========== PROJECT MANAGEMENT ==========

async function saveProject() {
    const projectNameEl = document.querySelector('input[placeholder="My Project"]');
    const descriptionEl = document.querySelector('textarea[placeholder="Project description"]');
    
    const projectName = projectNameEl ? projectNameEl.value : 'My Project';
    const description = descriptionEl ? descriptionEl.value : '';
    
    const project = {
        name: projectName || 'My Project',
        description: description || '',
        capabilities: state.capabilities,
        connections: state.connections
    };
    
    try {
        const response = await fetch('/api/project/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(project)
        });
        
        const result = await response.json();
        if (result.success) {
            alert(`Project saved as: ${result.name}`);
        } else {
            alert(`Error saving project: ${result.error}`);
        }
    } catch (error) {
        alert(`Error saving project: ${error.message}`);
    }
}

// Removed showLoadDialog - now using NiceGUI dropdown for project selection

async function loadProject(name) {
    try {
        const response = await fetch(`/api/project/${name}`);
        const result = await response.json();
        
        if (result.success) {
            const project = result.project;
            state.capabilities = project.capabilities || [];
            state.connections = project.connections || [];
            
            // Update ID counters based on loaded project
            updateIDCounters();
            const fixedIds = normalizeDuplicateIds();
            updateIDCounters();
            const removedConnections = sanitizeConnections();
            if (fixedIds > 0 || removedConnections > 0) {
                console.warn('State was normalized after project load:', {
                    fixedIds,
                    removedConnections,
                });
            }
            
            const projectNameEl = document.querySelector('input[placeholder="My Project"]');
            const descriptionEl = document.querySelector('textarea[placeholder="Project description"]');
            
            if (projectNameEl) projectNameEl.value = project.name || name;
            if (descriptionEl) descriptionEl.value = project.description || '';
            
            saveState();
            render();
            updateStats();
            
            console.log(`Project "${project.name}" loaded successfully`);
        } else {
            throw new Error(result.error);
        }
    } catch (error) {
        console.log(`Error loading project: ${error.message}`);
        throw error;
    }
}

function updateIDCounters() {
    // Scan all existing IDs and update counters to avoid duplicates
    let maxCapNum = 0;
    let maxDelNum = 0;
    let maxTaskNum = 0;
    
    state.capabilities.forEach(cap => {
        const match = cap.id.match(/cap(\d+)/);
        if (match) {
            maxCapNum = Math.max(maxCapNum, parseInt(match[1]));
        }
        
        cap.deliverables?.forEach(del => {
            const delMatch = del.id.match(/del(\d+)/);
            if (delMatch) {
                maxDelNum = Math.max(maxDelNum, parseInt(delMatch[1]));
            }
            
            del.tasks?.forEach(task => {
                const taskMatch = task.id.match(/task(\d+)/);
                if (taskMatch) {
                    maxTaskNum = Math.max(maxTaskNum, parseInt(taskMatch[1]));
                }
            });
        });
    });
    
    // Set counters to next available number
    state.nextCapId = maxCapNum + 1;
    state.nextDelId = maxDelNum + 1;
    state.nextTaskId = maxTaskNum + 1;
    
    console.log('Updated ID counters:', {
        nextCapId: state.nextCapId,
        nextDelId: state.nextDelId,
        nextTaskId: state.nextTaskId
    });
}

function normalizeDuplicateIds() {
    const seenIds = new Set();
    let fixedCount = 0;

    state.capabilities.forEach(cap => {
        if (!cap.id || seenIds.has(cap.id)) {
            cap.id = generateId('capability');
            fixedCount++;
        }
        seenIds.add(cap.id);

        (cap.deliverables || []).forEach(del => {
            if (!del.id || seenIds.has(del.id)) {
                del.id = generateId('deliverable');
                fixedCount++;
            }
            seenIds.add(del.id);

            (del.tasks || []).forEach(task => {
                if (!task.id || seenIds.has(task.id)) {
                    task.id = generateId('task');
                    fixedCount++;
                }
                seenIds.add(task.id);
            });
        });
    });

    return fixedCount;
}

function sanitizeConnections() {
    const connectionKeys = new Set();
    const validConnections = [];

    (state.connections || []).forEach(conn => {
        if (!conn || !conn.from || !conn.to) {
            return;
        }

        if (!findTask(conn.from) || !findTask(conn.to)) {
            return;
        }

        const key = `${conn.from}->${conn.to}`;
        if (connectionKeys.has(key)) {
            return;
        }

        connectionKeys.add(key);
        validConnections.push(conn);
    });

    const removedCount = (state.connections || []).length - validConnections.length;
    state.connections = validConnections;
    return removedCount;
}

// ========== EVENT LISTENERS ==========

function setupEventListeners() {
    if (!canvas) return;
    
    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('mouseup', handleMouseUp);
    
    // Prevent context menu on canvas
    canvas.addEventListener('contextmenu', (e) => {
        e.preventDefault();
    });
}

// ========== UI TOGGLES ==========

function toggleLeftMenu() {
    const leftMenu = document.querySelector('.left-menu');
    const toggleBtn = document.querySelector('.toggle-btn');
    
    if (leftMenu) {
        leftMenu.classList.toggle('hidden');
        
        // Update button text based on menu state
        if (toggleBtn) {
            if (leftMenu.classList.contains('hidden')) {
                toggleBtn.textContent = '>';
            } else {
                toggleBtn.textContent = '<';
            }
        }
    }
}

function init() {
    // Get DOM elements
    canvas = document.getElementById('canvas');
    capabilitiesLayer = document.getElementById('capabilities-layer');
    deliverablesLayer = document.getElementById('deliverables-layer');
    tasksLayer = document.getElementById('tasks-layer');
    connectionsLayer = document.getElementById('connections-layer');
    
    // Check if elements exist
    if (!canvas || !capabilitiesLayer || !deliverablesLayer || !tasksLayer || !connectionsLayer) {
        console.error('Required DOM elements not found. Retrying...');
        setTimeout(init, 100);
        return;
    }
    
    console.log('DOM elements found, initializing...');
    
    // Setup event listeners
    setupEventListeners();
    updateConnectModeUI();
    
    // Try to restore from localStorage first
    try {
        const savedState = localStorage.getItem('dagEditorState');
        if (savedState) {
            const parsed = JSON.parse(savedState);
            state.capabilities = parsed.capabilities || [];
            state.connections = parsed.connections || [];
            updateIDCounters();
            const fixedIds = normalizeDuplicateIds();
            updateIDCounters();
            const removedConnections = sanitizeConnections();
            if (fixedIds > 0 || removedConnections > 0) {
                console.warn('State was normalized after local restore:', {
                    fixedIds,
                    removedConnections,
                });
            }
            console.log('Restored state from localStorage');
            saveState();
            render();
            updateStats();
            return; // Don't load sample project
        }
    } catch (e) {
        console.warn('Could not restore from localStorage:', e);
    }
    
    // Load sample project only if no saved state
    loadProject('sample_project').then(() => {
        console.log('Sample project loaded');
    }).catch(err => {
        console.log('No sample project, starting fresh');
        // Save initial state even if sample doesn't load
        saveState();
        updateStats();
    });
    
    console.log('JIRA Scope DAG Editor initialized');
}

// Start the application when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// ========== DEBUG FUNCTIONS ==========
window.debugDAG = function() {
    console.group('DAG Debug Info');
    console.log('Connection Mode:', state.connectionMode);
    console.log('Connection Source:', state.connectionSource ? {
        id: state.connectionSource.id,
        name: state.connectionSource.name
    } : null);
    console.log('Total Connections:', state.connections.length);
    console.log('All Connections:', state.connections);
    console.log('All Tasks:', getTasksList());
    console.groupEnd();
};

function getTasksList() {
    const tasks = [];
    state.capabilities.forEach(cap => {
        cap.deliverables.forEach(del => {
            del.tasks.forEach(task => {
                tasks.push({ id: task.id, name: task.name });
            });
        });
    });
    return tasks;
}

console.log('💡 Tip: Call debugDAG() in console to see current state');

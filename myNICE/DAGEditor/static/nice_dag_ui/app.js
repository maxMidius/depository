const canvas = document.getElementById('canvas');
const nodeLabelInput = document.getElementById('nodeLabel');
const nodeTypeInput = document.getElementById('nodeType');
const addNodeBtn = document.getElementById('addNode');
const toggleConnectBtn = document.getElementById('toggleConnect');
const deleteNodeBtn = document.getElementById('deleteNode');
const deleteEdgeBtn = document.getElementById('deleteEdge');
const groupNameInput = document.getElementById('groupName');
const createGroupBtn = document.getElementById('createGroup');
const ungroupBtn = document.getElementById('ungroup');
const dagNameInput = document.getElementById('dagName');
const saveDagBtn = document.getElementById('saveDag');
const dagList = document.getElementById('dagList');
const loadDagBtn = document.getElementById('loadDag');
const newDagBtn = document.getElementById('newDag');
const nodeList = document.getElementById('nodeList');
const edgeList = document.getElementById('edgeList');
const groupList = document.getElementById('groupList');
const status = document.getElementById('status');

// Log initialization
console.log('[Init] DAG Elements:', {
  dagNameInput: !!dagNameInput,
  saveDagBtn: !!saveDagBtn,
  loadDagBtn: !!loadDagBtn,
  dagList: !!dagList,
  status: !!status
});

// Log when page loads to verify status element
if (status) {
  console.log('✓ Status element found');
} else {
  console.error('✗ Status element NOT found');
}

const state = {
  nodes: [],
  edges: [],
  groups: [],
  selectedNodeId: null,
  selectedNodeIds: [],
  selectedGroupId: null,
  selectedEdgeIdx: null,
  connectMode: false,
  connectSourceId: null,
  dragId: null,
  dragOffset: { x: 0, y: 0 },
  dragMode: 'single', // 'single' or 'multi'
  nextId: 1,
  nextGroupId: 1,
  zoom: 1,
  panX: 0,
  panY: 0,
  isPanning: false,
  lassoActive: false,
  lassoAdditive: false,
  lassoStart: { x: 0, y: 0 },
  lassoEnd: { x: 0, y: 0 },
  lassoJustFinished: false,
};

function setStatus(text, type = 'info') {
  if (!status) {
    console.error('Status element not available');
    return;
  }
  
  status.textContent = text;
  console.log(`[Status] ${type.toUpperCase()}: ${text}`);
  
  // Remove all status classes
  status.classList.remove('success', 'error');
  
  // Add appropriate class for visual feedback
  if (type === 'success') {
    status.classList.add('success');
    // Auto-clear success messages after 3 seconds
    setTimeout(() => {
      if (status) {
        status.classList.remove('success');
        status.textContent = 'Ready';
      }
    }, 3000);
  } else if (type === 'error') {
    status.classList.add('error');
    // Auto-clear error messages after 5 seconds
    setTimeout(() => {
      if (status) {
        status.classList.remove('error');
        status.textContent = 'Ready';
      }
    }, 5000);
  }
}

function uniqueId() {
  const id = `n${state.nextId}`;
  state.nextId += 1;
  return id;
}

function uniqueGroupId() {
  const id = `g${state.nextGroupId}`;
  state.nextGroupId += 1;
  return id;
}

function canvasSize() {
  const rect = canvas.getBoundingClientRect();
  return { width: rect.width, height: rect.height };
}

function screenToCanvas(clientX, clientY) {
  const rect = canvas.getBoundingClientRect();
  const x = (clientX - rect.left - state.panX) / state.zoom;
  const y = (clientY - rect.top - state.panY) / state.zoom;
  return { x, y };
}

function addNode() {
  const label = nodeLabelInput.value.trim() || `Node ${state.nextId}`;
  const type = nodeTypeInput.value;
  const id = uniqueId();
  const x = 80 + (state.nodes.length % 5) * 150;
  const y = 80 + Math.floor(state.nodes.length / 5) * 120;

  state.nodes.push({ id, label, type, x, y, width: 130, height: 46 });
  nodeLabelInput.value = '';
  setStatus(`Added node ${id}`);
  render();
}

function deleteSelectedNode() {
  // Handle lasso selection (multiple nodes)
  if (state.selectedNodeIds.length > 0) {
    const idsToDelete = state.selectedNodeIds;
    // Delete all selected nodes
    state.nodes = state.nodes.filter((n) => !idsToDelete.includes(n.id));
    // Delete all edges connected to any of the deleted nodes
    state.edges = state.edges.filter((e) => !idsToDelete.includes(e.source) && !idsToDelete.includes(e.target));
    // Remove deleted nodes from groups
    state.groups.forEach((group) => {
      group.nodeIds = group.nodeIds.filter((nodeId) => !idsToDelete.includes(nodeId));
    });
    // Remove empty groups
    state.groups = state.groups.filter((group) => group.nodeIds.length > 0);
    
    state.selectedNodeId = null;
    state.selectedNodeIds = [];
    state.selectedGroupId = null;
    state.selectedEdgeIdx = null;
    
    setStatus(`Deleted ${idsToDelete.length} node(s) and their edges`, 'success');
    render();
    return;
  }

  // Handle single node selection
  if (!state.selectedNodeId) {
    setStatus('Select a node first');
    return;
  }
  const id = state.selectedNodeId;
  state.nodes = state.nodes.filter((n) => n.id !== id);
  state.edges = state.edges.filter((e) => e.source !== id && e.target !== id);
  state.groups.forEach((group) => {
    group.nodeIds = group.nodeIds.filter((nodeId) => nodeId !== id);
  });
  state.groups = state.groups.filter((group) => group.nodeIds.length > 0);
  state.selectedNodeId = null;
  state.selectedNodeIds = [];
  state.selectedGroupId = null;
  state.selectedEdgeIdx = null;
  setStatus(`Deleted node ${id}`);
  render();
}

function deleteSelectedEdge() {
  if (state.selectedEdgeIdx === null) {
    setStatus('Select an edge first');
    return;
  }
  const edge = state.edges[state.selectedEdgeIdx];
  state.edges.splice(state.selectedEdgeIdx, 1);
  state.selectedEdgeIdx = null;
  setStatus(`Deleted edge: ${edge.source} -> ${edge.target}`);
  render();
}

function toggleConnectMode() {
  state.connectMode = !state.connectMode;
  state.connectSourceId = null;
  toggleConnectBtn.classList.toggle('primary', state.connectMode);
  toggleConnectBtn.textContent = state.connectMode ? 'Connecting...' : 'Connect';
  setStatus(state.connectMode ? 'Connect: click source node, then target node' : 'Connect mode off');
}

function addEdge(sourceId, targetId) {
  if (sourceId === targetId) {
    setStatus('Cannot connect node to itself');
    return;
  }
  const exists = state.edges.some((e) => e.source === sourceId && e.target === targetId);
  if (exists) {
    setStatus('Edge already exists');
    return;
  }
  state.edges.push({ source: sourceId, target: targetId });
  setStatus(`Connected ${sourceId} -> ${targetId}`);
  render();
}

function selectNode(id, event) {
  state.selectedEdgeIdx = null;
  if (state.connectMode) {
    state.selectedNodeId = id;
    state.selectedNodeIds = [id];
    if (!state.connectSourceId) {
      state.connectSourceId = id;
      setStatus(`Connect mode: select target for ${id}`);
    } else {
      addEdge(state.connectSourceId, id);
      state.connectSourceId = null;
      setStatus('Connect mode: select source node');
    }
    render();
    return;
  }

  const multi = event && event.shiftKey;
  if (multi) {
    if (state.selectedNodeIds.includes(id)) {
      state.selectedNodeIds = state.selectedNodeIds.filter((nodeId) => nodeId !== id);
    } else {
      state.selectedNodeIds = [...state.selectedNodeIds, id];
    }
  } else {
    state.selectedNodeIds = [id];
  }

  state.selectedNodeId = id;
  state.selectedGroupId = null;
  setStatus(`Selected ${state.selectedNodeIds.length} node(s)`);
  render();
}

function selectGroup(id) {
  // Avoid re-render if already selected (allows double-click to work)
  if (state.selectedGroupId === id) {
    return;
  }
  
  state.selectedGroupId = id;
  state.selectedNodeId = null;
  // Populate selectedNodeIds with the group's nodes for ungroup functionality
  const group = state.groups.find((g) => g.id === id);
  if (group) {
    state.selectedNodeIds = [...group.nodeIds];
  } else {
    state.selectedNodeIds = [];
  }
  state.selectedEdgeIdx = null;
  setStatus(`Selected group ${id}`);
  render();
}

function render() {
  const size = canvasSize();
  canvas.setAttribute('width', size.width);
  canvas.setAttribute('height', size.height);
  canvas.innerHTML = '';

  const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  g.setAttribute('transform', `translate(${state.panX}, ${state.panY}) scale(${state.zoom})`);

  const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
  defs.innerHTML = `
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#38bdf8" />
    </marker>
    <marker id="arrow-selected" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#facc15" />
    </marker>
  `;
  g.appendChild(defs);

  if (state.lassoActive) {
    const minX = Math.min(state.lassoStart.x, state.lassoEnd.x);
    const minY = Math.min(state.lassoStart.y, state.lassoEnd.y);
    const width = Math.abs(state.lassoEnd.x - state.lassoStart.x);
    const height = Math.abs(state.lassoEnd.y - state.lassoStart.y);
    const lassoRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    lassoRect.setAttribute('x', minX);
    lassoRect.setAttribute('y', minY);
    lassoRect.setAttribute('width', width);
    lassoRect.setAttribute('height', height);
    lassoRect.setAttribute('fill', 'rgba(56, 189, 248, 0.12)');
    lassoRect.setAttribute('stroke', '#38bdf8');
    lassoRect.setAttribute('stroke-width', '1.5');
    lassoRect.setAttribute('stroke-dasharray', '6 4');
    g.appendChild(lassoRect);
  }

  state.groups.forEach((group) => {
    const members = state.nodes.filter((node) => group.nodeIds.includes(node.id));
    if (!members.length) return;

    const padding = 22;
    const labelHeight = 22;
    const minX = Math.min(...members.map((n) => n.x)) - padding;
    const minY = Math.min(...members.map((n) => n.y)) - padding - labelHeight;
    const maxX = Math.max(...members.map((n) => n.x + n.width)) + padding;
    const maxY = Math.max(...members.map((n) => n.y + n.height)) + padding;
    const width = maxX - minX;
    const height = maxY - minY;

    const groupRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    groupRect.setAttribute('x', minX);
    groupRect.setAttribute('y', minY);
    groupRect.setAttribute('width', width);
    groupRect.setAttribute('height', height);
    groupRect.setAttribute('rx', '16');
    groupRect.setAttribute('fill', 'rgba(15, 23, 42, 0.55)');
    groupRect.setAttribute('stroke', group.id === state.selectedGroupId ? '#f8fafc' : '#38bdf8');
    groupRect.setAttribute('stroke-width', group.id === state.selectedGroupId ? '3' : '2');
    groupRect.setAttribute('stroke-dasharray', '6 4');
    groupRect.style.cursor = 'pointer';

    groupRect.addEventListener('pointerdown', (event) => {
      event.stopPropagation();
      selectGroup(group.id);
    });
    
    groupRect.addEventListener('click', (event) => {
      event.stopPropagation();
    });

    const groupLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    groupLabel.setAttribute('x', minX + 12);
    groupLabel.setAttribute('y', minY + 16);
    groupLabel.setAttribute('fill', '#e2e8f0');
    groupLabel.setAttribute('font-size', '12');
    groupLabel.setAttribute('font-weight', '700');
    groupLabel.setAttribute('pointer-events', 'all');
    groupLabel.textContent = group.label;
    groupLabel.style.cursor = 'text';
    groupLabel.style.userSelect = 'none';
    
    // Double-click to rename group label
    groupLabel.addEventListener('dblclick', (event) => {
      event.stopPropagation();
      event.preventDefault();
      
      // Create foreignObject for inline editing
      const foreign = document.createElementNS('http://www.w3.org/2000/svg', 'foreignObject');
      foreign.setAttribute('x', minX + 12);
      foreign.setAttribute('y', minY + 4);
      foreign.setAttribute('width', Math.max(150, width - 24));
      foreign.setAttribute('height', 24);
      
      const input = document.createElement('input');
      input.type = 'text';
      input.value = group.label;
      input.style.cssText = `
        width: 100%;
        height: 100%;
        border: 2px solid #38bdf8;
        background: white;
        color: #0f172a;
        font-size: 12px;
        font-weight: 700;
        padding: 2px 4px;
        box-sizing: border-box;
        font-family: inherit;
      `;
      
      foreign.appendChild(input);
      g.appendChild(foreign);
      
      // Focus and select all text
      setTimeout(() => {
        input.focus();
        input.select();
      }, 0);
      
      // Function to finish editing
      const finishEdit = () => {
        const newLabel = input.value.trim();
        if (newLabel) {
          group.label = newLabel;
          setStatus(`Renamed group to "${group.label}"`, 'success');
        }
        render();
      };
      
      // Save on Enter or blur
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          finishEdit();
        } else if (e.key === 'Escape') {
          render(); // Cancel edit
        }
      });
      input.addEventListener('blur', finishEdit);
    });
    
    // Prevent default behaviors on label to allow double-click
    groupLabel.addEventListener('pointerdown', (event) => {
      event.stopPropagation();
    });
    
    groupLabel.addEventListener('click', (event) => {
      event.stopPropagation();
      selectGroup(group.id);
    });

    g.appendChild(groupRect);
    g.appendChild(groupLabel);
  });

  state.edges.forEach((edge, idx) => {
    const source = state.nodes.find((n) => n.id === edge.source);
    const target = state.nodes.find((n) => n.id === edge.target);
    if (!source || !target) return;
    
    // Validate source and target have valid positions
    const sx1 = typeof source.x === 'number' && !isNaN(source.x) ? source.x : 0;
    const sy1 = typeof source.y === 'number' && !isNaN(source.y) ? source.y : 0;
    const sw = typeof source.width === 'number' && !isNaN(source.width) ? source.width : 130;
    const sh = typeof source.height === 'number' && !isNaN(source.height) ? source.height : 46;
    
    const tx1 = typeof target.x === 'number' && !isNaN(target.x) ? target.x : 0;
    const ty1 = typeof target.y === 'number' && !isNaN(target.y) ? target.y : 0;
    const tw = typeof target.width === 'number' && !isNaN(target.width) ? target.width : 130;
    const th = typeof target.height === 'number' && !isNaN(target.height) ? target.height : 46;

    // Calculate centers
    const scx = sx1 + sw / 2;
    const scy = sy1 + sh / 2;
    const tcx = tx1 + tw / 2;
    const tcy = ty1 + th / 2;
    
    // Calculate angle and distance
    const dx = tcx - scx;
    const dy = tcy - scy;
    const angle = Math.atan2(dy, dx);
    
    // Calculate edge points (offset from center by half width/height)
    const sourceX = scx + Math.cos(angle) * (sw / 2);
    const sourceY = scy + Math.sin(angle) * (sh / 2);
    const targetX = tcx - Math.cos(angle) * (tw / 2);
    const targetY = tcy - Math.sin(angle) * (th / 2);

    const isSelected = state.selectedEdgeIdx === idx;
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', sourceX);
    line.setAttribute('y1', sourceY);
    line.setAttribute('x2', targetX);
    line.setAttribute('y2', targetY);
    line.setAttribute('stroke', isSelected ? '#facc15' : '#38bdf8');
    line.setAttribute('stroke-width', isSelected ? '4' : '2.5');
    line.setAttribute('marker-end', isSelected ? 'url(#arrow-selected)' : 'url(#arrow)');
    line.style.cursor = 'pointer';
    line.addEventListener('click', (event) => {
      event.stopPropagation();
      state.selectedEdgeIdx = idx;
      state.selectedNodeId = null;
      state.selectedNodeIds = [];
      state.selectedGroupId = null;
      setStatus(`Selected edge: ${edge.source} -> ${edge.target}`);
      render();
    });
    g.appendChild(line);
  });

  state.nodes.forEach((node) => {
    // Validate node properties
    const nx = typeof node.x === 'number' && !isNaN(node.x) ? node.x : 80;
    const ny = typeof node.y === 'number' && !isNaN(node.y) ? node.y : 80;
    const nw = typeof node.width === 'number' && !isNaN(node.width) ? node.width : 130;
    const nh = typeof node.height === 'number' && !isNaN(node.height) ? node.height : 46;
    
    const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    group.setAttribute('data-id', node.id);

    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', nx);
    rect.setAttribute('y', ny);
    rect.setAttribute('width', nw);
    rect.setAttribute('height', nh);
    rect.setAttribute('rx', '10');
    rect.setAttribute('fill', typeColor(node.type));
    const isSelected = state.selectedNodeIds.includes(node.id);
    const isSource = state.connectSourceId === node.id;
    rect.setAttribute('stroke', isSource ? '#facc15' : (isSelected ? '#f8fafc' : '#0f172a'));
    rect.setAttribute('stroke-width', isSource ? '4' : (isSelected ? '3' : '2'));
    
    // Change cursor based on selection state
    if (isSelected && state.selectedNodeIds.length > 1) {
      rect.style.cursor = 'grab';
    } else {
      rect.style.cursor = 'pointer';
    }

    const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    label.setAttribute('x', nx + nw / 2);
    label.setAttribute('y', ny + nh / 2 + 4);
    label.setAttribute('text-anchor', 'middle');
    label.setAttribute('fill', '#0f172a');
    label.setAttribute('font-size', '12');
    label.setAttribute('font-weight', '700');
    label.setAttribute('pointer-events', 'all');
    label.textContent = node.label;
    label.style.cursor = 'text';
    label.style.userSelect = 'none';
    
    // Double-click to rename label with inline input
    label.addEventListener('dblclick', (event) => {
      event.stopPropagation();
      event.preventDefault();
      
      // Create foreignObject for inline editing
      const foreign = document.createElementNS('http://www.w3.org/2000/svg', 'foreignObject');
      foreign.setAttribute('x', nx);
      foreign.setAttribute('y', ny + nh / 2 - 10);
      foreign.setAttribute('width', nw);
      foreign.setAttribute('height', 24);
      
      const input = document.createElement('input');
      input.type = 'text';
      input.value = node.label;
      input.style.cssText = `
        width: 100%;
        height: 100%;
        border: 2px solid #38bdf8;
        background: white;
        color: #0f172a;
        font-size: 12px;
        font-weight: 700;
        text-align: center;
        padding: 2px;
        box-sizing: border-box;
        font-family: inherit;
      `;
      
      foreign.appendChild(input);
      g.appendChild(foreign);
      
      // Focus and select all text
      setTimeout(() => {
        input.focus();
        input.select();
      }, 0);
      
      // Function to finish editing
      const finishEdit = () => {
        const newLabel = input.value.trim();
        if (newLabel) {
          node.label = newLabel;
          setStatus(`Renamed node to "${node.label}"`);
        }
        render();
      };
      
      // Save on Enter or blur
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          finishEdit();
        } else if (e.key === 'Escape') {
          render(); // Cancel edit
        }
      });
      input.addEventListener('blur', finishEdit);
    });
    
    // Prevent dragging and clicking when interacting with label
    label.addEventListener('pointerdown', (event) => {
      event.stopPropagation();
    });
    
    label.addEventListener('click', (event) => {
      event.stopPropagation();
    });

    group.appendChild(rect);
    group.appendChild(label);
    group.addEventListener('pointerdown', (event) => {
      if (state.connectMode || event.shiftKey) {
        selectNode(node.id, event);
        return;
      }
      
      // Check if clicking on a node that's already part of multi-selection
      // If so, preserve the multi-selection for group drag
      const isPartOfMultiSelection = state.selectedNodeIds.length > 1 && state.selectedNodeIds.includes(node.id);
      
      if (!isPartOfMultiSelection) {
        selectNode(node.id, event);
      }
      startDrag(event, node.id);
    });
    group.addEventListener('click', (event) => selectNode(node.id, event));

    g.appendChild(group);
  });

  canvas.appendChild(g);

  nodeList.textContent = state.nodes.map((n) => `${n.id}: ${n.label} [${n.type}]`).join('\n') || '(none)';
  edgeList.textContent = state.edges.map((e) => `${e.source} -> ${e.target}`).join('\n') || '(none)';
  groupList.textContent = state.groups.map((g) => `${g.label}: ${g.nodeIds.join(', ')}`).join('\n') || '(none)';
}

function typeColor(type) {
  switch (type) {
    case 'start':
      return '#34d399';
    case 'end':
      return '#f97316';
    case 'decision':
      return '#facc15';
    default:
      return '#38bdf8';
  }
}

function startDrag(event, id) {
  event.preventDefault();
  const node = state.nodes.find((n) => n.id === id);
  if (!node) return;
  
  // Check if this node is part of a multi-selection
  const isPartOfSelection = state.selectedNodeIds.includes(id);
  
  state.dragId = id;
  state.dragMode = isPartOfSelection && state.selectedNodeIds.length > 1 ? 'multi' : 'single';
  
  // Calculate offset relative to the dragged node
  state.dragOffset = {
    x: event.clientX - node.x,
    y: event.clientY - node.y,
  };
  
  // For multi-drag, store initial positions of all selected nodes
  if (state.dragMode === 'multi') {
    state.dragInitialPositions = {};
    state.selectedNodeIds.forEach((nodeId) => {
      const n = state.nodes.find((nd) => nd.id === nodeId);
      if (n) {
        state.dragInitialPositions[nodeId] = { x: n.x, y: n.y };
      }
    });
  }
  
  canvas.setPointerCapture(event.pointerId);
  canvas.style.cursor = 'grabbing';
}

function onDrag(event) {
  if (!state.dragId) return;
  
  if (state.dragMode === 'multi') {
    // Multi-drag: move all selected nodes together
    const draggedNode = state.nodes.find((n) => n.id === state.dragId);
    if (!draggedNode) return;
    
    // Calculate the delta for the dragged node
    const currentX = event.clientX - state.dragOffset.x;
    const currentY = event.clientY - state.dragOffset.y;
    const deltaX = currentX - draggedNode.x;
    const deltaY = currentY - draggedNode.y;
    
    // Apply the same delta to all selected nodes
    state.selectedNodeIds.forEach((nodeId) => {
      const node = state.nodes.find((n) => n.id === nodeId);
      if (node) {
        node.x += deltaX;
        node.y += deltaY;
      }
    });
  } else {
    // Single-drag: move only the dragged node
    const node = state.nodes.find((n) => n.id === state.dragId);
    if (!node) return;
    node.x = event.clientX - state.dragOffset.x;
    node.y = event.clientY - state.dragOffset.y;
  }
  
  render();
}

function endDrag(event) {
  if (!state.dragId) return;
  canvas.releasePointerCapture(event.pointerId);
  state.dragId = null;
  state.dragMode = 'single';
  state.dragInitialPositions = {};
  canvas.style.cursor = 'default';
}

function createGroup() {
  if (!state.selectedNodeIds.length) {
    setStatus('Select one or more nodes to group');
    return;
  }
  const label = groupNameInput.value.trim() || `Group ${state.nextGroupId}`;
  const id = uniqueGroupId();
  state.groups.push({ id, label, nodeIds: [...state.selectedNodeIds] });
  state.selectedGroupId = id;
  groupNameInput.value = '';
  setStatus(`Created group ${label}`);
  render();
}

function ungroupSelected() {
  if (!state.selectedNodeIds.length) {
    setStatus('Select nodes to ungroup');
    return;
  }
  const selectedSet = new Set(state.selectedNodeIds);
  state.groups = state.groups.filter((group) => {
    const hasAny = group.nodeIds.some((nodeId) => selectedSet.has(nodeId));
    return !hasAny;
  });
  state.selectedGroupId = null;
  setStatus('Ungrouped selected nodes');
  render();
}

async function refreshDagList() {
  try {
    const response = await fetch('/api/dags');
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    dagList.innerHTML = '';
    if (data.success) {
      data.dags.forEach((dag) => {
        const option = document.createElement('option');
        option.value = dag.name;
        option.textContent = dag.name;
        dagList.appendChild(option);
      });
    }
  } catch (error) {
    console.error('Error refreshing DAG list:', error);
  }
}

async function saveDag() {
  console.log('[saveDag] Called');
  
  const name = dagNameInput.value.trim();
  console.log('[saveDag] DAG name:', name);
  
  if (!name) {
    setStatus('Enter a DAG name to save', 'error');
    return;
  }
  
  try {
    console.log('[saveDag] Preparing nodes...');
    // Ensure all nodes have complete visual properties
    const cleanNodes = state.nodes.map(node => ({
      id: node.id || '',
      label: node.label || '',
      type: node.type || 'default',
      x: typeof node.x === 'number' ? node.x : 80,
      y: typeof node.y === 'number' ? node.y : 80,
      width: typeof node.width === 'number' ? node.width : 130,
      height: typeof node.height === 'number' ? node.height : 46
    }));
    
    const payload = {
      name: name,
      description: '',
      nodes: cleanNodes,
      edges: state.edges,
      groups: state.groups,
    };
    
    console.log('[saveDag] Sending payload:', payload);
    setStatus('Saving DAG...', 'info');
    
    const response = await fetch('/api/dags/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    
    console.log('[saveDag] Response status:', response.status);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const result = await response.json();
    console.log('[saveDag] Result:', result);
    
    if (result.success) {
      setStatus(`✓ Saved ${result.name} with ${cleanNodes.length} nodes`, 'success');
      await refreshDagList();
    } else {
      setStatus(`✗ ${result.error || 'Save failed'}`, 'error');
    }
  } catch (error) {
    console.error('[saveDag] Error:', error);
    setStatus(`✗ Save error: ${error.message}`, 'error');
  }
}

async function loadDag() {
  console.log('[loadDag] Called');
  
  const name = dagList.value;
  console.log('[loadDag] Selected DAG:', name);
  
  if (!name) {
    setStatus('Select a DAG to load', 'error');
    return;
  }
  
  try {
    console.log('[loadDag] Fetching DAG...');
    const response = await fetch(`/api/dags/${encodeURIComponent(name)}`);
    
    console.log('[loadDag] Response status:', response.status);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const result = await response.json();
    console.log('[loadDag] Result:', result);
    
    if (result.success) {
      const data = result.data.data || { nodes: [], edges: [], groups: [] };
      
      // Validate and fix nodes with default values
      state.nodes = (data.nodes || []).map((node, idx) => ({
        id: node.id || `n${idx + 1}`,
        label: node.label || `Node ${idx + 1}`,
        type: node.type || 'default',
        x: typeof node.x === 'number' && !isNaN(node.x) ? node.x : (idx % 5) * 150 + 80,
        y: typeof node.y === 'number' && !isNaN(node.y) ? node.y : Math.floor(idx / 5) * 120 + 80,
        width: typeof node.width === 'number' && !isNaN(node.width) ? node.width : 130,
        height: typeof node.height === 'number' && !isNaN(node.height) ? node.height : 46
      }));
      
      // Update nextId to avoid ID collisions when adding new nodes
      const maxId = state.nodes.reduce((max, node) => {
        const match = node.id.match(/^n(\d+)$/);
        return match ? Math.max(max, parseInt(match[1], 10)) : max;
      }, 0);
      state.nextId = maxId + 1;
      
      state.edges = data.edges || [];
      state.groups = data.groups || [];
      state.selectedNodeId = null;
      state.selectedNodeIds = [];
      state.selectedGroupId = null;
      state.selectedEdgeIdx = null;
      state.connectSourceId = null;
      
      console.log('[loadDag] Loaded nodes:', state.nodes.length);
      setStatus(`✓ Loaded ${name} with ${state.nodes.length} nodes, ${state.edges.length} edges`, 'success');
      render();
    } else {
      setStatus(`✗ ${result.error || 'Load failed'}`, 'error');
    }
  } catch (error) {
    console.error('[loadDag] Error:', error);
    setStatus(`✗ Load error: ${error.message}`, 'error');
  }
}

function newDag() {
  state.nodes = [];
  state.edges = [];
  state.groups = [];
  state.selectedNodeId = null;
  state.selectedNodeIds = [];
  state.selectedGroupId = null;
  state.selectedEdgeIdx = null;
  state.connectSourceId = null;
  setStatus('New DAG');
  render();
}

console.log('[Setup] Setting up event listeners...');

addNodeBtn.addEventListener('click', addNode);
deleteNodeBtn.addEventListener('click', deleteSelectedNode);
deleteEdgeBtn.addEventListener('click', deleteSelectedEdge);
toggleConnectBtn.addEventListener('click', toggleConnectMode);
createGroupBtn.addEventListener('click', createGroup);
ungroupBtn.addEventListener('click', ungroupSelected);
saveDagBtn.addEventListener('click', saveDag);
loadDagBtn.addEventListener('click', loadDag);
newDagBtn.addEventListener('click', newDag);

console.log('[Setup] Event listeners ready');
console.log('[Setup] Save button listeners:', saveDagBtn ? 'YES' : 'NO');
console.log('[Setup] Load button listeners:', loadDagBtn ? 'YES' : 'NO');

canvas.addEventListener('pointermove', onDrag);
canvas.addEventListener('pointerup', endDrag);
canvas.addEventListener('pointerleave', endDrag);

// Zoom with mouse wheel
canvas.addEventListener('wheel', (event) => {
  event.preventDefault();
  const delta = event.deltaY > 0 ? 0.9 : 1.1;
  state.zoom *= delta;
  state.zoom = Math.max(0.1, Math.min(5, state.zoom));
  render();
});

// Pan with right-click drag
let lastX = 0, lastY = 0;
canvas.addEventListener('pointerdown', (event) => {
  if (event.button === 2) {
    state.isPanning = true;
    lastX = event.clientX;
    lastY = event.clientY;
    return;
  }

  if (event.button === 0 && event.target === canvas && !state.connectMode) {
    const start = screenToCanvas(event.clientX, event.clientY);
    state.lassoActive = true;
    state.lassoAdditive = event.shiftKey;
    state.lassoStart = { ...start };
    state.lassoEnd = { ...start };
    if (!state.lassoAdditive) {
      state.selectedNodeIds = [];
      state.selectedNodeId = null;
      state.selectedGroupId = null;
      state.selectedEdgeIdx = null;
    }
    canvas.setPointerCapture(event.pointerId);
    render();
  }
});

canvas.addEventListener('pointermove', (event) => {
  if (state.lassoActive && event.buttons === 1) {
    const pos = screenToCanvas(event.clientX, event.clientY);
    state.lassoEnd = { ...pos };
    render();
    return;
  }
  if (state.isPanning && event.buttons === 2) {
    const dx = event.clientX - lastX;
    const dy = event.clientY - lastY;
    state.panX += dx;
    state.panY += dy;
    lastX = event.clientX;
    lastY = event.clientY;
    render();
  }
});

canvas.addEventListener('pointerup', (event) => {
  state.isPanning = false;
  if (state.lassoActive) {
    const minX = Math.min(state.lassoStart.x, state.lassoEnd.x);
    const minY = Math.min(state.lassoStart.y, state.lassoEnd.y);
    const maxX = Math.max(state.lassoStart.x, state.lassoEnd.x);
    const maxY = Math.max(state.lassoStart.y, state.lassoEnd.y);

    const selected = state.nodes.filter((node) => {
      const nx = node.x;
      const ny = node.y;
      const nw = node.width || 130;
      const nh = node.height || 46;
      const intersects = nx < maxX && nx + nw > minX && ny < maxY && ny + nh > minY;
      return intersects;
    }).map((node) => node.id);

    if (state.lassoAdditive) {
      const set = new Set([...state.selectedNodeIds, ...selected]);
      state.selectedNodeIds = Array.from(set);
    } else {
      state.selectedNodeIds = selected;
    }
    state.selectedNodeId = state.selectedNodeIds[0] || null;
    state.selectedGroupId = null;
    state.selectedEdgeIdx = null;
    state.lassoActive = false;
    state.lassoJustFinished = true;
    canvas.releasePointerCapture(event.pointerId);
    setStatus(`Selected ${state.selectedNodeIds.length} node(s)`);
    render();
  }
});

canvas.addEventListener('contextmenu', (event) => {
  event.preventDefault();
});

canvas.addEventListener('click', (event) => {
  if (state.lassoJustFinished) {
    state.lassoJustFinished = false;
    return;
  }
  if (event.target === canvas && !state.lassoActive) {
    state.selectedNodeId = null;
    state.selectedNodeIds = [];
    state.selectedGroupId = null;
    state.selectedEdgeIdx = null;
    render();
  }
});

refreshDagList();
render();

// Test notification on load
setTimeout(() => {
  console.log('[Init] Testing status bar');
  setStatus('✓ DAG Editor Ready', 'success');
}, 500);

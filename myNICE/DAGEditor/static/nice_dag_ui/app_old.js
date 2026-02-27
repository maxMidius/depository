const canvas = document.getElementById('canvas');
const nodeLabelInput = document.getElementById('nodeLabel');
const nodeTypeInput = document.getElementById('nodeType');
const addNodeBtn = document.getElementById('addNode');
const toggleConnectBtn = document.getElementById('toggleConnect');
const deleteNodeBtn = document.getElementById('deleteNode');
const groupNameInput = document.getElementById('groupName');
const createGroupBtn = document.getElementById('createGroup');
const ungroupBtn = document.getElementById('ungroup');
const removeGroupBtn = document.getElementById('removeGroup');
const deleteEdgeBtn = document.getElementById('deleteEdge');
const dagNameInput = document.getElementById('dagName');
const saveDagBtn = document.getElementById('saveDag');
const dagList = document.getElementById('dagList');
const loadDagBtn = document.getElementById('loadDag');
const newDagBtn = document.getElementById('newDag');
const nodeList = document.getElementById('nodeList');
const edgeList = document.getElementById('edgeList');
const groupList = document.getElementById('groupList');
const status = document.getElementById('status');

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
  nextId: 1,
  nextGroupId: 1,
};

function setStatus(text) {
  status.textContent = text;
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

function addNode() {
  const label = nodeLabelInput.value.trim() || `Node ${state.nextId}`;
  const type = nodeTypeInput.value;
  const size = canvasSize();
  const id = uniqueId();
  const x = 80 + (state.nodes.length % 5) * 150;
  const y = 80 + Math.floor(state.nodes.length / 5) * 120;

  state.nodes.push({ id, label, type, x, y, width: 130, height: 46 });
  nodeLabelInput.value = '';
  setStatus(`Added node ${id}`);
  render();
}

function deleteSelectedNode() {
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
  state.selectedGroupId = id;
  state.selectedNodeId = null;
  state.selectedNodeIds = [];
  state.selectedEdgeIdx = null;
  setStatus(`Selected group ${id}`);
  render();
}

function render() {
  const size = canvasSize();
  canvas.setAttribute('width', size.width);
  canvas.setAttribute('height', size.height);
  canvas.innerHTML = '';

  const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
  defs.innerHTML = `
    <marker id="arrow" markerWidth="16" markerHeight="16" refX="13" refY="4" orient="auto">
      <polygon points="0 0, 16 4, 0 8" fill="#38bdf8"></polygon>
    </marker>
    <marker id="arrow-selected" markerWidth="16" markerHeight="16" refX="13" refY="4" orient="auto">
      <polygon points="0 0, 16 4, 0 8" fill="#facc15"></polygon>
    </marker>
  `;
  canvas.appendChild(defs);

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

    groupRect.addEventListener('pointerdown', (event) => {
      event.stopPropagation();
      selectGroup(group.id);
    });

    const groupLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    groupLabel.setAttribute('x', minX + 12);
    groupLabel.setAttribute('y', minY + 16);
    groupLabel.setAttribute('fill', '#e2e8f0');
    groupLabel.setAttribute('font-size', '12');
    groupLabel.setAttribute('font-weight', '700');
    groupLabel.textContent = group.label;
    groupLabel.addEventListener('pointerdown', (event) => {
      event.stopPropagation();
      selectGroup(group.id);
    });

    canvas.appendChild(groupRect);
    canvas.appendChild(groupLabel);
  });

  state.edges.forEach((edge, idx) => {
    const source = state.nodes.find((n) => n.id === edge.source);
    const target = state.nodes.find((n) => n.id === edge.target);
    if (!source || !target) return;

    const isSelected = state.selectedEdgeIdx === idx;
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', source.x + source.width / 2);
    line.setAttribute('y1', source.y + source.height / 2);
    line.setAttribute('x2', target.x + target.width / 2);
    line.setAttribute('y2', target.y + target.height / 2);
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
    canvas.appendChild(line);
  });

  state.nodes.forEach((node) => {
    const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    group.setAttribute('data-id', node.id);

    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', node.x);
    rect.setAttribute('y', node.y);
    rect.setAttribute('width', node.width);
    rect.setAttribute('height', node.height);
    rect.setAttribute('rx', '10');
    rect.setAttribute('fill', typeColor(node.type));
    const isSelected = state.selectedNodeIds.includes(node.id);
    const isSource = state.connectSourceId === node.id;
    rect.setAttribute('stroke', isSource ? '#facc15' : (isSelected ? '#f8fafc' : '#0f172a'));
    rect.setAttribute('stroke-width', isSource ? '4' : (isSelected ? '3' : '2'));

    const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    label.setAttribute('x', node.x + node.width / 2);
    label.setAttribute('y', node.y + node.height / 2 + 4);
    label.setAttribute('text-anchor', 'middle');
    label.setAttribute('fill', '#0f172a');
    label.setAttribute('font-size', '12');
    label.setAttribute('font-weight', '700');
    label.textContent = node.label;

    group.appendChild(rect);
    group.appendChild(label);
    group.addEventListener('pointerdown', (event) => {
      if (state.connectMode || event.shiftKey) {
        selectNode(node.id, event);
        return;
      }
      selectNode(node.id, event);
      startDrag(event, node.id);
    });
    group.addEventListener('click', (event) => selectNode(node.id, event));

    canvas.appendChild(group);
  });

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
  state.dragId = id;
  state.dragOffset = {
    x: event.clientX - node.x,
    y: event.clientY - node.y,
  };
  canvas.setPointerCapture(event.pointerId);
}

function onDrag(event) {
  if (!state.dragId) return;
  const node = state.nodes.find((n) => n.id === state.dragId);
  if (!node) return;
  node.x = event.clientX - state.dragOffset.x;
  node.y = event.clientY - state.dragOffset.y;
  render();
}

function endDrag(event) {
  if (!state.dragId) return;
  canvas.releasePointerCapture(event.pointerId);
  state.dragId = null;
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

function removeSelectedGroup() {
  if (!state.selectedGroupId) {
    setStatus('Select a group to remove');
    return;
  }
  state.groups = state.groups.filter((group) => group.id !== state.selectedGroupId);
  setStatus('Removed selected group');
  state.selectedGroupId = null;
  render();
}

async function refreshDagList() {
  const response = await fetch('/api/dags');
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
}

async function saveDag() {
  const name = dagNameInput.value.trim();
  if (!name) {
    setStatus('Enter a DAG name to save');
    return;
  }
  const payload = {
    description: '',
    nodes: state.nodes,
    edges: state.edges,
    groups: state.groups,
  };
  const response = await fetch(`/api/dags/save?name=${encodeURIComponent(name)}` , {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const result = await response.json();
  if (result.success) {
    setStatus(`Saved ${result.name}`);
    await refreshDagList();
  } else {
    setStatus(result.error || 'Save failed');
  }
}

async function loadDag() {
  const name = dagList.value;
  if (!name) {
    setStatus('Select a DAG to load');
    return;
  }
  const response = await fetch(`/api/dags/${encodeURIComponent(name)}`);
  const result = await response.json();
  if (result.success) {
    const data = result.data.data || { nodes: [], edges: [] };
    state.nodes = data.nodes || [];
    state.edges = data.edges || [];
    state.groups = data.groups || [];
    state.selectedNodeId = null;
    state.selectedNodeIds = [];
    state.connectSourceId = null;
    setStatus(`Loaded ${name}`);
    render();
  } else {
    setStatus(result.error || 'Load failed');
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

addNodeBtn.addEventListener('click', addNode);
deleteNodeBtn.addEventListener('click', deleteSelectedNode);
deleteEdgeBtn.addEventListener('click', deleteSelectedEdge);
toggleConnectBtn.addEventListener('click', toggleConnectMode);
createGroupBtn.addEventListener('click', createGroup);
ungroupBtn.addEventListener('click', ungroupSelected);
removeGroupBtn.addEventListener('click', removeSelectedGroup);
saveDagBtn.addEventListener('click', saveDag);
loadDagBtn.addEventListener('click', loadDag);
newDagBtn.addEventListener('click', newDag);
canvas.addEventListener('pointermove', onDrag);
canvas.addEventListener('pointerup', endDrag);
canvas.addEventListener('pointerleave', endDrag);
canvas.addEventListener('click', (event) => {
  if (event.target === canvas) {
    state.selectedNodeId = null;
    state.selectedNodeIds = [];
    state.selectedGroupId = null;
    state.selectedEdgeIdx = null;
    render();
  }
});

window.addEventListener('resize', render);

refreshDagList();
render();

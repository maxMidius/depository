const nodes = new vis.DataSet([
    { id: 1, label: 'Node 1' },
    { id: 2, label: 'Node 2' },
    { id: 3, label: 'Node 3' },
    { id: 4, label: 'Node 4' }
]);

const edges = new vis.DataSet([
    { from: 1, to: 2 },
    { from: 2, to: 3 },
    { from: 3, to: 4 }
]);

const container = document.getElementById('network');
const data = { nodes: nodes, edges: edges };
const options = { /* Customize your options */ };

const network = new vis.Network(container, data, options);

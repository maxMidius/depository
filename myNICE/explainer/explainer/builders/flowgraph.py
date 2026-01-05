def flowgraph(edges: list[tuple[str, str]]):
    """Return Cytoscape elements for a simple flowgraph."""
    nodes = {}
    for src, dst in edges:
        nodes[src] = {'data': {'id': src, 'label': src}}
        nodes[dst] = {'data': {'id': dst, 'label': dst}}
    elements = list(nodes.values())
    for src, dst in edges:
        elements.append({'data': {'id': f'{src}->{dst}', 'source': src, 'target': dst}})
    return elements

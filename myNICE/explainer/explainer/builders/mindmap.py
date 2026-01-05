def mindmap(root: str, branches: dict[str, list[str]]):
    """Mindmap: root with categories and leaves."""
    elements = [{'data': {'id': root, 'label': root}}]

    for category, leaves in branches.items():
        elements.append({'data': {'id': category, 'label': category}})
        elements.append({'data': {'id': f'{root}-{category}', 'source': root, 'target': category}})
        for leaf in leaves:
            elements.append({'data': {'id': leaf, 'label': leaf}})
            elements.append({'data': {'id': f'{category}-{leaf}', 'source': category, 'target': leaf}})
    return elements

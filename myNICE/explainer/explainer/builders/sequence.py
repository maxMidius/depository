def sequence(interactions: list[tuple[str, str, str]]):
    """Simple sequence diagram: (from, to, label)."""
    participants = {}
    elements = []

    for frm, to, label in interactions:
        participants.setdefault(frm, {'data': {'id': frm, 'label': frm}})
        participants.setdefault(to, {'data': {'id': to, 'label': to}})

    elements.extend(participants.values())

    for i, (frm, to, label) in enumerate(interactions):
        elements.append({
            'data': {
                'id': f'seq_{i}',
                'source': frm,
                'target': to,
                'label': label,
            }
        })
    return elements

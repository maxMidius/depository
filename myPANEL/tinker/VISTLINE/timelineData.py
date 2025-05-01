def timeline_data():
    """Sample timeline data with items and groups"""
    return {
        "data": {
            "items": [
                {"id": 1, "content": "Task 1", "start": "2023-01-01", "end": "2023-01-10", "group": 1},
                {"id": 2, "content": "Task 2", "start": "2023-01-05", "end": "2023-01-15", "group": 1},
                {"id": 3, "content": "Task 3", "start": "2023-01-12", "end": "2023-01-20", "group": 2},
                {"id": 4, "content": "Task 4", "start": "2023-01-18", "end": "2023-02-05", "group": 2},
                {"id": 5, "content": "Milestone", "start": "2023-01-25", "type": "point", "group": 3},
                {"id": 6, "content": "Task 5", "start": "2023-01-28", "end": "2023-02-10", "group": 3},
                {"id": 7, "content": "Task 6", "start": "2023-02-01", "end": "2023-02-15", "group": 4}
            ],
            "groups": [
                {"id": 1, "content": "Project A"},
                {"id": 2, "content": "Project B"},
                {"id": 3, "content": "Project C"},
                {"id": 4, "content": "Project D"}
            ]
        },
        "options": {
            "stack": True,
            "editable": False,
            "margin": {
                "item": 10,
                "axis": 5
            },
            "orientation": "top",
            "showTooltips": True,
            "tooltip": {
                "followMouse": True,
                "overflowMethod": "flip"
            },
            "zoomKey": "ctrlKey",
            "zoomMin": 1000 * 60 * 60 * 24,  # one day in milliseconds
            "zoomMax": 1000 * 60 * 60 * 24 * 31 * 3  # about 3 months in milliseconds
        }
    }

# Make available for import
def available_timelines():
    return {
        "Simple Project": timeline_data
    }
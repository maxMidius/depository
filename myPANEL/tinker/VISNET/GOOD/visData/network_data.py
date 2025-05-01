def hierarchical_tree_data():
    """Original hierarchical tree data set."""
    return {
        "data": {
            "nodes": [
                {"id": 1, "label": "Root", "level": 0},
                
                # Level 1 - Three main branches
                {"id": 2, "label": "Branch 1", "level": 1},
                {"id": 3, "label": "Branch 2", "level": 1},
                {"id": 4, "label": "Branch 3", "level": 1},
                
                # Level 2 - Two children per branch
                {"id": 5, "label": "Node 1.1", "level": 2},
                {"id": 6, "label": "Node 1.2", "level": 2},
                {"id": 7, "label": "Node 2.1", "level": 2},
                {"id": 8, "label": "Node 2.2", "level": 2},
                {"id": 9, "label": "Node 3.1", "level": 2},
                {"id": 10, "label": "Node 3.2", "level": 2},
                
                # Level 3 - Two children per level 2 node
                {"id": 11, "label": "Node 1.1.1", "level": 3},
                {"id": 12, "label": "Node 1.1.2", "level": 3},
                {"id": 13, "label": "Node 1.2.1", "level": 3},
                {"id": 14, "label": "Node 1.2.2", "level": 3},
                {"id": 15, "label": "Node 2.1.1", "level": 3},
                {"id": 16, "label": "Node 2.1.2", "level": 3},
                {"id": 17, "label": "Node 2.2.1", "level": 3},
                {"id": 18, "label": "Node 2.2.2", "level": 3},
                {"id": 19, "label": "Node 3.1.1", "level": 3},
                {"id": 20, "label": "Node 3.1.2", "level": 3},
                {"id": 21, "label": "Node 3.2.1", "level": 3},
                {"id": 22, "label": "Node 3.2.2", "level": 3}
            ],
            "edges": [
                # Root to Level 1
                {"id": "e1-2", "from": 1, "to": 2, "label": "Root→Branch 1"},
                {"id": "e1-3", "from": 1, "to": 3, "label": "Root→Branch 2"},
                {"id": "e1-4", "from": 1, "to": 4, "label": "Root→Branch 3"},
                
                # Branch 1 to Level 2
                {"id": "e2-5", "from": 2, "to": 5, "label": "B1→1.1"},
                {"id": "e2-6", "from": 2, "to": 6, "label": "B1→1.2"},
                
                # Branch 2 to Level 2
                {"id": "e3-7", "from": 3, "to": 7, "label": "B2→2.1"},
                {"id": "e3-8", "from": 3, "to": 8, "label": "B2→2.2"},
                
                # Branch 3 to Level 2
                {"id": "e4-9", "from": 4, "to": 9, "label": "B3→3.1"},
                {"id": "e4-10", "from": 4, "to": 10, "label": "B3→3.2"},
                
                # Level 2 to Level 3 (Branch 1)
                {"id": "e5-11", "from": 5, "to": 11, "label": "1.1→1.1.1"},
                {"id": "e5-12", "from": 5, "to": 12, "label": "1.1→1.1.2"},
                {"id": "e6-13", "from": 6, "to": 13, "label": "1.2→1.2.1"},
                {"id": "e6-14", "from": 6, "to": 14, "label": "1.2→1.2.2"},
                
                # Level 2 to Level 3 (Branch 2)
                {"id": "e7-15", "from": 7, "to": 15, "label": "2.1→2.1.1"},
                {"id": "e7-16", "from": 7, "to": 16, "label": "2.1→2.1.2"},
                {"id": "e8-17", "from": 8, "to": 17, "label": "2.2→2.2.1"},
                {"id": "e8-18", "from": 8, "to": 18, "label": "2.2→2.2.2"},
                
                # Level 2 to Level 3 (Branch 3)
                {"id": "e9-19", "from": 9, "to": 19, "label": "3.1→3.1.1"},
                {"id": "e9-20", "from": 9, "to": 20, "label": "3.1→3.1.2"},
                {"id": "e10-21", "from": 10, "to": 21, "label": "3.2→3.2.1"},
                {"id": "e10-22", "from": 10, "to": 22, "label": "3.2→3.2.2"}
            ]
        },
        "options": {
            "physics": {
                "enabled": True,
                "hierarchicalRepulsion": {
                    "centralGravity": 0.0,
                    "springLength": 100,
                    "springConstant": 0.01,
                    "nodeDistance": 120
                }
            },
            "layout": {
                "hierarchical": {
                    "enabled": True,
                    "direction": "UD",
                    "sortMethod": "directed"
                }
            },
            "nodes": {
                "shape": "dot",
                "size": 16
            },
            "edges": {
                "arrows": "to",
                "font": {
                    "align": "middle"
                }
            }
        }
    }

def mesh_network_data():
    """A mesh-style network with bidirectional connections."""
    return {
        "data": {
            "nodes": [
                {"id": 1, "label": "Server", "level": 0, "group": "server"},
                {"id": 2, "label": "Router 1", "level": 1, "group": "network"},
                {"id": 3, "label": "Router 2", "level": 1, "group": "network"},
                {"id": 4, "label": "Router 3", "level": 1, "group": "network"},
                {"id": 5, "label": "Client 1", "level": 2, "group": "client"},
                {"id": 6, "label": "Client 2", "level": 2, "group": "client"},
                {"id": 7, "label": "Client 3", "level": 2, "group": "client"},
                {"id": 8, "label": "Client 4", "level": 2, "group": "client"},
                {"id": 9, "label": "Client 5", "level": 2, "group": "client"},
                {"id": 10, "label": "Client 6", "level": 2, "group": "client"}
            ],
            "edges": [
                # Server to Routers
                {"id": "e1-2", "from": 1, "to": 2, "label": "100Mbps", "width": 2},
                {"id": "e1-3", "from": 1, "to": 3, "label": "100Mbps", "width": 2},
                {"id": "e1-4", "from": 1, "to": 4, "label": "100Mbps", "width": 2},
                
                # Router interconnections (mesh)
                {"id": "e2-3", "from": 2, "to": 3, "label": "10Mbps", "dashes": True},
                {"id": "e3-4", "from": 3, "to": 4, "label": "10Mbps", "dashes": True},
                {"id": "e4-2", "from": 4, "to": 2, "label": "10Mbps", "dashes": True},
                
                # Router 1 to Clients
                {"id": "e2-5", "from": 2, "to": 5, "label": "1Mbps"},
                {"id": "e2-6", "from": 2, "to": 6, "label": "1Mbps"},
                
                # Router 2 to Clients
                {"id": "e3-7", "from": 3, "to": 7, "label": "1Mbps"},
                {"id": "e3-8", "from": 3, "to": 8, "label": "1Mbps"},
                
                # Router 3 to Clients
                {"id": "e4-9", "from": 4, "to": 9, "label": "1Mbps"},
                {"id": "e4-10", "from": 4, "to": 10, "label": "1Mbps"}
            ]
        },
        "options": {
            "physics": {
                "enabled": True,
                "barnesHut": {
                    "gravitationalConstant": -2000,
                    "centralGravity": 0.3,
                    "springLength": 150,
                    "springConstant": 0.04,
                    "damping": 0.09
                }
            },
            "layout": {
                "hierarchical": {
                    "enabled": False
                }
            },
            "nodes": {
                "shape": "dot",
                "size": 16,
                "color": {
                    "border": "#2B7CE9",
                    "background": "#97C2FC",
                    "highlight": {
                        "border": "#FFA500",
                        "background": "#FFC864"
                    }
                }
            },
            "edges": {
                "arrows": {
                    "to": {
                        "enabled": True,
                        "scaleFactor": 0.5
                    },
                    "from": {
                        "enabled": True,
                        "scaleFactor": 0.2
                    }
                },
                "color": {
                    "color": "#848484",
                    "highlight": "#FF0000"
                },
                "font": {
                    "align": "middle"
                }
            },
            "groups": {
                "server": {
                    "shape": "diamond",
                    "color": {
                        "background": "#FF9900",
                        "border": "#FF6600"
                    },
                    "size": 25
                },
                "network": {
                    "shape": "triangle",
                    "color": {
                        "background": "#00CC66",
                        "border": "#009933"
                    }
                },
                "client": {
                    "shape": "dot",
                    "color": {
                        "background": "#6699FF",
                        "border": "#3366FF"
                    }
                }
            }
        }
    }

# Function to get all available networks
def available_networks():
    return {
        "Hierarchical Tree": hierarchical_tree_data,
        "Mesh Network": mesh_network_data
    }

# For backwards compatibility
def network_data():
    return hierarchical_tree_data()
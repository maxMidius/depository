// ============================================================================
//  Explainer Framework Core (Cytoscape + Custom JS→Python Bridge)
// ============================================================================

console.log("explainer_core_new.js LOADED");

window.Explainer = (function () {

    let cy = null;

    // ------------------------------------------------------------------------
    //  JS → Python event bridge (via FastAPI route)
    // ------------------------------------------------------------------------
    window.cytoEventChannel = async function(event_name, payload) {
        try {
            await fetch(`/cyto/event/${event_name}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload || {})
            });
        } catch (e) {
            console.warn('cytoEventChannel failed:', event_name, e);
        }
    };

    function sendToPython(event, payload) {
        window.cytoEventChannel(event, payload);
    }

    // ------------------------------------------------------------------------
    //  Initialize Cytoscape
    // ------------------------------------------------------------------------
    function init(containerId, elements, style, layoutName) {
        return new Promise(resolve => {

            const script = document.createElement("script");
            script.src = "https://unpkg.com/cytoscape@3.26.0/dist/cytoscape.min.js";

            script.onload = () => {
                const container = document.getElementById(containerId);

                cy = cytoscape({
                    container,
                    elements,
                    style: style || [
                        { selector: 'node', style: { 'label': 'data(label)' } },
                        { selector: 'edge', style: { 'curve-style': 'bezier', 'target-arrow-shape': 'triangle' } },
                    ],
                    layout: { name: layoutName || 'breadthfirst' },
                });

                // Node click
                cy.on('tap', 'node', evt => {
                    sendToPython('node_click', { id: evt.target.id() });
                });

                // Edge click
                cy.on('tap', 'edge', evt => {
                    const e = evt.target;
                    sendToPython('edge_click', {
                        id: e.id(),
                        source: e.data('source'),
                        target: e.data('target'),
                    });
                });

                // WAIT for layout to complete before resolving
                cy.layout({ name: layoutName || 'breadthfirst' }).run();
                cy.on('layoutstop', () => {
                    resolve(cy);
                });
            };

            document.head.appendChild(script);
        });
    }

    // ------------------------------------------------------------------------
    //  Expand / Collapse
    // ------------------------------------------------------------------------
    function getChildren(nodeId) {
        return cy.getElementById(nodeId).outgoers('node');
    }

    function expand(nodeId) {
        const children = getChildren(nodeId);
        children.forEach(child => {
            child.style('display', 'element');
            child.connectedEdges().style('display', 'element');
            expand(child.id());
        });
        sendToPython('expand', { id: nodeId });
    }

    function collapse(nodeId) {
        const children = getChildren(nodeId);
        children.forEach(child => {
            child.style('display', 'none');
            child.connectedEdges().style('display', 'none');
            collapse(child.id());
        });
        sendToPython('collapse', { id: nodeId });
    }

    // ------------------------------------------------------------------------
    //  Sprite (Ball)
    // ------------------------------------------------------------------------
    function createSprite(id, options) {
        console.log("🎨 createSprite: id=", id, "options=", options);
        
        const startNode = options.startNode;
        const startPos = startNode ? cy.getElementById(startNode).position() : {x:0, y:0};
        console.log("  startNode:", startNode, "startPos:", startPos);

        // Offset the sprite slightly so it doesn't completely hide the node
        const offsetPos = { x: startPos.x + 15, y: startPos.y - 15 };

        cy.add({
            group: 'nodes',
            data: { id, label: '' },
            classes: 'sprite',
            position: offsetPos,
        });
        console.log("  ✅ Sprite added to cy at offset position:", offsetPos);

        if (!cy.scratch('_sprite_styles_added')) {
            cy.style().selector('.sprite').style({
                'background-color': options.color || 'red',
                'background-opacity': 0.7,  // Semi-transparent so you can see nodes beneath
                'width': options.size || 20,
                'height': options.size || 20,
                'shape': 'ellipse',
                'z-index': 9999,
                'label': '',
                'border-width': 2,
                'border-color': 'white',
            }).update();

            cy.scratch('_sprite_styles_added', true);
            console.log("  ✅ Sprite styles applied with transparency and border");
        }
        
        // Verify sprite was created
        const verifySprite = cy.getElementById(id);
        console.log("  🔍 Verify sprite exists:", verifySprite?.id());
    }

    // ------------------------------------------------------------------------
    //  SAFE Sprite Movement (never breaks graph init)
    // ------------------------------------------------------------------------
    async function moveSprite(id, path, opts) {
        console.log("🔵 moveSprite START: id=", id, "path=", path, "opts=", opts);

        // SAFETY 1: Cytoscape must exist
        if (typeof cy === "undefined" || !cy) {
            console.warn("❌ moveSprite FAIL: cy not ready");
            return;
        }
        console.log("✅ SAFETY 1: cy exists");

        // SAFETY 2: Path must be valid
        if (!Array.isArray(path) || path.length === 0) {
            console.warn("❌ moveSprite FAIL: invalid path", path);
            return;
        }
        console.log("✅ SAFETY 2: path is valid, length=", path.length);

        // SAFETY 3: Sprite must exist
        const sprite = cy.getElementById(id);
        console.log("🔍 Looking for sprite:", id, "result=", sprite, "length=", sprite?.length);
        if (!sprite || sprite.length === 0) {
            console.warn("❌ moveSprite FAIL: sprite not found:", id);
            console.log("   Available nodes:", cy.nodes().map(n => n.id()));
            return;
        }
        console.log("✅ SAFETY 3: sprite found");

        const speed = (opts && opts.speed) || 600;
        console.log("Speed:", speed);

        // SAFETY 4: First node must exist
        const firstNodeId = path[0];
        const firstNode = cy.getElementById(firstNodeId);
        console.log("🔍 Looking for first node:", firstNodeId, "result=", firstNode, "length=", firstNode?.length);
        if (!firstNode || firstNode.length === 0) {
            console.warn("❌ moveSprite FAIL: first node not found:", firstNodeId);
            console.log("   Available nodes:", cy.nodes().map(n => n.id()));
            return;
        }
        console.log("✅ SAFETY 4: first node exists");

        // SAFETY 5: Position sprite on first node BEFORE animation
        const firstPos = firstNode.position();
        console.log("🔍 First node position:", firstPos);
        if (!firstPos || firstPos.x === undefined) {
            console.warn("❌ moveSprite FAIL: first node has no position:", firstNodeId, "pos=", firstPos);
            return;
        }
        sprite.position(firstPos);
        console.log("✅ SAFETY 5: sprite positioned at", firstPos);

        // SAFETY 6: Animation helper
        function animateToPosition(pos) {
            return new Promise(resolve => {
                try {
                    console.log("🎬 Starting animation to position:", pos);
                    
                    const animation = sprite.animate(
                        { position: pos },
                        { duration: speed, easing: 'ease-in-out' }
                    );
                    
                    console.log("🎬 Animation object:", animation);
                    console.log("🎬 Animation type:", typeof animation);
                    
                    // Try binding to 'complete'
                    animation.on('complete', () => {
                        console.log("✅ Animation complete via callback, sprite now at:", sprite.position());
                        resolve();
                    });
                    
                    // FALLBACK: Timeout in case callback never fires
                    setTimeout(() => {
                        console.log("⏱️  Animation timeout reached (fallback), sprite at:", sprite.position());
                        resolve();
                    }, speed + 100);
                    
                } catch (e) {
                    console.warn("❌ moveSprite: animation error", e);
                    resolve();
                }
            });
        }

        // SAFETY 7: Sequential movement
        console.log("🚀 Starting sequential movement through", path.length, "nodes");
        for (let idx = 0; idx < path.length; idx++) {
            const nodeId = path[idx];
            console.log(`  [${idx}/${path.length}] Moving to node: ${nodeId}`);

            const target = cy.getElementById(nodeId);

            if (!target || target.length === 0) {
                console.warn(`❌ Node ${nodeId} not found, skipping`);
                continue;
            }

            const pos = target.position();
            console.log(`  Position of ${nodeId}:`, pos);
            if (!pos || pos.x === undefined) {
                console.warn(`❌ Node ${nodeId} has no position, skipping`, pos);
                continue;
            }

            console.log(`  ▶️  Animating to ${nodeId}`);
            await animateToPosition(pos);

            console.log(`  ✨ Ball arrived at ${nodeId}`);
            sendToPython('ball_arrive', { sprite: id, node: nodeId });
        }

        console.log("🎯 moveSprite DONE");
        sendToPython('ball_done', { sprite: id });
    }

    // ------------------------------------------------------------------------
    //  Utility functions
    // ------------------------------------------------------------------------
    function show(nodeId) {
        cy.getElementById(nodeId).style('display', 'element');
    }

    function hide(nodeId) {
        cy.getElementById(nodeId).style('display', 'none');
    }

    function blink(nodeId, opts) {
        const n = cy.getElementById(nodeId);
        const color = (opts && opts.color) || 'yellow';
        const duration = (opts && opts.duration) || 800;
        const original = n.style('background-color') || '#888';

        n.style('background-color', color);
        setTimeout(() => n.style('background-color', original), duration);
    }

    // ------------------------------------------------------------------------
    //  Public API
    // ------------------------------------------------------------------------
    return {
        init,
        expand,
        collapse,
        createSprite,
        moveSprite,
        show,
        hide,
        blink,
    };

})();

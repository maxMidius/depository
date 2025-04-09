/**
 * Markmap Plugin for Reveal.js
 * Renders markdown as mind maps using the markmap library
 */
const RevealMarkmap = {
    id: 'markmap',
    
    /**
     * Initialize the plugin
     * @param {object} reveal - the reveal.js instance
     */
    init: function(reveal) {
        // Process markmap elements when a slide is shown
        function processSlide(event) {
            const slide = event.currentSlide;
            const markmapElements = slide.querySelectorAll('[data-markmap]');
            
            markmapElements.forEach(el => {
                renderMarkmap(el);
            });
        }
        
        // Render a single markmap element
        function renderMarkmap(el) {
            const markdown = el.getAttribute('data-markdown');
            if (!markdown) {
                console.error("No markdown content found");
                return;
            }

            // Clear any existing content
            el.innerHTML = '';

            try {
                // Create SVG element
                const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                svg.style.width = '90%';
                svg.style.height = '95%';
                svg.style.display = 'block'; // Prevent extra space below SVG
                svg.style.border = '0px solid #933';
                el.appendChild(svg);

                // Extract Markmap from the global object
                const { Markmap } = markmap;

                // Transform the markdown to markmap data
                const transformer = new markmap.Transformer();
                const { root } = transformer.transform(markdown);

                // Create the markmap visualization
                const mm = Markmap.create(svg, {
                    duration: 500,
                    autoFit: true, // Enable auto-fit
                    fitRatio: 0.55, // Use full space
                }, root);

                // Add click handlers to nodes using foreignObject
                mm.svg.selectAll('foreignObject').on('click', (e, d) => {
                    const nodeText = d.data?.v || 'Unknown Node';
                    console.log('Data:', d); // FlextreeNode<INode>
                    onNodeClick(nodeText); // Call the custom method
                });

                // Custom method to handle node clicks
                function onNodeClick(nodeText) {
                    alert(`You clicked on: ${nodeText}`);
                    // Add your custom logic here (e.g., navigation, toggling)
                }
            } catch (error) {
                console.error("Error rendering markmap:", error);
                el.innerHTML = '<div style="color: red">Error: ' + error.message + '</div>';
            }
        }
        
        // Register event listeners for Reveal.js
        reveal.on('ready', processSlide);
        reveal.on('slidechanged', processSlide);
    }
};

// Export the plugin for use with Reveal.js
window.RevealMarkmap = RevealMarkmap;

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
                svg.style.height = '90%';
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
                    fitRatio: 0.6, // Use full space
                }, root);

                // Adjust the viewBox to ensure the SVG is centered with a margin
                const handleResize = () => {
                    if (mm && mm.fit) {
                        //mm.fit();
                        const bbox = svg.getBBox();
                        console.log(bbox)
                        console.log(svg.width, svg.height)
                        //const margin = 20; // Add a comfortable margin
                        //const width = bbox.width*1.5 + 2 * margin;
                        //const height = bbox.height*1.5 + 2 * margin;
                        //const x = bbox.x - margin;
                        //const y = bbox.y - margin;

                        // svg.setAttribute('viewBox', `-${x} -${y} ${width} ${height}`);
                        // svg.style.width = '110%';
                        // svg.style.height = '110%';
                    }
                };

                // Call resize handler initially and on window resize
                // handleResize();
                // window.addEventListener('resize', handleResize);
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

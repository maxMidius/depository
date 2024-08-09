const express = require('express');
const bodyParser = require('body-parser');
const puppeteer = require('puppeteer');

const app = express();
app.use(bodyParser.json());

app.post('/generate-svg', async (req, res) => {
    const { code } = req.body;

    try {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        await page.setContent(`
            <!DOCTYPE html>
            <html>
            <head>
                <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            </head>
            <body>
                <div class="mermaid">${code}</div>
                <script>
                    mermaid.initialize({ startOnLoad: true });
                </script>
            </body>
            </html>
        `);

        // Wait for the Mermaid diagram to be rendered
        await page.waitForSelector('.mermaid svg');

        // Extract the SVG content
        const svgContent = await page.$eval('.mermaid', element => element.innerHTML);

        await browser.close();
        res.send(svgContent);
    } catch (error) {
        res.status(500).send(error.toString());
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

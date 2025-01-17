const express = require('express');
const bodyParser = require('body-parser');

const { JSDOM } = require('jsdom');
// const mermaid = require('mermaid');


const app = express();
app.use(bodyParser.json());

app.post('/generate-svg', async (req, res) => {
    const { mmScript } = req.body;

    console.log(req.body)
    try {
        const { default: mermaid } = await import('mermaid');
        console.log("import ok", Object.keys(mermaid) )
        const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
        global.document = dom.window.document;
        global.window = dom.window;

        mermaid.initialize({ startOnLoad: false });

        svgCode = await mermaid.render('mmGraph', mmScript )
        console.log(svgCode) ;
        res.send(svgCode);
    } catch (error) {
        console.log(error)
        res.status(500).send(error.toString());
    }
} )

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

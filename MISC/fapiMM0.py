from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def get_diagram():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mermaid Diagram</title>
        <script src="https://cdn.jsdelivr.net/npm/mermaid@8.13.8/dist/mermaid.min.js"></script>
        <script>
            window.onload = function() {
                mermaid.initialize({ startOnLoad: true });
            };
        </script>
    </head>
    <body>
        <div class="mermaid">
            graph TD;
            A-->B;
            A-->C;
            B-->D;
            C-->D;
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

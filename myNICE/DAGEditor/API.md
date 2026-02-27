# DAG Editor Pro - API Documentation

## Base URL

```
http://localhost:8000/api
```

## Authentication

Currently, the API is **open** (no authentication required). For production, add authentication as needed.

## Content Types

All requests and responses use `application/json` format.

---

## Endpoints

### Retrieve All DAGs

**Endpoint**: `GET /dags`

**Description**: List all saved DAGs with metadata

**Response**:
```json
{
  "success": true,
  "dags": [
    {
      "name": "simple-pipeline",
      "description": "Simple ETL pipeline",
      "created": "2026-02-26T10:00:00",
      "updated": "2026-02-26T10:00:00",
      "nodes": 5,
      "edges": 4
    }
  ]
}
```

**Example**:
```bash
curl http://localhost:8000/api/dags
```

---

### Get Specific DAG

**Endpoint**: `GET /dags/{dag_name}`

**Parameters**:
- `dag_name` (string, path): Name of the DAG to retrieve

**Response**:
```json
{
  "success": true,
  "data": {
    "name": "simple-pipeline",
    "description": "Simple ETL pipeline",
    "data": {
      "nodes": [
        {
          "id": "start",
          "label": "Start",
          "type": "start",
          "x": 100,
          "y": 50
        },
        {
          "id": "extract",
          "label": "Extract Data",
          "type": "normal",
          "x": 100,
          "y": 150
        }
      ],
      "edges": [
        {
          "source": "start",
          "target": "extract",
          "id": "e1"
        }
      ]
    },
    "created": "2026-02-26T10:00:00",
    "updated": "2026-02-26T10:00:00"
  }
}
```

**Example**:
```bash
curl http://localhost:8000/api/dags/simple-pipeline
```

---

### Save a DAG

**Endpoint**: `POST /dags/save`

**Request Body**:
```json
{
  "name": "my-workflow",
  "description": "My custom workflow",
  "nodes": [
    {
      "id": "start",
      "label": "Start",
      "type": "start",
      "x": 100,
      "y": 50
    },
    {
      "id": "task1",
      "label": "Task 1",
      "type": "normal",
      "x": 100,
      "y": 150
    },
    {
      "id": "end",
      "label": "End",
      "type": "end",
      "x": 100,
      "y": 250
    }
  ],
  "edges": [
    {
      "source": "start",
      "target": "task1",
      "id": "e1"
    },
    {
      "source": "task1",
      "target": "end",
      "id": "e2"
    }
  ]
}
```

**Response**:
```json
{
  "success": true,
  "message": "DAG saved",
  "name": "my-workflow"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/api/dags/save \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-workflow",
    "description": "My workflow",
    "nodes": [...],
    "edges": [...]
  }'
```

---

### Delete a DAG

**Endpoint**: `DELETE /dags/{dag_name}`

**Parameters**:
- `dag_name` (string, path): Name of the DAG to delete

**Response**:
```json
{
  "success": true
}
```

**Example**:
```bash
curl -X DELETE http://localhost:8000/api/dags/my-workflow
```

---

### Export DAG as JSON File

**Endpoint**: `POST /dags/{dag_name}/export`

**Description**: Download DAG as JSON file

**Response**: JSON file download

**Example**:
```bash
curl http://localhost:8000/api/dags/simple-pipeline/export > pipeline.json
```

---

### Import DAG from JSON File

**Endpoint**: `POST /dags/import`

**Request**:
- Multipart form data with file upload

**Response**:
```json
{
  "success": true,
  "name": "imported-dag"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/api/dags/import \
  -F "file=@my-dag.json"
```

---

### Get System Statistics

**Endpoint**: `GET /stats`

**Description**: Get overall system statistics

**Response**:
```json
{
  "dags": 5,
  "totalNodes": 23,
  "totalEdges": 20,
  "storageDir": "/path/to/storage"
}
```

**Example**:
```bash
curl http://localhost:8000/api/stats
```

---

### Health Check

**Endpoint**: `GET /health`

**Description**: Check if API is running

**Response**:
```json
{
  "status": "ok",
  "service": "DAG Editor API v1"
}
```

**Example**:
```bash
curl http://localhost:8000/api/health
```

---

## Data Models

### Node Object

```json
{
  "id": "unique-identifier",
  "label": "Display Label",
  "type": "start|normal|end",
  "x": 100,
  "y": 50,
  "properties": {}
}
```

**Fields**:
- `id` (string, required): Unique identifier for the node
- `label` (string, optional): Display text
- `type` (string, required): Node type - "start", "normal", or "end"
- `x` (number, optional): X coordinate on canvas
- `y` (number, optional): Y coordinate on canvas
- `properties` (object, optional): Custom properties

### Edge Object

```json
{
  "source": "node-id-1",
  "target": "node-id-2",
  "id": "unique-edge-id",
  "label": "Optional Label"
}
```

**Fields**:
- `source` (string, required): Source node ID
- `target` (string, required): Target node ID
- `id` (string, optional): Unique edge identifier
- `label` (string, optional): Edge label

### DAG Object

```json
{
  "name": "workflow-name",
  "description": "Workflow description",
  "data": {
    "nodes": [Node],
    "edges": [Edge]
  },
  "created": "ISO 8601 timestamp",
  "updated": "ISO 8601 timestamp"
}
```

---

## Error Handling

### Success Response

```json
{
  "success": true,
  "data": {}
}
```

### Error Response

```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created
- `400 Bad Request` - Invalid request format
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Examples

### Complete Workflow Example

#### 1. Create a new DAG

```bash
curl -X POST http://localhost:8000/api/dags/save \
  -H "Content-Type: application/json" \
  -d '{
    "name": "etl-pipeline",
    "description": "Data ETL workflow",
    "nodes": [
      {"id": "start", "label": "Start", "type": "start", "x": 100, "y": 50},
      {"id": "extract", "label": "Extract", "type": "normal", "x": 100, "y": 150},
      {"id": "transform", "label": "Transform", "type": "normal", "x": 100, "y": 250},
      {"id": "load", "label": "Load", "type": "normal", "x": 100, "y": 350},
      {"id": "end", "label": "End", "type": "end", "x": 100, "y": 450}
    ],
    "edges": [
      {"source": "start", "target": "extract", "id": "e1"},
      {"source": "extract", "target": "transform", "id": "e2"},
      {"source": "transform", "target": "load", "id": "e3"},
      {"source": "load", "target": "end", "id": "e4"}
    ]
  }'
```

#### 2. List all DAGs

```bash
curl http://localhost:8000/api/dags
```

#### 3. Get specific DAG

```bash
curl http://localhost:8000/api/dags/etl-pipeline
```

#### 4. Export DAG

```bash
curl http://localhost:8000/api/dags/etl-pipeline/export > etl-pipeline.json
```

#### 5. Delete DAG

```bash
curl -X DELETE http://localhost:8000/api/dags/etl-pipeline
```

---

## Python Client Example

```python
import requests
import json

API_URL = "http://localhost:8000/api"

# Create DAG
new_dag = {
    "name": "python-example",
    "description": "Created from Python",
    "nodes": [
        {"id": "start", "label": "Start", "type": "start"},
        {"id": "process", "label": "Process", "type": "normal"},
        {"id": "end", "label": "End", "type": "end"}
    ],
    "edges": [
        {"source": "start", "target": "process"},
        {"source": "process", "target": "end"}
    ]
}

response = requests.post(f"{API_URL}/dags/save", json=new_dag)
print(response.json())

# List DAGs
response = requests.get(f"{API_URL}/dags")
dags = response.json()['dags']
print(f"Total DAGs: {len(dags)}")

# Get specific DAG
response = requests.get(f"{API_URL}/dags/python-example")
dag = response.json()['data']
print(f"DAG: {dag['name']} ({len(dag['data']['nodes'])} nodes)")

# Get stats
response = requests.get(f"{API_URL}/stats")
stats = response.json()
print(f"Statistics: {stats}")
```

---

## JavaScript/Fetch Example

```javascript
const API_URL = "http://localhost:8000/api";

// Create DAG
async function createDAG() {
  const dag = {
    name: "js-example",
    description: "Created from JavaScript",
    nodes: [
      { id: "start", label: "Start", type: "start" },
      { id: "end", label: "End", type: "end" }
    ],
    edges: [
      { source: "start", target: "end" }
    ]
  };

  const response = await fetch(`${API_URL}/dags/save`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dag)
  });

  const result = await response.json();
  console.log(result);
}

// List DAGs
async function listDAGs() {
  const response = await fetch(`${API_URL}/dags`);
  const data = await response.json();
  console.log(data.dags);
}

createDAG();
listDAGs();
```

---

## Rate Limiting

Currently, no rate limiting is applied. For production use, consider implementing rate limiting based on your requirements.

---

## CORS

CORS is enabled for all origins. For production, configure CORS appropriately in `app_advanced.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)
```

---

## Versioning

Current API Version: **1.0**

Future versions may introduce changes. API will maintain backward compatibility whenever possible.

---

For more information, see the main [README.md](./README.md)

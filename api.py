from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import os

app = FastAPI()

# Enable CORS to allow requests from the HTML page
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mapping of project names to file names
PROJECT_FILES = {
    'fcfs': 'fcfs.txt',
    'sjf_np': 'sjf_np.txt',
    'sjf_p': 'sjf_p.txt',
    'ps_np': 'ps_np.txt',
    'ps_p': 'ps_p.txt',
    'rr': 'rr.txt',
    'pr': 'pr.txt',
    'ffbfwf': 'ffbfwf.txt',
    'rw': 'rw.txt',
    'pc': 'pc.txt',
    'b': 'b.txt',
    'fo':'fo.txt',
    'bellman':'bellman.txt',
    'dij':'dij.txt',
    'kushkal':'kushkal.txt',
    'prims':'prims.txt',
    'sm':'sm.txt',
    'nqueen':'nqueen.txt',
    'cn':'cn.txt',
    'ipv4':'ipv4.txt',
    'mm':'mm.txt',
    'hc':'hc.txt'
}

# Mapping of theory topics to file names
THEORY_FILES = {
    'fcfs': 'fcfs.txt',
    'sjf': 'sjf.txt',
    'ps': 'ps.txt',
    'rr': 'rr.txt',
    'pr': 'pr.txt',
    'ffbfwf': 'ffbfwf.txt',
    'rw': 'rw.txt',
    'pc': 'pc.txt',
    'b': 'b.txt',
    'fo': 'fo.txt'
}

@app.get("/code", response_class=PlainTextResponse)
async def get_code(project: str = Query(..., description="Project name")):
    """
    Get code content by project name.

    Example: GET /code?project=fcfs
    """
    # Normalize project name to lowercase
    project = project.lower()

    # Check if project exists
    if project not in PROJECT_FILES:
        raise HTTPException(
            status_code=404,
            detail=f"Project '{project}' not found. Available projects: {', '.join(PROJECT_FILES.keys())}"
        )

    file_name = PROJECT_FILES[project]
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    # Check if file exists
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"File '{file_name}' not found"
        )

    # Read and return file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reading file: {str(e)}"
        )

@app.get("/theory", response_class=PlainTextResponse)
async def get_theory(topic: str = Query(..., description="Theory topic name")):
    """
    Get theory content by topic name.

    Example: GET /theory?topic=fcfs
    """
    # Normalize topic name to lowercase
    topic = topic.lower()

    # Check if topic exists
    if topic not in THEORY_FILES:
        raise HTTPException(
            status_code=404,
            detail=f"Theory topic '{topic}' not found. Available topics: {', '.join(THEORY_FILES.keys())}"
        )

    file_name = THEORY_FILES[topic]
    file_path = os.path.join(os.path.dirname(__file__), 'theory', file_name)

    # Check if file exists
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"Theory file '{file_name}' not found"
        )

    # Read and return file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reading theory file: {str(e)}"
        )

@app.get("/projects")
async def list_projects():
    """
    List all available projects.

    Example: GET /projects
    """
    return {
        "projects": list(PROJECT_FILES.keys()),
        "count": len(PROJECT_FILES)
    }

@app.get("/se")
async def get_se():
    return {
        "aneesh":"https://drive.google.com/file/d/1WpD6wkLpf_bA6_LEH1ygDcKqLcHneCdd/view",
        "aakash":"https://drive.google.com/file/d/1V7MQN1Fv85A2y1Y9oN7EnYHGXeIu-G7K/view"
    }

@app.get("/info")
async def get_info():
    """
    Get API information including all project IDs.

    Example: GET /info
    """
    return {
        "api_name": "Code Scripts API",
        "version": "1.0",
        "total_projects": len(PROJECT_FILES),
        "project_ids": list(PROJECT_FILES.keys()),
        "endpoints": {
            "/": "API root information",
            "/info": "Detailed API information with all project IDs",
            "/code?project=<name>": "Get code for a specific project",
            "/projects": "List all available projects"
        },
        "usage_example": {
            "get_code": "/code?project=fcfs",
            "list_projects": "/projects",
            "get_info": "/info"
        }
    }

@app.get("/theory-info")
async def get_theory_info():
    """
    Get theory API information including all theory topic IDs.

    Example: GET /theory-info
    """
    return {
        "api_name": "Theory Notes API",
        "version": "1.0",
        "total_topics": len(THEORY_FILES),
        "theory_topics": list(THEORY_FILES.keys()),
        "endpoints": {
            "/theory-info": "Detailed theory API information with all topic IDs",
            "/theory?topic=<name>": "Get theory notes for a specific topic"
        },
        "usage_example": {
            "get_theory": "/theory?topic=fcfs",
            "get_theory_info": "/theory-info"
        }
    }

@app.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Code Scripts API",
        "endpoints": {
            "/info": "Get detailed API information with all project IDs",
            "/code?project=<name>": "Get code for a specific project",
            "/projects": "List all available projects",
            "/theory-info": "Get detailed theory API information with all topic IDs",
            "/theory?topic=<name>": "Get theory notes for a specific topic"
        },
        "example": {
            "code": "/code?project=fcfs",
            "theory": "/theory?topic=fcfs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    PORT = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=PORT)

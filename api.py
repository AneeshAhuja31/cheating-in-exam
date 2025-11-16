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
    'ffbtwt': 'ffbtwt.txt',
    'rw': 'rw.txt',
    'pc': 'pc.txt',
    'b': 'b.txt',
    'fo':'fo.txt',
    'bellman':'bellman.txt',
    'dij':'dij.txt',
    'kushkal':'kushkal.txt',
    'prims':'prims.txt',
    'sm':'sm.txt'
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
            "/projects": "List all available projects"
        },
        "example": "/code?project=fcfs"
    }

if __name__ == "__main__":
    import uvicorn
    PORT = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=PORT)

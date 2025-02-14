from fastapi import FastAPI, HTTPException, Response
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Serve static files from the 'public' directory
app.mount("/static", StaticFiles(directory="public"), name="static")

# Alternative to serving all static files (for more granular control):
@app.get("/css/{path:path}")  # {path:path} handles subdirectories
async def read_css(path: str):
    """Serves CSS files from the 'public' directory."""
    file_path = os.path.join("public", path)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=400, detail="Invalid path")

    if not path.endswith(".css"): # Ensure it's a CSS file (optional security)
        raise HTTPException(status_code=400, detail="Invalid file type")

    try:
        with open(file_path, "rb") as f: # Open in binary mode for all files
            file_content = f.read()
        return Response(content=file_content, media_type="text/css")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {e}")


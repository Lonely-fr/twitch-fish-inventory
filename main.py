from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Constants
INVENTORY_DIR = Path("inventory")
FISH_DATA_PATH = Path("fish_api.json")

def load_json(filepath: Path):
    """Универсальная функция загрузки JSON"""
    try:
        return json.loads(filepath.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise HTTPException(404, detail="File not found")
    except json.JSONDecodeError:
        raise HTTPException(500, detail="Invalid JSON format")

@app.get("/api/fishes")
async def get_fishes():
    """Получение данных о всех рыбах"""
    return load_json(FISH_DATA_PATH)

@app.get("/api/inventory/{username}")
async def get_inventory(username: str):
    """Получение инвентаря пользователя"""
    inventory_path = INVENTORY_DIR / f"{username.lower()}.json"
    try:
        return load_json(inventory_path)
    except HTTPException as e:
        if e.status_code == 404:
            return {"fishes": []}
        raise

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
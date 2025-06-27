from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Загрузка данных о рыбах
def load_fish_data():
    with open("fish_api.json", "r", encoding="utf-8") as f:
        return json.load(f)

# API endpoint
@app.get("/api/fishes")
async def get_fishes():
    return load_fish_data()

# Endpoint для инвентаря пользователя
@app.get("/api/inventory/{username}")
async def get_user_inventory(username: str):
    try:
        with open(f"inventory/{username.lower()}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"fishes": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
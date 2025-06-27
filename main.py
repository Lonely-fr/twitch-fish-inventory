from fastapi import FastAPI
app = FastAPI()

@app.get("/api/fishes")
def get_fishes():
    import json
    with open("fish_api.json") as f:
        return json.load(f)
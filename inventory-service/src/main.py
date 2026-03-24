from fastapi import FastAPI

app = FastAPI(title="Inventory Service")

@app.get("/")
def read_root():
    return {"service": "Inventory Service", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

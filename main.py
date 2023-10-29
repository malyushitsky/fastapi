from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, AI Student!"}

@app.get("/add")
def add(x: int, y: int) -> int:
    return x + y

@app.get("/double/{number}")
def double(number: int) -> int:
    return number * 2
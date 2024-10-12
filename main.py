from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from threading import Thread

app = FastAPI()

# Dummy data to simulate code validation
valid_codes = {"123ABC", "456DEF", "WHXGPO"}

@app.get("/validate")
async def validate_code(code: str):
    """
    Validate the given code. Returns true if valid, false otherwise.
    """
    if not code:
        raise HTTPException(status_code=400, detail="Code is required")

    # Check if the code is in the list of valid codes
    if code in valid_codes:
        return {"valid": True}
    else:
        return {"valid": False}


def run() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    thread = Thread(target=run)
    thread.start()

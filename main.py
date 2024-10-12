from fastapi import FastAPI, HTTPException, Header
from threading import Thread
import uvicorn
import os

app = FastAPI()

# File to store the validated codes
VALIDATED_CODES_FILE = "validated.txt"

# Password for protected actions
ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]

# Ensure the file exists before starting
if not os.path.exists(VALIDATED_CODES_FILE):
    with open(VALIDATED_CODES_FILE, "w") as f:
        pass  # Create an empty file if not present

def normalize_code(code: str) -> str:
    """Normalize code by stripping whitespace and converting to uppercase."""
    return code.strip().upper()

def verify_password(provided_password: str):
    """Check if the provided password matches the admin password."""
    if provided_password != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Invalid password")


@app.get("/validate")
async def validate_code(code: str):
    """
    Validate the given code. Returns true if valid, false otherwise.
    """
    if not code:
        raise HTTPException(status_code=400, detail="Code is required")

    normalized_code = normalize_code(code)

    # Check if the code is valid
    try:
        with open(VALIDATED_CODES_FILE, "r") as file:
            valid_codes = file.readlines()
            if normalized_code in map(str.strip, valid_codes):
                return {"valid": True}
            else:
                return {"valid": False}
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Code file not found")


@app.post("/add")
async def add_code(code: str, password: str = Header(None)):
    """
    Add a code to the list of validated codes (requires password).
    """
    verify_password(password)  # Verify the provided password

    if not code:
        raise HTTPException(status_code=400, detail="Code is required")

    normalized_code = normalize_code(code)

    try:
        with open(VALIDATED_CODES_FILE, "a") as file:
            file.write(normalized_code + "\n")

        return {"message": "Code added successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add code: {str(e)}")


@app.get("/getCodes")
async def get_codes():
    """
    Retrieve all valid codes.
    """
    try:
        with open(VALIDATED_CODES_FILE, "r") as file:
            codes = [code.strip() for code in file.readlines()]
        return {"codes": codes}
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Code file not found")


@app.post("/removeCode")
async def remove_code(code: str, password: str = Header(None)):
    """
    Remove a specific code from the list of validated codes (requires password).
    """
    verify_password(password)  # Verify the provided password

    if not code:
        raise HTTPException(status_code=400, detail="Code is required")

    normalized_code = normalize_code(code)

    try:
        with open(VALIDATED_CODES_FILE, "r") as file:
            lines = file.readlines()

        with open(VALIDATED_CODES_FILE, "w") as file:
            for line in lines:
                if line.strip() != normalized_code:
                    file.write(line)

        return {"message": "Code removed successfully"}
    
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Code file not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove code: {str(e)}")


@app.post("/removeAll")
async def remove_all_codes(password: str = Header(None)):
    """
    Remove all codes from the list of validated codes (requires password).
    """
    verify_password(password)  # Verify the provided password

    try:
        with open(VALIDATED_CODES_FILE, "w") as file:
            file.write("")  # Overwrite file with empty content

        return {"message": "All codes removed successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove all codes: {str(e)}")


def run() -> None:
    """
    Start the FastAPI application.
    """
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    thread = Thread(target=run)
    thread.start()

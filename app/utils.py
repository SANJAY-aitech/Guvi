from fastapi.responses import JSONResponse

def error_response(message: str, status_code: int = 400):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message
        }
    )

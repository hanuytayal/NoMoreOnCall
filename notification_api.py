from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/notify")
async def notify(request: Request):
    data = await request.json()
    logger.info(f"Received notification: {data}")
    return JSONResponse(content={"status": "received", "data": data})

if __name__ == "__main__":
    uvicorn.run("notification_api:app", host="0.0.0.0", port=8001, reload=True) 
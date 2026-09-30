import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["ecse3038"]
devices = db["tutorial5"]

app = FastAPI()


class Device(BaseModel):
    name: str
    room: str
    temp: float
    online: bool


# Your handlers go below this line.

@app.get("/devices")
async def get_devices():
    device_list = list(devices.find({}, {"_id": 0}))
    return device_list

@app.get("/devices/{device_name}")
async def get_device(device_name: str):
    device = devices.find_one({"name": device_name}, {"_id": 0})
    if device is None:
        raise HTTPException(status_code=404, detail=f"No device called {device_name} found")
    return device

@app.post("/devices", status_code=201)
async def create_device(device: Device):
    if devices.find_one({"name": device.name}):
        raise HTTPException(status_code=409, detail=f"Device called {device.name} already exists")
    devices.insert_one(device.model_dump())
    return {"message": "Device created successfully"}

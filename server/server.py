from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import certifi

app = FastAPI()
client = MongoClient("mongodb+srv://aghathfaan08_db_user:ntrOwZssqpjTQDPV@clusterbelajar.ebafnib.mongodb.net/?appName=clusterbelajar", tlsCAFile=certifi.where())
db = client["iot_suhu"]
col = db["suhu"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/lapor")
def lapor(data: dict):
    col.insert_one({"suhu": data["suhu"], "kelembapan": data["kelembapan"], 
                    "waktu": datetime.now().strftime("%H:%M:%S %d-%m-%Y")})
    return {"pesan": "status diterima"}

@app.get("/suhu")
def suhu():
    data = col.find_one(sort=[("_id", -1)])
    data["_id"] = str(data["_id"])
    return data

@app.get("/suhu/history")
def suhu_history():
    data = list(col.find().sort("_id", -1).limit(10))
    for id in data:
        id["_id"] = str(id["_id"])
    return data



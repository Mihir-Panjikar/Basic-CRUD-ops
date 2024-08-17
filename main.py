from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os

load_dotenv(".env")

class Data(BaseModel):
    name: str
    roll_no: int
    year: int
    division: str
    age: int


app = FastAPI()

mongoclient = MongoClient(os.getenv("MONGO_URI"))
db = mongoclient["students"]
collection = db["student_data"]

@app.get("/read_data")
def read_data():
    try:
        # with open("data.json", "r") as json_file:
        #     file_data = json.load(json_file)
        #     return {"status": 200, "response": file_data}
        
        data = list(collection.find({}, {"_id": False}))
        return {"status": 200, "response": data}

    except FileNotFoundError:
        return {"status": 404, "response": "No data found"}
    
    except Exception as e:
        return {"status": 503, "response": f"An error occurred: {e}"}


@app.post("/add_data")
def add_data(new_data: Data):
    if not os.path.exists("data.json"):
        with open("data.json", "w") as json_file:
            json.dump([], json_file)
    
    try:
        new_data = jsonable_encoder(new_data)
        with open("data.json", "r+") as json_file:
            file_data = json.load(json_file)
            
            if not isinstance(file_data, list):
                raise TypeError("The JSON file content is not a list. Can't append data.")
            
            file_data.append(new_data)
            json_file.seek(0)
            
            json.dump(file_data, json_file, indent=4, separators=(",", ":"))
        
        inserted_document_id = collection.insert_one(new_data).inserted_id
        inserted_document = collection.find_one({"_id": inserted_document_id}, {"_id": False})

        return {"status": 200, "response": inserted_document}
    
    except Exception as e:
        return {"status": 503, "response": f"An error occurred: {e}"}


@app.put("/update_data")
def update_data(roll_no: int, data: Data):
    try:
        data = jsonable_encoder(data)
        with open("data.json", "r+") as json_file:
            file_data = json.load(json_file)
            
            for i in range(len(file_data)):
                if file_data[i]["roll_no"] == roll_no:
                    file_data[i] = data
                    break
            
            json_file.seek(0)
            json.dump(file_data, json_file, indent=4, separators=(",", ":"))
        
        data_updated = collection.find_one_and_update({"roll_no": roll_no}, {"$set": dict(data)}, projection={"_id": False})
        return {"status": 200, "response": data_updated}
    
    except Exception as e:
        return {"status": 503, "response": f"An error occurred: {e}"}


@app.delete("/delete_data")
def delete_data(roll_no: int):
    try:
        with open("data.json", "r") as json_file:
            file_data = json.load(json_file)
        
        deleted_data = None
        for i in range(len(file_data)):
            if file_data[i]["roll_no"] == roll_no:
                deleted_data = file_data.pop(i)
                break
            
        with open("data.json", "w") as json_file:
            json_file.seek(0)
            json.dump(file_data, json_file, indent=4, separators=(",", ":"))
            
        deleted_data = collection.find_one_and_delete({"roll_no": roll_no}, projection={"_id": False})
        return {"status": 200, "response": deleted_data}
    
    except Exception as e:
        return {"status": 503, "response": f"An error occurred: {e}"},
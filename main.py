from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from generate_asset_report import generate_asset_report

app = FastAPI()

class Input(BaseModel):
    start_time: int
    end_time: int

@app.get("/")
async def root():
    return {"message":"Welcome! This is the root endpoint. To generate an Excel report, please send a POST request to '/generate_report/' with 'start_time' and 'end_time' as integers in the request body. The report will be returned as an Excel file."
    }

@app.post("/generate_report/")
async def generate_report(input: Input):
    if input.start_time >= input.end_time:
        raise HTTPException(status_code=400, detail="start_time should be less than end_time")

    # Generate Excel file
    file_name = f"report_{input.start_time}_to_{input.end_time}.xlsx"
    
    file = generate_asset_report(input.start_time, input.end_time)

    if not file:
        raise HTTPException(status_code=400, detail="No data available for the time period mentioned")

    return FileResponse(file, filename=file_name)

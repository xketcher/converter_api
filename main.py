from fastapi import FastAPI, Request
from pydantic import BaseModel
from myanmar import converter

app = FastAPI()

class ConvertRequest(BaseModel):
    type: str  # "ztu" or "utz"
    text: str

@app.post("/")
async def convert_text(request: ConvertRequest):
    if request.type == "ztu":
        converted = converter.zg2uni(request.text)
    elif request.type == "utz":
        converted = converter.uni2zg(request.text)
    else:
        return {"error": "Invalid conversion type. Use 'ztu' or 'utz'."}
    
    return {"converted": converted}

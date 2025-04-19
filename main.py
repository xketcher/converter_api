from fastapi import FastAPI
from pydantic import BaseModel
from myanmar_tools import ZawgyiConverter

app = FastAPI()
converter = ZawgyiConverter()

class ConvertRequest(BaseModel):
    type: str  # "ztu" or "utz"
    text: str

@app.post("/")
async def convert_text(request: ConvertRequest):
    if request.type == "ztu":
        # Zawgyi to Unicode
        converted = converter.convert(request.text)
    elif request.type == "utz":
        # Unicode to Zawgyi is not directly supported by myanmar-tools
        return {"error": "Unicode to Zawgyi conversion is not supported by myanmar-tools."}
    else:
        return {"error": "Invalid type. Use 'ztu' only."}

    return {"converted": converted}

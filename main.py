from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ConvertRequest(BaseModel):
    type: str  # "ztu" or "utz"
    text: str

# --- Basic Rabbit Rules ---
RULES = [
    (u"\u106A", u"\u1009"),
    (u"\u1025(?=[\u1039\u102C])", u"\u1009"),
    (u"\u1025\u102E", u"\u1026"),
    (u"\u106B", u"\u100A"),
    (u"\u1090", u"\u101B"),
    (u"\u1040", u"\u1040"),
    (u"\u108F", u"\u1014"),
    (u"\u1012", u"\u1012"),
    (u"\u1013", u"\u1013"),
    (u"([\u1000-\u1021])\u1064", u"\u1004\u103A\u1039\\1"),
    (u"([\u1000-\u1021])\u108B", u"\u1004\u103A\u1039\\1\u102D"),
    (u"([\u1000-\u1021])\u108C", u"\u1004\u103A\u1039\\1\u102E"),
    (u"([\u1000-\u1021])\u108D", u"\u1004\u103A\u1039\\1\u1036"),
    (u"\u105A", u"\u102B\u103A"),
    (u"\u108E", u"\u102D\u1036"),
    (u"\u1033", u"\u102F"),
    (u"\u1034", u"\u1030"),
    (u"\u103F", u"\u1030"),
    (u"\u1086", u"\u103F"),
    (u"\u103D\u103E", u"\u103E\u103D"),
]

def zg2uni(text):
    for rule in RULES:
        text = text.replace(*rule)
    return text

def uni2zg(text):
    # This is a simplified reverse mapper. Full accuracy would require more rules.
    for rule in RULES[::-1]:  # reverse rules
        text = text.replace(rule[1], rule[0])
    return text

@app.post("/")
async def convert_text(request: ConvertRequest):
    if request.type == "ztu":
        converted = zg2uni(request.text)
    elif request.type == "utz":
        converted = uni2zg(request.text)
    else:
        return {"error": "Invalid type. Use 'ztu' or 'utz'."}

    return {"converted": converted}

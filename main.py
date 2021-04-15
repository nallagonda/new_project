from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI

class Comparison(BaseModel):
    resume: str
    jd: str

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/jdresume")
async def create_comparison(comp: Comparison):
    comp_dict = comp.dict()
    print(comp.resume)
    print(comp.jd)
    comp_dict.update({"resume": resume, "jd":jd})
    return comp_dict

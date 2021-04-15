from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from text_processing import compatibility_matrix

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
    common_words, resume_alone, jd_alone = compatibility_matrix(comp.resume,comp.jd)
    comp_dict.update({"resume": comp.resume, "jd": comp.jd, "common_words": common_words, "only_in_resume": resume_alone, "only_in_jd": jd_alone})
    return comp_dict

import random
from typing import Union

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/random-fail")
def read_root():
    if random.randrange(10) < 5:
        raise HTTPException(500, "Internal Sever Error")
    return {"Hello": "World"}


@app.get("/fail/{fail_or_success}")
def read_fail(fail_or_success: str):
    if fail_or_success == "fail":
        raise HTTPException(500, "Internal Sever Error")
    else:
        return {"Hello": "World", "value": fail_or_success}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

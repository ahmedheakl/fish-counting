from fastapi import FastAPI, Request
import json
import numpy as np

from fish_feeding import FishFeeding

app = FastAPI()

model = FishFeeding()
model.load_models()


@app.get("/test")
def read_root():
    return {"Hello": "World"}


@app.post("/fish_feeding")
async def get_fish_feeding(request: Request):
    request_body = await request.body()
    images = json.loads(request_body)["images"]
    for i, img in enumerate(images):
        images[i] = np.array(img, dtype=np.uint8)

    model.final_fish_feed(images)
    total_feed, times = model.final_fish_feed(images)

    return {"total_feed": total_feed, "times": times}
    
    

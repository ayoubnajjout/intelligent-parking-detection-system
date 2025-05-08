from fastapi import FastAPI, File, UploadFile
import torch
import numpy as np
import cv2
from io import BytesIO

app = FastAPI()

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.eval()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = model(img_rgb)

    detections = results.pandas().xyxy[0]
    detected_classes = detections['name'].tolist()

    if 'car' in detected_classes:
        return {"status": "occupied"}
    else:
        return {"status": "empty"}

from ultralytics import YOLO
import cv2
import numpy as np
from fastapi import UploadFile

model = YOLO("yolov8n.pt")

async def detect_pencil(image: UploadFile) -> bool:
    contents = await image.read()
    npimg = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    results = model(frame)
    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]
            if class_name.lower() == "pencil" or class_name.lower() == "knife" or class_name.lower() == "baseball bat":
                return True
    return False
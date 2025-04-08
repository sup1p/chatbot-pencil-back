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
    person_count = 0
    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id].lower()

            if class_name in {"pencil", "cell phone", "remote"}:
                return True

            if class_name == "person":
                person_count += 1

    if person_count > 1:
        return True
    return False
from ultralytics import YOLO
import cv2
import tempfile
from PIL import Image

model = YOLO("models/model_reptil80models.pt")

def detect_image(image_file, conf_threshold):
    image = Image.open(image_file)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    image.save(temp_file.name, 'JPEG', quality=100)
    temp_file.close()

    results = model.predict(
        source=temp_file.name,
        conf=conf_threshold,
        imgsz=640,
        save=False,
        verbose=False
    )

    image = cv2.imread(temp_file.name)
    names = model.names
    detected_classes = []

    for result in results:
        for box in result.boxes:
            cls = int(box.cls)
            conf = float(box.conf)
            if conf >= conf_threshold:
                label = names[cls]
                detected_classes.append((label, conf))

    if not detected_classes:
        return None, []

    return results[0].plot(), detected_classes

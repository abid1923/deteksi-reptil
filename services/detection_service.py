from ultralytics import YOLO
import cv2
import tempfile
from PIL import Image
import os
import pandas as pd
from datetime import datetime

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
        return None, []  #penanganan bukan reptil

    return results[0].plot(), detected_classes

def log_detection(filename, detected_classes):
    log_path = "logs/detection_logs.csv"
    if not os.path.exists(log_path) or os.stat(log_path).st_size == 0:
        log_df = pd.DataFrame(columns=["timestamp", "filename", "detected_classes"])
        log_df.to_csv(log_path, index=False)

    log_df = pd.read_csv(log_path)
    new_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "filename": filename,
        "detected_classes": ', '.join([f"{label} ({conf:.2f})" for label, conf in detected_classes]) if detected_classes else "Tidak Terdeteksi"
    }
    log_df.loc[len(log_df)] = new_row
    log_df.to_csv(log_path, index=False)
from ultralytics import YOLO

class Detector:
    def __init__(self, model_path):
        
        self.model = YOLO(model_path)
        self.classes = self.model.names 

    def get_detections(self, frame):
       
        results = self.model(frame, verbose=False, conf=0.4) # Confiança min 40%
        detections = []

        for result in results:
            for box in result.boxes:
                # Extrair coordenadas e converter para int
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # Classe e Confiança
                cls_id = int(box.cls[0])
                label = self.classes[cls_id]
                conf = float(box.conf[0])

                detections.append({
                    'label': label,          
                    'box': [x1, y1, x2, y2],  
                    'conf': conf,            
                    'class_id': cls_id
                })
        
        return detections
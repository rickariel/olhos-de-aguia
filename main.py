import cv2
from src.detector import Detector
from src.logic import SafetyLogic
from src.visualizer import Visualizer
from dotenv import load_dotenv
from roboflow import Roboflow
import os


load_dotenv()
api_key = os.getenv("ROBOFLOW_API_KEY")


rf = Roboflow(api_key=api_key)
project = rf.workspace("testcasque").project("ppe-detection-qlq3d")
version = project.version(1)


def main():

    MODEL_PATH = version.model 
    VIDEO_SOURCE = "data/video_1.mp4" 

    # --- INICIALIZAÇÃO ---
    print("Iniciando Olhos de Águia...")
    detector = Detector(MODEL_PATH)
    logic = SafetyLogic()
    visualizer = Visualizer()

    # Captura de vídeo
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    cap.set(3, 1280) # Largura HD
    cap.set(4, 720)  # Altura HD

    while True:
        success, frame = cap.read()
        if not success:
            print("Fim do vídeo ou erro na webcam.")
            break

        # 1. DETECTAR (Olhos)
        raw_detections = detector.get_detections(frame)

        # 2. PENSAR (Cérebro)
        analyzed_results = logic.check_compliance(raw_detections)

        # 3. MOSTRAR (Interface)
        frame = visualizer.draw_results(frame, analyzed_results)
        frame = visualizer.draw_fps(frame)

        cv2.imshow("Olhos de Aguia - Monitoramento de EPI", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

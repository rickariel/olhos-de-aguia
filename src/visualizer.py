import cv2
import time

class Visualizer:
    def __init__(self):
        # Cores (B, G, R)
        self.COLOR_SAFE = (0, 255, 0)    # Verde
        self.COLOR_DANGER = (0, 0, 255)  # Vermelho
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.prev_time = 0

    def draw_results(self, frame, people_results):
        
        for person in people_results:
            x1, y1, x2, y2 = person['box']
            is_safe = person['safe']

            color = self.COLOR_SAFE if is_safe else self.COLOR_DANGER
            status_text = "SEGURO" if is_safe else "PERIGO: SEM EPI"

            # 1. Desenha a Caixa (Bounding Box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)

            # 2. Desenha o Fundo do Texto (para ficar legível)
            (w, h), _ = cv2.getTextSize(status_text, self.font, 0.8, 2)
            cv2.rectangle(frame, (x1, y1 - 30), (x1 + w, y1), color, -1)

            # 3. Escreve o Texto
            cv2.putText(frame, status_text, (x1, y1 - 5), 
                        self.font, 0.8, (255, 255, 255), 2)

        return frame

    def draw_fps(self, frame):
        """Calcula e exibe o FPS no canto da tela"""
        curr_time = time.time()
        fps = 1 / (curr_time - self.prev_time) if self.prev_time != 0 else 0
        self.prev_time = curr_time
        
        cv2.putText(frame, f'FPS: {int(fps)}', (20, 50), 
                    self.font, 1, (255, 0, 0), 2)
        return frame
class SafetyLogic:
    def __init__(self):
        # Defina aqui os nomes EXATOS das classes do seu modelo
        self.TARGET_PERSON = ['person', 'worker'] 
        self.TARGET_PPE = ['helmet', 'hardhat', 'security_helmet'] # Adicione 'vest' se quiser

    def check_compliance(self, detections):
       
        people = [d for d in detections if d['label'] in self.TARGET_PERSON]
        ppes = [d for d in detections if d['label'] in self.TARGET_PPE]

        processed_people = []

        for person in people:
            px1, py1, px2, py2 = person['box']
            person_area = (px2 - px1) * (py2 - py1)
            
            has_ppe = False

            for ppe in ppes:
                hx1, hy1, hx2, hy2 = ppe['box']
                
                # --- MATEMÁTICA DE INTERSEÇÃO ---
                # Verifica se a caixa do capacete intersecta com a da pessoa
                dx = min(px2, hx2) - max(px1, hx1)
                dy = min(py2, hy2) - max(py1, hy1)

                if dx > 0 and dy > 0:
                    intersection_area = dx * dy
                    ppe_area = (hx2 - hx1) * (hy2 - hy1)

                    # Regra: Se mais de 50% do capacete está dentro da área da pessoa
                    # consideramos que ela está usando o capacete.
                    if (intersection_area / ppe_area) > 0.5:
                        has_ppe = True
                        break # Já achou um capacete para esta pessoa, vai para a próxima
            
            # Adiciona o status à pessoa
            person['safe'] = has_ppe
            processed_people.append(person)

        return processed_people
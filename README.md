## Olhos de Águia: Detecção de EPI (Equipamento de Proteção Individual)

### Status Atual do Modelo

Este projeto utiliza a arquitetura modular completa (Visão + Lógica + Visualização). Atualmente, ele está configurado para utilizar o modelo base **`yolov8n.pt`** (treinado no COCO).

  * **Comportamento:** O sistema detecta a `person` (pessoa), mas, como não consegue identificar `helmet` (capacete) ou `vest` (colete), a **Lógica de Segurança** é acionada, resultando em um **alerta VERMELHO** para todas as pessoas em cena, indicando "PERIGO: SEM EPI".
  * **Próxima Etapa:** O projeto está pronto para receber um modelo customizado (`best_ppe.pt`) treinado em EPIs para alcançar a funcionalidade total.

-----

### Visão Geral do Projeto

O **Olhos de Águia** é um sistema de Visão Computacional de alta performance projetado para fiscalizar e garantir a conformidade com as normas de segurança (HSE) em ambientes industriais, como canteiros de obras e fábricas. O sistema analisa um feed de vídeo (webcam ou arquivo) em tempo real e verifica se os trabalhadores estão utilizando os EPIs obrigatórios (Capacete e Colete de Segurança).

### Stack Tecnológico

| Componente | Tecnologia | Função |
| :--- | :--- | :--- |
| **Framework** | PyTorch | Base do modelo de Deep Learning. |
| **Detecção** | YOLOv8 (Ultralytics) | Modelo de inferência rápida em tempo real. |
| **Processamento** | OpenCV | Captura de vídeo, cálculo de FPS e renderização de caixas. |
| **Gerenciamento** | Poetry | Gerenciamento robusto de dependências e ambientes virtuais. |

### 📐 Arquitetura Modular

O projeto foi desenhado seguindo o princípio de Responsabilidade Única (SRP), separando as três principais etapas do pipeline de Visão Computacional. Isso garante escalabilidade e fácil manutenção.

| Módulo | Arquivo | Responsabilidade |
| :--- | :--- | :--- |
| **Visão (O Olho)** | `src/detector.py` | Carrega o modelo YOLO e realiza a inferência em cada frame. Retorna uma lista bruta de detecções. |
| **Lógica (O Cérebro)** | `src/logic.py` | Implementa a regra de negócio. Calcula a **Interseção sobre União (IoU)** entre as caixas de **Pessoa** e **EPI** para garantir que o equipamento esteja sendo *usado* e não apenas *presente* na cena. |
| **Visualização** | `src/visualizer.py` | Lida com toda a parte visual do OpenCV (desenho de caixas, texto, cor condicional, e cálculo/exibição do FPS). |
| **Orquestrador** | `main.py` | Controla o loop principal: captura frame, chama a Visão, processa com a Lógica e renderiza com o Visualizador. |

###  Configuração e Execução (Usando Poetry)

Este projeto utiliza **Poetry** para gerenciar dependências.

#### Pré-requisitos

  * Python 3.10+
  * Poetry instalado globalmente.

#### 1\. Clonar o Repositório

```bash
git clone https://github.com/rickariel/olhos-de-aguia.git
cd olhos-de-aguia
```

#### 2\. Instalar Dependências

O Poetry lerá o `pyproject.toml` e instalará todas as bibliotecas (incluindo PyTorch e OpenCV) em um ambiente virtual isolado.

```bash
poetry install
```

#### 3\. Executar o Protótipo

Use o comando `poetry run` para executar o script dentro do ambiente virtual gerenciado.

**Para usar a Webcam:**

```bash
poetry run python main.py
```

**Para usar um arquivo de vídeo (ex: `data/video_1.mp4`):**

  * Edite a variável `VIDEO_SOURCE` no arquivo `main.py` para o caminho desejado.

### Próximos Passos (Roadmap)

1.  **Integração do Modelo Customizado:** Treinar ou integrar um modelo `best_ppe.pt` de EPIs do Roboflow.
2.  **Alerta de Áudio:** Adicionar um módulo para reproduzir um som de alerta quando a condição "PERIGO" for detectada.
3.  **Registro:** Implementar o log de eventos (data, hora, pessoa) no caso de não conformidade.
4.  **Interface Web:** Exportar a visualização para um stream de vídeo (ex: usando Flask ou FastAPI) para monitoramento remoto.

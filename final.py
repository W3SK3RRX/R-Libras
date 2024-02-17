import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import tkinter as tk
from PIL import Image, ImageTk
import threading

camera_running = False

def hand_gesture_classifier(canvas, no_hand_label):
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1)
    classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

    offset = 20
    imgSize = 300

    labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
              "V", "W", "X", "Y", "Z"]

    def update_camera():
        success, img = cap.read()
        imgOutput = img.copy()
        hands, img = detector.findHands(img)

        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

            imgCropShape = imgCrop.shape

            aspectRatio = h / w

            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                print(prediction, index)

            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)

            cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                          (x - offset + 90, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
            cv2.putText(imgOutput, labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
            cv2.rectangle(imgOutput, (x - offset, y - offset),
                          (x + w + offset, y + h + offset), (255, 0, 255), 4)

            # Quando uma mão for detectada, limpe o texto do Label de aviso
            no_hand_label.config(text="")
        else:
            # Quando nenhuma mão for detectada, atualize o Label de aviso
            no_hand_label.config(text="Nenhuma mão detectada")
            # Defina um temporizador para limpar o texto após 2 segundos
            root.after(2000, lambda: no_hand_label.config(text=""))

            # Converter a imagem para o formato Tkinter
        img = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)

        # Atualizar o Canvas com a imagem da câmera centralizada
        canvas.delete("all")
        canvas.create_image(canvas.winfo_width() / 2, canvas.winfo_height() / 2, image=img)
        canvas.image = img

        # Agendar a próxima atualização da câmera
        canvas.after(10, update_camera)

        # Iniciar a primeira atualização da câmera

    update_camera()

def start_classification():
    global camera_running
    camera_running = True

    # Criar uma thread para iniciar a função de classificação
    classification_thread = threading.Thread(target=hand_gesture_classifier, args=(camera_canvas, no_hand_label))
    classification_thread.start()

def stop_classification():
    global camera_running
    camera_running = False

#######################################################################################################################

root = tk.Tk()

# Título
root.title("R-Libras")

# Tamanho da janela
largura = 1000
altura = 600

# Dimensões da janela
screenw_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Centralizando a janela
center_x = int(screenw_width/2 - largura/2)
center_y = int(screen_height/2 - altura/2)

root.geometry(f"{largura}x{altura}+{center_x}+{center_y}")

# Janela não redimensionável
root.resizable(False, False)

# Cor do background
root.config(bg="lavender")

# Frame para conter os botões
frame_botoes = tk.Frame(root)
frame_botoes.config(bg="lavender")
frame_botoes.pack(side=tk.BOTTOM)

# Botão Ligar Câmera
botao1 = tk.Button(frame_botoes, text="Ligar Câmera", bg="green", fg="white", border="2", font="roboto", command=start_classification)
botao1.pack(side=tk.LEFT, padx=10, pady=10)

# Botão Desligar Câmera
botao2 = tk.Button(frame_botoes, text="Desligar Câmera", bg="red", fg="white", border="2", font="roboto", command=stop_classification)
botao2.pack(side=tk.LEFT, padx=10, pady=10)

# Criar um Label para exibir a mensagem de aviso quando nenhuma mão for detectada
no_hand_label = tk.Label(root, text="", fg="red", font=("Helvetica", 16))
no_hand_label.pack(side=tk.TOP, pady=10)

# Criar um Canvas para exibir a saída da câmera centralizada
camera_canvas = tk.Canvas(root, width=800, height=600, bg="black")
camera_canvas.pack(side=tk.TOP, pady=10)

# Iniciar o loop principal do tkinter
root.mainloop()

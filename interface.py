import tkinter as tk
from test import hand_gesture_classifier
import threading

def start_classification():
    classification_thread = threading.Thread(target=hand_gesture_classifier)
    classification_thread.start()

root = tk.Tk()

# Título
root.title("#####")

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
botao1 = tk.Button(frame_botoes, text="Ligar Câmera", bg="green", fg="white", border="2", font="roboto", command=start_classification())
botao1.pack(side=tk.LEFT, padx=10, pady=10)

# Botão Desligar Câmera
botao2 = tk.Button(frame_botoes, text="Desligar Câmera", bg="red", fg="white", border="2", font="roboto")
botao2.pack(side=tk.LEFT, padx=10, pady=10)


root.mainloop()
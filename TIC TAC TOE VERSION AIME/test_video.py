import cv2
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

# -------------------------------------------------------------------------------------------------------------------------------------
# Cette partie inclue une vidéo d'introduction au début du jeu, l'utilisateur peut sauter la vidéo en appuyant sur la touche q du clavier
#--------------------------------------------------------------------------------------------------------------------------------------

# Chemin relatif vers ta vidéo d'introduction
video_path = "assets/intro_video.mp4"

# Créer une fenêtre Tkinter
root = tk.Tk()
root.title("Vidéo d'introduction")

# Obtenir les dimensions de l'écran
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Configurer la fenêtre pour qu'elle utilise les dimensions de l'écran
root.geometry(f"{screen_width}x{screen_height}")

# Créer un label pour afficher la vidéo
video_label = Label(root)
video_label.pack(fill=tk.BOTH, expand=True)

# Créer un objet de capture vidéo
cap = cv2.VideoCapture(video_path)

# Vérifier que la vidéo s'est correctement ouverte
if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir la vidéo.")
    exit()

# Variables pour stocker la taille actuelle de la fenêtre
window_width = screen_width
window_height = screen_height

# Fonction pour mettre à jour la taille de la fenêtre
def update_window_size(event):
    global window_width, window_height
    window_width = event.width
    window_height = event.height

# Lier l'événement de redimensionnement de la fenêtre
root.bind("<Configure>", update_window_size)

# Fonction pour lire et afficher la vidéo dans Tkinter
def play_video():
    ret, frame = cap.read()
    if ret:
        # Redimensionner la frame en fonction de la taille actuelle de la fenêtre
        frame = cv2.resize(frame, (window_width, window_height))
        
        # Convertir la frame en image compatible avec Tkinter
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        
        # Mettre à jour le label avec la nouvelle image
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
        
        # Appeler cette fonction à nouveau après 25ms
        root.after(25, play_video)
    else:
        # Libérer la capture et fermer la fenêtre Tkinter
        cap.release()
        root.destroy()

# Lancer la lecture de la vidéo
play_video()

# Démarrer la boucle principale Tkinter
root.mainloop()
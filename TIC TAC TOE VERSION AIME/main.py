#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Author: Assiongbon aimé KPODAR
# Created: 12 November, 2024, 7:06 PM
# Email: assiogbonaimékpodar@gmail.com

from tkinter import *
import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk

size_of_board = 600
symbol_size = (size_of_board / 3 - size_of_board / 10) / 2  # Taille réduite des pions
symbol_thickness = 50
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
background_color = "white"
Green_color = '#7BC043'

# -------------------------------------------------------------------------------------------------------------------------------------~--
# Cette partie inclue une vidéo d'introduction au début du jeu, l'utilisateur peut sauter la vidéo en appuyant sur la touche q du clavier
#-----------------------------------------------------------------------------------------------------------------------------------------

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
# Fontion pour détecter la touche q
def skip_video(event):
    """Permet de sauter la vidéo en appuyant sur 'q'."""
    print("Vidéo ignorée par l'utilisateur.")
    cap.release()  # Libère la vidéo
    root.destroy()  # Ferme la fenêtre de la vidéo
# Lier la touche 'q' à la fonction skip_video
root.bind('<q>', skip_video)

# Lancer la lecture de la vidéo
play_video()

# Démarrer la boucle principale Tkinter
root.mainloop()
#--------------------------------------------------------------------------------------------------------------------------------------

#======================================================================================================================================
# Cette partie est la partie logique du jeu 
# This part is the logical part of the game
#=======================================================================================================================================

class Tic_Tac_Toe():
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe Version Assiongbon Aimé KPODAR')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board, bg=background_color)
        self.canvas.pack()

        # Variables pour les scores
        self.score_X = 0
        self.score_O = 0

        # Ajouter deux labels pour afficher les scores séparément
        self.score_X_label = Label(self.window, text=f"Score X: {self.score_X}", font=("Arial", 14), fg=symbol_X_color)
        self.score_X_label.pack(side=LEFT, padx=20)

        self.score_O_label = Label(self.window, text=f"Score O: {self.score_O}", font=("Arial", 14), fg=symbol_O_color)
        self.score_O_label.pack(side=RIGHT, padx=20)

        # Ajouter un label pour le chronomètre
        self.timer_label = Label(self.window, text="Time: 00:00:00", font=("Arial", 14), fg="black")
        self.timer_label.pack(pady=10)

        # Ajouter un bouton "Play Again"
        self.play_again_button = Button(self.window, text="Play Again The Game", command=self.play_again, font=("Arial", 14))
        self.play_again_button.pack(pady=10)

        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros((3, 3))

        self.X_pieces = 0
        self.O_pieces = 0
        self.selected_piece = None
        self.reset_board = False
        self.gameover = False

        # Chronomètre
        self.time_elapsed = 0
        self.update_timer()

    def initialize_board(self):
        """Initialise la grille du jeu."""
        self.canvas.delete("all")
        for i in range(1, 3):
            self.canvas.create_line(0, size_of_board / 3 * i, size_of_board, size_of_board / 3 * i, width=2)
            self.canvas.create_line(size_of_board / 3 * i, 0, size_of_board / 3 * i, size_of_board, width=2)

    def play_again(self):
        """Réinitialise le jeu."""
        print("Redémarrage du jeu...")
        self.initialize_board()
        self.board_status = np.zeros((3, 3))
        self.X_pieces = 0
        self.O_pieces = 0
        self.player_X_turns = True
        self.selected_piece = None
        self.reset_board = False
        self.gameover = False
        self.time_elapsed = 0  # Réinitialiser le chronomètre
        self.update_timer()

    def update_timer(self):
        """Met à jour le chronomètre au format heures:minutes:secondes."""
        if not self.gameover:
            self.time_elapsed += 1

            # Calcul des heures, minutes et secondes
            hours = self.time_elapsed // 3600
            minutes = (self.time_elapsed % 3600) // 60
            seconds = self.time_elapsed % 60

            # Mettre à jour le label du chronomètre
            self.timer_label.config(text=f"Time: {hours:02d}:{minutes:02d}:{seconds:02d}")

            # Appeler cette méthode toutes les secondes
            self.window.after(1000, self.update_timer)

    def update_score(self):
        """Met à jour le score du joueur gagnant."""
        if self.player_X_turns:
            self.score_O += 1  # Si c'est au tour de X, O a gagné
            self.score_O_label.config(text=f"Score O: {self.score_O}")  # Mettre à jour le label de O
        else:
            self.score_X += 1  # Si c'est au tour de O, X a gagné
            self.score_X_label.config(text=f"Score X: {self.score_X}")  # Mettre à jour le label de X
        print(f"Score mis à jour - X: {self.score_X}, O: {self.score_O}")

    def display_gameover(self):
        """Affiche le message de fin de jeu."""
        self.canvas.delete("all")
        winner = "O" if self.player_X_turns else "X"
        self.update_score()  # Mettre à jour les scores
        self.canvas.create_text(size_of_board / 2, size_of_board / 2, font="cmr 40 bold",
                                fill="green", text=f"Player: ~ {winner} ~ wins!")
        print(f"Game Over! {winner} wins!")
        self.reset_board = True
        self.gameover = True  # Arrêter le chronomètre

    def draw_X(self, logical_position):
        """Dessine un X à la position donnée."""
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size,
                                width=symbol_thickness, fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size,
                                width=symbol_thickness, fill=symbol_X_color)

    def draw_O(self, logical_position):
        """Dessine un O à la position donnée."""
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size,
                                width=symbol_thickness, outline=symbol_O_color)

    def click(self, event):
        """Gère les clics de l'utilisateur."""
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        print(f"Clic detected : {grid_position}, Position logique : {logical_position}")

        if not self.is_valid_position(logical_position):
            print("Position invalide")
            return

        if not self.reset_board:
            if self.player_X_turns:
                if self.X_pieces < 3:
                    if not self.is_grid_occupied(logical_position):
                        print("Placement d'un X")
                        self.draw_X(logical_position)
                        self.board_status[logical_position[0]][logical_position[1]] = -1
                        self.X_pieces += 1
                        self.player_X_turns = not self.player_X_turns
                else:
                    if self.selected_piece is None:
                        if self.board_status[logical_position[0]][logical_position[1]] == -1:
                            print("Sélection d'un X existant")
                            self.selected_piece = logical_position
                    else:
                        if not self.is_grid_occupied(logical_position):
                            print("Déplacement d'un X")
                            self.move_piece(self.selected_piece, logical_position, 'X')
                            self.selected_piece = None
                            self.player_X_turns = not self.player_X_turns
            else:
                if self.O_pieces < 3:
                    if not self.is_grid_occupied(logical_position):
                        print("Placement d'un O")
                        self.draw_O(logical_position)
                        self.board_status[logical_position[0]][logical_position[1]] = 1
                        self.O_pieces += 1
                        self.player_X_turns = not self.player_X_turns
                else:
                    if self.selected_piece is None:
                        if self.board_status[logical_position[0]][logical_position[1]] == 1:
                            print("Sélection d'un O existant")
                            self.selected_piece = logical_position
                    else:
                        if not self.is_grid_occupied(logical_position):
                            print("Déplacement d'un O")
                            self.move_piece(self.selected_piece, logical_position, 'O')
                            self.selected_piece = None
                            self.player_X_turns = not self.player_X_turns

            if self.is_gameover():
                print("Fin du jeu")
                self.display_gameover()
        else:
            print("Redémarrage du jeu")
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

    def is_valid_position(self, logical_position):
        """Vérifie si la position est valide."""
        return 0 <= logical_position[0] < 3 and 0 <= logical_position[1] < 3

    def is_grid_occupied(self, logical_position):
        """Vérifie si une case est occupée."""
        return self.board_status[logical_position[0]][logical_position[1]] != 0

    def move_piece(self, from_position, to_position, player):
        """Déplace un pion d'une position à une autre."""
        grid_position_from = self.convert_logical_to_grid_position(from_position)
        grid_position_to = self.convert_logical_to_grid_position(to_position)

        # Augmenter la taille du rectangle de suppression
        rectangular = 25
        self.canvas.create_rectangle(
            grid_position_from[0] - symbol_size - rectangular, grid_position_from[1] - symbol_size - rectangular,
            grid_position_from[0] + symbol_size + rectangular, grid_position_from[1] + symbol_size + rectangular,
            fill=background_color, outline=background_color
        )

        if player == 'X':
            self.draw_X(to_position)
            self.board_status[from_position[0]][from_position[1]] = 0
            self.board_status[to_position[0]][to_position[1]] = -1
        else:
            self.draw_O(to_position)
            self.board_status[from_position[0]][from_position[1]] = 0
            self.board_status[to_position[0]][to_position[1]] = 1

    def convert_grid_to_logical_position(self, grid_position):
        """Convertit une position de grille en position logique."""
        return tuple((np.array(grid_position) // (size_of_board / 3)).astype(int))

    def convert_logical_to_grid_position(self, logical_position):
        """Convertit une position logique en position de grille."""
        return (size_of_board / 3) * np.array(logical_position) + size_of_board / 6

    def is_gameover(self):
        """Vérifie si le jeu est terminé."""
        for i in range(3):
            if abs(sum(self.board_status[i, :])) == 3 or abs(sum(self.board_status[:, i])) == 3:
                return True
        if abs(self.board_status.trace()) == 3 or abs(np.fliplr(self.board_status).trace()) == 3:
            return True
        return False
#===============================================================================================================================================

# Lancer le jeu
game_instance = Tic_Tac_Toe()
game_instance.window.mainloop()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
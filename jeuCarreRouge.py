# -*- coding: utf8 -*-

import tkinter as tk
from controleur import MenuControleur, JeuControleur

if __name__ == "__main__" :
    root = tk.Tk()
    root.title("Jeu du carré rouge")

    # appeler le controlleur ici.
    jeu = JeuControleur(root)
    menu = MenuControleur(root,jeu)
    menu.debuter()

    root.mainloop()
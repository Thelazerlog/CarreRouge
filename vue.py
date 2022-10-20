import tkinter as tk
from tkinter import simpledialog
from c31Geometry2 import *

class MenuVue:
    def __init__(self, root, fctLancerPartie, closeApp):
        self.menuFrame= tk.Frame (root, width=300, height=450, highlightbackground="blue", highlightthickness=3)
        self.root = root
        self.btn_nouvellePartie = tk.Button(root, text='Nouvelle Session',
                                            command=fctLancerPartie)
        self.btn_quitApp = tk.Button(root, text='Quitter',
                                     command=closeApp)

    def draw(self):
        self.btn_nouvellePartie.pack()
        self.btn_quitApp.pack() 
        self.menuFrame.pack(side=tk.LEFT)

    

class JeuVue:
    def __init__(self, root):
        self.root = root
        self.timer = tk.Label(root, text= "0.00") # a incrémenter 
        self.difficulter = tk.Label(root, text="") # a aller chercher au debut de la partie
        self.nom = tk.Label(root, text="") # a aller chercher au debut de la partie 
        self.canvas = tk.Canvas(root, width=450, height=450,
                highlightbackground="black", highlightthickness=50, bg="white")
        self.items = []
        #a VOIR et tester 
        self.timer.pack(ipadx=10, ipady=10, anchor=tk.NE)
        self.difficulter.pack(ipadx=10, ipady=10, anchor=tk.SW)
        self.nom.pack(ipadx=10, ipady=10, anchor=tk.SW)
        self.canvas.pack(side=tk.RIGHT)

    def destroy(self):
        self.canvas.destroy()
       
    def draw(self) : # dessine les item ( carre et rectangle)
        for item in self.items :
            item.draw()

    def setListen(self, eventName, command) : # prend en paramètre le nom de l'event et la commande qui lui est asocier par exemple self.vue.setListen("<ButtonPress-1>", self.setPlayerPosition)
        self.root.bind(eventName, command)

    def setNom(self,nom) :
        self.nom.config(text= "Nom du joueur : " + nom )

    def setDif(self,difficulter) :
        reponse = ''
        while reponse != '1' or reponse != '2' or reponse != '3' :
            reponse = simpledialog.askstring("Input","Entrez le niveau de difficulté désiré (1, 2, 3)",parent=root)
            if reponse == '1' or reponse == '2' or reponse == '3' :
                break
        return reponse
    
    def demanderDif(self,root) :
        return simpledialog.askstring("Input","Entrez le niveau de difficulté désiré (1, 2, 3)",parent=root) 

    def setTimer(self,temp) :
        self.timer.config(text= "Mineuteur : " + str(temp) + "s")

    def demanderNom(self,root) :
        return simpledialog.askstring("Input","Quel est votre nom",parent=root) 

    def addRectangle(self,origine, largeur, hauteur, orientation, remplissage,bordure,epaisseur): #test
        self.items.append(Rectangle(self.canvas,origine, largeur, hauteur, orientation, remplissage,bordure,epaisseur))

    def addCarre(self,origine,largeur,orientation,remplissage,bordure,epaisseur):
        self.items.append(Carre(self.canvas,origine,largeur,orientation,remplissage,bordure,epaisseur))
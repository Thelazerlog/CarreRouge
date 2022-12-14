import tkinter as tk
from tkinter import simpledialog
from c31Geometry2 import *

class MenuVue:
    """ cette classe permet de définir l'aparence du menu
    """
    def __init__(self, root, fctLancerPartie,voirScore,closeApp):
        """ Initialise le menu graphique

        :param root: Widget parent de notre boucle
        :type  root: tk.Widget
        :param fctLancerParti: methode de lancement de partie
        :type  fctLancerParti: methode()
        :param voirScore: methode voir le score
        :type  voirScore: methode()
        :param closeApp: methode fermer l'application
        :type closeApp : method() 
        """
        self.root = root
        self.score = tk.Label(root, text="")         
        self.btn_nouvellePartie = tk.Button(root, text='Nouvelle Session',
                                            command=fctLancerPartie)
        self.btn_quitApp = tk.Button(root, text='Quitter',
                                     command=closeApp)
        self.btn_voirScore = tk.Button(root, text='voirScore',
                                            command=voirScore)

    def draw(self):
        """ dessine le menu graphique et tout les boutons
        """
        self.btn_nouvellePartie.pack(side=tk.LEFT)
        self.btn_voirScore.pack(side=tk.LEFT)
        self.btn_quitApp.pack(side=tk.LEFT) 

    def setScore(self,score):
        """ change le champ score

            Args: score(String): la liste des score du fichier csv
        """
        self.score.config(text= "Nom    Temps   Difficulté \n" + score )
        self.score.pack(side=tk.LEFT)


class JeuVue:
    """ cette classe permet de définir l'aparence de l'espace de jeu
    """
    def __init__(self, root):
        """
        :param root: Widget parent de notre boucle
        :type  root: tk.Widget
        """
        self.root = root
        self.timer = tk.Label(root, text= "0.00") # a incrémenter 
        self.difficulter = tk.Label(root, text="") # a aller chercher au debut de la partie
        self.nom = tk.Label(root, text="") # a aller chercher au debut de la partie 
        self.timer.pack(ipadx=10, ipady=10, anchor=tk.NE) # place le timer
        self.difficulter.pack(ipadx=10, ipady=10, anchor=tk.SW) # place la dificulter
        self.nom.pack(ipadx=10, ipady=10, anchor=tk.SW) # place le nom du joueur 

    def destroy(self, canvas):
        """ ferme l'espace de jeu
        """
        canvas.destroy()

       
    def draw(self,rectangle) : 
        """ dessine tout les rectangle bleu

        Args:
            rectangle (RectangleBleu[]) : tableau d'objet de type Rectangle a dessiner
        """
        for rectangle in rectangle :
            rectangle.draw()
        
    def drawCarre(self,carre) :
        """ dessine le carré rouge

        Args:
            carre (CarreRouge) :  objet de type Carre a dessiner
        """
        carre.draw()

    def setListen(self, eventName, command) :
        """ Ecoute les evenement qui ce déroule sur sur le canvas et bind une commande sur un evenement 

        Args:
            eventName (String) : le nom de l'evenement 
            command (methode()) : la commande a effectuer 

        """ 
        self.root.bind(eventName, command)

    def setNom(self,nom) :
        """ change la valeur du champ nom

        Args:
            nom (String) : le nom du joueur chosi  
        """
        self.nom.config(text= "Nom du joueur : " + nom )

    def setDif(self,difficulter) :
        """ change la valeur du champ difficulter

        Args:
            difficulter (String) : la difficulté choisie  
        """
        self.difficulter.config(text= "Difficulté : " + difficulter)
    
    def demanderDif(self,root) :
        """ demande la difficulter a l'utulisateur dans un pop up et empêche un autre résultat que 1,2,3

        Args:
            root (tk.Widjet) : Widget parent de notre boucle

        Returns:
            String: la difficulter choisie 
        """
        reponse = ''
        while reponse != '1' or reponse != '2' or reponse != '3' :
            reponse = simpledialog.askstring("Input","Entrez le niveau de difficulté désiré (1, 2, 3)",parent=root)
            if reponse == '1' or reponse == '2' or reponse == '3' :
                break
        return reponse 

    def setTimer(self,temp) :
        """ change le champ timer

        Args:
            temp(String(format)) : le temp de la partie
        """
        self.timer.config(text= str(temp) + "s")

    def demanderNom(self,root) :
        """ demande le nom de l'utulisateur dans un pop up

        Args: 
            root (tk.Widjet) : Widget parent de notre boucle

        Returns:
            String: le nom choisi        
        """
        return simpledialog.askstring("Input","Quel est votre nom",parent=root) 
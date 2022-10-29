# -*- coding: utf8 -*-
import random
import time
from c31Geometry2 import *
import csv

class CarreRouge(Carre):
    """Cette classe représente le carré rouge (Hérite de Carre de c31Geometry2) 

    Attributes:
        origine(Vecteur): position du carré
        arrete(int): taille de la hauteur et largeur du carré
        axeDeplacement(int) : direction du mouvement du carré
    """    

    def __init__(self, canvas):
        """Permet de definir un carré rouge

            Initialise origine, arrete et axeDeplacement
            Args: 
                canvas (tk.Canvas): canvas où l'on dessine le carré
        """
        self.axeDeplacement = random.randint(0, 3)
        self.arrete = 40
        super().__init__(canvas, Vecteur(225, 225), self.arrete, 0 , "red", "red", 0)


    def getOrigine(self) -> Vecteur:
        """Permet de récupérer l'origine du carré

        Returns:
            Vecteur: Origine du carré
        """
        return super().get_origine()

    def getArrete(self):
        """Permet de récupérer l'arrete du carré

        Returns:
            int: hauteur et largeur du carré
        """
        return self.arrete
    
    def getAxe(self):
        """Permet de récupérer l'axe de déplacement du carré

        Returns:
            int: direction du mouvement du carré
        """
        return self.axeDeplacement

    def setAxe(self, axe):
        """Définit l'axe de déplacement

        Args:
            axe (int): Axe de déplacement
        """
        self.axeDeplacement = axe
        
    def modificationPos(self, position: Vecteur) -> None:
        """Définit l'origine du carré et le deplace

        Args:
            position (Vecteur): Nouvelle position du carré
        """
        self.origine = position
        return super().translateTo(position)

    

class RectangleBleu(Rectangle):
    """Cette classe représente les rectangles bleus dans le jeu (Hérite de Rectangle de c31Geometry2)

        Attributes:
            origine(Vecteur): position du rectangle
            hauteur(int): taille de la hauteur du rectangle
            largeur(int): taille de la largeur du rectangle
            axeDeplacement(int) : direction du mouvement du rectangle
            vitesse(int) = vitesse de déplacement du rectangle
    """    

    def __init__(self, vitesse, rectangleChiffre, canvas):
        """Permet de definir un rectangle bleu

            Initialise origine, vitesse, axeDeplacement, largeur et hauteur

            Args: 
                canvas (tk.Canvas): canvas où l'on dessine le rectangle
                rectangleChiffre(int): chiffre pour identifier quel rectangle on crée afin de donner les bonnes tailles et positions de départ
                vitesse(int): vitesse initiale du rectangle
        """
        self.vitesse = vitesse
        self.axeDeplacement = random.randint(0, 3)
        if rectangleChiffre == 1: #Rectangle superieur gauche
            self.largeur = 60
            self.hauteur = 60
            super().__init__(canvas, Vecteur(100,100),self.largeur ,self.hauteur, 0, "blue", "blue", 1)

        elif rectangleChiffre == 2:  #Rectangle superieur droit
            self.largeur = 60
            self.hauteur = 50
            super().__init__(canvas, Vecteur(300,85),self.largeur ,self.hauteur, 0, "blue", "blue", 1)


        elif rectangleChiffre == 3: #Rectangle inferieur gauche
            self.largeur = 30
            self.hauteur = 60
            super().__init__(canvas, Vecteur(85,300),self.largeur ,self.hauteur, 0, "blue", "blue", 1)


        elif rectangleChiffre == 4: #Rectangle inferieur droit
            self.largeur = 100
            self.hauteur = 20
            super().__init__(canvas, Vecteur(355,340),self.largeur ,self.hauteur, 0, "blue", "blue", 1)       
 
    def getAxe(self):
        """Permet de récupérer l'axe de déplacement

        Returns:
            int: direction du mouvement
        """
        return self.axeDeplacement

    def getOrigine(self) -> Vecteur:
        """Permet de récupérer l'origine

        Returns:
            Vecteur: Origine du rectangle
        """
        return super().get_origine()

    def getHauteur(self):
        """Permet de récupérer la hauteur

        Returns:
            int: la hauteur du rectangle
        """
        return self.hauteur

    def getLargeur(self):
        """Permet de récupérer la largeur

        Returns:
            int: largeur du rectangle
        """
        return self.largeur

    def getVitesse(self):
        """Permet de récupérer a vitesse de déplacement

        Returns:
            int: vitesse de déplacement du rectangle
        """
        return self.vitesse
 
    def setVitesse(self, vitesse):
        """Définit la vitesse de déplacement

        Args:
            vitesse (int): vitesse de déplacement
        """
        self.vitesse = vitesse 

    def setAxe(self, axe):
        """Définit l'axe de déplacement

        Args:
            axe (int): Axe de déplacement
        """
        self.axeDeplacement = axe
        
    def modificationPos(self, position: Vecteur) -> None:
        """Définit l'origine du rectangle et le deplace

        Args:
            position (Vecteur): Nouvelle position du rectangle
        """
        self.origine = position
        return super().translateTo(position)


class BordureNoire(Rectangle):
    """Cette représente la bordure noire de l'aire de jeu (Hérite de Rectangle de c31Geometry2)

        Attributes:
            origine(Vecteur): position du rectangle
            hauteur(int): taille de la hauteur du rectangle
            largeur(int): taille de la largeur du rectangle
    """    

    def __init__(self, x, y, canvas):
        """Permet de definir la bordure noire

            Initialise origine, largeur et hauteur

            Args: 
                canvas (tk.Canvas): canvas où l'on dessine le rectangle
                x(int): x en pixel de la bordure 
                y(int): x en pixel de la bordure
        """
        self.largeur = 450
        self.hauteur = 540
        super().__init__(canvas, Vecteur(x,y), self.largeur, self.hauteur, 0, "black", "black", 0)

    def getHauteur(self):
        """Permet de récupérer la hauteur

        Returns:
            int: la hauteur de la bordure noire
        """
        return self.hauteur

    def getLargeur(self):
        """Permet de récupérer la largeur

        Returns:
            int: largeur de la bordure noire
        """
        return self.largeur

    def getOrigine(self) -> Vecteur:
        """Permet de récupérer l'origine

        Returns:
            Vecteur: Origine  de la bordure noire
        """
        return super().get_origine()

class ZoneBlanche(Rectangle):
    """Cette classe représente la zone blanche de l'aire de jeu (Hérite de Rectangle de c31Geometry2)

        Attributes:
            origine(Vecteur): position du rectangle
            hauteur(int): taille de la hauteur du rectangle
            largeur(int): taille de la largeur du rectangle
    """    

    def __init__(self, x, y, canvas):
        """Permet de definir la bordure noire

            Initialise origine, largeur et hauteur

            Args: 
                canvas (tk.Canvas): canvas où l'on dessine le rectangle
                x(int): x en pixel de la bordure 
                y(int): x en pixel de la bordure
        """
        self.largeur = 400
        self.hauteur = 490
        super().__init__(canvas, Vecteur(x,y), self.largeur, self.hauteur, 0, "white", "white", 0)

    def getHauteur(self):
        """Permet de récupérer la hauteur

        Returns:
            int: la hauteur de la zone blanche
        """
        return self.hauteur

    def getLargeur(self):
        """Permet de récupérer la largeur

        Returns:
            int: largeur de la zone blanche
        """
        return self.largeur
    
    def getOrigine(self) -> Vecteur:
        """Permet de récupérer l'origine

        Returns:
            Vecteur: Origine de la zone blanche
        """
        return super().get_origine()

class Session():
    """Cette classe représente une session de jeu

        Attributes:
                nomJoueur(string): nom du joueur
                difficulte(string): niveau de difficulté
                parties(Partie): tableau des differentes parties jouées dans cette session
    """    

    def __init__(self, nom, difficulte):
        """Permet de definir la session

            Initialise nomJoueur, difficulte et parties

            Args: 
                nomJoueur(string): nom du joueur pour cette session
                difficulte(string): niveau de difficulté pour cette session
        """
        self.nomJoueur = nom
        self.difficulte = difficulte
        self.parties = []

    def sauverScore(self):
        """Permet d'ajouter les informations de cette session dans le fichier csv
        """
        with open('FichierScores.csv', 'a') as csvFile :
            ecriture_score = csv.writer(csvFile, delimiter=',')
            for i in range(0, len(self.parties)):
                ecriture_score.writerow(str(self.nomJoueur) + ", " + str(self.parties[i].getTemps) + ", " + str(self.difficulte))       

    def ajouterPartie(self, partie):
        """Permet d'ajouter une partie completée à la session

        Args:
            partie (Parite): partie qui vient d'être terminée
        """
        self.parties.append(partie)

    def getNom(self):
        """Permet de récupérer nom du joueur cette session

        Returns:
            string: nom du joueur
        """
        return self.nomJoueur

    def getDif(self):
        """Permet de récupérer le niveau de difficulté cette session

        Returns:
            string: niveau de difficulté 
        """
        return self.difficulte 

class Partie():
    """Cette classe représente une partie dans le jeu

        Attributes:
            tempsDebut(double): temps quand le minuteur commence
    """    
    def __init__(self):
        """Permet de definir la partie

            Initialise tempsDebut
        """
        self.tempsDebut = time.time()

    def getTemps(self):
        """Permet de récupérer le temps actuel de la minuterie

        Returns:
            double: temps passé depuis début de la partie
        """
        return round((time.time() - self.tempsDebut), 2)

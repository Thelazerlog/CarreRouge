# -*- coding: utf8 -*-
import random
from c31Geometry2 import *

class CarreRouge(Carre):
    def __init__(self, canvas):
        self.axeDeplacement = random.randint(0, 3)
        self.arrete = 40
        super().__init__(canvas, Vecteur(225, 225), self.arrete, self.axeDeplacement , "red", "red", 0)


    def getOrigine(self) -> Vecteur:
        return super().get_origine()

    def getArrete(self):
        return self.arrete
    
    def getAxe(self):
        return self.axeDeplacement

    def setAxe(self, axe):
        self.axeDeplacement = axe
        
    def getPosition(self):
        return  super().get_origine().x + "x"  + super().get_origine().y

    def modificationPos(self, position: Vecteur) -> None:
        self.origine = position
        return super().translateTo(position)

    

class RectangleBleu(Rectangle):
    def __init__(self, vitesse, rectangleChiffre, canvas):
        self.vitesse = vitesse
        self.axeDeplacement = random.randint(0, 3)
        if rectangleChiffre == 1: #Rectangle superieur gauche
            self.largeur = 60
            self.hauteur = 60
            super().__init__(canvas, Vecteur(100,100),self.largeur ,self.hauteur, self.axeDeplacement, "blue", "blue", 1)

        elif rectangleChiffre == 2:  #Rectangle superieur droit
            self.largeur = 60
            self.hauteur = 50
            super().__init__(canvas, Vecteur(300,85),self.largeur ,self.hauteur, self.axeDeplacement, "blue", "blue", 1)


        elif rectangleChiffre == 3: #Rectangle inferieur gauche
            self.largeur = 30
            self.hauteur = 60
            super().__init__(canvas, Vecteur(85,300),self.largeur ,self.hauteur, self.axeDeplacement, "blue", "blue", 1)


        elif rectangleChiffre == 4: #Rectangle inferieur droit
            self.largeur = 100
            self.hauteur = 20
            super().__init__(canvas, Vecteur(355,340),self.largeur ,self.hauteur, self.axeDeplacement, "blue", "blue", 1)       
 
    def getAxe(self):
        return self.axeDeplacement

    def getOrigine(self) -> Vecteur:
        return super().get_origine()

    def getHauteur(self):
        return self.hauteur

    def getLargeur(self):
        return self.largeur

    def getVitesse(self):
        return self.vitesse
 
    def setVitesse(self, vitesse):
        self.vitesse = vitesse 

    def setAxe(self, axe):
        self.axeDeplacement = axe
        
    def getPosition(self):
        return  super().get_origine().x + "x"  + super().get_origine().y

    def translateTo(self, position: Vecteur) -> None:
        return super().translateTo(position)


class BordureNoire(Rectangle):
    def __init__(self, x, y, canvas):
        self.largeur = 450
        self.hauteur = 540
        super().__init__(canvas, Vecteur(x,y), self.largeur, self.hauteur, 0, "black", "black", 0)

    def getHauteur(self):
        return self.hauteur

    def getLargeur(self):
        return self.largeur

    def getOrigine(self) -> Vecteur:
        return super().get_origine()

class ZoneBlanche(Rectangle):
    def __init__(self, x, y, canvas):
        self.largeur = 400
        self.hauteur = 490
        super().__init__(canvas, Vecteur(x,y), self.largeur, self.hauteur, 0, "white", "white", 0)

    def getHauteur(self):
        return self.hauteur

    def getLargeur(self):
        return self.largeur
    
    def getOrigine(self) -> Vecteur:
        return super().get_origine()
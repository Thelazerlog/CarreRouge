# -*- coding: utf8 -*-
from c31Geometry2 import *

class CarreRouge(Polygone):
    def __init__(self, axe, canvas):
        super().__init__(canvas, Vecteur(self.x, self.y), "red", "red", 0)
        self.axeDeplacement = axe
        self.arrete = 40
        self.x = 225
        self.y = 225

    def getX(self):
        return self.x
    def getY(self):
        return self.y

    def getArrete(self):
        return self.arrete
    
    def getAxe(self):
        return self.axeDeplacement

    def setPosition(self, x, y):
        self.x = x
        self.y = y
    
    def setAxe(self, axe):
        self.axeDeplacement = axe
        
    def getPosition(self):
        return str(self.getX()) + "x" + str(self.getY())

class RectangleBleu(Polygone):
    def __init__(self, vitesse, rectangleChiffre, axe, canvas):
        if rectangleChiffre == 1: #Rectangle superieur gauche
            self.largeur = 60
            self.hauteur = 60

        elif rectangleChiffre == 2:  #Rectangle superieur droit
            self.largeur = 60
            self.hauteur = 50

        elif rectangleChiffre == 3: #Rectangle inferieur gauche
            self.largeur = 30
            self.hauteur = 60

        elif rectangleChiffre == 4: #Rectangle inferieur droit
            self.largeur = 100
            self.hauteur = 20

        if rectangleChiffre == 1: #Rectangle superieur gauche
            self.x = 100
            self.y = 100
        elif rectangleChiffre == 2:  #Rectangle superieur droit
            self.x = 300
            self.y = 85

        elif rectangleChiffre == 3: #Rectangle inferieur gauche
            self.x = 85
            self.y = 300

        elif rectangleChiffre == 4: #Rectangle inferieur droit
            self.x = 355
            self.y = 340

        self.vitesse = vitesse
        self.axeDeplacement = axe
        
        super().__init__(canvas, Vecteur(self.x,self.y), "blue", "blue", 1)

 
    def getAxe(self):
        return self.axeDeplacement

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getHauteur(self):
        return self.hauteur

    def getLargeur(self):
        return self.largeur

    def getVitesse(self):
        return self.vitesse

    def setPosition(self, x, y):
        self.x = x  
        self.y = y
 
    def setVitesse(self, vitesse):
        self.vitesse = vitesse 

    def setAxe(self, axe):
        self.axeDeplacement = axe
        
    def getPosition(self):
        return str(self.x) + "x" + str(self.y)


class BordureNoire(Polygone):
    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y
        self.largeur = 450
        self.hauteur = 540
        super().__init__(canvas, Vecteur(self.x,self.y), "black", "black", 0)


    def getHauteur(self):
        return self.hauteur

    def getLargeur(self):
        return self.largeur

    def getX(self):
        return self.x

    def getY(self):
        return self.y

class ZoneBlanche(Polygone):
    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y
        self.largeur = 400
        self.hauteur = 490
        super().__init__(canvas, Vecteur(self.x,self.y), "white", "white", 0)


    def getHauteur(self):
        return self.hauteur

    def getLargeur(self):
        return self.largeur
    
    def getX(self):
        return self.x

    def getY(self):
        return self.y

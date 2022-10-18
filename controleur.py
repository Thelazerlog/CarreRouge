from vue import JeuVue, MenuVue
from modeles import BordureNoire, ZoneBlanche, CarreRouge, RectangleBleu
import csv
import time
import random
from c31Geometry2 import *
from functools import partial

class MenuControleur:
    def __init__(self, root, fermerJeu, jeuControleur) :
        self.jeuControleur = jeuControleur
        self.vue = MenuVue(root, self.nouvellePartie(), fermerJeu)
        #nom = self.vue.demanderNom(root)
        #self.vue.setNom(nom)

    def debuter(self) :
        self.vue.draw()                        
    
    def nouvellePartie(self) :
        if self.jeuControleur.demarrerPartie() :
            root = self.jeuControleur.vue.root
            vue = self.jeuControleur.vue
            self.jeuControleur.vue.destroy()     ##### A voir avec l'equipe : le destroy()
            self.jeuControleur = JeuControleur(root, vue)
        
        self.jeuControleur.debuter()
        self.jeuControleur.nouvellePartie = self.nouvellePartie

    def quitter(self) :
       self.root.destroy()


class JeuControleur :
    tempsDebut = 0
    tempsFin = 0
    def __init__(self, root) :
        self.partieDemarree = False
        self.nouvellePartie = lambda : print("Nouvelle partie")    
        self.vue = JeuVue(root)
        self.bordureNoire = BordureNoire(0, 0, self.vue.canvas, Vecteur(0, 0), "black", "black", 0)  
        self.zoneBlanche = ZoneBlanche(75, 75, self.vue.canvas, Vecteur(0, 0), "white", "white", 0) 
        self.carreRouge = CarreRouge(0, self.vue.canvas, Vecteur(225, 225), "red", "red", 0)
        self.vecteurC = Vecteur(self.carreRouge.getX(), self.carreRouge.getY())
        self.nom = self.vue.demanderNom(root)
        self.vue.setNom(self.nom)
        self.difficulte = self.vue.demanderDif(root)
        self.vue.setDif(self.difficulte)

        self.rectangleBleu = []
        for i in range(0, 4) :
            self.rectangleBleu.append(RectangleBleu(1, i+1, 0, self.vue.canvas, "blue", "blue", 10))   # on place les rectangles bleus
            self.vecteurR = Vecteur(self.rectangleBleu[i].getX(), self.rectangleBleu[i].getY())
            self.vue.addRectangle(self.vecteurR, self.rectangleBleu[i].getLargeur(), self.rectangleBleu[i].getHauteur(),0, "blue", "blue", 1)
        self.vue.addCarre(self.vecteurC, self.carreRouge.getArrete(),0, "red", "red", 0)
        #self.__defineEvent()
        
    def demarrerPartie(self) :
        return self.partieDemarree

    def __defineEvent(self) :
        self.vue.setListen("<ButtonPress-1>", self.evenement())

    def evenement(self) :
        self.deplacementCarreRouge()
        self.deplacementRectangleBleu()

    def debuter(self) :
        self.partieDemarree = True
        self.vue.draw()
        self.tempsDebut = time.time()
        
    
    def verifierCollision(self) :
        # On recupere la position du carré rouge
        carreRougePosition = self.carreRouge.getPosition()
        # On recupere les positions des rectangles blues
        for i in range(0, 4) :
            rectangleBleuPosition = self.rectangleBleu[i].getPosition()
            if carreRougePosition == rectangleBleuPosition :
                self.vue.messageBox("Vous avez survécu : " + self.minuteur() + " secondes!")
                self.tempsFin = time.time()
                return True
            else :
                continue
        return False
    
    def minuteur(self) :
        sec = self.tempsFin - self.tempsDebut
        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        total = "{0}:{1}:{2}".format(int(hours),int(mins),sec)
        return total
    
    def ecrireScore(self) :
        score = self.minuteur()
        self.fileData = [self.nomJoueur, self.niveau, self.difficulte, score]                           ###### Les classes Session et Partie sont supposé etre dans modele
        with open('FichierScores.csv', 'w') as csvFile :
            ecriture_score = csv.writer(csvFile, delimiter=',')
            ecriture_score.writerow(self.fileData)
    
    def lireScore(self) :
        with open('FichierScores.csv', 'r') as csvFile :
            lecteur_score = csv.reader(csvFile, delimiter=',')
            self.dataList = [[]]
            self.dataRead = []
            cpt = 0

            for row in lecteur_score :
                self.dataRead.append(row)
                cpt += 1
                if cpt % 4 == 0 :
                    self.dataList.append(self.dataRead)
                    self.dataRead = []
    '''
    def trier(self) :                                       ###### pas sur du fonctionnement de cette fonction! demander a isi
        for i in range(0, len(self.dataList) - 1) :
            max = i
            for j in range(i, len(self.dataList)) :
                if self.dataList[j][3] >= self.dataList[max][3] :
                    max = j
            temp = self.dataList[i]
            self.dataList[i] = self.dataList[max]
            self.dataList[max] = temp
    '''
    
    def deplacementRectangleBleu(self) :
        for i in range(0, 4) :
            positionInit = self.rectangleBleu[i].getPosition() # renvoie une string de format : "100x45", "35x550"
            positionInit = positionInit.split("x") # séparation de la string, puis attribution des valeurs à la position en x et en y
            x = positionInit[0]
            y = positionInit[1]

            '''
            deplacement : 
                axeDeplacement :
                    0 = nord-ouest
                    1 = nord-est
                    2 = sud-est
                    3 = sud-ouest
                    4 = ... fonctionnalités futures
            '''
    
            self.rectangleBleu[i].setAxe(random.randint(0, 3))
            if self.verifierCollision() == False :                                                
                if(self.rectangleBleu[i].getAxe() == 0) :
                    x -= 1
                    y -= 1
                elif(self.rectangleBleu[i].getAxe() == 1) :
                    x += 1
                    y -= 1
                elif(self.rectangleBleu[i].getAxe() == 2) :
                    x += 1
                    y += 1
                elif(self.rectangleBleu[i].getAxe() == 3) :
                    x -= 1
                    y += 1
            else :
                if(self.rectangleBleu[i].getPosition() == "0x0") : #coin nord-ouest
                    self.rectangleBleu[i].setAxe(2)
                if(self.rectangleBleu[i].getPosition() == "400x0") : #coin nord-est
                    self.rectangleBleu[i].setAxe(3)       
                if(self.rectangleBleu[i].getPosition() == "400x490") : #coin sud-est
                    self.rectangleBleu[i].setAxe(0)
                if(self.rectangleBleu[i].getPosition() == "0x490") : #coin sud-ouest
                    self.rectangleBleu[i].setAxe(1)
                
                position = self.rectangleBleu[i].getPosition()
                position = position.split("x")
                x = position[0]
                y = position[1]
                currentAxeDeplacement = self.rectangleBleu[i].getAxe()
                if y == 0 : #bordure du haut mais pas les coins             
                    if(currentAxeDeplacement == 0):
                        self.rectangleBleu[i].setAxe(3) #si vers nord-ouest, rebondi vers sud-ouest      
                    else :
                        self.rectangleBleu[i].setAxe(2) #si vers nord-est, rebondi vers sud-est
                if(y == 490) : #bordure du bas
                    if(currentAxeDeplacement == 2) :
                        self.rectangleBleu[i].setAxe(1) #si vers sud-est, rebondi vers nord-est
                    else :
                        self.rectangleBleu[i].setAxe(0) #si vers sud-ouest, rebondi vers nord-ouest
                if(x == 0) : #bordure de gauche
                    if(currentAxeDeplacement == 0) :
                        self.rectangleBleu[i].setAxe(1) #si vers nord-ouest, rebondi vers nord-est
                    else :
                        self.rectangleBleu[i].setAxe(2) #si vers sud-ouest, rebondi vers sud-est
                if(x == 400) : #bordure de droite
                    if(currentAxeDeplacement == 1) :
                        self.rectangleBleu.setAxe(0) #si vers nord-est, rebondi vers nord-ouest
                    else :
                        self.rectangleBleu.setAxe(3) #si vers sud-est, rebondi vers sud-ouest

            newPosition = x + "x" + y # reconstruction d'une string de format "99x44", "34x549" 
            deplacement = Vecteur(x, y)                                                          
            #RectangleBleu.translate(deplacement) # effectue une translation de 1 pixel en diagonal    
            self.rectangleBleu[i].setPosition(Polygone.translate(deplacement))                                             
            self.rectangleBleu[i].setPosition(newPosition)       
                                            
    def deplacementCarreRouge(self) : 
        posX = self.vue.root.winfo_pointerx #recoit position du curseur             
        posY = self.vue.root.winfo_pointery
        deplacement = Vecteur(posX, posY) 
        x = str(posX)  # transforme les int en string 
        y = str(posY)
        newPosition = x + "x" + y # construit une string position
        self.carreRouge.translate(deplacement) # TODO : pas sur de ce qui se passe ici
        self.carreRouge.setPosition(posX, posY)
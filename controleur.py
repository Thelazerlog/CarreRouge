from vue import JeuVue, MenuVue
from modeles import BordureNoire, ZoneBlanche, CarreRouge, RectangleBleu
import csv
import time
import random
from c31Geometry2 import *
from functools import partial

class MenuControleur:
    def __init__(self, root, jeuControleur) :
        self.jeuControleur = jeuControleur
        self.vue = MenuVue(root, self.nouvellePartie(), self.lireScore() ,self.quitter())
        #nom = self.vue.demanderNom(root)
        #self.vue.setNom(nom)

    def debuter(self) :
        self.vue.draw()                        
    
    def nouvellePartie(self) :
        if self.jeuControleur.demarrerPartie() :
            root = self.jeuControleur.vue.root
            self.jeuControleur.vue.destroy()  
            self.jeuControleur = JeuControleur(root)
        self.jeuControleur.debuter()
        #self.jeuControleur.nouvellePartie = self.nouvellePartie

    def quitter(self) :
       #self.jeuControleur.vue.destroy()
       test= 1

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


class JeuControleur :
    def __init__(self, root) :
        self.partieDemarree = False
        self.nouvellePartie = lambda : print("Nouvelle partie")    
        self.vue = JeuVue(root)
        self.carreRouge = CarreRouge(self.vue.canvas)
        self.bordureNoire = BordureNoire(0, 0, self.vue.canvas) 
        self.zoneBlanche = ZoneBlanche(75, 75, self.vue.canvas) 
        self.nom = self.vue.demanderNom(root)
        self.vue.setNom(self.nom)
        self.difficulte = self.vue.demanderDif(root)
        self.vue.setDif(self.difficulte)
        self.rectangleBleu = []
        self.itemCollection = []
        for i in range(0, 4) :
            self.rectangleBleu.append(RectangleBleu(1,i+1, self.vue.canvas))
        self.__defineEvent()
        
    def demarrerPartie(self) :
        return self.partieDemarree
    

    def __defineEvent(self) :    
        self.vue.setListen("<ButtonPress-1>", self.evenement)

    def evenement(self, event) :
        tempsDebut = time.time()
        i = 0
        while event:
            #self.deplacementCarreRouge()
            self.deplacementRectangleBleu()
            i += 1
            if i == 15000:
                break
        tempsFin = time.time()
        self.minuteur(tempsFin - tempsDebut)
        temps = tempsFin - tempsDebut
        self.ecrireScore("{:.2f}".format(temps))
        self.vue.setTimer("{:.2f}".format(temps))  # Pour afficher 2 chiffres après la virgule

    def debuter(self) :
        self.partieDemarree = True
        self.vue.draw(self.rectangleBleu)
        self.vue.drawCarre(self.carreRouge)
        #self.tempsDebut = time.time()
        
    
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
    
    def minuteur(self, sec) :
        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        self.vue.setTimer("{0}:{1}:{2}".format(int(hours),int(mins),sec))
    
    def ecrireScore(self, score) :
        self.fileData = [self.nom, self.difficulte, score]
        with open('FichierScores.csv', 'w') as csvFile :
            ecriture_score = csv.writer(csvFile, delimiter=',')
            ecriture_score.writerow(self.fileData)
    

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
            x = self.rectangleBleu[i].getOrigine().x
            y = self.rectangleBleu[i].getOrigine().y
            '''
            deplacement : 
                axeDeplacement :
                    0 = nord-ouest
                    1 = nord-est
                    2 = sud-est
                    3 = sud-ouest
                    4 = ... fonctionnalités futures
            '''
            
            # DÉTECTION DE COLLISIONS LATÉRALES 
            if x >= 75 and x <= 85 : #collision bordure gauche (axes de directions ouest deviennent de direction est)
                if self.rectangleBleu[i].getAxe() == 0 :
                    self.rectangleBleu[i].setAxe(1)
                else : 
                    self.rectangleBleu[i].setAxe(2)
            if x >= 465 and x <= 490 : #collision bordure droite (axes de directions est deviennent de direction ouest)
                if self.rectangleBleu[i].getAxe() == 1 :
                    self.rectangleBleu[i].setAxe(0)
                else :
                    self.rectangleBleu[i].setAxe(3)
            if y >= 88 and y <= 96 : #collision bordure haut (axes de directions nord deviennent de direction sud)
                if self.rectangleBleu[i].getAxe() == 1 :
                    self.rectangleBleu[i].setAxe(2)
                else :
                    self.rectangleBleu[i].setAxe(3)
            if y >= 465 and y <= 475 : #collision bordure bas (axes de directions sud deviennent de direction nord)
                if self.rectangleBleu[i].getAxe() == 2 :
                    self.rectangleBleu[i].setAxe(1)
                else :
                    self.rectangleBleu[i].setAxe(0)
            
            # DÉTECTION DE COLLISIONS DANS LES COINS
            """" 
            if(self.rectangleBleu[i].getPosition() == "80x80") : #coin nord-ouest
                    self.rectangleBleu[i].setAxe(2)
            if(self.rectangleBleu[i].getPosition() == "400x0") : #coin nord-est
                    self.rectangleBleu[i].setAxe(3)       
            if(self.rectangleBleu[i].getPosition() == "400x490") : #coin sud-est
                    self.rectangleBleu[i].setAxe(0)
            if(self.rectangleBleu[i].getPosition() == "0x490") : #coin sud-ouest
                    self.rectangleBleu[i].setAxe(1)
            """
            # DÉPLACEMENT LOGIQUE
            if self.rectangleBleu[i].getAxe() == 0 :
                    x -= 0.2
                    y -= 0.2
            elif self.rectangleBleu[i].getAxe() == 1 :
                    x += 0.2
                    y -= 0.2
            elif self.rectangleBleu[i].getAxe() == 2 :
                    x += 0.2
                    y += 0.2
            elif self.rectangleBleu[i].getAxe() == 3 :
                    x -= 0.2
                    y += 0.2

            # AFFECTATIONS MODÈLES & VUE
            deplacement = Vecteur(x, y)
            self.rectangleBleu[i].translateTo(deplacement)
            self.rectangleBleu[i].modificationPos(deplacement)
        self.vue.draw(self.rectangleBleu)
                                                                             
                                            
    def deplacementCarreRouge(self) : 
        posX = self.vue.root.winfo_pointerx #recoit position du curseur             
        posY = self.vue.root.winfo_pointery
        deplacement = Vecteur(posX, posY) 
        self.carreRouge.translateTo(deplacement)

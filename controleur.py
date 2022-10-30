from vue import JeuVue, MenuVue
from modeles import BordureNoire, CanvasJeu, Partie, Session, ZoneBlanche, CarreRouge, RectangleBleu
import csv
import time
from c31Geometry2 import *

class MenuControleur:
    def __init__(self, root, jeuControleur):
        self.jeuControleur = jeuControleur
        self.vue = MenuVue(root, self.nouvellePartie, self.lireScore, self.quitter)

    def debuter(self):
        self.vue.draw()                        
    
    def nouvellePartie(self):
        if self.jeuControleur.demarrerPartie():
            root = self.jeuControleur.vue.root
            self.jeuControleur.vue.destroy()  
            self.jeuControleur = JeuControleur(root)
        self.jeuControleur.debuter()

    def quitter(self):
        self.jeuControleur.vue.destroy()

    def lireScore(self):
        with open('FichierScores.csv', 'r') as csvFile:
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

class JeuControleur:
    def __init__(self, root):
        self.partieDemarree = False
        self.nouvellePartie = lambda : print("Nouvelle partie")    
        self.vue = JeuVue(root)
        self.canvasJeu = CanvasJeu(root)
        self.carreRouge = CarreRouge(self.canvasJeu.canvas)
        self.bordureNoire = BordureNoire(0, 0, self.canvasJeu.canvas) 
        self.zoneBlanche = ZoneBlanche(75, 75, self.canvasJeu.canvas) 
        self.partie = Partie()
        self.session = Session(self.vue.demanderNom(root), self.vue.demanderDif(root))
        self.vue.setNom(self.session.getNom())
        self.vue.setDif(self.session.getDif())
        self.rectangleBleu = []
        self.itemCollection = []
        for i in range(0, 4):
            self.rectangleBleu.append(RectangleBleu(1,i+1, self.canvasJeu.canvas))
        self.debuter()
        self.__defineEvent()
        
    def demarrerPartie(self):
        return self.partieDemarree

    def __defineEvent(self):
        self.vue.setListen("<ButtonPress-1>", self.evenement)

    def evenement(self, event):
        self.vue.setListen("<Motion>", self.evenement)
        self.roulerJeu(event.x, event.y)
        if self.verifierCollision():
            #tempsFin = time.time()
            #self.minuteur(tempsFin - self.partie.getTemps())
            #temps = tempsFin - self.partie.getTemps()
            self.session.sauverScore()
            #self.vue.setTimer("{:.2f}".format(temps))  # Pour afficher 2 chiffres après la virgule

    def debuter(self) :
        self.partieDemarree = True
        self.vue.draw(self.rectangleBleu)
        self.vue.drawCarre(self.carreRouge)

    def roulerJeu(self, x, y):
        self.deplacementRectangleBleu()
        self.deplacementCarreRouge(x, y)
        self.vue.setTimer(self.partie.getTemps())
        self.verifierCollision()

    def verifierCollision(self) :
        # On recupere la position du carré rouge
        carreX = self.carreRouge.get_origine().x
        carreY = self.carreRouge.get_origine().y

        # Détéction de collision avec la bordure noire
        if carreX >= 75 and carreX <= 85:
            return True
        elif carreX >= 465 and carreX <= 490:
            return True
        elif carreY >= 88 and carreY <= 96:
            return True
        elif carreY >= 465 and carreY <= 475:
            return True
        else:
            for i in range(0, 4):
                rectangleX = self.rectangleBleu[i].getOrigine().x
                rectangleY = self.rectangleBleu[i].getOrigine().y
                for j in range(0, 10):
                    rectangleX += j
                    rectangleY += j
                    if (carreX == rectangleX or carreX == rectangleX) or (carreY == rectangleY or carreY == rectangleY) :
                        return True
                    else:
                        continue
            return False
    
    #def minuteur(self, sec):
        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        self.vue.setTimer("{0}:{1}:{2}".format(int(hours), int(mins), sec))
    
    #def ecrireScore(self, score):
        self.fileData = [self.nom, self.difficulte, score]
        with open('FichierScores.csv', 'a') as csvFile :
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
                if self.rectangleBleu[i].getAxe() == 0:
                    self.rectangleBleu[i].setAxe(1)
                else : 
                    self.rectangleBleu[i].setAxe(2)
            if x >= 465 and x <= 490 : #collision bordure droite (axes de directions est deviennent de direction ouest)
                if self.rectangleBleu[i].getAxe() == 1:
                    self.rectangleBleu[i].setAxe(0)
                else :
                    self.rectangleBleu[i].setAxe(3)
            if y >= 70 and y <= 80 : #collision bordure haut (axes de directions nord deviennent de direction sud)
                if self.rectangleBleu[i].getAxe() == 1:
                    self.rectangleBleu[i].setAxe(2)
                else :
                    self.rectangleBleu[i].setAxe(3)
            if y >= 465 and y <= 475 : #collision bordure bas (axes de directions sud deviennent de direction nord)
                if self.rectangleBleu[i].getAxe() == 2:
                    self.rectangleBleu[i].setAxe(1)
                else :
                    self.rectangleBleu[i].setAxe(0)

            # DÉPLACEMENT LOGIQUE
            if self.rectangleBleu[i].getAxe() == 0:
                x -= 0.2
                y -= 0.2
            elif self.rectangleBleu[i].getAxe() == 1:
                x += 0.2
                y -= 0.2
            elif self.rectangleBleu[i].getAxe() == 2:
                x += 0.2
                y += 0.2
            elif self.rectangleBleu[i].getAxe() == 3:
                x -= 0.2
                y += 0.2

            # AFFECTATIONS MODÈLES & VUE
            deplacement = Vecteur(x, y)
            self.rectangleBleu[i].translateTo(deplacement)
            self.rectangleBleu[i].modificationPos(deplacement)
        self.vue.draw(self.rectangleBleu)
                                            
    def deplacementCarreRouge(self, x, y):
        deplacement = Vecteur(x, y) 
        self.carreRouge.translateTo(deplacement)
        self.carreRouge.modificationPos(deplacement)
        self.vue.drawCarre(self.carreRouge)

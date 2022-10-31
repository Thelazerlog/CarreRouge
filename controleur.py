from vue import JeuVue, MenuVue
from modeles import BordureNoire, ZoneBlanche, CarreRouge, RectangleBleu
import csv
import time
from c31Geometry2 import *

class MenuControleur:
    def __init__(self, root, jeuControleur):
        self.jeuControleur = jeuControleur
        self.vue = MenuVue(root, self.nouvellePartie, self.lireScore, self.quitter)

    def debuter(self) :
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
        self.isMoving = False
        self.isPressed = False
        self.vitesse = 1
        self.carreRouge.vertices = []
        for i in range(0, 4):
            self.rectangleBleu.append(RectangleBleu(1,i+1, self.vue.canvas))
        self.__defineEvent()
        
        
        
    def demarrerPartie(self):
        return self.partieDemarree

    def __defineEvent(self):
        self.vue.setListen("<B1-Motion>", self.buttonPressed)
        self.vue.setListen("<ButtonRelease-1>", self.buttonReleased())

    def buttonPressed(self, event) : 
        self.isPressed = True
        self.x = event.x
        self.y = event.y
        if not self.partieDemarree :
            self.debuter()

    def buttonReleased(self) :
        self.isPressed = False


    def evenement(self):
        self.isMoving = True
        self.tempsDebut = time.time()
        self.roulerJeu()

    def debuter(self) :
        self.partieDemarree = True
        self.vue.draw(self.rectangleBleu)
        self.vue.drawCarre(self.carreRouge)
        self.e = LoopEvent(self.vue.root, self.roulerJeu, 10)
        self.e.start()

    def roulerJeu(self) :
        self.deplacementRectangleBleu()
        if(self.isPressed) :
            self.deplacementCarreRouge(self.x, self.y)
        





    # def arretCarreRouge(self, event) :
    #     self.deplacementCarreRouge(event.x, event.y)
    #     self.isMoving = False

    

    # def roulerJeu(self, x, y):
    #     self.deplacementRectangleBleu()
    #     while (not self.verifierCollision()) :
    #         if(self.isMoving) :
    #             self.deplacementCarreRouge(x, y)
    #             self.verifierCollision()



    # if self.verifierCollision():
    #     tempsFin = time.time()
    #     self.minuteur(tempsFin - self.tempsDebut)
    #     temps = tempsFin - self.tempsDebut
    #     self.ecrireScore("{:.2f}".format(temps))
    #     self.vue.setTimer("{:.2f}".format(temps))  # Pour afficher 2 chiffres après la virgule
    
            
            
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
        else :
            for i in range(0, 4) :
                rectangleX = self.rectangleBleu[i].getOrigine().x
                rectangleY = self.rectangleBleu[i].getOrigine().y
                for j in range(0, 10) :
                    rectangleX += j
                    rectangleY += j
                    if (carreX == rectangleX or carreX == rectangleX) or (carreY == rectangleY or carreY == rectangleY) :
                        return True
                    else :
                        continue
            return False

    def isInside(self) :

        '''
        VERTICES DU POLYGONE : SENS HORAIRE À PARTIR DU COIN SUPÉRIEUR GAUCHE : 
        0 = COIN HAUT-GAUCHE
        1 = COIN HAUT-DROITE
        2 = COIN BAS-DROITE
        3 = COIN BAS-GAUCHE
        '''

        #Génération vertices carré rouge
        for i in range (0, 4) :
            if i == 0 :
                x = self.carreRouge.getOrigine().x - self.carreRouge.getArrete / 2
                y = self.carreRouge.getOrigine().y - self.carreRouge.getArrete / 2
            elif i == 1 :
                x = self.carreRouge.getOrigine().x + self.carreRouge.getArrete / 2
                y = self.carreRouge.getOrigine().y - self.carreRouge.getArrete / 2
            elif i == 2 :
                x = self.carreRouge.getOrigine().x + self.carreRouge.getArrete / 2
                y = self.carreRouge.getOrigine().y + self.carreRouge.getArrete / 2
            elif i == 3 : 
                x = self.carreRouge.getOrigine().x - self.carreRouge.getArrete / 2
                y = self.carreRouge.getOrigine().y + self.carreRouge.getArrete / 2
            self.carreRouge.vertices[i] = Vecteur(x,y)

        #Vérification si 1 vertex du carré rouge est à l'intérieur de chaque rectangle bleu
        for i in range(0, 4) :
            if self.carreRouge.vertice[i].y <= self.rectangleBleu[i].edge[1] and self.carreRouge.vertice[i].x <= self.rectangleBleu[i].edge[1] and self.carreRouge[i].vertice[i].x <= self.rectangleBleu[i].edge[2] and self.carreRouge[i].vertice[i].x >= self.rectangleBleu[i].edge[3] :
                return True

        
    
    def minuteur(self, sec) :
        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        self.vue.setTimer("{0}:{1}:{2}".format(int(hours),int(mins),sec))
    
    def ecrireScore(self, score) :
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
        #if self.tempsDebut > 10 :
         #   self.vitesse = 1.5
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
                x -= 2 * self.vitesse
                y -= 2 * self.vitesse
            elif self.rectangleBleu[i].getAxe() == 1:
                x += 2 * self.vitesse
                y -= 2 * self.vitesse
            elif self.rectangleBleu[i].getAxe() == 2 :
                x += 2 * self.vitesse
                y += 2 * self.vitesse
            elif self.rectangleBleu[i].getAxe() == 3 :
                x -= 2 * self.vitesse
                y += 2 * self.vitesse

            # AFFECTATIONS MODÈLES & VUE
            deplacement = Vecteur(x, y)
            self.rectangleBleu[i].translateTo(deplacement)
            self.rectangleBleu[i].modificationPos(deplacement)
        self.vue.draw(self.rectangleBleu)
                                            
    def deplacementCarreRouge(self, x, y) : 
        deplacement = Vecteur(x, y) 
        self.carreRouge.translateTo(deplacement)
        self.carreRouge.modificationPos(deplacement)
        self.vue.drawCarre(self.carreRouge)
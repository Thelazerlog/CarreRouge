from vue import JeuVue, MenuVue
from modeles import BordureNoire, CanvasJeu, Partie, Session, ZoneBlanche, CarreRouge, RectangleBleu
import csv
from c31Geometry2 import *

class MenuControleur:
    """Cette classe controle le menu du jeu 

    Attributes:
        jeuControleur: le controleur du jeu
        vue: l'affichage du jeu sur l'écran
    """
    def __init__(self, root, jeuControleur):
        """Initialise le menu du jeu

        Param:
            root: la fenêtre tkinter
            jeuControleur: le controleur du jeu
        """
        self.jeuControleur = jeuControleur
        self.vue = MenuVue(root, self.nouvellePartie, self.lireScore, self.quitter)

    def debuter(self):
        """Dessine le menu sur la fenêtre du jeu
        """
        self.vue.draw()                        
    
    def nouvellePartie(self):
        """Permet de créer une nouvelle partie
        """
        if self.jeuControleur.demarrerPartie():
            root = self.jeuControleur.vue.root
            self.jeuControleur.vue.destroy()  
            self.jeuControleur = JeuControleur(root)
        self.jeuControleur.debuter()

    def quitter(self):
        """Ferme la fenêtre du jeu
        """
        self.jeuControleur.vue.destroy(self.jeuControleur.vue.root)

    def lireScore(self):
        """Récupère les données dans le fichier de scores externe
        
        Attributes:
            dataList: la liste de données
            dataRead: 
        """
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
    """Cette classe contrôle la logique du jeu

    Attributes:
        partieDemarree: l'état de la partie
        nouvellePartie: initialiser les paramètre du jeu 
        vue: l'affichage du jeu sur l'écran
        canvasJeu: l'aire du jeu
        carreRouge: les attributs du carré rouge
        bordureNoire: les attributs de la bordure noire
        zoneBlanche: les attributs de la zone blanche
        partie: les attributs de la partie actuelle
        session: les attributs de la session actuelle
        rectangleBleu: les attrbuts des rectangles bleus
        isMoving: dit si le carré rouge est en train de bouger
        isPressed: dit si le bouton de la souris est cliquée 
        vitesse: la vitesse de mouvement des rectangles bleus
        x: la position actuelle des rectangles bleus et du carré rouge sur l'axe X
        y: la position actuelle des rectangles bleus et du carré rouge sur l'axe Y
        e: la loop du jeu
    """
    def __init__(self, root):
        self.partieDemarree = False
        self.nouvellePartie = lambda : print("Nouvelle partie")    
        self.vue = JeuVue(root)
        self.canvasJeu = CanvasJeu(root)
        self.carreRouge = CarreRouge(self.canvasJeu.canvas)
        self.bordureNoire = BordureNoire(0, 0, self.canvasJeu.canvas) 
        self.zoneBlanche = ZoneBlanche(75, 75, self.canvasJeu.canvas) 
        self.session = Session(self.vue.demanderNom(root), self.vue.demanderDif(root))
        self.vue.setNom(self.session.getNom())
        self.vue.setDif(self.session.getDif())
        self.rectangleBleu = []
        self.isMoving = False
        self.isPressed = False
        self.vitesse = int(self.session.getDif())
        for i in range(0, 4):
            self.rectangleBleu.append(RectangleBleu(1,i+1, self.canvasJeu.canvas))
        self.vue.draw(self.rectangleBleu)
        self.vue.drawCarre(self.carreRouge)
        self.__defineEvent()
        
    def demarrerPartie(self):
        '''
        L'état d'une partie de jeu (une partie en cours ou non)
        
        Return: 
            boolean: l'état de la partie
        '''
        return self.partieDemarree

    def __defineEvent(self):
        '''
        Créer des écouteurs d'évenements
        '''
        self.vue.setListen("<B1-Motion>", self.buttonPressed)
        self.vue.setListen("<ButtonRelease-1>", self.buttonReleased())

    def buttonPressed(self, event) : 
        '''
        Action lorsque le bouton est appuyé : récupère position du curseur et démarre partie
        Param : 
            event: évènement du canvas
        '''
        self.isPressed = True
        self.x = event.x
        self.y = event.y
        if not self.partieDemarree :
            self.partie = Partie()
            self.debuter()

    def buttonReleased(self) :
        '''
        Détermine lorsque le boutton a été relâché
        '''
        self.isPressed = False
        
    def debuter(self) :
        '''
        Fait débuter une partie, génère la boucle pour faire rouler le jeu, termine la partie en cas de collision
        '''
        self.partieDemarree = True
        self.e = LoopEvent(self.vue.root, self.roulerJeu, 10)
        self.e.start()
        
             
    def roulerJeu(self) :
        '''
        Actualise le timer, les déplacements des rectangles bleus et le déplacement du carré rouge
        '''
        if not self.verifierCollision() :
            self.vue.setTimer(self.partie.getTemps())
            self.deplacementRectangleBleu()
            if self.isPressed :
                self.deplacementCarreRouge(self.x, self.y)
        else :
            self.terminerPartie()
            
    def terminerPartie(self) :
        self.session.ajouterPartie(self.partie)
            
    def verifierCollision(self) :
        '''
        Vérifie si le carré rouge a eu une collision avec la bordure ou avec un rectangle
        Retourne :
            Si une collision a eu lieu (boolean), true = il y a eu collision
        '''
        # On recupere la position du carré rouge
        carreX = self.carreRouge.getOrigine().x
        carreY = self.carreRouge.getOrigine().y

        # Détéction de collision avec la bordure noire
        if carreX <= 50 + self.carreRouge.getArrete() / 2:
            return True
        elif carreX >= 460 + self.carreRouge.getArrete() / 2:
            return True
        elif carreY <= 50 + self.carreRouge.getArrete() / 2:
            return True
        elif carreY >= 460 + self.carreRouge.getArrete() / 2:
            return True
        elif self.isInside() :
            return True
        else :
            return False

    def isInside(self) :
        '''
        Cette fonction détecte si le carré rouge est situé à l'intérieur d'un rectangle bleu
            VERTICES DU POLYGONE : SENS HORAIRE À PARTIR DU COIN SUPÉRIEUR GAUCHE : 
            0 = COIN HAUT-GAUCHE
            1 = COIN HAUT-DROITE
            2 = COIN BAS-DROITE
            3 = COIN BAS-GAUCHE
        Retourne : si le carré rouge est en collision avec un rectangle bleu (boolean), true = collision entre carré rouge et rectangle bleu
        '''
        self.carreRouge.resetVertices()
        for i in range(0, 4) :
            self.rectangleBleu[i].resetEdge()

        #Vérification si 1 vertex du carré rouge est à l'intérieur de chaque rectangle bleu
        for i in range(0, 4) : #boucle des rectangles
            for j in range (0,4) : #boucle des vertices
                if self.carreRouge.vertices[j].y >= self.rectangleBleu[i].getEdge(0) :
                    if self.carreRouge.vertices[j].x <= self.rectangleBleu[i].getEdge(1) :
                        if self.carreRouge.vertices[j].y <= self.rectangleBleu[i].getEdge(2) :
                            if self.carreRouge.vertices[j].x >= self.rectangleBleu[i].getEdge(3) :
                                return True

    # def ecrireScore(self, score):
    #     self.fileData = [self.nom, self.difficulte, score]
    #     with open('FichierScores.csv', 'a') as csvFile :
    #         ecriture_score = csv.writer(csvFile, delimiter=',')
    #         ecriture_score.writerow(self.fileData)

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
        '''
        Vérifie la position de chaque rectangle bleu et le déplace en conséquence
        le déplacement est représenté par : 
                axeDeplacement :
                    0 = nord-ouest
                    1 = nord-est
                    2 = sud-est
                    3 = sud-ouest
        '''
        for i in range(0, 4) :
            x = self.rectangleBleu[i].getOrigine().x
            y = self.rectangleBleu[i].getOrigine().y
            self.detectionCollisionsLaterales(i, x, y)
            deplacement = self.deplacementLogique(i, x, y)
            
            # AFFECTATIONS MODÈLES & VUE
            self.rectangleBleu[i].translateTo(deplacement)
            self.rectangleBleu[i].modificationPos(deplacement)
        self.vue.draw(self.rectangleBleu)
        
    def detectionCollisionsLaterales(self, i, x, y) : 
        '''
        Détermine s'il y a collision latérale, puis affecte le nouvel axe de déplacement de chaque rectangle bleu en conséquence
        Param :  
            i: index du rectangle dans le tableau des rectangles bleus (int)
            x: position en x de l'origine du rectangle (int)
            y: position en y de l'origine du rectangle (int)
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

    def deplacementLogique(self, i, x, y) : 
        '''
        Effectue les déplacements de l'origine de chaque rectangle bleu
        Param :
            i: index du rectangle dans le tableau des rectangles bleus (int)
            x: position en x de l'origine du rectangle (int)
            y: position en y de l'origine du rectangle (int)
        Retourne : 
            Vecteur représentant la coordonnée d'origine de chaque rectangle (Vecteur)
        '''
        self.vitesse *= 1.0004
        if self.vitesse >= 4.5 :
            self.vitesse = 4.5
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
        return Vecteur(x, y)
                                            
    def deplacementCarreRouge(self, x, y):
        '''
        Déplace le carré rouge aux positions du curseur
        Param :
            x : position en y du curseur (int)
            y : position en y du curseur (int)
        '''
        deplacement = Vecteur(x, y) 
        self.carreRouge.translateTo(deplacement)
        self.carreRouge.modificationPos(deplacement)
        self.vue.drawCarre(self.carreRouge)

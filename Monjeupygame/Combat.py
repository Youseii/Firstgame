import pygame
import pygame as pg
from pygame import *
from pygame.locals import *

pygame.init()

hauteur = 480

largeur = 1200

#Création de la fenetre de jeu avec sa taille
fenetre = pygame.display.set_mode((largeur,hauteur))

#Nom de la fenetre de jeu
pygame.display.set_caption("Little Fighter remix ")

#Les sprites pour chaque cotés du personnage(lorsqu'il se tient de dos, de cotés, ect..)
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'),
             pygame.image.load('R3.png'), pygame.image.load('R4.png'),
             pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'),
             pygame.image.load('R9.png')]

walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'),
            pygame.image.load('L3.png'), pygame.image.load('L4.png'),
            pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'),
            pygame.image.load('L9.png')]

#Fond de la fenetre de jeux
zoneDebut = pygame.image.load('aaa.png')

zonefinal = pygame.image.load('bbb.png') #Changement de zone

#ATTAQUE DU BOSS DRAGON DE FEU-------------------------------------------------
dragon = pygame.image.load("spellsprite.png")
#Affichage du personnage
perso = pygame.image.load('standing.png')

clock = pygame.time.Clock()

phaseAffichage = 1

#Ajout de song
songtoucher = pygame.mixer.Sound("hit.wav")

musique = pygame.mixer.music.load("ost.mp3")
pygame.mixer.music.play(-1)


font = pygame.font.SysFont("comicsans", 100)

fin = pygame.image.load('END.png')
fin2 = pg.transform.scale(fin, (1200, 480))


score = 0 #Pour le score a chaque fois que l'ennemie est touché

#------------------CODE TRANSITION DE ZONE-----------------------

def fondu(largeur, taille): #transition fondu
    fondu = pygame.Surface((largeur, taille))
    fondu.fill((0,0,0))
    for alpha in range(0, 300):
        fondu.set_alpha(alpha)
        fenetre.blit(fondu, (0,0))
        pygame.time.delay(5)
        pygame.display.flip()


#----------------------------CARACTERISTIQUE DU PERSONNAGE--------------------------
#J'ai fais une classe (au début, je ne travaillier pas avec les classes), cela me permet d'alléger le code et de le rendre plus compréhensible
#Initialisation des coordonnée de base du personnage(Taille et largeur et rapidité, ect)
class Joueur(object):
    def __init__(self, x, y, largeur, taille):
        self.x = x #Horizontal
        self.y = y #Vertical
        self.largeur = largeur
        self.taille = taille
        self.rapidite = 10 #Vitesse de déplacement du carré rouge (personnage)
        #Variable pour l'évenement Jump (saut)
        self.sauter = False
        self.compteurSaut = 10
        #Variable pour les sprites de mouvement
        self.gauche = False
        self.droite = False
        self.compteurMarche = 0
        self.immobile = True #Lorsque le personnage ne bouge plus
        self.hitbox = (self.x + 17, self.y + 11, 29,52) #Rectangle pour voir la hitbox de chaque individus

    def changement(self, fenetre):

        if self.compteurMarche +1 >= 27: #Il y a 9 images pour l'animation de mouvement, nous allons montrer la meme image 3 fois
            self.compteurMarche = 0     #Donc 9*3 = 27, due aux 3 fois chaque animations.

        if not(self.immobile): #Si il n'est pas immobile, alors on a une animation qu'il marche a droite ou gauche

            if self.gauche:

                fenetre.blit(walkLeft[self.compteurMarche//3], (self.x,self.y)) #divisé par 3 car on montre 3 fois la meme animations
                self.compteurMarche += 1

            elif self.droite:
                fenetre.blit(walkRight[self.compteurMarche//3], (self.x,self.y))
                self.compteurMarche += 1

        else: #Si il est immobile, alors on a une animation ou il regarde a droite ou a gauche( Pour les tirs)

            if self.droite:
                fenetre.blit(walkRight[0], (self.x, self.y))
            else:
                fenetre.blit(walkLeft[0], (self.x, self.y))

        self.hitbox = (self.x + 17, self.y + 11, 29,52)#Création d"un rectangle rouge pour apercevoir la hitbox du heros
        #pygame.draw.rect(fenetre, (255,0,0), self.hitbox, 2)#Affichage de la hitbox

            #fenetre.blit(perso, (self.x,self.y))
            #self.compteurMarche = 0
    def toucher(self): #Si le personnage se fait toucher par l"ennemie alors il revien a sa position de base.
        self.sauter = False
        self.compteurSaut = 10
        self.x = 1150 #Coordonnée d'ou le personnage apparaitras lorsqu'il meurt
        self.y = 410
        self.compteurMarche = 0
        #font1 = pygame.font.SysFont("comicsans", 100)
        texte = pygame.image.load("death.png")
        #texte = font1.render("MORT", 1, (255,255,255)) #Affichage lorsque le personnage perd ces 5 points de vie
        fenetre.blit(texte, (600 - (texte.get_width() / 2), 50)) #Afficher au millieu de l'écran
        pygame.display.flip()
        i = 0
        while i < 300:
            pygame.time.delay(4) #Le temps que reste l'image "death" lorsque l'on meurt
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


    
    #def test(self): #Si le personnage se fait toucher par l"ennemie alors il revien a sa position de base.
     #   self.sauter = False
     #   self.compteurSaut = 10
     #   self.x = 1150 #Coordonnée d'ou le personnage apparaitras lorsqu'il meurt
     #   self.y = 410
     #   self.compteurMarche = 0
     #   pygame.display.flip()


#Classe pour les tirs (projectiles),et pour l'orientation du personnage lorsqu"il tire
class projectile(object):
    def __init__(self, x, y, rayon, couleur, face):
        self.x = x
        self.y = y
        self.rayon = rayon
        self.couleur = couleur
        self.face = face
        self.rapidite = 8 * face
#Création des tirs ( des cercles verts de rayon 6), a remplacer plus tard par une image peut etre.
    def changement(self, fenetre):
        pygame.draw.circle(fenetre, self.couleur, (self.x, self.y), self.rayon, 6)


class Firedragon(object):
    def __init__(self, x, y):
        self.img=pygame.image.load("spellsprite.png")
        self.coord=self.img.get_rect()
        self.coord.left = x
        self.coord.top = y
        self.coord.width=120 #4680px/13 images
        self.idxImage=0
        self.estActif=False
        
    def lance(self,x,y):
        self.estActif=True
        self.idxImage=0
        self.positionne(x,y)
        
    def positionne(self,x,y):
        self.coord.left = x
        self.coord.top = y
        
    def anime(self):
        self.idxImage+=1
        if self.idxImage>12:
            self.idxImage=12

    def changement(self, fenetre):
        if self.estActif:
            fenetre.blit(self.img, self.coord, pygame.Rect(0,360*self.idxImage,120,360))
        

#----------------------------------------POUR LE MAGE-------------------------------------------
class magie(object): #Classe magie pour le magicien qui rest statique et pour peut etre le Boss final

    mechant = pygame.image.load('magicien.png')
    boss = pygame.image.load("BOSS.png") #Boss final

    def __init__(self, x, y, taille, largeur, fin):
        self.x = x
        self.y = y
        self.taille = taille
        self.largeur = largeur
        self.fin = fin
        self.compteurMarche = 0
        self.hitbox = (self.x + 17, self.y + 2, 31,57)
        self.vie =  10  #Point de vie
        self.visible = True #Actuellement la barre de vie est visible tant qu'elle ne perd pas c'est 10 points de vie


    def changement(self, fenetre):
        if self.visible:
            if self.vie >=0:
                fenetre.blit((self.mechant), (self.x, self.y))
                fenetre.blit((self.boss), (self.x, self.y))


            #Création de la barre de vie
            pygame.draw.rect(fenetre, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))#Rectangle rouge pour la barre de vie
            pygame.draw.rect(fenetre, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.vie)), 10))#Rectangle vert pour la barre de vie
            self.hitbox = (self.x + 17, self.y + 2, 31,57) #Création d"un rectangle rouge pour apercevoir la hitbox de l'ennemie
            #pygame.draw.rect(fenetre, (255,0,0), self.hitbox, 2)#Affichage de la hitbox


    def toucher(self): #On définie toucher lorsque l'ennemie est toucher par les tirs, pour que la hitbox le detecte
        if self.vie > 0:
            self.vie -= 2 #Les dégats que prend, a chaque fois qu'il est touché il perd 1 point de vie
        else:
            #pygame.time.delay(10)
            self.visible = False #La barre de vie disparait


        print("Hit")
        
    
    #----------------------TIR DU MAGE-----------------------------
    def tirMage(self):
        global Magic
        if True: #goblin2.visible == False and Magic == 0:
            print(len(tirMagic))
            if len(tirMagic) < 45: #Le numéros est le nombre de tir qu'il y'auras sur l"écran
                tirMagic.append(projectile(round(mage.x -5), round(mage.y), 6, (255,128,0), 1))
                #tirMagic.append(projectile(round(mage.x + mage.taille //1), round(400), 6, (255,128,0), 1))#- mage.taille //1
            for tirM in tirMagic:
                tirM.x+=tirM.rapidite
                #print("tirM",cptFrame)
            if mage.visible == False:
                   len(tirMagic) == 0
                   tirMagic.append(projectile(round(mage.x + mage.taille //1), round(mage.y), 6, (255,128,0), 1))
                   #tirMagic.pop(tirMagic.index(tirM))
                   
        Magic = 0
       
      
    def tir1(self):
        global Magic
        if True: #Le numéros est le nombre de tir qu'il y'auras sur l"écran
            print(len(tirMagic))
            if len(tirMagic) < 20:
                tirMagic.append(projectile(round(mage.x - mage.taille //1), round(400), 6, (255,128,0), 1))#- mage.taille //1
                #tirMagic.append(projectile(round(mage.x - mage.taille //1), round(200), 6, (255,128,0), 1))#- mage.taille //1
            for tirM in tirMagic:
                tirM.x+=tirM.rapidite
                #print("tirM",cptFrame)
            if mage.visible == False:
                   len(tirMagic) == 0
                   tirMagic.append(projectile(round(mage.x + mage.taille //1), round(mage.y), 6, (255,128,0), 1))
                   #tirMagic.pop(tirMagic.index(tirM))#Pour enlever un élément, le index sert a chercher l'élément est pour ainsi le supprimer
                #tirMagic.pop(tirMagic.index(tirM))#Pour enlever un élément, le index sert a chercher l'élément est pour ainsi le supprimer
            
                
        Magic = 0
        
    pygame.display.flip()    

#--------------------------------------------POUR LE BOSS------------------------------------
class final(object): #Classe final pour le BOSS qui rest statique

    boss = pygame.image.load("BOSS.png") #Boss final

    def __init__(self, x, y, taille, largeur, fin):
        self.x = x
        self.y = y
        self.taille = taille
        self.largeur = largeur
        self.fin = fin          
        self.compteurMarche = 0
        self.hitbox = (self.x + 295, self.y + 215, 50,50)
        self.vie =  20  #Point de vie
        self.visible = True #Actuellement la barre de vie est visible tant qu'elle ne perd pas c'est 20 points de vie


    def changement(self, fenetre):
        if self.visible:
            if self.vie >=0:
                fenetre.blit((self.boss), (self.x, self.y))


            #Création de la barre de vie
            pygame.draw.rect(fenetre, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))#Rectangle rouge pour la barre de vie
            pygame.draw.rect(fenetre, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - 5 *(10 - self.vie), 10))#Rectangle vert pour la barre de vie
            self.hitbox = (self.x + 520, self.y + 215, 50,50)
            #self.hitbox = (self.x + 295, self.y + 215, 50,50) #Création d"un rectangle rouge pour apercevoir la hitbox de l'ennemie
            #self.hitbox = (self.x + 200, self.y + 100, 31,300)
            #pygame.draw.rect(fenetre, (255,0,0), self.hitbox, 2)#Affichage de la hitbox


    def toucher(self): #On définie toucher lorsque l'ennemie est toucher par les tirs, pour que la hitbox le detecte
        if self.vie > 0:
            self.vie -= 1 #Les dégats que prend, a chaque fois qu'il est touché il perd 1 point de vie
        else:
            #pygame.time.delay(10)
            self.visible = False #La barre de vie disparait

        print("Hit")
        
                   
     #A REGLER POUR LES TIRS DU BOSS   
    def tir2(self):
        global Feu
        if True: #Le numéros est le nombre de tir qu'il y'auras sur l"écran
            print("test")
            if len(tirFeu) < 10:
                pass
                #tirFeu.append(firedragon(round(boss.y - boss.x), round(400), 6, (255,0,0), 1))#- mage.taille //1
                #tirMagic.append(projectile(round(mage.x - mage.taille //1), round(200), 6, (255,128,0), 1))#- mage.taille //1
        for tirB in tirFeu:
                tirB.x+=tirB.rapidite
                print("tirB",cptFrame)
                
        Feu = 0

pygame.display.flip()

class ennemy(object):

    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'),
            pygame.image.load('R3E.png'), pygame.image.load('R4E.png'),
            pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
            pygame.image.load('R7E.png'), pygame.image.load('R8E.png'),
            pygame.image.load('R9E.png'), pygame.image.load('R10E.png'),
            pygame.image.load('R11E.png')]

    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'),
            pygame.image.load('L3E.png'), pygame.image.load('L4E.png'),
            pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
            pygame.image.load('L7E.png'), pygame.image.load('L8E.png'),
            pygame.image.load('L9E.png'), pygame.image.load('L10E.png'),
            pygame.image.load('L11E.png')]

    def __init__(self, x, y, taille, largeur, fin):
        self.x = x
        self.y = y
        self.taille = taille
        self.largeur = largeur
        self.fin = fin
        self.chemin = [self.x, self.fin] #chemin que parcourt le mechant(ou il commence et ou il fini)
        self.compteurMarche = 0
        self.rapidite = 3
        self.hitbox = (self.x + 17, self.y + 2, 31,57)
        self.vie =  10  #Point de vie
        self.visible = True #Actuellement la barre de vie est visible tant qu'elle ne perd pas c'est 10 points de vie

    def changement(self, fenetre):
        self.mouvement()
        if self.visible:
            if self.compteurMarche + 1 >= 33: #Comme pour le heros mis en commentaire au dessus, mais la c'est pour l'ennemie
                self.compteurMarche = 0

            if self.rapidite > 0:
                fenetre.blit(self.walkRight[self.compteurMarche //3], (self.x, self.y))
                self.compteurMarche += 1
            else:
                fenetre.blit(self.walkLeft[self.compteurMarche //3], (self.x, self.y))
                self.compteurMarche += 1
            #Création de la barre de vie
            pygame.draw.rect(fenetre, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))#Rectangle rouge pour la barre de vie
            pygame.draw.rect(fenetre, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.vie)), 10))#Rectangle vert pour la barre de vie
            self.hitbox = (self.x + 17, self.y + 2, 31,57) #Création d"un rectangle rouge pour apercevoir la hitbox de l'ennemie
            #pygame.draw.rect(fenetre, (255,0,0), self.hitbox, 2)#Affichage de la hitbox

    def mouvement(self):
        if self.rapidite > 0: #> 0 c'est qu'il va a droite
            if self.x + self.rapidite < self.chemin[1]:
                self.x += self.rapidite
            else:
                self.rapidite = self.rapidite * -1
                self.compteurMarche = 0
        else:
            if self.x - self.rapidite > self.chemin[0]:
                self.x += self.rapidite

            else:
                self.rapidite = self.rapidite * -1
                self.compteurMarche = 0

    def toucher(self): #On définie toucher lorsque l'ennemie est toucher par les tirs, pour que la hitbox le detecte
        if self.vie > 0:
            self.vie -= 1 #Les dégats que prend, a chasque fois qu'il est touché il perd 1 point de vie
        else:
            #pygame.time.delay(10)
            self.visible = False #La barre de vie disparait


        print("Hit")

def affichefond(leFond):

    fenetre.blit(leFond, (0,0))
    texte = font.render("Score: " + str(score), 1, (255,255,255)) #Affichage du score
    fenetre.blit(texte, (570, 100)) #Positionnement d'ou sera l'affichage

def transition():


    fondu = pygame.Surface((largeur, hauteur))
    fondu.fill((0,0,0))
    for alpha in range(0, 300):
        fondu.set_alpha(alpha)
        fenetre.blit(fondu, (0,0))
        pygame.time.delay(5)
        pygame.display.flip()

class Niveau:

    def __init__(self, fond):
        self.fond = fond
        self.tabAdversaires = []

    def ajouteAdversaire(self, adversaire):
        self.tabAdversaires.append(adversaire)

    def afficheAdversaires(self, fenetre):
        for adv in self.tabAdversaires:
            adv.changement(fenetre)

    def affichefond(self, fenetre):
        fenetre.blit(self.fond, (0,0))
        texte = font.render("Score: " + str(score), 1, (255,255,255)) #Affichage du score
        fenetre.blit(texte, (570, 100)) #Positionnement d'ou sera l'affichage

    def afficheHero(self, fenetre):
        heros.changement(fenetre)

    def afficheTout(self,fenetre):
        self.affichefond(fenetre)
        self.afficheAdversaires(fenetre)
        self.afficheHero(fenetre)
        
    def afficheEND(self, fenetre):
        self.affichefond(fenetre)


def changementFenetre():
    global phaseAffichage

    if phaseAffichage == 1: # Fond 1

        niveau1.afficheTout(fenetre)
        #affichefond(zoneDebut)
        #heros.changement(fenetre)
        #goblin.changement(fenetre)
        #mage.changement(fenetre)
        #goblin2.changement(fenetre)

        if mage.visible == False: # Si le mage meurt on passe a la zone suivante
            phaseAffichage = 2


    elif phaseAffichage == 2: #Transition ( fondu )

        transition() #Lorsque l'ennemie meurt transition
        phaseAffichage = 3
        pygame.display.flip()



    elif phaseAffichage == 3:# Fond 2

        niveau2.afficheTout(fenetre)
        affichefond(zonefinal)
        boss.changement(fenetre)
        fireDragon.changement(fenetre)
        fireDragon2.changement(fenetre)
        fireDragon3.changement(fenetre)
        fireDragon4.changement(fenetre)
        heros.changement(fenetre)
        #heros.test()
        
        if boss.visible == False: #Une fois le boss mort, la phase change pour afficher le message de fin
            phaseAffichage = 4
    
    elif phaseAffichage == 4:
        
        transition()
        phaseAffichage = 5
        pygame.display.flip()
        
    elif phaseAffichage == 5:
        
        niveau3.afficheEND(fenetre)# Affichage de la page de fin lorsque le boss est mort
    #pygame.display.flip()

    # !! !!!! !! ! ! Peut etre mette une image de tir plus agréable( A voir plus tard)  !! ! ! !! ! ! !
    #Boucle Pour afficher le tir
    
    for tir in tirs:
        tir.changement(fenetre)

    for letir in tirMagic:
        letir.changement(fenetre)
        
    for fireshoot in tirFeu:
        fireshoot.changement(fenetre)



#J'utilisais fenetre.fill pour colorier en noir la surface du rectangle, donc evité le prolongement (sans cette commande, le rectangle se prolonge a l'infinie, comme le jeux Snake)
    #fenetre.fill((0,0,0))
#Création du personnage (C'est un rectangle au début), Initialisation de la taille, couleur ect..
    #pygame.draw.rect(fenetre, (255,0,0), (x, y, largeur, taille))

cptFrame=0
cptframe=0
cptMort=0
font = pygame.font.SysFont("comicsans", 30, True) #La police de caractère
heros = Joueur(1150, 410, 64, 64) #Position du joueur
mage = magie(5, 350, 100,100, 1150) # Création du mage
boss = final(20, 0, 100,1000, 1000)
goblin2 = ennemy(50, 410, 64, 64, 1000)
goblin = ennemy(250, 410, 64, 64, 1000)
shoot = 0
Magic = 0
Feu = 0
tirs = []
tirMagic = []
tirFeu = []
fonctionnement = True

fireDragon=Firedragon(200,100)
fireDragon2=Firedragon(200,100)
fireDragon3=Firedragon(200,100)
fireDragon4=Firedragon(200,100)

niveau1 = Niveau(zoneDebut)
niveau1.ajouteAdversaire(goblin)
niveau1.ajouteAdversaire(goblin2)
niveau1.ajouteAdversaire(mage)


niveau2 = Niveau(zonefinal)
niveau2.ajouteAdversaire(boss)

niveau3 = Niveau(fin2)

    #----------------Compteur pour les points de vie du joueur-------------------------------
#if heros.toucher:
 #    cptMort += 1
  #   print(cptMort)
   #  if cptMort == 3:
    #     pygame.quit()
          
#Boucle pour fermer la fenetre lorsqu'on appuye sur la croix en haut à droite
while fonctionnement:
    clock.tick(27)
    
#------------------------POUR GOBLIN 1 ---------------------------------------------------------------------
    if goblin.visible == True: #Pour regler le probleme lorsque le goblin meurt il disparait mais si on se deplace vers son cadavre on meurt quand meme
        #Cette ligne est utile pour detecter lorsque le goblin attaque le personnage dans la zone de hitbox
        if heros.hitbox[1] < goblin.hitbox[1] +  goblin.hitbox[3] and heros.hitbox[1] + heros.hitbox[3] > goblin.hitbox[1]:
            if heros.hitbox[0] + heros.hitbox[2] > goblin.hitbox[0] and heros.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                heros.toucher()
                print("toucher")
                if heros.toucher:
                    cptMort +=1
                    print(cptMort)
                if cptMort == 3:
                    print("YOU LOSE")
                    pygame.quit()
                        #score -= 5 #A chaque fois que sa touche, le personnage est toucher alors il perd 5

#------------------------POUR GOBLIN2 ---------------------------------------------------------------------
    if goblin2.visible == True: #Pour regler le probleme lorsque le goblin2 meurt il disparait mais si on se deplace vers son cadavre on meurt quand meme
        #Cette ligne est utile pour detecter lorsque le goblin2 attaque le personnage dans la zone de hitbox
        if heros.hitbox[1] < goblin2.hitbox[1] +  goblin2.hitbox[3] and heros.hitbox[1] + heros.hitbox[3] > goblin2.hitbox[1]:
            if heros.hitbox[0] + heros.hitbox[2] > goblin2.hitbox[0] and heros.hitbox[0] < goblin2.hitbox[0] + goblin2.hitbox[2]:
                heros.toucher()
                if heros.toucher:
                    cptMort +=1
                if cptMort == 3:
                    print("YOU LOSE")
                    pygame.quit()

#-----------------------------POUR LE MAGE---------------------------------------------------
    if mage.visible == True: #Pour regler le probleme lorsque le goblin2 meurt il disparait mais si on se deplace vers son cadavre on meurt quand meme
        #Cette ligne est utile pour detecter lorsque le goblin2 attaque le personnage dans la zone de hitbox
        if heros.hitbox[1] < mage.hitbox[1] +  mage.hitbox[3] and heros.hitbox[1] + heros.hitbox[3] > mage.hitbox[1]:
            if heros.hitbox[0] + heros.hitbox[2] > mage.hitbox[0] and heros.hitbox[0] < mage.hitbox[0] + mage.hitbox[2]:
                heros.toucher()
                if heros.toucher:
                    cptMort +=1
                if cptMort == 3:
                    print("YOU LOSE")
                    pygame.quit()
    
    if shoot > 0 : #Boucle pour le cooldown de shoot, le temps entre chaque tir, la fréquence a laquelle on peux tirer
        shoot += 1
    if shoot > 3:
        shoot = 0

    #if Magic > 0 : #Boucle pour le cooldown de shoot, le temps entre chaque tir, la fréquence a laquelle on peux tirer
     #   Magic += 1
    #if Magic > 3:
     #   Magic = 0



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fonctionnement = False

#-------------------Boucle pour les tirs du personnage(lorsque les tirs touche la cible, alors les tirs disparaissent)------------------
#----------------------------POUR QUE LE PERSO PREND LES DEGATS DU MAGE-------------------------------
    for tirM in tirMagic: #Pour que le heros meurt lorsque les tirs du mage le touche
            #Cette ligne est utile pour detecter lorsqu'un tir entre dans la zone de hitbox
            if tirM.y - tirM.rayon < heros.hitbox[1] +  heros.hitbox[3] and tirM.y + tirM.rayon > heros.hitbox[1]:
                if tirM.x + tirM.rayon > heros.hitbox[0] and tirM.x - tirM.rayon < heros.hitbox[0] + heros.hitbox[2]:
                    songtoucher.play()
                    heros.toucher()
                    if heros.toucher:
                        cptMort +=1
                        if cptMort == 6:
                            print("YOU LOSE")
                            pygame.quit()
    
            if tirM.x < 1200 and tirM.x > 0:#x car les tirs sont horizontals et 1200 pour ne pas que les tirs aillent en dehors de l'écran
                tirM.x += tirM.rapidite

            else:
                tirMagic.pop(tirMagic.index(tirM))# Fait disparaitre les tirs du mage pour en crée de nouvelle

#----------------------------POUR LE BOSS----------------------------------------------------------------
    for tirB in tirFeu: #Pour que le heros meurt lorsque les tirs du mage le touche
            #Cette ligne est utile pour detecter lorsqu'un tir entre dans la zone de hitbox
            if tirB.y - tirB.rayon < heros.hitbox[1] +  heros.hitbox[3] and tirB.y + tirB.rayon > heros.hitbox[1]:
                if tirB.x + tirB.rayon > heros.hitbox[0] and tirB.x - tirB.rayon < heros.hitbox[0] + heros.hitbox[2]:
                    songtoucher.play()
                    heros.toucher()
                    score += 1 #A chaque fois que sa touche le heros, on incrémente de 1
                    tirFeu.pop(tirFeu.index(tirB))#Pour enlever un élément, le index sert a chercher l'élément est pour ainsi le supprimer
        
            if tirB.x < 1200 and tirB.x > 0:#x car les tirs sont horizontals et 1200 pour ne pas que les tirs aillent en dehors de l'écran
                tirB.x += tirB.rapidite

            else:
                tirFeu.pop(tirFeu.index(tirB))# Fait disparaitre les tirs du mage pour en crée de nouvelle


    if phaseAffichage==3:
        if not fireDragon.estActif:
            fireDragon.lance(200,0)
        else:
            if cptFrame%2==1:
                fireDragon.anime()
                nouvelleHauteur=fireDragon.coord.top+10
                if nouvelleHauteur>580:
                    fireDragon.estActif=False
                else:
                    fireDragon.positionne(20,nouvelleHauteur)


    if phaseAffichage==3:
        if not fireDragon2.estActif:
            fireDragon2.lance(100,0)
        else:
            if cptframe%2==0: #Le nombre de frame donc la fluidité à laquelle le dragon vas
                fireDragon2.anime()
                nouvelleHauteur=fireDragon2.coord.top+10
                if nouvelleHauteur>580: # La distance vertical à laquelle les dragons se réinitialise
                    fireDragon2.estActif=False
                else:
                    fireDragon2.positionne(800,nouvelleHauteur) #Les coords ou le dragon apparait

    if phaseAffichage==3:
        if not fireDragon3.estActif:
            fireDragon3.lance(100,0)
        else:
            if cptframe%2==0: #Le nombre de frame donc la fluidité à laquelle le dragon vas
                fireDragon3.anime()
                nouvelleHauteur=fireDragon3.coord.top+10
                if nouvelleHauteur>280: # La distance vertical à laquelle les dragons se réinitialise
                    fireDragon3.estActif=False
                else:
                    fireDragon3.positionne(500,nouvelleHauteur) #Les coords ou le dragon apparait

    if phaseAffichage==3:
        if not fireDragon4.estActif:
            fireDragon4.lance(100,0)
        else:
            if cptframe%2==1: #Le nombre de frame donc la fluidité à laquelle le dragon vas
                fireDragon4.anime()
                nouvelleHauteur=fireDragon4.coord.top+10
                if nouvelleHauteur>380: # La distance vertical à laquelle les dragons se réinitialise
                    fireDragon4.estActif=False
                else:
                    fireDragon4.positionne(150,nouvelleHauteur) #Les coords ou le dragon apparait
                
#------------------------POUR GOBLIN 1 ---------------------------------------------------------------------
    for tir in tirs:
        if goblin.visible == True: # Regler le probleme lorsque le goblin est invisible mais qu'on le touche quand meme
            #Cette ligne est utile pour detecter lorsqu'un tir entre dans la zone de hitbox
            if tir.y - tir.rayon < goblin.hitbox[1] +  goblin.hitbox[3] and tir.y + tir.rayon > goblin.hitbox[1]:
                if tir.x + tir.rayon > goblin.hitbox[0] and tir.x - tir.rayon < goblin.hitbox[0] + goblin.hitbox[2]:
                    songtoucher.play()
                    goblin.toucher()
                    score += 1 #A chaque fois que sa touche le goblin, on incrémente de 1
                    tirs.pop(tirs.index(tir))#Pour enlever un élément, le index sert a chercher l'élément est pour ainsi le supprimer

#------------------------POUR GOBLIN2 ---------------------------------------------------------------------
    for tir in tirs:
        if goblin2.visible == True: # Regler le probleme lorsque le goblin2 est invisible mais qu'on le touche quand meme
            #Cette ligne est utile pour detecter lorsqu'un tir entre dans la zone de hitbox
            if tir.y - tir.rayon < goblin2.hitbox[1] +  goblin2.hitbox[3] and tir.y + tir.rayon > goblin2.hitbox[1]:
                if tir.x + tir.rayon > goblin2.hitbox[0] and tir.x - tir.rayon < goblin2.hitbox[0] + goblin2.hitbox[2]:
                    songtoucher.play()
                    goblin2.toucher()
                    score += 1 #A chaque fois que sa touche le goblin2, on incrémente de 1
                    tirs.pop(tirs.index(tir))#Pour enlever un élément, le index sert a chercher l'élément est pour ainsi le supprimer


        if tir.x < 1200 and tir.x > 0:#x car les tirs sont horizontals et 1200 pour ne pas que les tirs aillent en dehors de l'écran
            tir.x += tir.rapidite

        else: #Si les tirs ne remplissent pas les conditions précédente(on ne veut pas de tir qui reste sur l'écran) alors on les supprimes
            tirs.pop(tirs.index(tir))#Pour enlever un élément, le index sert a chercher l'élément est pour ainsi le supprimer

#--------------------------------------------------------------POUR LE HEROS---------------------------------------
        if tir.x < 1200 and tir.x > 0:#x car les tirs sont horizontals et 1200 pour ne pas que les tirs aillent en dehors de l'écran
            tir.x += tir.rapidite

        pygame.display.flip()
#Mouvement du personnage, touche basique (haut, bas , droite et gauche), déplacement simple
    touche = pygame.key.get_pressed()

    if touche[pygame.K_SPACE] and shoot == 0:
        if heros.gauche:
            face = -1
        else:
            face = 1
        if len(tirs) < 5: #Le numéros est le nombre de tir qu'il y'auras sur l"écran
            tirs.append(projectile(round(heros.x + heros.taille //2), round(heros.y + heros.taille //2), 6, (0,128,0), face)) #Pour que les tirs vienne du millieux du personnage et non de gauche et droite, le 6 reprensete  le rayon

        shoot = 1

#------------------------------------------POUR TUER LE MAGE IL FAUT BIEN VISER LE MILLIEU SON COEUR-----------------------------------
    for tir in tirs:
        if mage.visible == True: # Regler le probleme lorsque le mage est invisible mais qu'on le touche quand meme
            #Cette ligne est utile pour detecter lorsqu'un tir entre dans la zone de hitbox
            if tir.y - tir.rayon < mage.hitbox[1] +  mage.hitbox[3] and tir.y + tir.rayon > mage.hitbox[1]:
                if tir.x + tir.rayon > mage.hitbox[0] and tir.x - tir.rayon < mage.hitbox[0] + mage.hitbox[2]:
                    songtoucher.play()
                    mage.toucher()
                    score += 1 #A chaque fois que sa touche le mage, on incrémente de 1
                    tirs.pop(tirs.index(tir))#Pour enlever un élément, le index sert a chercher l'élément est pour ainsi le supprimer

    if goblin2.visible == False:
        if cptFrame%1==0: #toutes les 1 frames on met l'animation
            mage.tirMage()
#---------------------------------------------------POUR TUER LE BOSS----------------------------------------------------
    for tir in tirs:
        if boss.visible == True: # Regler le probleme lorsque le mage est invisible mais qu'on le touche quand meme
            #Cette ligne est utile pour detecter lorsqu'un tir entre dans la zone de hitbox
            if tir.y - tir.rayon < boss.hitbox[1] +  boss.hitbox[3] and tir.y + tir.rayon > boss.hitbox[1]:
                if tir.x + tir.rayon > boss.hitbox[0] and tir.x - tir.rayon < boss.hitbox[0] + boss.hitbox[2]:
                    songtoucher.play()
                    boss.toucher()
                    score += 1 #A chaque fois que sa touche le mage, on incrémente de 1
                    tirs.pop(tirs.index(tir))#Pour enlever un élément, le index sert a chercher l'élément est pour ainsi le supprimer 
    
    if mage.visible == False:
        if cptFrame%1==0: #toutes les 1 frames on met l'animation
            boss.tir2()
            
            
    pygame.display.flip()

    if touche[pygame.K_LEFT] and heros.x > heros.rapidite: # le and pour empecher le personnage d'aller en dehors de la fenetre

        heros.x -= heros.rapidite # J'utilise le -à coté du = car le personnage est à 0,0 donc on utilise le negatif pour aller à gauche
        heros.gauche = True
        heros.droite = False
        heros.immobile = False #De base en True, on l'iniatilise en False car on appue sur la fleche de droite,donc pas immobile

    elif touche[pygame.K_RIGHT] and heros.x < 1200 - heros.largeur - heros.rapidite : #Le 1200 représente distance que le personnage pourrait parcourir(à changer si besoin !)

        heros.x += heros.rapidite # Meme logique pour tous , aller dans les postif permet d'aller a droite en Horizontal ( x )
        heros.gauche = False
        heros.droite = True
        heros.immobile = False #De base en True, on l'iniatilise en False car on appue sur la fleche de gauche,donc pas immobile

    else: #Si le personnage ne bouge pas alors on initalise les deux a False

        #heros.gauche = False
        #heros.droite = False
        heros.immobile = True
        heros.compteurMarche = 0

    if not(heros.sauter): #Ce if not permet d'empecher d'avancer et de reculer lorsque nous sautons

        if touche[pygame.K_UP]:#En appuyant sur la fleche du haut , nous déclenchons le Saut

            heros.sauter = True
            heros.droite = False
            heros.gauche = False
            heros.compteurMarche = 0

#---------------------------------Gestion du saut(j'ai bien souffert, pour trouver tout sa)------------
    else:

        if heros.compteurSaut >= -10:  #Lorsque le joueur saute , il change d'emplacement donc va plus loin sur l'axe vertical (y)

            neg = 1

            if heros.compteurSaut < 0:
                neg = -1

            heros.y -= (heros.compteurSaut ** 2) * 0.5 * neg
            heros.compteurSaut -= 1

        else:
            heros.sauter = False
            heros.compteurSaut = 10

    changementFenetre() #On fais l'appel de la fonction précédente
    
    pygame.display.flip()

    pygame.time.delay(10)
    cptFrame+=1;
    cptframe+=1;

pygame.quit()




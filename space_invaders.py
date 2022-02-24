    ###############################################################
    ###             On import Les bibliothèques :               ###
    ###############################################################
import pygame  
import random
from pygame import *

class Joueur():  # classe pour créer le vaisseau du joueur
    def __init__(self):
        self.sens = ""
        self.image = pygame.image.load('IMG/vaisseau.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.position = 400 #On donne la position du joueur
        self.score = 0 #on definie le score à 0
        self.vie = 4 # on definie le nombre de vie à 4
        self.img_vie = pygame.image.load("IMG/4.png").convert_alpha() # On definie l'image de la vie quand on en a 4
        self.img_vie = pygame.transform.scale(self.img_vie, (45, 100))# On definie l'image de la vie quand on en a 4


    def deplacer_l(self):
        if self.position > 0: # si la position du joueur est à droite de la bordure de gauche
            self.position -= 0.5 # il se déplace


    def deplacer_r(self):
        if self.position < 740: # si la position du joueur est à gauche de la bordure de droite
            self.position += 0.5 # il se déplace


    def tirer(self):
        pass


    def marquer(self):
        self.score += 1 # on ajoute 1 au score


class Balle():
    def __init__(self, joueur):
        self.etat = "" # on definie l'état de la balle sur None
        self.image = pygame.image.load("IMG/balle.png").convert_alpha() # On choisi l'image de la balle
        self.image = pygame.transform.scale(self.image, (30, 60)) # On choisi l'image de la balle
        self.depart = joueur.position + 16 # on met pour que l'image soit juste au dessus du robot
        self.hauteur = 470 # on def sa hauteur
        self.joueur = joueur 
                

    def bouger(self):
        if self.etat != "tiree": #si la balle n'est pas encore tirée
            self.depart = 5000 # on cache la balle 
            self.tirpos = False # et la tirpos est sur False
        else:
            if self.hauteur > 0: # si on est dans la fenetre
                if self.tirpos == False: # si la tirpos est False
                    # self.balster= pygame.mixer.music.play() # on joue le bruit de blaster
                    self.depart = self.joueur.position + 16 # la balle prend la position du robot a l'instant 
                    self.tirpos = True # la conduit repasse true
                self.hauteur -= 2 # donc la balle part
            else: # = si la balle sort de la fenetre
                self.etat = ""  # la balle n'est plus tiree
                self.depart = self.joueur.position + 16 # elle reprend sa positon
                self.hauteur = 470 # et sa hauteur


    def toucher(self, ennemi):
        if (-50 < self.hauteur - ennemi.hauteur < 50 
            and -50 < self.depart - ennemi.depart < 50): # On fait une sorte de hitboxe de 50px autour de l'image
            self.hauteur = 470 # donc la balle revient
            self.etat = "" # et la balle n'est plus tirée
            return True # on renvoie True
        else:
            return False # on renvoie False


class Ennemi():
    NbEnnemis = 3 # on definie notre nombre d'ennemi

    def __init__(self, player):
        self.depart = random.randint(50, 700) # on fait un random pour la position horizontale des Ennemi
        self.hauteur = -100 # on les met un peu plus que la fenetre comme ca il ne sont pas coller au début
        self.type = 1 # on choisi le type de Ennemi sur 1
        
        self.image1 = pygame.image.load("IMG/invader.png").convert_alpha() #on choisi l'image de l'Ennemi 
        self.image1 = pygame.transform.scale(self.image1, (64, 64)) 
        
        self.image2 = pygame.image.load("IMG/invader2.png").convert_alpha() #on choisi l'image de l'Ennemi 
        self.image2 = pygame.transform.scale(self.image2, (64, 64)) 
        
        self.image3 = pygame.image.load("IMG/invader3.png").convert_alpha() #on choisi l'image de l'Ennemi 
        self.image3 = pygame.transform.scale(self.image3, (64, 64))
        
        self.image4 = pygame.image.load("IMG/invader4.png").convert_alpha() #on choisi l'image de l'Ennemi 
        self.image4 = pygame.transform.scale(self.image4, (64, 64))
        
        self.vitesse = random.uniform(0.05, 0.2) # on met une vitesse aléatoire entre deux float
        self.player = player 
        self.cond = False # on met une cond sur False
        self.explosion = pygame.image.load("IMG/Anim/1.png") # on import l'image de la première explosion
        self.l_explosion = [] # on crée une liste
        self.fichier = open("score.txt","a") #on ouvre notre fichier txt pour ecrire les score
        for i in range(1,7): # on vas ajouter toute les images de l'explotion dans la liste
            self.l_explosion.append(pygame.image.load(f"IMG/Anim/{i}.png"))
        self.current = 0 #on def current à 0
        

    def change(self,screen,):    
        if self.type == 1:    
            screen.blit(self.image1,[self.depart, self.hauteur])  # appel de la fonction qui dessine le vaisseau du joueur
        if self.type == 2:  
            screen.blit(self.image2,[self.depart, self.hauteur])  # appel de la fonction qui dessine le vaisseau du joueur
        if self.type == 3: 
            screen.blit(self.image3,[self.depart, self.hauteur])  # appel de la fonction qui dessine le vaisseau du joueur
        if self.type == 4: 
            screen.blit(self.image4,[self.depart, self.hauteur])  # appel de la fonction qui dessine le vaisseau du joueur  
    
    def explo(self):
        self.current+=0.05 #ca vas etre un chiffre qui augmente
        self.explosion = pygame.transform.scale(self.l_explosion[int(self.current)], (100, 100))# on afficher de la liste l_explosion le numero avec comme indice le curent avec comme taille 100x100
        
        
    def avancer(self):
        self.hauteur += self.vitesse # on fait simplement avancer


    def disparaitre(self): 
        """ Fonction pour faire disparaite les Ennemis"""
        self.hauteur = -100 # On les remet en haut
        self.depart = random.randint(50, 700) # avec toujours un départ aléatoire
        
        
    def sante(self):
        """ Fonction qui gère tout ce qui touche à la vie """
        if self.hauteur > 600: # si les robot sortent de la fenetre par en bas
            self.player.vie -= 1 # on enleve une vie
            if self.player.vie != 0: # si la vie n'est pas égal à 0
                self.player.img_vie = pygame.image.load(f"IMG/{str(self.player.vie)}.png").convert_alpha() #on affiche l'image correspondante au niveau de vie
                self.player.img_vie = pygame.transform.scale(self.player.img_vie, (45, 100)) 
                self.disparaitre() # on appelle disparaitre()
            if self.player.vie == 0: # si la vie vaut 0
                self.fichier.write(f"\n{str(self.player.score)}") # on écrit le score dans le fichier texte
                perdu() # on appelle la fonction perdu() qui lance l'écran de défaite


###############################################################
###                     Fin des Classes :                   ###
###############################################################


def meilleur_score():
    """
    C'est une fonction qui parcours le fichier score.txt 
    et qui met toute les lignes dans une liste pour ensuite 
    chercher le max de cette liste
    Pour return le maximum
    """
    liste = []
    with open("score.txt", "r") as f:
        for line in f.readlines():
            liste.append(line.strip())
    liste = list(map(int,liste))
    max = None
    for num in liste:
        if (max is None or num > max):
            max = num
    return max


    liste = []
    with open("score.txt", "r") as f:
        for line in f.readlines():
            liste.append(line.strip())
    return liste[-1]
 
###############################################################
###             On définie differentes variables :          ###
###############################################################
s = 0  
color = (4,20,39)


def menu():
    """ Ecran de menu """
    global color # on utilise color def en haut
    
    pygame.init()# on démarre pygame
    
    running = True
    
    screen = pygame.display.set_mode((800, 600)) # on crée la fenetre
    
    pygame.display.set_caption("Space Invaders") # on appelle la fenetre Space Invaders 
    
    ###############################################################
    ###             On définie les different boutons :          ###
    ###############################################################
    
    play = pygame.image.load("IMG/jouer.png")
    play = pygame.transform.scale(play, (250, 100))
    play_rect = play.get_rect()
    play_rect.x, play_rect.y = 270, 350

    Quit = pygame.image.load("IMG/quitter.png")
    Quit = pygame.transform.scale(Quit, (200, 80))
    Quit_rect = Quit.get_rect()
    Quit_rect.x, Quit_rect.y = 290, 450

    Titre = pygame.image.load("IMG/titre.png")
    Titre_rect = Titre.get_rect()
    Titre = pygame.transform.scale(Titre, (700, 150))
    Titre_rect.x, Titre_rect.y = 50, 50

    image = pygame.image.load("IMG/menu.png")
    image_r = image.get_rect()
    image = pygame.transform.scale(image, (400, 400))
    image_r.x, image_r.y = 50,150
    
    
    ###############################################################
    ###                     Boucle de jeux :                    ###
    ###############################################################
    
    while running:
        # On blit tout 
        screen.fill(color) 
        
        screen.blit(image, image_r)
        
        screen.blit(play, play_rect)
        
        screen.blit(Titre, Titre_rect)
        
        screen.blit(Quit, Quit_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            x,y = pygame.mouse.get_pos() # on définie les coordonées
            if play_rect.collidepoint(x,y) and event.type == pygame.MOUSEBUTTONUP:
                # clic = pygame.mixer.music.play()            #   On definie
                # clic = pygame.mixer.music.set_volume(0.1)   #   le bruit de clique
                time.delay(1000) # on met un délay de 1 sec entre le son et changement de fenetre
                game() #on lance le jeux
                
            if Quit_rect.collidepoint(x,y) and event.type == pygame.MOUSEBUTTONUP:
                # clic = pygame.mixer.music.play()            #   On definie
                # clic = pygame.mixer.music.set_volume(0.1)   #   le bruit de clique
                time.delay(1000) # on met un délay de 1 sec entre le son et changement de fenetre
                pygame.quit()   # on ferme la fenetre        
        pygame.display.update()

def game():
    global s, color
    pygame.init() # on demarre pygame
    
    screen = pygame.display.set_mode((800, 600)) # on crée la fenetre
    
    pygame.display.set_caption("Space Invaders") # on appelle la fenetre Space Invaders
    
    font = pygame.font.Font("Police.ttf", 40)  # we def font
    
    player = Joueur() #on crée le joueur
    # creation de la balle
    tir = Balle(player) # on crée tir
    tir.etat = "chargee"
    
    # creation des ennemis
    listeEnnemis = []
    for indice in range(Ennemi.NbEnnemis):
        vaisseau = Ennemi(player)
        listeEnnemis.append(vaisseau)

    
    valeur = 0 #on def une valeur pour crée des boucle d'image
    
    pressed = {} # on crée un dico qui vas servir pour les déplacement
    
    running = True  # variable pour laisser la fenêtre ouverte
    
    ###############################################################
    ###                     Boucle de jeux :                    ###
    ###############################################################
    
    while running:  # boucle infinie pour laisser la fenêtre ouverte
        screen.fill(color) # on met le fond avec la couleur def plus haut
        
        valeur += 1
        
        if valeur % 150 == 0:
            cond = False
            
            
        ###############################################################
        ###                 Gestion des evenements :                ###
        ###############################################################
        
        for event in pygame.event.get():  # parcours de tous les event pygame dans cette fenêtre
            if event.type == pygame.QUIT:  # si l'événement est le clic sur la fermeture de la fenêtre
                running = False  # running est sur False
                sys.exit()  # pour fermer correctement

            # gestion du clavier
            if event.type == pygame.KEYDOWN:  # si une touche a été tapée, le marque dans le dictionnaire pressed la touche enfoncer
                pressed[event.key] = True
            if event.type == pygame.KEYUP:
                pressed[event.key] = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # espace pour tirer
                    player.tirer()
                    tir.etat = "tiree"

        if pressed.get(pygame.K_RIGHT):  # Si le joueur veut aller a droite
            player.deplacer_r()
        if pressed.get(pygame.K_LEFT):  # Si le joueur veut aller a gauche
            player.deplacer_l()
            
        player.deplacer_l()
        player.deplacer_r()
        
        ###############################################################
        ###             Gestion des colitions :                     ###
        ###############################################################


        for ennemi in listeEnnemis:
            ennemi.change(screen)
            if tir.toucher(ennemi):
                player.marquer()
                ennemi.cond = True
                
        # placement des objets
        # le joueur

        
        screen.blit(tir.image, [tir.depart, tir.hauteur])  # appel de la fonction qui dessine le vaisseau du joueur
        
        # la balle
        tir.bouger()
        screen.blit(player.img_vie, [20, 20])
        
        ###############################################################
        ###             Affichage du score :                        ###
        ###############################################################
        score = str(player.score)
        score_text = font.render((score), 1, (255, 255, 255))  # le score
        score_text_pos = score_text.get_rect()  # on crée le get_rect
        screen.blit(score_text, (720, 30))
        
        ###############################################################
        ###           Animation de vie qui clignote :               ###
        ###############################################################
        
        if player.vie == 1:
            if valeur % 500 == 250: #si la valeur vaut 250 on affiche l'image verte
                player.img_vie = pygame.image.load(f"IMG/1.png").convert_alpha()
                player.img_vie = pygame.transform.scale(player.img_vie, (45, 100))
            elif valeur % 500 == 490: #si la valeur vaut 490 on affiche l'image rouge
                player.img_vie = pygame.image.load(f"IMG/1-r.png").convert_alpha()
                player.img_vie = pygame.transform.scale(player.img_vie, (45, 100))
                
                
        ###############################################################
        ###                      Les Ennemis :                      ###
        ###############################################################
        
        for ennemi in listeEnnemis:
            # on fait que plus on a de score plus il y'a de vitesse
                  
            if player.score == 20:
                ennemi.type = 2
                ennemi.vitesse = random.uniform(0.20, 0.25)
            elif player.score == 40:
                ennemi.type = 3
                ennemi.vitesse = random.uniform(0.25, 0.30)
            elif player.score == 60:
                ennemi.type = 4
                ennemi.vitesse = random.uniform(0.30, 0.35)
            elif player.score == 80:
                ennemi.vitesse = 0.50
               
            ennemi.sante() # on appele la fonction sante 
            ennemi.avancer() # on appele la fonction avancé                   
                
            if ennemi.cond == True:
                if ennemi.current < 5:
                    ennemi.explo()
                    screen.blit(ennemi.explosion , (ennemi.depart-20, ennemi.hauteur-20))
                else:
                    ennemi.current = 0
                    ennemi.cond = False
                    ennemi.disparaitre()
                     
                    
        screen.blit(player.image, [player.position, 500])  # appel de la fonction qui dessine le vaisseau du joueur  
                  
        s = player.score #on definie s avec le score pour le recuperer sur l'écran de fin
        pygame.display.update()  # pour ajouter tout changement à l'écran

def perdu():
    global s # on global s pour le score
    
    pygame.init()# on démarre pygame
    
    running = True
    
    font = pygame.font.Font("Police.ttf", 40)  # on definie une police
    

    screen = pygame.display.set_mode((800, 600))
    
    pygame.display.set_caption("Space Invaders") # on appelle la fenetre Space Invaders
    
    color = (4,20,39)
    
    ###############################################################
    ###             On définie les different boutons :          ###
    ###############################################################
    
    play = pygame.image.load("IMG/rejouer.png")
    play = pygame.transform.scale(play, (250, 100))
    play_rect = play.get_rect()
    play_rect.x, play_rect.y = 270, 350
    
    Quit = pygame.image.load("IMG/quitter.png")
    Quit = pygame.transform.scale(Quit, (200, 80))
    Quit_rect = Quit.get_rect()
    Quit_rect.x, Quit_rect.y = 290, 450
    
    Titre = pygame.image.load("IMG/game_over.png")
    Titre_rect = Titre.get_rect()
    Titre = pygame.transform.scale(Titre, (600, 150))
    Titre_rect.x, Titre_rect.y = 100, 50
    
    score_m = f"le meilleur score est {str(meilleur_score())}"
    score_text_m = font.render((score_m), 1, (255, 255, 255))  # le score
    score_text_pos_m = score_text_m.get_rect()  # on crée le get_rect
    
    score_t = f"Votre score est {str(s)}"
    score_text = font.render((score_t), 1, (255, 255, 255))  # le score
    score_text_pos = score_text_m.get_rect()  # on crée le get_rect
    
    
    ###############################################################
    ###                     Boucle de jeux :                    ###
    ###############################################################
    
    
    while running:
        
        # On blit tout
        screen.fill(color)
        
        screen.blit(play, play_rect)
        
        screen.blit(Titre, Titre_rect)
        
        screen.blit(Quit, Quit_rect)
        
        screen.blit(score_text_m, (150, 220))
        
        screen.blit(score_text, (220, 270))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            x, y = pygame.mouse.get_pos()
            if play_rect.collidepoint(x,y) and event.type == pygame.MOUSEBUTTONUP:
                # clic = pygame.mixer.music.play() 
                # clic = pygame.mixer.music.set_volume(0.1)
                time.delay(1000) # on met un délay de 1 sec entre le son et changement de fenetre
                game()
                
            if Quit_rect.collidepoint(x,y) and event.type == pygame.MOUSEBUTTONUP:
                # clic = pygame.mixer.music.play() 
                # clic = pygame.mixer.music.set_volume(0.1)
                time.delay(1000) # on met un délay de 1 sec entre le son et changement de fenetre
                pygame.quit()  
        pygame.display.update()

menu() # on démarre la fenetre avec le menu
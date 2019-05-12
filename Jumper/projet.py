																													"""
JEU JUMPER :
Par Etienne Clairis
	Lois Castets																									"""

"""_____________________________________________________________________________________________________________________
#IMPORTATIONS###########################################################################################################
¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""

import pygame, os, time, random, math, subprocess
from pygame.locals import* 

#INITIALISATIONS DE LA FENETRE ET PYGAME
pygame.init() #initialisation de la librairie
width_screen,height_screen=1366,768
pygame.display.set_caption("Jumper")
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,27) #placement de la fenetre par rapport au top left
screen = pygame.display.set_mode((int(width_screen),741))

pygame.key.set_repeat(70,5) # delai pour la reception de l'evenement clavier : set_repeat(delay,interval)

#INITIALISATION DES VARIABLES
BACKCOLOR = (196,233,242) #couleur de fond du jeu
WHITE = (255,255,255)
YELLOW = (255,218,74)

#probabilités d'apparition de chaque objet :
proba_powerup = 20 #--> 1 chance sur 21
proba_coin = 5
proba_enemy = 5
proba_env = 1

#repertoires des images
UI = "IMAGES/UI/"
NUMBERS = "IMAGES/UI/NUMBERS/"
OBJECTS = "IMAGES/OBJECTS/"
ENV = "IMAGES/ENVIRONNEMENT/"
TILES = "IMAGES/tiles/"


#système de saisons
Decors_Autumn=os.listdir(ENV+"Autumn") #on liste tous les fichiers dans le repertoire "IMAGES/ENVIRONNEMENT/Autumn"
Decors_Spring=os.listdir(ENV+"Spring")
Decors_Summer=os.listdir(ENV+"Summer")
Decors_Winter=os.listdir(ENV+"Winter")
seasons_list = {"Autumn":Decors_Autumn,"Winter":Decors_Winter,"Spring":Decors_Spring,"Summer":Decors_Summer}
seasons = ['Winter','Autumn','Spring','Summer']


FPS = 175 #vitesse du jeu
fpsClock = pygame.time.Clock() #init de l'horloge

sens = random.randint(0,1) #Pour sens=0, les nuages vont a droite, sinon a gauche
globalSpeed = 2 #vitesse globale du jeu
water = pygame.image.load("IMAGES/water.png").convert_alpha() #image de fond de l'eau

#listes de Sprites contenant les instanciations des classes
#https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.RenderUpdates
discs = pygame.sprite.RenderUpdates()
clouds = pygame.sprite.RenderUpdates()
platforms = pygame.sprite.RenderUpdates()
enemies = pygame.sprite.RenderUpdates()
coins = pygame.sprite.RenderUpdates()
powerups = pygame.sprite.RenderUpdates()
decors = pygame.sprite.RenderUpdates() #environnement
animations = pygame.sprite.RenderUpdates() 
playerGroup = pygame.sprite.RenderUpdates() #juste le joueur


"""_____________________________________________________________________________________________________________________
#DECLARATION DES CLASSES################################################################################################
¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""


########################################################################################################################
#Joueur#################################################################################################################
########################################################################################################################
#joueur + changement de joueur + collision plateformes + chute + saut + mort
########################################################################################################################

class PLAYER(pygame.sprite.Sprite): #Tout ce qui concerne le joueur
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#GLOBAL
		self.posX = 470  #Position en X (Par rapport au Left)
		self.posY = -700 #Position en Y (par rapport au Top) .. 700 pixels + hauts, pour tomber sur une plateforme
		self.lives = 5 #Nombre de vies
		self.isdead = False
		self.coins = 0
		self.playerChangeTime = 0 #pour changer le perso du joueur au bout d'un certain teù^s

		#SCORING
		self.distance = 0

		#IMAGES
		sprites = ["walk1","walk2","walk3","walk4","walk3","walk2","Dead","DeadFall"] #tous les sprites du joueur
		self.player = "player_Blue" #On commence avec le personn age bleu
		self.players = ["player_Blue","player_Green","player_Grey","player_Red"]
		for player in self.players: #Pour chacune des couleurs de personnage
			LIST_name = player+"_Images" 
			setattr(self, LIST_name, []) #on va créer une liste des sprites du perso
			for sprite in sprites: #pour chaque sprite, on va le chercher dans le répertoire, et on l'ajoute dans la liste
				img_rep = "IMAGES/"+player.lower()+"/player_"+str(sprite)+".png"
				img_name = "image"+sprite+player
				image = pygame.image.load(img_rep).convert_alpha()
				setattr(self, img_name, image) #on associe l'image à la variable player.{img_name}
				exec("self."+LIST_name+".append(self."+"image"+str(sprite)+player+")") #ajout à la liste

		self.persos = {"player_Blue":self.player_Blue_Images,"player_Green":self.player_Green_Images,"player_Grey":self.player_Grey_Images,"player_Red":self.player_Red_Images} #dictionnaire contenant les persos et leurs listes d'images

		self.imageNumber = 0
		self.image = self.player_Blue_Images[self.imageNumber] #on commence par les sprites du personnage bleu

		self.bubble = pygame.image.load("IMAGES/player_red/bubble.png").convert_alpha() #bulle protectrice autour de red
		self.bubbleRect = self.bubble.get_rect()
		#RECT
		self.rect = self.image.get_rect() #on obtient le rectangle et le placons
		self.rect.x = self.posX
		self.rect.y = self.posY

		#FORCES ET MOUVEMENTS
		self.isJumping = False #On définit les variables d'état du joueur
		self.hasLanded = False
		self.speed = 0.05
		self.XForce = 0  #on definit des forces qui s'appliquent en x et y au joueur
		self.YForce = 0
		self.g = 0.01 #une gravite s'appliquant aux forces en y
		self.playersMass = {"player_Blue":1,"player_Green":1.5,"player_Grey":1,"player_Red":1} #la masse des differents joueurs qui affectent la force Y lors de la chute

		#GROUPE DE RENDU
		playerGroup.add(self)

	def update(self):
		if not self.player=="player_Blue": #changer le joueur au bout d'un certain temps..
			self.playerChangeTime+=1
		if self.playerChangeTime>=3000:
			anim = ANIMATIONS(player.rect.x,player.rect.y)
			animations.add(anim)
			self.playerChangeTime=0
			self.player = "player_Blue"

		if int(self.XForce) != 0: #si le joueur subit une force laterale, on change d'image
			self.imageNumber += 1/15
			self.imageNumber%=6
		else:
			self.imageNumber= 2*(self.isJumping) #s'il saute, on affiche l'image de saut sinon le joueur est au repos

		if self.posY>height_screen: #si le joueur tombe il reapparait en haut
			self.posY = 0
			self.lives-=1 

		if self.posX<-45 or self.posX>width_screen: #si le joueur disparait sur un bord il revient dans le jeu
			self.posX=470
			self.posY=200
			self.lives-=1

		self.image = self.persos[self.player][int(self.imageNumber)] #l'image est cherchee dans la liste du bon joueur, suivant le numero de l'image dans la liste
		if self.player=="player_Red": #si on est red, on affiche aussi sa bulle
			self.bubbleRect.x = self.rect.x-33
			self.bubbleRect.y = self.rect.y-30
			screen.blit(self.bubble,self.bubbleRect)

		self.rect = self.image.get_rect()

		self.rect.x = self.posX #on update les coordonnees du rect
		self.rect.y = self.posY

		if self.lives <= 0 and not self.isdead: #Quand on a plus de vies..
			self.isdead = True #..et bah on meurt..
			self.isDead() #lancement de l'animation de mort

		if not self.hasLanded and not self.isJumping: #si le joueur n'est pas sur une plateforme
			self.Fall()

		if self.isJumping:
			self.Jump()

		for platform in platforms: #collisions
			if self.rect.colliderect(platform.rect):
				if self.rect.bottom<platform.rect.top+30: #si on est sur la plateforme
					self.posY+=platform.rect.top-self.rect.bottom+1
					self.hasLanded = True
					self.YForce = 0
					self.isJumping = False
				else:
					self.hasLanded = False

				if self.rect.right>platform.rect.left and self.rect.right-40<platform.rect.left and self.rect.bottom>platform.rect.top+30: #si on arrive par la droite de la plateforme
					self.XForce = -globalSpeed*1.2
				elif self.rect.left<platform.rect.right and self.rect.left+40>platform.rect.right and self.rect.bottom>platform.rect.top+30: #de meme a gauche
					self.XForce = 0
			else:
				self.hasLanded = False

	def move(self):
		self.posX += self.XForce    #deplacement lateral
		# self.distance+=self.XForce

	def Jump(self):
		self.posY-=self.YForce #deplacement vertical
		self.YForce -= self.g*self.playersMass[player.player] #YForce est positive puis negative

	def Fall(self):
		self.posY-=self.YForce #chute
		self.YForce -= self.g*self.playersMass[player.player] #incrémentation de la force de chute

	def isDead(self): #le joueur est mort, on joue une animation
		exec("self.image=self.imageDead"+str(self.player)) #on change l'image et update l'ecran
		ALLTYPES = {platforms,enemies,coins,discs,powerups,decors}
		screen.fill(BACKCOLOR)
		game.UI() 
		clouds.update()
		clouds.draw(screen)
		playerGroup.draw(screen)
		animations.update()
		for Type in ALLTYPES:
			Type.update()
			Type.draw(screen)
		screen.blit(water,(0,576))
		pygame.display.update() #maj de l'ecran
		time.sleep(0.5)
		exec("self.image=self.imageDeadFall"+str(self.player))
		self.YForce = 2.5
		self.g*=2

		while self.posY<height_screen: #on fait chuter le joueur, tout en updatant l'ecran
			ALLTYPES = {platforms,enemies,coins,discs,powerups,decors}
			screen.fill(BACKCOLOR)
			game.UI() 
			clouds.update()
			clouds.draw(screen)
			self.Fall()
			self.rect.y = self.posY
			playerGroup.draw(screen)
			animations.update()
			for Type in ALLTYPES:
				Type.update()
				Type.draw(screen)
			screen.blit(water,(0,576))
			pygame.display.update() #maj de l'ecran
			fpsClock.tick(FPS)
			pygame.time.wait(1)

		#on quitte le jeu, direction le menu
		game.Menu()

########################################################################################################################
#Environnement##########################################################################################################
########################################################################################################################
#decor instancié par plateforme : mouvement + suppression
########################################################################################################################
class ENVIRONNEMENT(pygame.sprite.Sprite):
	def __init__(self,x,platform):
		pygame.sprite.Sprite.__init__(self)
		#IMAGES
		self.modele = seasons_list[game.GeneratedSeason][random.randint(0,len(seasons_list[game.GeneratedSeason])-1)] #on choisit un fichier dans les differents decprs
		self.image = pygame.image.load(ENV+game.GeneratedSeason+'/'+self.modele).convert_alpha() #on charge l'image
		self.rect = self.image.get_rect()

		#GLOBAL
		self.doDisplay = True #affichage de l'image?
		self.platform = platform
		self.y = self.rect.height
		self.rect.x = self.platform.rect.x +x
		self.rect.y = self.platform.rect.y - self.y
		if self.rect.width+20>self.platform.rect.width: #si l'image est plus large que sa plateforme
			self.doDisplay = False

		if self.rect.right>self.platform.rect.right: #si l'image depasse sur la droite, on la decale
			self.rect.x-=self.rect.right-platform.rect.right+20

	def update(self):
		if self.doDisplay:
			self.rect.x -= globalSpeed #deplacement vers la gauche
		else:
			self.delete()

	def delete(self):
		self.kill()


########################################################################################################################
#Plateformes qui se deplacent###########################################################################################
########################################################################################################################
#nouvelle plateforme + nouveaux attributs(decor/piece/bonus/ennemi) + deplacement
########################################################################################################################
class PLATFORM(pygame.sprite.Sprite):
	def __init__(self,x,size,y,season):
		pygame.sprite.Sprite.__init__(self)
		#PARAMETERS
		self.size = size #la longueur de la plateforme
		self.season = season
		self.image = pygame.image.load(TILES+str(self.season)+"/"+str(self.size)+".png").convert_alpha() #on charge l'image correspondante

		#GLOBAL
		self.posX = width_screen+x
		self.posY = y
		self.enemy = None #ennemis, pièces, bonus ou décors présents sur la plateforme
		self.coin = None
		self.powerup = None
		self.decors = None
		
		#COLLISIONS
		self.rect = self.image.get_rect().inflate(10,0) #on grossit de 5px de chaque cote le rect pour ameliorer la detection des collisions
		self.rect.x = self.posX
		self.rect.y = self.posY*52

	def update(self):
		if self.posX < -64*self.size: #si la plateforme disparait à gauche de l'ecran, on la recharge
			player.distance += 1
			game.platformCount+=1
			if game.platformCount == game.lenSeason: #changement de la saison
				game.lenSeason = random.randint(5,10)
				game.platformCount = 0
				game.GeneratedSeason = seasons[random.randint(0,3)]

			self.posX = game.lastPlatformX+ width_screen #nouvelles positions
			self.posY=game.lastPlatformY
			while game.lastPlatformY-self.posY > 2 or self.posY == game.lastPlatformY: #si trop grande différence de hauteur entre 2 plateformes
				self.posY = random.randint(3,10)


			game.lastPlatformSize=self.size
			game.lastPlatformY = self.posY
			game.lastPlatformX = width_screen

			self.size = random.randint(2,5)  #nouveaux attributs
			self.season = game.GeneratedSeason
			self.image = pygame.image.load(TILES+str(self.season)+"/"+str(self.size)+".png").convert_alpha()
			self.rect = self.image.get_rect().inflate(10,0)
			self.rect.x = self.posX
			self.rect.y = self.posY*52

			if self.powerup: #on supprime les anciens attributs
					self.powerup.delete()
					self.powerup = None
			if self.enemy:
					self.enemy.die()
					self.enemy = None
			if self.coin:
					self.coin.delete()
					self.coin = None
			if self.decors:
					self.decors.delete()
					self.decors = None

			#on rajoute de nouveaux attributs suivant des probabilités
			if random.randint(0,proba_enemy)==1 and len(enemies)<=2: #nouvel ennemi si y'en a au max 3 sur l'ecran
				enemy = ENEMY(["Flying","Walking","Floating"][random.randint(0,2)],random.randint(self.size,(self.size-1)*64),self)
				enemies.add(enemy)
				self.enemy = enemy
			elif random.randint(0,proba_coin)==1 and len(coins)<=2:
				coin = COIN(50,50,self)
				coins.add(coin)
				self.coin = coin
			elif random.randint(0,proba_powerup)==1 and len(powerups)==0:
				powerup = POWERUP(50,50,self)
				powerups.add(powerup)
				self.powerup = powerup
			if random.randint(0,proba_env)==1:
				decor = ENVIRONNEMENT(random.randint(0,(self.size-1)*64),self)
				decors.add(decor)
				self.decors = decor
			

		#deplacement de la plateforme
		self.posX -= globalSpeed
		self.rect.x = self.posX
		self.rect.y = self.posY*52


########################################################################################################################
#Nuages en fond ########################################################################################################
########################################################################################################################
#deplacement + nouveau nuage
########################################################################################################################
class CLOUD(pygame.sprite.Sprite):
	def __init__(self,x,y,speed):
		pygame.sprite.Sprite.__init__(self)
		#GLOBAL
		self.speed = (speed-2*sens*speed)/random.randint(30,50) #vitesse
		self.posX = x
		self.posY = y

		#IMAGES AND COLLISIONS
		self.image = pygame.image.load("IMAGES/CLOUDS/cloud"+str(random.randint(1,8))+".png").convert_alpha() #on charge une image aléatoire
		self.rect = self.image.get_rect()
		self.rect.x = self.posX
		self.rect.y = self.posY

	def update(self):
		self.posX += self.speed
		if self.posX>width_screen or self.posX<-98: #si on sort de l'ecran, on redifinit nos proprietes avant de reaparaitre de l"autre cote
			self.posX=-98+sens*(width_screen+98)
			self.posY = random.randint(0,512)
			self.speed = (random.randint(8,15)-2*sens*random.randint(8,15))/random.randint(30,50)
			self.image = pygame.image.load("IMAGES/CLOUDS/cloud"+str(random.randint(1,8))+".png").convert_alpha()
			self.rect = self.image.get_rect()


		self.rect.x = self.posX #deplacement
		self.rect.y = self.posY

########################################################################################################################
#Disque d'attaque de Grey###############################################################################################
########################################################################################################################
#disque lancé par grey contre un ennemi : deplacement + detection collision ennemi + suppression
########################################################################################################################
class DISC(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#GLOBAL
		self.speed = 10

		#IMAGE AND COLLISIONS
		self.image = pygame.image.load("IMAGES/player_grey/disc.png").convert_alpha() #on charge l'image
		self.rect = self.image.get_rect() #on obtient son rectangle
		self.rect.x = player.posX + 10
		self.rect.y = player.posY +10

	def update(self):
		self.rect.x += self.speed #deplacement
		for enemy in enemies: #si on touche un ennemi
				if self.rect.colliderect(enemy.rect):
					coin = COIN(enemy.x,50,enemy.platform) #on le remplace par un coin
					coins.add(coin)
					platform.coin = coin
					enemy.die() # on retire l'ennemi et le disque
					self.kill()
					return

		if self.rect.x > width_screen: #on le supprime si il est sorti de l'ecran
			self.kill()


########################################################################################################################
#Types : Flying, Walking, Floating######################################################################################
########################################################################################################################
#ennemi se déplacant en marchant, flottant ou volant : animation et deplacement + mort + animation de projection au contact de red 
########################################################################################################################
class ENEMY(pygame.sprite.Sprite):
	def __init__(self,EnemyType,x,platform):
		pygame.sprite.Sprite.__init__(self)
		#PARAMETERS
		self.x = x
		self.speed = 0.25
		self.direction = 1 #1:droite,-1:gauche

		#GLOBAL
		self.platform = platform #plateforme à laquelle il est lie
		self.yMove = 0 #le deplacement en x et y de l'ennemi par rapport à sa plateforme attachee
		self.xMove = 0
		self.isAlive = True

		#IMAGES AND ANIMATIONS
		types = ["Flying","Walking","Floating"] #3 types d'ennemis
		self.type = EnemyType

		sprites = ["1","2","3","dead"] #differents sprites de l'ennemi

		for Type in types: #on charge tous ses sprites en parcourant les listes et on les associe à l'instance de classe

			for sprite_name in sprites:
				image="IMAGES/enemy_"+Type+"/"+sprite_name+".png"
				setattr(self, str("img"+sprite_name+Type),pygame.image.load(image).convert_alpha())

		self.imgsFlying = [self.img1Flying,self.img2Flying,self.img3Flying,self.img2Flying] #on definit une animation pour chaque ennemi
		self.imgsWalking = [self.img1Walking,self.img2Walking,self.img3Walking,self.img2Walking]
		self.imgsFloating = [self.img1Floating,self.img2Floating,self.img3Floating,self.img2Floating]

		self.enemies = {"Flying":self.imgsFlying,"Walking":self.imgsWalking,"Floating":self.imgsFloating} #on associe le type de l'ennemi à une animation

		self.imgNumber = 0
		self.image = self.enemies[self.type][self.imgNumber]
		self.imgPersistance = {"Flying":0.04,"Walking":0.02,"Floating":0.02} #les durees relatives d'affichage des images
		self.animations = {"Flying":"self.flying()","Walking":"self.walking()","Floating":"self.floating()"} #on associe le type de l'ennemi aux fonctions d'animations

		#COLLISIONS
		self.rect = self.image.get_rect()

		#PUSHED
		self.XForce = 0 #les forces de l'animation de projection
		self.YForce = 0
		self.angle = 0


	def update(self):
		if self.isAlive: #si l'ennemi est vivant, on l'anime et le deplace
			self.image = self.enemies[self.type][int(self.imgNumber)]
			self.rect = self.image.get_rect()
			self.rect.x = self.platform.posX + self.x + self.xMove #positions liees à sa plateforme, au decalage initial par rapport à elle, et au mouvement de l'ennemi
			self.rect.y = self.platform.posY*52-self.rect.height + self.yMove
			self.imgNumber+=self.imgPersistance[self.type]
			self.imgNumber%=4

			exec(self.animations[self.type]) #on lance sa fonction correspondante (flying,floating ou walking)

			if self.rect.colliderect(player.rect): #collision avec un joueur
				player.lives-=1
				self.isAlive = False
				self.die()

			if player.player=="player_Red" and self.rect.colliderect(player.bubbleRect): #collision avec red
				self.isAlive = False
				coin = COIN(self.x,self.platform.rect.y-self.rect.y,self.platform) #on crée une pièce
				coins.add(coin)
				angle = random.randint(0,75)
				self.XForce = math.fabs(math.degrees(math.cos(angle)))/10
				self.YForce = math.degrees(math.sin(angle))/10
		else:
			self.pushed() #projection


	def die(self): #l'ennemi est mort
		self.kill()
		self.platform.enemy = None


	def pushed(self):
		if self.rect.x>width_screen or self.rect.y<0 or self.rect.y>height_screen: #quand on n'est plus visible sur l'ecran
			self.die()
		exec("self.image = self.imgdead"+self.type) #image de l'ennemi mort
		self.angle+=5%360 
		self.image = pygame.transform.rotate(self.image, self.angle) #on fait tourner l'image
		self.imgNumber+=self.imgPersistance[self.type] #on change l'image suivant le taux de rafraichissement
		self.imgNumber%=4 

		self.rect.x += self.XForce #deplacements
		self.rect.y -= self.YForce

	def flying(self): #ennemi qui vole
		self.yMove += (self.direction==-1)*self.speed - (self.direction==1)*self.speed #on definit un decalage y pour son deplacement
		#changement de direction
		if self.rect.bottom>self.platform.rect.top:
			self.direction = 1
		elif self.rect.bottom+40<self.platform.rect.top:
			self.direction = -1


	def walking(self): #ennemi qui marche
		self.xMove += (self.direction==-1)*self.speed - (self.direction==1)*self.speed #on definit un decalage x pour son deplacement
		#changement de direction au bout de la plateforme:
		if self.rect.right>self.platform.rect.right:
			self.direction = 1
		if self.rect.left<self.platform.rect.left:
			self.direction = -1

	def floating(self): #ennemi qui flotte
		self.yMove += (self.direction==-1)*self.speed - (self.direction==1)*self.speed #on definit un decalage y pour son deplacement
		#changement de direction
		if self.rect.bottom>self.platform.rect.top:
			self.direction=1
		if self.rect.bottom+10<self.platform.rect.top:
			self.direction = -1

########################################################################################################################
#Objets : Bonus#########################################################################################################
########################################################################################################################
#deplacement + collision avec joueur + changer joueur et animation + suppression
########################################################################################################################
class POWERUP(pygame.sprite.Sprite):
	def __init__(self,x,y,platform):
		pygame.sprite.Sprite.__init__(self)
		#GLOBAL
		self.platform = platform
		self.x = x
		self.y = y

		#IMAGES and RECT
		self.image = pygame.image.load(OBJECTS+"powerup_empty.png").convert_alpha()
		self.rect = self.image.get_rect()

	def update(self):
		self.rect.x = self.platform.posX + self.x #deplacement
		self.rect.y = self.platform.posY*51 - self.y

		if self.rect.colliderect(player.rect): #si le joueur prend le bonus
			player.playerChangeTime = 0 #on remet le temps de bonus à 0
			anim = ANIMATIONS(player.rect.x,player.rect.y) #on créé l'animation de cercle
			animations.add(anim)
			NewPlayer = player.player
			while NewPlayer==player.player: # on change le joueur
				NewPlayer = random.choice(player.players)
			player.player = NewPlayer
			self.platform.powerup = None
			self.delete()

	def delete(self):
		self.kill()

########################################################################################################################
#Objets : Pièces########################################################################################################
########################################################################################################################
#deplacement + animation rotation + collision joueur + deplacement vers tas de pièces + suppression
########################################################################################################################
class COIN(pygame.sprite.Sprite):
	def __init__(self,x,y,platform):
		pygame.sprite.Sprite.__init__(self)
		#GLOBAL
		self.platform = platform
		self.x = x
		self.y = y

		#IMAGES AND ANIMATIONS
		self.sprites = ["coin1","coin2","coin3","coin4","coin5","coin6"]
		for sprite in self.sprites:
			setattr(self,sprite,pygame.image.load(OBJECTS+sprite+".png").convert_alpha()) # on charge les images
		self.animation = [self.coin1,self.coin2,self.coin3,self.coin4,self.coin5,self.coin6] #ordre de l'animation
		self.animNumber = 0
		self.image = self.animation[self.animNumber]

		#COLLISIONS
		self.rect = self.image.get_rect()

		#GO
		self.took = False #si le joueur a pris la piece
		self.Xmove = 0
		self.Ymove = 0

	def update(self):
		self.animNumber+=0.05 #animation rotation
		self.animNumber%=6
		self.image = self.animation[int(self.animNumber)]

		if not self.took: #si elle n'est pas encore prise : on anime et deplace
			self.rect = self.image.get_rect()

			self.rect.x = self.platform.posX + self.x #on suit la plateforme liee, et en induisant le decalage de la pos de la pièce
			self.rect.y = self.platform.posY*51 - self.y #de même

			if self.rect.colliderect(player.rect): #si le joueur prend la pièce
				self.platform.coin = None
				self.Xmove = 1280-self.rect.x
				self.Ymove = self.rect.y-10
				self.took = True
		else: #on déplace la piece jusqu'au tas
			self.go()

	def go(self): #deplacement vers le tas en utilisant un coefficient directeur
		if self.rect.x <= 1280 and self.rect.y >=10:

			self.Xmove = 1280-self.rect.x
			self.Ymove = self.rect.y-10
			if self.Ymove%2:
				self.rect.y+=1
			if self.Ymove==0:
				self.Ymove+=1
			self.rect.x += self.Xmove/self.Ymove*4
			self.rect.y -= 4
		else:
			player.coins += 1
			self.delete()

	def delete(self):
		self.kill()

########################################################################################################################
#Animation : player prend powerup#######################################################################################
########################################################################################################################
#animation lorsque le joueur prend ou perd un bonus
########################################################################################################################
class ANIMATIONS(pygame.sprite.Sprite): #animation qui trace un cercle blanc qui s'agrandit
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		#GLOBAL
		self.x = x
		self.y = y
		self.radius = 106
		self.growSpeed = 30
		self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255)) #couleur aléatoire

	def update(self):
		self.radius+=self.growSpeed #on augmente le rayon
		pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius,10) #on le dessine
		if self.radius>width_screen: #si le cercle est assez grand, on retire l'animation du groupe
			self.kill()

########################################################################################################################
#le jeu, l'UI###########################################################################################################
########################################################################################################################
#classe gerant les variables du jeu et l'affichage des pièces et vies
########################################################################################################################
class GAME():
	def __init__(self):
		#GESTION GLOBALE
		self.GAME = True #variable de boucle de jeu
		self.lastPlatformY = 11  #3 variables sur la derniere plateforme (utilisé pour limiter la difference de hauteur entre 2 plateformes)
		self.lastPlatformSize = 5
		self.lastPlatformX = 3456
		self.platformCount = 0
		self.lenSeason = random.randint(5,10) #durée de la saison
		self.GeneratedSeason = seasons[random.randint(0,3)] 

		#IMAGES
		#VIES
		self.heartFull = pygame.image.load(UI+"heartFull.png").convert_alpha() #chargement des images pour l'UI
		self.numbers = []

		#PIECES
		for i in range(10):
			self.numbers.append(pygame.image.load(NUMBERS+str(i)+".png").convert_alpha()) #on charge les images des nombres
		spritesCoin = ["coin"+str(i+1) for i in range(6)]
		for sprite in spritesCoin: #on charge les images des pièces
			setattr(self,sprite,pygame.image.load(OBJECTS+sprite+".png").convert_alpha())

		#COIN ANIMATION
		self.animationCoin = [self.coin1,self.coin2,self.coin3,self.coin4,self.coin5,self.coin6] #ordre de l'animation
		self.animNumber = 0
		self.imgCoin = self.animationCoin[self.animNumber]


	def UI(self): #affichage
		x = 60
		live = 0

		for live in range(player.lives):
			screen.blit(self.heartFull,((live+1)*x,10)) #afficher le nombre de coeurs correspondant

		if player.coins==10: #+1vie au bout de 10 pièces
			player.coins = 0
			player.lives+=1

		self.animNumber+=0.05 
		self.animNumber%=6
		self.imgCoin = self.animationCoin[int(self.animNumber)]
		screen.blit(self.imgCoin,(1300,10))
		screen.blit(self.numbers[int(player.coins)],(1267,15)) #afficher le nombre de pièces et l'image pièce

	########################################################################################################################
	#Mise à jour de l'ecran#################################################################################################
	########################################################################################################################
	def ScreenDisplay(self): #on update l'ecran
		#Group.clear(screen, background) efface la zone du sprite en remplacant avec background, sur le screen
		#Group.update() appelle la fonction update de tous les membres du groupe
		#Group.draw(screen) dessine chaque sprite à l'ecran avec son rect et son image sur le screen
		player.move()
		player.XForce += (player.XForce<0)*player.speed*1/3 - (player.XForce>0)*player.speed*1/3

		ALLTYPES = {platforms,enemies,coins,discs,playerGroup,powerups}
		screen.fill(BACKCOLOR)
		
		self.UI() #on update l'UI
		clouds.update()
		clouds.draw(screen)
		animations.update()
		decors.update()
		decors.draw(screen)
		for Type in ALLTYPES:
			Type.update()
			Type.draw(screen)
		screen.blit(water,(0,576))
		pygame.display.update() #maj de l'ecran


	####################################################################################################################
	#Ouverture Menu#####################################################################################################
	####################################################################################################################
	def Menu(self):
		pass
		subprocess.Popen(("python","LauncherMenu.py")) #Programme annexe Menu
		game.GAME=False  #--> on sort de la boucle de jeu


"""_____________________________________________________________________________________________________________________
#Instanciation des objets###############################################################################################
¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""


player = PLAYER()
game = GAME()

for i in range(random.randint(10,20)): #instanciation des nuages pour le fond
	cloud = CLOUD(random.randint(0,width_screen),random.randint(0,512),random.randint(8,15)) #(x,y,speed)
	clouds.add(cloud) #ajout au groupe de sprites

for i in range(9): #instanciation des 6 plateformes
	platformSize = 5
	platformX = i*64*(platformSize+1)
	platformY = 10
	platform = PLATFORM(platformX,platformSize,platformY,game.GeneratedSeason) #instanciation de la class (time,size,y,season)
	platforms.add(platform) #ajout au groupe de sprites
	game.platformCount+=1


"""_____________________________________________________________________________________________________________________
#BOUCLE PRINCIPALE######################################################################################################
¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""

while game.GAME:
	fpsClock.tick(FPS) #on regule la vitesse de jeu

	for event in pygame.event.get(): #pile des evènements
		if event.type == KEYDOWN:
			###DEPLACEMENTS HORIZONTAUX
			if event.key == K_LEFT:
				player.XForce -= player.speed
			elif event.key == K_RIGHT:
				player.XForce += player.speed
			###DEPLACEMENTS VERTICAUX
			if event.key == K_UP and player.YForce == 0: #on saute si on n'est pas deja en train de sauter
				player.isJumping = True
				if player.player=="player_Green": #si on est green, on saute plus haut
					player.YForce = 5
					player.g = 0.029
				else:
					player.YForce = 3
					player.g = 0.03

			if event.key == K_DOWN and player.YForce>0:
				player.YForce = -1 #YForce<0 donc phase de chute, on donne -1 pour qu'il ait deja une vitesse de chute
			
			###LANCER UN DISQUE AVEC GREY
			if event.key == K_SPACE and player.player=="player_Grey" and len(discs)<1: #une attaque de grey à la fois
				disc = DISC()
				discs.add(disc)

		####QUITTER
		if event.type == QUIT or event.type==KEYDOWN and event.key == K_ESCAPE or game.GAME==False: #on quitte le jeu
			score=str(int(player.distance)) 
			with open("Files/Score.txt","w") as file: #on ecrit le score dans un fichier
				file.write(score)
			game.Menu()

	game.lastPlatformX-=globalSpeed
	game.ScreenDisplay() #on update et affiche tout
pygame.quit()

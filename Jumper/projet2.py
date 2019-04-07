# -*-coding:utf-8 -*-
"""
#####Dernières modifs : 7 avril a 14h53, Loïs
""" 
"""
#######################################################################################################################
#####TASKLIST :########################################################################################################
#######################################################################################################################

LOIS:#################################################################################################################
#######################################################################################################################

-scoring
-menu tkinter, lier le menu dans la boucle principale OK
-plaque de debut, qui fait que le joueur ne tombe pas direct
-aleatoire organise : 
	regles :-pas 2 plateformes qui se superposent
			-pas 2 plateformes l'une juste au dessus de l'autre
			-pas plus de 4 ou 3 hauteurs de difference de hauteur entre 2 plateformes
Le prof voulait des trucs intelligents? ca me semble bien ca :
les plaques, des arbres, fleurs ou herbes qui changent suivant la saison du jeu
-creer une class environnement
	-permet de gerer des arbres, fleurs et plantes
	-s'inspirer des classes enemy ou coin
	-chaque instance de cette classe appartiendra à une plateforme
	-passer à la classe les arguments model(le nom de l'image),x,y,platform(a qui elle "appartient")
	-dans init redeclarer les variables + image+rect
	-dans update() : juste bouger la plateforme en x et en y avec le rect en prenant la pos de la plateforme+la pos de l'env 
	-fontion delete() où on degage de la liste env_objects et où on del self
	-fonction __del__() avec juste pass dedans
-4 types d'environnement (juste de la deco, pas d'effets speciaux) :
	-blue   : tree_winter 1+2
	-brown  : tree_automn 1+2
	-green  : tree 1+2 ; grass 1+2+3
	-yellow : flowers purple+blue grass 1+2+3
	--> ca veut dire creer dans GAME() une var sur le type d'environnement (pourquoi pas les 4 saisons)
	--> var qui change tous les x cycles, x aleatoire en a et b (à definir)
	--> dans class platform
		- creer var self.environnement, que l'on efface quand la plaque disparait cf fonction update(), avec les coins, enemy et powerup (c'est le meme systeme)
		- modifier le systeme aleatoire qui genère des environnements pour qu'il s'adapte à la saison
	--> creer des listes pour chaque saison, creer une liste contenant les 4 noms de saison
		Dans Game init
		self.seasons = {"winter":self.winterList;"summer":self.summerList...}
		self.winterList = [""] #noms des images possibles de winter
	--> pour generer un environnement : season=seasons[game.season]
										environnement = season[random.randint(0,len(season))]
										instancier la classe ENVIRONNMENT avec le type defini juste au dessus, et les autres paramètres, cf fonction update(), 1ere condition dans platform
ETIENNE:###############################################################################################################
#######################################################################################################################

A RÉPARTIR :###########################################################################################################
#######################################################################################################################
"""
 
"""
#######################################################################################################################
#####Problèmes rencontrés dans le jeu, a débuguer par quelqu'un :######################################################
#######################################################################################################################
-on voit pu trop les symboles des joueurs
-1 symbole sans transparence et mal dimensionne
-mort du joueur
"""

########################################################################################################################
#IMPORTATIONS###########################################################################################################
########################################################################################################################

import pygame, os, numpy as np,time, random, math, cProfile,subprocess
from pygame.locals import* 

#INITIALISATIONS DE LA FENETRE ET PYGAME
pygame.init() #Youhouuu installe toi, le jeu commence
py_info = pygame.display.Info() #1366/768 dimensions ecran etienne
width_screen,height_screen=1366,768
pygame.display.set_caption("Jumper")
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,int(3.5/100*height_screen))#placement de la fenetre par rapport au top left
screen = pygame.display.set_mode((int(width_screen),int(height_screen-3.5/100*height_screen)))

pygame.key.set_repeat(70,5) #set_repeat(delay,interval)
pygame.display.update() #application des parametres d'affichage de la fenetre

#INITIALISATION DES VARIABLES
Game = True #--->Le jeu tourne
proba_powerup = 20
proba_coin = 10
proba_enemy = 10
proba_arbre = 5
proba_feuille = 3

sprite_numbers = ["1","2","3","4","Dead","DeadFall"] #1,2,3 et 4 sont des sprites quand le player marche
sprite_type = ["walk","walk","walk","walk","",""]

FPS = 300
sens = random.randint(0,1) #Pour sens=0, les nuages vont a droite,sinon, a gauche
globalSpeed = 2 #vitesse globale du jeu

#listes de Sprites contenant les instanciations des classes
#https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.RenderUpdates
discs = pygame.sprite.RenderUpdates()
clouds = pygame.sprite.RenderUpdates()
platforms = pygame.sprite.RenderUpdates()
enemies = pygame.sprite.RenderUpdates()
coins = pygame.sprite.RenderUpdates()
powerups = pygame.sprite.RenderUpdates()
decors = pygame.sprite.RenderUpdates() #environnement

playerGroup = pygame.sprite.RenderUpdates() #juste le joueur

#images repositories
UI="IMAGES/UI/"
NUMBERS="IMAGES/UI/NUMBERS/"
OBJECTS="IMAGES/OBJECTS/"
ENV = "IMAGES/ENVIRONNEMENT/"


########################################################################################################################
#DECLARATION DES CLASSES################################################################################################
########################################################################################################################
class PLAYER(pygame.sprite.Sprite): #Tout ce qui concerne le joueur
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#GLOBAL
		self.posX = 470  #Position en X (Par rapport au Left)
		self.posY = 200 #Position en Y (par rapport au Top)
		self.lives = 3 #Nombre de vies
		self.isdead = False #Qualite de la vie
		self.coins = 0 #Money Money Money (ABBA)

		#SCORING
		self.instantspeed = 0 #vitesse instantanee
		self.distance = 0

		#IMAGES
		self.player = "player_Blue" #On commence avec le personnage bleu
		self.players = ["player_Blue","player_Green","player_Grey","player_Red"]
		for player in self.players: #Pour chacune des couleurs de personnage
			for number in sprite_numbers: #Pour chacune des sprites par couleur
				image="IMAGES/"+player.lower()+"/player_"+str(sprite_type[sprite_numbers.index(number)]).lower()+number.lower()+".png"
				setattr(self, str("image"+number+player[7:]),pygame.image.load(image).convert_alpha()) #lie self.imageXcolor a la position de son image

		self.imagesBlue = [self.image1Blue,self.image2Blue,self.image3Blue,self.image4Blue,self.image3Blue,self.image2Blue] #Ordre d'apparition des Sprites en marche
		self.imagesGreen = [self.image1Green,self.image2Green,self.image3Green,self.image4Green,self.image3Green,self.image2Green]
		self.imagesGrey = [self.image1Grey,self.image2Grey,self.image3Grey,self.image4Grey,self.image3Grey,self.image2Grey]
		self.imagesRed = [self.image1Red,self.image2Red,self.image3Red,self.image4Red,self.image3Red,self.image2Red]

		self.persos = {"player_Blue":self.imagesBlue,"player_Green":self.imagesGreen,"player_Grey":self.imagesGrey,"player_Red":self.imagesRed} #dictionnaire contenant les persos et leurs listes d'images

		self.imageNumber = 0
		self.image = self.imagesBlue[self.imageNumber] #on commence par les sprites du personnage bleu
		self.bubble = pygame.image.load("IMAGES/player_red/bubble.png").convert_alpha()
		self.bubbleRect = self.bubble.get_rect()

		#RECT
		self.rect = self.image.get_rect()
		self.rect.x = self.posX
		self.rect.y = self.posY

		#FORCES ET MOUVEMENTS
		self.isJumping = False #On ne saute pas
		self.hasLanded = False
		self.speed = 0.05
		self.XForce = 0  #on definit des forces qui s'appliquent en x et y au joueur
		self.YForce = 0
		self.g = 0.01 #une gravite s'appliquant aux forces en y
		self.playersMass = {"player_Blue":1,"player_Green":1.5,"player_Grey":1,"player_Red":1} #la masse des differents joueurs qui affectent la force Y lors de la chute

		#GROUPE DE RENDU
		playerGroup.add(self)

	def update(self):
		if int(self.XForce) != 0: #si le joueur subit une force laterale, on change d'image
			self.imageNumber += 1/15
		elif self.isJumping: #s'il saute, on affiche l'image de saut
			self.imageNumber = 2
		else:
			self.imageNumber = 0 #sinon le joueur est au repos

		if self.posY>height_screen: #!!!juste pour le debug
			self.posY = 0
			self.lives-=1

		if self.imageNumber > 5:
			self.imageNumber = 0

		self.image = self.persos[self.player][int(self.imageNumber)] #l'image est cherchee dans la liste du bon joueur, suivant le numero de l'image dans la liste
		if self.player=="player_Red":
			self.bubbleRect.x = self.rect.x-33
			self.bubbleRect.y = self.rect.y-30
			# pygame.draw.rect(screen,(196,233,242),self.bubbleRect)
			screen.blit(self.bubble,self.bubbleRect)

		self.rect = self.image.get_rect()

		self.rect.x = self.posX #on update les coordonnees du rect
		self.rect.y = self.posY

		if self.XForce > 0 and not self.isdead:
			self.distance+=int(self.XForce)

		if self.lives <= 0 and not self.isdead: #Quand on a plus de vies..
			self.isdead = True #..et bah on meurt..
			self.isDead() #lancement de l'animation de mort

		if not self.hasLanded and not self.isJumping: #si on a pas les pieds sur terre
			self.Fall()

		if self.isJumping:
			self.Jump()

		# platform = pygame.sprite.spritecollideany(self,platforms)
		# if platform:
		for platform in platforms:
			if self.rect.colliderect(platform.rect):
				if self.rect.bottom<platform.rect.top+30: #si on est sur la plateforme
					self.posY+=platform.rect.top-self.rect.bottom+1
					self.hasLanded = True
					self.YForce = 0
					self.isJumping = False
					# self.XForce = -globalSpeed
				else:
					self.hasLanded = False

				if self.rect.right>platform.rect.left and self.rect.right-40<platform.rect.left and self.rect.bottom>platform.rect.top+30: #si on arrive par la droite de la plateforme
					self.XForce = -globalSpeed*1.2
				elif self.rect.left<platform.rect.right and self.rect.left+40>platform.rect.right and self.rect.bottom>platform.rect.top+30: #de meme a gauche
					self.XForce = 0
			else:
				self.hasLanded = False
		#print(self.YForce)

	def move(self):
		self.posX += self.XForce    #deplacement lateral
		self.distance+=self.XForce


	def Jump(self):
		self.posY-=self.YForce
		if self.instantspeed != 0:
		   	self.posX+=self.instantspeed
		self.YForce -= self.g*self.playersMass[player.player] #YForce est positive puis negative

	def Fall(self): #quand t'as pas les pieds sur terre..
		self.posY-=self.YForce #..ben tu tombes
		self.YForce -= self.g*self.playersMass[player.player]

	def isDead(self): #le joueur est kaput, on joue une animation
		exec("self.image=self.imageDead"+str(self.player[7:])) #on change l'image et update l'ecran
		ScreenDisplay()
		time.sleep(0.5)
		exec("self.image=self.imageDeadFall"+str(self.player[7:]))
		self.YForce = 2.5

		while self.posY<height_screen: #on fait chuter le joueur, tout en updatant l'ecran
			ScreenDisplay()
			self.Fall()
			fpsClock.tick(FPS)
			pygame.time.wait(1)

		Menu()
		Game = False  #on quitte le jeu, direction le menu
		

########################################################################################################################
#le jeu, l'UI###########################################################################################################
########################################################################################################################
class GAME():
	def __init__(self):
		#IMAGES
		self.heartFull = pygame.image.load(UI+"heartFull.png").convert_alpha() #chargement des images pour l'UI
		self.heartEmpty = pygame.image.load(UI+"heartEmpty.png").convert_alpha()
		self.numbers = []
		for i in range(10):
			self.numbers.append(pygame.image.load(NUMBERS+str(i)+".png").convert_alpha()) #on charge les images des nombres
		self.discSymbol = pygame.image.load(UI+"DiscSymbol.png").convert_alpha()
		self.jumpSymbol = pygame.image.load(UI+"JumpSymbol.png").convert_alpha()
		self.shieldSymbol = pygame.image.load(UI+"ShieldSymbol.png").convert_alpha()

		self.spritesCoin = ["coin1","coin2","coin3","coin4","coin5","coin6"]
		for sprite in self.spritesCoin:
			setattr(self,sprite,pygame.image.load(OBJECTS+sprite+".png").convert_alpha())

		#COIN ANIMATION
		self.animationCoin = [self.coin1,self.coin2,self.coin3,self.coin4,self.coin5,self.coin6]
		self.animNumber = 0
		self.imgCoin = self.animationCoin[self.animNumber]

		#SYMBOLES IMAGES
		self.symboles = {"player_Blue":None,"player_Green":self.jumpSymbol,"player_Grey":self.discSymbol,"player_Red":self.shieldSymbol}

	def UI(self):
		pygame.draw.rect(screen,(196,233,242),(1166,0,1366,60))
		pygame.draw.rect(screen,(196,233,242),(0,0,1366,60))
		x = 60
		live = 0

		for live in range(player.lives):
			screen.blit(self.heartFull,((live+1)*x,10)) #afficher le nombre de coeurs correspondant

		if player.coins>9:
			player.coins = 0

		self.animNumber+=0.05
		if self.animNumber>6:
			self.animNumber = 0
		self.imgCoin = self.animationCoin[int(self.animNumber)]
		screen.blit(self.imgCoin,(width_screen*15/16,10))
		screen.blit(self.numbers[int(player.coins)],(width_screen*29/32,15)) #afficher le nombre de pièces et l'image pièce

		#on affiche les symboles correspondant au joueur
		symbol = self.symboles[player.player]
		if symbol:
			screen.blit(symbol,(10,height_screen-50))
########################################################################################################################
#Environnement##########################################################################################################
########################################################################################################################
class ENVIRONNEMENT(pygame.sprite.Sprite):
	def __init__(self,biome,modele,x,y,platform):
		pygame.sprite.Sprite.__init__(self)
		#GLOBAL
		self.platform = platform
		self.x = x
		self.y = y

		#IMAGES
		self.image = pygame.image.load(ENV+biome+modele).convert_alpha()
		self.rect = self.image.get_rect()

	def update(self):
		self.rect.x = self.platform.posX + self.x
		self.rect.y = self.platform.posY*int(height_screen/15) - self.y
########################################################################################################################
#Plateformes qui se deplacent###########################################################################################
########################################################################################################################
class PLATFORM(pygame.sprite.Sprite):
	def __init__(self,time,size,y,platform_model="tiles/green/1.png"):
		pygame.sprite.Sprite.__init__(self)
		#PARAMETERS
		self.time = time #le temps d'arrivee à l'ecran !!on modifiera
		self.size = size #la longueur
		self.t = 0
		#IMAGE
		self.image = pygame.image.load("IMAGES/tiles/green/"+str(self.size)+".png").convert_alpha()

		#GLOBAL
		self.posX = width_screen
		self.posY = y
		self.enemy = None
		self.coin = None
		self.powerup = None
		self.Artefact = None

		#COLLISIONS
		self.rect = self.image.get_rect().inflate(10,0) #on grossit de 5px de chaque cote le rect pour ameliorer la detection des collisions
		self.rect.x = self.posX
		self.rect.y = self.posY


	def update(self):
		if self.posX < -64*self.size:
			self.posX = width_screen
			self.posY = random.randint(5,10)
			self.size = random.randint(2,5)
			self.image = pygame.image.load("IMAGES/tiles/green/"+str(self.size)+".png").convert_alpha()
			self.rect = self.image.get_rect().inflate(10,0)
			if self.powerup:
					self.powerup.delete()
					self.powerup = None
			if self.enemy:
					self.enemy.die()
					self.enemy = None
			if self.coin:
					self.coin.delete()
					self.coin = None


			if random.randint(0,proba_enemy)==1 and len(enemies)<=2: #nouvel ennemi si y'en a au max 3 sur l'ecran
				enemy = ENEMY(["Flying","Walking","Floating"][random.randint(0,2)],random.randint(0,(self.size-1)*64),42,self)
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
			if random.randint(0,proba_arbre)==1:
				Arbre = ENVIRONNEMENT(["Spring Summer/","Autumn/","Winter/"][random.randint(0,2)],["tree1.png","tree2.png"] [random.randint(0,1)],random.randint(0,(self.size-1)*64),104,self)
				decors.add(Arbre)
			if random.randint(0,proba_feuille)==1:
				feuille = ENVIRONNEMENT("Spring Summer/",["flowerB.png","flowerP.png","grass1.png","grass2.png","grass3.png"] [random.randint(0,4)],random.randint(0,(self.size-1)*64),57,self)
				decors.add(feuille)

		self.t+=0.01
		if self.t>self.time: #si le temps est ecoule, on arrive à l'ecran
			self.posX -= globalSpeed
			self.rect.x = self.posX
			self.rect.y = self.posY*int(height_screen/15)


########################################################################################################################
#Nuages en fond ########################################################################################################
########################################################################################################################
class CLOUD(pygame.sprite.Sprite):
	def __init__(self,x,y,speed):
		pygame.sprite.Sprite.__init__(self)
		#GLOBAL
		self.speed = (speed-2*sens*speed)/random.randint(30,50)
		self.posX = x
		self.posY = y

		#IMAGES AND COLLISIONS
		self.image = pygame.image.load("IMAGES/CLOUDS/cloud"+str(random.randint(1,8))+".png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = self.posX
		self.rect.y = self.posY

	def update(self):
		self.posX += self.speed
		if self.posX>width_screen or self.posX<-98: #si on sort de l'ecran, on redifinit nos proprietes avant de reaparaitre de l"autre cote
			self.posX=-98+sens*(width_screen+98)
			self.posY = random.randint(0,height_screen*2/3)
			self.speed = (random.randint(8,15)-2*sens*random.randint(8,15))/random.randint(30,50)
			self.image = pygame.image.load("IMAGES/CLOUDS/cloud"+str(random.randint(1,8))+".png").convert_alpha()
			self.rect = self.image.get_rect()
		self.rect.x = self.posX
		self.rect.y = self.posY

########################################################################################################################
#Disque d'attaque de Grey###############################################################################################
########################################################################################################################
class DISC(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#GLOBAL
		self.speed = 5*(width_screen/768)
		self.posX = player.posX + 10
		self.posY = player.posY + 10

		#IMAGE AND COLLISIONS
		self.image = pygame.image.load("IMAGES/player_grey/disc.png").convert_alpha()
		self.rect = self.image.get_rect()

	def update(self):
		self.posX += self.speed
		self.rect.x = self.posX
		self.rect.y = self.posY

		for enemy in enemies: #si on touche un ennemi
				if self.rect.colliderect(enemy.rect):
					enemy.die()
					discs.remove(self)
					del self
					return

		if self.posX > width_screen: #on le supprime si il est sorti de l'ecran
			discs.remove(self)
			del self
			return

	def __del__(self):
		pass

########################################################################################################################
#Types : Flying, Walking, Floating######################################################################################
########################################################################################################################

class ENEMY(pygame.sprite.Sprite): #INFOS : (pour walking : y>=42)
	def __init__(self,EnemyType,x,y,platform):
		pygame.sprite.Sprite.__init__(self)
		#PARAMETERS
		self.x = x
		self.y = y
		self.speed = 0.25
		self.direction = 1 #1:droite,-1:gauche

		#GLOBAL
		self.platform = platform #plateforme à laquelle il est lie
		self.yMove = 0 #le deplacement en x et y de l'ennemi par rapport à sa plateforme attachee
		self.xMove = 0
		self.isAlive = True

		#IMAGES AND ANIMATIONS
		self.types = ["Flying","Walking","Floating"] #3 types d'ennemis
		self.type = EnemyType

		self.sprites = ["1","2","3","dead"] #differents sprites de l'ennemi

		for Type in self.types: #on charge tous ses sprites en parcourant les listes
			for sprite_name in self.sprites:
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
		self.XForce = 0
		self.YForce = 0


	def update(self):
		if self.isAlive:
			self.image = self.enemies[self.type][int(self.imgNumber)]
			self.rect = self.image.get_rect()
			self.rect.x = self.platform.posX + self.x + self.xMove #positions liees à sa plateforme, au decalage initial par rapport à elle, et au mouvement de l'ennemi
			self.rect.y = self.platform.posY*int(height_screen/15) - self.y + self.yMove
			self.imgNumber+=self.imgPersistance[self.type]
			if self.imgNumber>4:
				self.imgNumber = 0

			exec(self.animations[self.type])

			if self.rect.colliderect(player.rect): #collision avec un joueur
				player.lives-=1
				self.isAlive = False
				self.die()
			if player.player=="player_Red" and self.rect.colliderect(player.bubbleRect):
				self.isAlive = False
				angle = random.randint(0,75)
				self.XForce = math.fabs(math.degrees(math.cos(angle)))/10
				self.YForce = math.degrees(math.sin(angle))/10
		else:
			self.pushed()
			self.image = self.enemies[self.type][int(self.imgNumber)]
			self.imgNumber+=self.imgPersistance[self.type]
			if self.imgNumber>4:
				self.imgNumber = 0
			exec(self.animations[self.type])
			self.rect.x += self.XForce
			self.rect.y -= self.YForce

	def die(self): #l'ennemi est mort
		enemies.remove(self)
		self.platform.enemy = None
		del self

	def __del__(self): #destruction de la classe
		pass

	def pushed(self):
		if self.rect.x>width_screen or self.rect.y<0 or self.rect.y>height_screen:
			self.die()

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
		self.rect.x = self.platform.posX + self.x
		self.rect.y = self.platform.posY*int(height_screen/15) - self.y
		if self.rect.colliderect(player.rect):
			NewPlayer = player.player
			while NewPlayer==player.player:
				NewPlayer = random.choice(player.players)
			player.player = NewPlayer
			powerups.remove(self)
			self.platform.powerup = None
			del self

	def delete(self):
		powerups.remove(self)
		del self

	def __del__(self):
		pass

########################################################################################################################
#Objets : Pièces########################################################################################################
########################################################################################################################
class COIN(pygame.sprite.Sprite): #INFOS : (pour coins : y>=50)
	def __init__(self,x,y,platform):
		pygame.sprite.Sprite.__init__(self)
		#GLOBAL
		self.platform = platform
		self.x = x
		self.y = y

		#IMAGES AND ANIMATIONS
		self.sprites = ["coin1","coin2","coin3","coin4","coin5","coin6"]
		for sprite in self.sprites:
			setattr(self,sprite,pygame.image.load(OBJECTS+sprite+".png").convert_alpha())
		self.animation = [self.coin1,self.coin2,self.coin3,self.coin4,self.coin5,self.coin6]
		self.animNumber = 0
		self.image = self.animation[self.animNumber]

		#COLLISIONS
		self.rect = self.image.get_rect()


	def update(self):
		self.animNumber+=0.05
		if self.animNumber>6:
			self.animNumber = 0
		self.image = self.animation[int(self.animNumber)]
		self.rect = self.image.get_rect()

		self.rect.x = self.platform.posX + self.x #on suit la plateforme liee, et en induisant le decalage de la pos de la pièce
		self.rect.y = self.platform.posY*int(height_screen/15) - self.y #de même

		if self.rect.colliderect(player.rect): #si le joueur prend la pièce
			player.coins += 1
			self.platform.coin = None
			self.delete()

	def delete(self):
		coins.remove(self)
		del self

	def __del__(self):
		pass




########################################################################################################################
#Mise à jour de l'ecran#################################################################################################
########################################################################################################################
def ScreenDisplay(): #on update l'ecran
	#Group.clear(screen, background) efface la zone du sprite en remplacant avec background, sur le screen
	#Group.update() appelle la fonction update de tous les membres du groupe
	#Group.draw(screen) dessine chaque sprite à l'ecran avec son rect et son image sur le screen
	ALLTYPES = {platforms,enemies,coins,discs,playerGroup,powerups,decors}
	# pygame.draw.rect(screen,(196,233,242),player.bubbleRect) #effacer la bulle
	# clouds.clear(screen,background)
	# for Type in ALLTYPES:
	#     Type.clear(screen,background)

	screen.fill((196,233,242))
	game.UI() #on update l'UI

	clouds.update()
	clouds.draw(screen)
	for Type in ALLTYPES:
		Type.update()
		Type.draw(screen)

	for x in range(22):
		screen.blit(water,(x*64,704))
	for x in range(22):
		screen.blit(water,(x*64,640))
	for x in range(22):
		screen.blit(water_top,(x*64,576))
	pygame.display.update() #maj de l'ecran

########################################################################################################################
#Ouverture Menu###############################################################################################
########################################################################################################################

def Menu():
	subprocess.Popen(("python","LauncherMenu.py")) #Boucle de Menu
	pygame.quit()

########################################################################################################################
#Instanciation des objets###############################################################################################
########################################################################################################################

player = PLAYER()
game = GAME()
fpsClock = pygame.time.Clock()

background = pygame.image.load("IMAGES/background.png").convert_alpha()
water = pygame.image.load("IMAGES/fluidBlue.png").convert_alpha()
water_top = pygame.image.load("IMAGES/fluidBlue_top.png").convert_alpha()

screen.blit(background,(0,0))

for i in range(random.randint(10,20)): #instanciation des nuages pour le fond
	cloud = CLOUD(random.randint(0,width_screen),random.randint(0,height_screen*2/3),random.randint(8,15)) #(x,y,speed)
	clouds.add(cloud)


for i in range(5):
	size = random.randint(4,5)
	platform = PLATFORM(i*3,size,random.randint(5,10))
	platforms.add(platform)


########################################################################################################################
#BOUCLE PRINCIPALE######################################################################################################
########################################################################################################################
while Game:


	fpsClock.tick(FPS)

	player.move()
	player.XForce += (player.XForce<0)*player.speed*1/3 - (player.XForce>0)*player.speed*1/3

	for event in pygame.event.get(): #pile des evènements
		if event.type == QUIT or event.type==KEYDOWN and event.key == K_ESCAPE: #on quitte le jeu
			score=str(int(player.distance/1366))
			with open("Files/Score","w") as file:
				file.write(score)
			Menu()

		if event.type == KEYDOWN:
			if event.key == K_LEFT:
				player.XForce -= player.speed
			elif event.key == K_RIGHT:
				player.XForce += player.speed


			if event.key == K_UP and player.YForce == 0: #on saute si on n'est pas deja en train de sauter
				player.isJumping = True
				if player.player=="player_Green":
					player.YForce = 5
					player.g = 0.029
				else:
					player.YForce = 3
					player.g = 0.03


			if event.key == K_DOWN and player.YForce>0:
				player.YForce = -1/(height_screen/768) #YForce<0 donc phase de chute, on donne -1 pour qu'il ait deja une vitesse de chute
			if event.key == K_SPACE and player.player=="player_Grey" and len(discs)<1: #une attaque de grey à la fois
				disc = DISC()
				discs.add(disc)

			if event.key == K_TAB: #changer de joueur
				pygame.key.set_repeat(70,5) #(delay,interval)
				if player.player == "player_Red":
					player.player = player.players[0]
				else:
					player.player = player.players[player.players.index(player.player)+1]
			if event.key == K_h: #juste pour le debug
				player.lives -= 1
			if event.key == K_j:
				player.lives += 1
				Game = False


	ScreenDisplay()
	pygame.time.wait(1)

pygame.quit()
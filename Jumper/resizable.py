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
width_screen,height_screen = pygame.display.Info().current_w, pygame.display.Info().current_h
width_screen,height_screen = 683,384
pygame.display.set_caption("Jumper")
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,27) #placement de la fenetre par rapport au top left
screen = pygame.display.set_mode((int(width_screen),int(0.9673*height_screen)),RESIZABLE)

pygame.key.set_repeat(70,5) # delai pour la reception de l'evenement clavier : set_repeat(delay,interval)

#INITIALISATION DES VARIABLES
BACKCOLOR = (196,233,242) #couleur de fond du jeu
WHITE = (255,255,255)
YELLOW = (255,218,74)

#probabilites d'apparition de chaque objet :
proba_powerup = 18 #--> 1 chance sur 21
proba_coin = 5
proba_enemy = 5
proba_env = 1

#repertoires des images
UI = "IMAGES/UI/"
NUMBERS = "IMAGES/UI/NUMBERS/"
OBJECTS = "IMAGES/OBJECTS/"
ENV = "IMAGES/ENVIRONNEMENT/"
TILES = "IMAGES/tiles/"


#systeme de saisons
Decors_Autumn=os.listdir(ENV+"Autumn") #on liste tous les fichiers dans le repertoire "IMAGES/ENVIRONNEMENT/Autumn"
Decors_Spring=os.listdir(ENV+"Spring")
Decors_Summer=os.listdir(ENV+"Summer")
Decors_Winter=os.listdir(ENV+"Winter")
seasons_list = {"Autumn":Decors_Autumn,"Winter":Decors_Winter,"Spring":Decors_Spring,"Summer":Decors_Summer}
seasons = ['Winter','Autumn','Spring','Summer']

def schrink(image):
	return pygame.transform.scale(image,[int(width_screen/1366*1.77*image.get_rect().w),int(height_screen/768*1.77*image.get_rect().h)])


FPS = 175 #vitesse du jeu
fpsClock = pygame.time.Clock() #init de l'horloge

sens = random.randint(0,1) #Pour sens=0, les nuages vont a droite, sinon a gauche
globalSpeed = 2 #vitesse globale du jeu
water = schrink(pygame.image.load("IMAGES/water.png").convert_alpha()) #image de fond de l'eau

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
stars = pygame.sprite.RenderUpdates()

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
		self.posX = 0.344*width_screen  #Position en X (Par rapport au Left)
		self.posY = -700 #Position en Y (par rapport au Top) .. 700 pixels + hauts, pour tomber sur une plateforme
		self.lives = 50 #Nombre de vies
		self.isdead = False
		self.coins = 0
		self.playerChangeTime = 0 #pour changer le perso du joueur au bout d'un certain tes

		#SCORING
		self.distance = 0

		#IMAGES
		sprites = ["walk1","walk2","walk3","walk4","walk3","walk2","Dead","DeadFall"] #tous les sprites du joueur
		self.player = "player_Blue" #On commence avec le personnage bleu
		self.players = ["player_Blue","player_Green","player_Grey","player_Red"]
		for player in self.players: #Pour chacune des couleurs de personnage
			LIST_name = player+"_Images" 
			setattr(self, LIST_name, []) #on va creer une liste des sprites du perso
			for sprite in sprites: #pour chaque sprite, on va le chercher dans le repertoire, et on l'ajoute dans la liste
				img_rep = "IMAGES/"+player.lower()+"/player_"+str(sprite)+".png"
				img_name = "image"+sprite+player
				image = schrink(pygame.image.load(img_rep).convert_alpha())
				setattr(self, img_name, image) #on associe l'image a la variable player.{img_name}
				exec("self."+LIST_name+".append(self."+"image"+str(sprite)+player+")") #ajout a la liste

		self.persos = {"player_Blue":self.player_Blue_Images,"player_Green":self.player_Green_Images,"player_Grey":self.player_Grey_Images,"player_Red":self.player_Red_Images} #dictionnaire contenant les persos et leurs listes d'images

		self.imageNumber = 0
		self.image = self.player_Blue_Images[self.imageNumber] #on commence par les sprites du personnage bleu

		self.bubble = schrink(pygame.image.load("IMAGES/player_red/bubble.png").convert_alpha()) #bulle protectrice autour de red
		self.bubbleRect = self.bubble.get_rect()
		#RECT
		self.rect = self.image.get_rect() #on obtient le rectangle et le placons
		self.rect.x = self.posX
		self.rect.y = self.posY

		#FORCES ET MOUVEMENTS
		self.isJumping = False #On definit les variables d'etat du joueur
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
			self.posX=0.34*width_screen
			self.posY=0.26*height_screen
			self.lives-=1

		self.image = schrink(self.persos[self.player][int(self.imageNumber)]) #l'image est cherchee dans la liste du bon joueur, suivant le numero de l'image dans la liste
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
		self.YForce -= self.g*self.playersMass[player.player] #incrementation de la force de chute

	def isDead(self): #le joueur est mort, on joue une animation
		exec("self.image=self.imageDead"+str(self.player)) #on change l'image et update l'ecran
		ALLTYPES = {platforms,enemies,coins,discs,powerups,decors}
		BACKCOLOR=(game.red,game.green,game.blue)
		screen.fill(BACKCOLOR)
		game.UI() 
		stars.update()
		stars.draw(screen)
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
			BACKCOLOR=(game.red,game.green,game.blue)
			screen.fill(BACKCOLOR)
			game.UI() 
			stars.update()
			stars.draw(screen)
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
#decor instancie par plateforme : mouvement + suppression
########################################################################################################################
class ENVIRONNEMENT(pygame.sprite.Sprite):
	def __init__(self,x,platform):
		pygame.sprite.Sprite.__init__(self)
		#IMAGES
		self.modele = seasons_list[game.GeneratedSeason][random.randint(0,len(seasons_list[game.GeneratedSeason])-1)] #on choisit un fichier dans les differents decprs
		self.image = schrink(pygame.image.load(ENV+game.GeneratedSeason+'/'+self.modele).convert_alpha()) #on charge l'image
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
		self.image = schrink(pygame.image.load(TILES+str(self.season)+"/"+str(self.size)+".png").convert_alpha()) #on charge l'image correspondante

		#GLOBAL
		self.posX = width_screen+x
		self.posY = y
		self.enemy = None #ennemis, pieces, bonus ou decors presents sur la plateforme
		self.coin = None
		self.powerup = None
		self.decors = None
		
		#COLLISIONS
		self.rect = self.image.get_rect().inflate(10,0) #on grossit de 5px de chaque cote le rect pour ameliorer la detection des collisions
		self.rect.x = self.posX
		self.rect.y = self.posY*52*height_screen/768

	def update(self):
		if self.posX < -64*self.size: #si la plateforme disparait a gauche de l'ecran, on la recharge
			player.distance += 1
			game.platformCount+=1
			if game.platformCount == game.lenSeason: #changement de la saison
				game.lenSeason = random.randint(5,10)
				game.platformCount = 0
				game.GeneratedSeason = seasons[random.randint(0,3)]

			self.posX = game.lastPlatformX+ width_screen*width_screen/1366 #nouvelles positions
			self.posY=game.lastPlatformY

			while game.lastPlatformY-self.posY > 2 or self.posY == game.lastPlatformY: #si trop grande difference de hauteur entre 2 plateformes
				self.posY = random.randint(3,10)


			game.lastPlatformSize=self.size
			game.lastPlatformY = self.posY
			game.lastPlatformX = width_screen

			self.size = random.randint(2,5)  #nouveaux attributs
			self.season = game.GeneratedSeason
			self.image = schrink(pygame.image.load(TILES+str(self.season)+"/"+str(self.size)+".png").convert_alpha())
			self.rect = self.image.get_rect().inflate(10,0)
			self.rect.x = self.posX
			self.rect.y = self.posY*52*height_screen/768

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

			#on rajoute de nouveaux attributs suivant des probabilites
			if random.randint(0,proba_enemy) and len(enemies)<=2: #nouvel ennemi si y'en a au max 3 sur l'ecran
				enemy = ENEMY(["Flying","Walking","Floating","Static","Piranha"][random.randint(0,4)],random.randint(self.size,(self.size-1)*64),self)
				enemies.add(enemy)
				self.enemy = enemy
			elif random.randint(0,proba_coin) and len(coins)<=2:
				coin = COIN(50*width_screen/1366,50*height_screen/768,self)
				coins.add(coin)
				self.coin = coin
			elif random.randint(0,proba_powerup) and len(powerups)==0:
				powerup = POWERUP(50*width_screen/1366,50*height_screen/768,self)
				powerups.add(powerup)
				self.powerup = powerup
			if random.randint(0,proba_env):
				decor = ENVIRONNEMENT(random.randint(0,(self.size-1)*64),self)
				decors.add(decor)
				self.decors = decor
			

		#deplacement de la plateforme
		self.posX -= globalSpeed
		self.rect.x = self.posX
		self.rect.y = self.posY*52*height_screen/768


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
		self.image = schrink(pygame.image.load("IMAGES/CLOUDS/cloud"+str(random.randint(1,8))+".png").convert_alpha()) #on charge une image aleatoire
		self.rect = self.image.get_rect()
		self.rect.x = self.posX
		self.rect.y = self.posY

	def update(self):
		self.posX += self.speed
		if self.posX>width_screen or self.posX<-98: #si on sort de l'ecran, on redifinit nos proprietes avant de reaparaitre de l"autre cote
			self.posX=-98+sens*(width_screen+98)
			self.posY = random.randint(0,int(0.66*height_screen))
			self.speed = (random.randint(8,15)-2*sens*random.randint(8,15))/random.randint(30,50)
			self.image = pygame.image.load("IMAGES/CLOUDS/cloud"+str(random.randint(1,8))+".png").convert_alpha()
			self.rect = self.image.get_rect()


		self.rect.x = self.posX #deplacement
		self.rect.y = self.posY

########################################################################################################################
#Disque d'attaque de Grey###############################################################################################
########################################################################################################################
#disque lance par grey contre un ennemi : deplacement + detection collision ennemi + suppression
########################################################################################################################
class DISC(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#GLOBAL
		self.speed = 10

		#IMAGE AND COLLISIONS
		self.image = schrink(pygame.image.load("IMAGES/player_grey/disc.png").convert_alpha()) #on charge l'image
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
#ennemi se deplacant en marchant, flottant ou volant : animation et deplacement + mort + animation de projection au contact de red 
########################################################################################################################
class ENEMY(pygame.sprite.Sprite):
	def __init__(self,EnemyType,x,platform):
		pygame.sprite.Sprite.__init__(self)
		#PARAMETERS
		self.x = x
		self.speed = 0.25
		self.direction = 1 #1:droite,-1:gauche
		self.dir_changed = False

		#GLOBAL
		self.platform = platform #plateforme a laquelle il est lie
		self.yMove = 0 #le deplacement en x et y de l'ennemi par rapport a sa plateforme attachee
		self.xMove = 0
		self.isAlive = True

		#IMAGES AND ANIMATIONS
		types = ["Flying","Walking","Floating","Static","Piranha"] #4 types d'ennemis
		self.type = EnemyType

		sprites = ["1","2","3","dead"] #differents sprites de l'ennemi

		for Type in types: #on charge tous ses sprites en parcourant les listes et on les associe a l'instance de classe

			for sprite_name in sprites:
				if game.ISNIGHT:
					image="IMAGES/enemy_"+Type+"_night"+"/"+sprite_name+".png"
				else:
					image="IMAGES/enemy_"+Type+"/"+sprite_name+".png"					
				setattr(self, str("img"+sprite_name+Type),schrink(pygame.image.load(image).convert_alpha()))

		self.imgsFlying = [self.img1Flying,self.img2Flying,self.img3Flying,self.img2Flying] #on definit une animation pour chaque ennemi
		self.imgsWalking = [self.img1Walking,self.img2Walking,self.img3Walking,self.img2Walking]
		self.imgsFloating = [self.img1Floating,self.img2Floating,self.img3Floating,self.img2Floating]
		self.imgsStatic = [self.img1Static,self.img2Static,self.img3Static,self.img2Static]
		self.imgsPiranha = [self.img1Piranha,self.img2Piranha,self.img3Piranha,self.img2Piranha]

		self.enemies = {"Flying":self.imgsFlying,"Walking":self.imgsWalking,"Floating":self.imgsFloating,"Static":self.imgsStatic,"Piranha":self.imgsPiranha} #on associe le type de l'ennemi a une animation

		self.imgNumber = 0
		self.image = self.enemies[self.type][self.imgNumber]
		self.imgPersistance = {"Flying":0.04,"Walking":0.02,"Floating":0.02,"Static":0.05,"Piranha":0.02} #les durees relatives d'affichage des images
		self.animations = {"Flying":"self.flying()","Walking":"self.walking()","Floating":"self.floating()","Static":"self.static()","Piranha":"self.piranha()"} #on associe le type de l'ennemi aux fonctions d'animations

		#COLLISIONS
		self.rect = self.image.get_rect()

		#PUSHED
		self.XForce = 0 #les forces de l'animation de projection
		self.YForce = 0
		self.angle = 0


	def update(self):
		if self.isAlive: #si l'ennemi est vivant, on l'anime et le deplace
			self.image = self.enemies[self.type][int(self.imgNumber)]
			if self.dir_changed and not self.type=="Piranha":
				self.image = pygame.transform.flip(self.image,1,0)
			self.rect = self.image.get_rect()
			self.rect.x = self.platform.posX + self.x + self.xMove #positions liees a sa plateforme, au decalage initial par rapport a elle, et au mouvement de l'ennemi
			self.rect.y = self.platform.posY*52*height_screen/768-self.rect.height + self.yMove
			if not self.type=="Piranha":
				self.imgNumber+=self.imgPersistance[self.type]
				self.imgNumber%=4
			elif self.direction==1:
				self.image = self.img1Piranha
			else:
				self.image = self.img2Piranha

			exec(self.animations[self.type]) #on lance sa fonction correspondante (flying,floating ou walking)

			if self.rect.colliderect(player.rect): #collision avec un joueur
				player.lives-=1
				self.isAlive = False
				self.die()

			if player.player=="player_Red" and self.rect.colliderect(player.bubbleRect): #collision avec red
				self.isAlive = False
				coin = COIN(self.x,self.platform.rect.y-self.rect.y,self.platform) #on cree une piece
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
			self.dir_changed = not self.dir_changed
		if self.rect.left<self.platform.rect.left:
			self.direction = -1
			self.dir_changed = not self.dir_changed

	def floating(self): #ennemi qui flotte
		self.yMove += (self.direction==-1)*self.speed - (self.direction==1)*self.speed #on definit un decalage y pour son deplacement
		#changement de direction
		if self.rect.bottom>self.platform.rect.top:
			self.direction=1
		if self.rect.bottom+10<self.platform.rect.top:
			self.direction = -1

	def static(self):
		pass

	def piranha(self):
		self.yMove += (self.direction==-1)*self.speed*10 - (self.direction==1)*self.speed*10 #on definit un decalage y pour son deplacement
		#changement de direction
		if self.rect.bottom>height_screen+200:
			self.direction = 1
		elif self.rect.bottom+40<height_screen-random.randint(300,600):
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
		self.image = schrink(pygame.image.load(OBJECTS+"powerup_empty.png").convert_alpha())
		self.rect = self.image.get_rect()

	def update(self):
		self.rect.x = self.platform.posX + self.x #deplacement
		self.rect.y = self.platform.posY*51*width_screen/1366 - self.y

		if self.rect.colliderect(player.rect): #si le joueur prend le bonus
			player.playerChangeTime = 0 #on remet le temps de bonus a 0
			anim = ANIMATIONS(player.rect.x,player.rect.y) #on cree l'animation de cercle
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
#Objets : Pieces########################################################################################################
########################################################################################################################
#deplacement + animation rotation + collision joueur + deplacement vers tas de pieces + suppression
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
			setattr(self,sprite,schrink(pygame.image.load(OBJECTS+sprite+".png").convert_alpha())) # on charge les images
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

			self.rect.x = self.platform.posX + self.x #on suit la plateforme liee, et en induisant le decalage de la pos de la piece
			self.rect.y = self.platform.posY*51*height_screen/768 - self.y #de meme

			if self.rect.colliderect(player.rect): #si le joueur prend la piece
				self.platform.coin = None
				self.Xmove = 0.937*width_screen-self.rect.x
				self.Ymove = self.rect.y-10
				self.took = True
		else: #on deplace la piece jusqu'au tas
			self.go()

	def go(self): #deplacement vers le tas en utilisant un coefficient directeur
		if self.rect.x <= 0.937*width_screen and self.rect.y >=10:

			self.Xmove = 0.937*width_screen-self.rect.x
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
		self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255)) #couleur aleatoire

	def update(self):
		self.radius+=self.growSpeed #on augmente le rayon
		pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius,10) #on le dessine
		if self.radius>width_screen: #si le cercle est assez grand, on retire l'animation du groupe
			self.kill()

class STAR(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		stars.add(self)
		game.stars_list.append(self)
		self.image = pygame.image.load(ENV+"star.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x=random.randint(0,1366)
		self.rect.y=random.randint(0,200)

	def delete():
		self.kill()

########################################################################################################################
#le jeu, l'UI###########################################################################################################
########################################################################################################################
#classe gerant les variables du jeu et l'affichage des pieces et vies
########################################################################################################################
class GAME():
	def __init__(self):
		#GESTION GLOBALE
		self.GAME = True #variable de boucle de jeu
		self.lastPlatformY = 11  #3 variables sur la derniere plateforme (utilise pour limiter la difference de hauteur entre 2 plateformes)
		self.lastPlatformSize = 5
		self.lastPlatformX = 3456
		self.platformCount = 0
		self.lenSeason = random.randint(5,10) #duree de la saison
		self.GeneratedSeason = seasons[random.randint(0,3)] 
		self.blue = 242
		self.red = 196
		self.green = 233
		self.dir_color = -1
		self.time_color = 0
		self.max_time_color = 4000
		self.night = (64,17,142) 
		self.day = (196,233,242)
		self.night_mode = "day"
		self.stars_list = []

		#IMAGES
		self.moon_img = schrink(pygame.image.load("IMAGES/moon.png").convert_alpha())
		self.moon_rect = self.moon_img.get_rect()
		self.moon_rect.x = 0
		self.moon_rect.y = height_screen/2
		self.moon_angle = 0

		self.sun_img = schrink(pygame.image.load("IMAGES/sun.png").convert_alpha())
		self.sun_rect = self.moon_img.get_rect()
		self.sun_rect.x = width_screen
		self.sun_rect.y = height_screen/2
		self.sun_angle = math.pi

		self.ISNIGHT = False

		#VIES
		self.heartFull = schrink(pygame.image.load(UI+"heartFull.png").convert_alpha()) #chargement des images pour l'UI
		self.numbers = []

		#PIECES
		for i in range(10):
			self.numbers.append(schrink(pygame.image.load(NUMBERS+str(i)+".png").convert_alpha())) #on charge les images des nombres
		spritesCoin = ["coin"+str(i+1) for i in range(6)]
		for sprite in spritesCoin: #on charge les images des pieces
			setattr(self,sprite,schrink(pygame.image.load(OBJECTS+sprite+".png").convert_alpha()))

		#COIN ANIMATION
		self.animationCoin = [self.coin1,self.coin2,self.coin3,self.coin4,self.coin5,self.coin6] #ordre de l'animation
		self.animNumber = 0
		self.imgCoin = self.animationCoin[self.animNumber]


	def UI(self): #affichage
		x = 60
		live = 0

		for live in range(player.lives):
			screen.blit(self.heartFull,((live+1)*x,10)) #afficher le nombre de coeurs correspondant

		if player.coins==10: #+1vie au bout de 10 pieces
			player.coins = 0
			player.lives+=1

		self.animNumber+=0.05 
		self.animNumber%=6
		self.imgCoin = self.animationCoin[int(self.animNumber)]
		screen.blit(self.imgCoin,(1300/1366*width_screen,10/768*height_screen))
		screen.blit(self.numbers[int(player.coins)],(1267/1366*width_screen,15/768*height_screen)) #afficher le nombre de pieces et l'image piece

	def nightMode(self):
		for i in range(random.randint(10,15)):
			star = STAR()

	def moon_sun(self):
		self.sun_rect.x = math.cos(self.sun_angle)*800/768*height_screen+width_screen/2
		self.sun_rect.y = math.sin(self.sun_angle)*800/768*height_screen+height_screen
		self.moon_rect.x = math.cos(self.moon_angle)*800/768*height_screen+width_screen/2
		self.moon_rect.y = math.sin(self.moon_angle)*800/768*height_screen+height_screen
		self.sun_angle%=2*math.pi
		self.moon_angle%=2*math.pi
		screen.blit(self.sun_img,self.sun_rect)
		screen.blit(self.moon_img,self.moon_rect)

	########################################################################################################################
	#Mise a jour de l'ecran#################################################################################################
	########################################################################################################################
	def ScreenDisplay(self): #on update l'ecran
		#Group.clear(screen, background) efface la zone du sprite en remplacant avec background, sur le screen
		#Group.update() appelle la fonction update de tous les membres du groupe
		#Group.draw(screen) dessine chaque sprite a l'ecran avec son rect et son image sur le screen
		player.move()
		player.XForce += (player.XForce<0)*player.speed*1/3 - (player.XForce>0)*player.speed*1/3

		ALLTYPES = {platforms,enemies,coins,discs,playerGroup,powerups}



		if self.night_mode=="day":
			self.sun_angle+=math.pi/6000
			self.time_color+=1
			if self.time_color>self.max_time_color:
				self.moon_angle=math.pi
				self.night_mode="day>night"
				self.time_color=0
				self.max_time_color = 4000
				self.ISNIGHT = True

		if self.night_mode=="day>night":
			self.sun_angle+=math.pi/10000
			self.time_color+=1
			self.blue-=1/142
			self.green-=1/32
			self.red-=1/64
			if random.randint(0,200)==0:
				star = STAR()
			if self.time_color>self.max_time_color:
				self.night_mode="night"
				self.time_color=0
				self.max_time_color = 4000

		if self.night_mode=="night":
			self.moon_angle+=math.pi/6000
			self.time_color+=1
			if self.time_color>self.max_time_color:
				self.ISNIGHT = False
				self.night_mode="night>day"
				self.sun_angle=math.pi
				self.time_color=0
				self.max_time_color = 4000


		if self.night_mode=="night>day":
			try:
				if random.randint(0,100)==0:
					self.stars_list[len(self.stars_list)-1].kill()
					self.stars_list.remove(self.stars_list[len(self.stars_list)-1])
			except:
				pass
			self.moon_angle+=math.pi/10000
			self.time_color+=1
			self.blue+=1/142
			self.green+=1/32
			self.red+=1/64
			if self.time_color>self.max_time_color:
				self.night_mode="day"
				self.time_color=0
				self.max_time_color = 4000


		BACKCOLOR=(self.red,self.green,self.blue)
		screen.fill(BACKCOLOR)

		self.moon_sun()
		stars.update()
		stars.draw(screen)
		clouds.update()
		clouds.draw(screen)
		self.UI() #on update l'UI
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
		score=str(int(player.distance)) 
		with open("Files/Score.txt","w") as file: #on ecrit le score dans un fichier
			file.write(score)
		subprocess.Popen(("python","LauncherMenu.py")) #Programme annexe Menu
		game.GAME=False  #--> on sort de la boucle de jeu


"""_____________________________________________________________________________________________________________________
#Instanciation des objets###############################################################################################
¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""


player = PLAYER()
game = GAME()

for i in range(random.randint(10,15)): #instanciation des nuages pour le fond
	cloud = CLOUD(random.randint(0,width_screen),random.randint(0,512),random.randint(8,15)) #(x,y,speed)
	clouds.add(cloud) #ajout au groupe de sprites

for i in range(9): #instanciation des 6 plateformes
	platformSize = 5
	platformX = i*64*(platformSize+1)*width_screen/1366
	platformY = random.randint(7,10)
	platform = PLATFORM(platformX,platformSize,platformY,game.GeneratedSeason) #instanciation de la class (time,size,y,season)
	platforms.add(platform) #ajout au groupe de sprites
	game.platformCount+=1




"""_____________________________________________________________________________________________________________________
#BOUCLE PRINCIPALE######################################################################################################
¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨"""
lastevt = 0
while game.GAME:
	fpsClock.tick(FPS) #on regule la vitesse de jeu, pour pas que la boucle tourne trop vite
	for event in pygame.event.get(): #pile des evenements
		if event.type == VIDEORESIZE:
			
			width_screen,height_screen = event.size
			screen = pygame.display.set_mode((int(width_screen),int(height_screen)),RESIZABLE)
			globalSpeed=globalSpeed*width_screen/1366


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
			if event.key == K_SPACE and player.player=="player_Grey" and len(discs)<1: #une attaque de grey a la fois
				disc = DISC()
				discs.add(disc)

		####QUITTER
		if event.type == QUIT or event.type==KEYDOWN and event.key == K_ESCAPE or game.GAME==False: #on quitte le jeu
			game.Menu()

	game.lastPlatformX-=globalSpeed
	game.ScreenDisplay() #on update et affiche tout
pygame.quit()

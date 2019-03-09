#IMPORTATIONS
import pygame, os, numpy as np,time, random
from pygame.locals import*

#INITIALISATIONS DE LA FENETRE ET PYGAME
pygame.init()
py_info=pygame.display.Info() #1366/768 dimensions écran etienne
width_screen,height_screen=(py_info.current_w),(py_info.current_h)
pygame.display.set_caption("Jumper")
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,int(3.5/100*height_screen))#placage de la fenetre par rapport au top left
screen=pygame.display.set_mode((int(width_screen),int(height_screen-3.5/100*height_screen)))

pygame.key.set_repeat(70,5) #(delay,interval)
pygame.display.update()

#INITIALISATION DES VARIABLES
Game = True
inGame = True
inMenu = False

#DECLARATION DES CLASSES
class PLAYER():
	def __init__(self):
		self.posX = width_screen*1/4
		self.posY = 400
		self.speed = 5
		self.lives = 3
		self.isdead = False
		self.coins = 0
		self.player = "player_blue"
		self.img1Blue = pygame.image.load("IMAGES/player_blue/player_walk1.png").convert_alpha()
		self.img2Blue = pygame.image.load("IMAGES/player_blue/player_walk2.png").convert_alpha()
		self.img3Blue = pygame.image.load("IMAGES/player_blue/player_walk3.png").convert_alpha()
		self.img4Blue = pygame.image.load("IMAGES/player_blue/player_walk4.png").convert_alpha()
		self.imgDeadBlue = pygame.image.load("IMAGES/player_blue/player_dead.png").convert_alpha()
		self.imgDeadFallBlue = pygame.image.load("IMAGES/player_blue/player_fall.png").convert_alpha()

		self.img1Green = pygame.image.load("IMAGES/player_green/player_walk1.png").convert_alpha()
		self.img2Green = pygame.image.load("IMAGES/player_green/player_walk2.png").convert_alpha()
		self.img3Green = pygame.image.load("IMAGES/player_green/player_walk3.png").convert_alpha()
		self.img4Green = pygame.image.load("IMAGES/player_green/player_walk4.png").convert_alpha()
		self.imgDeadGreen = pygame.image.load("IMAGES/player_green/player_dead.png").convert_alpha()
		self.imgDeadFallGreen = pygame.image.load("IMAGES/player_green/player_fall.png").convert_alpha()

		self.img1Grey = pygame.image.load("IMAGES/player_grey/player_walk1.png").convert_alpha()
		self.img2Grey = pygame.image.load("IMAGES/player_grey/player_walk2.png").convert_alpha()
		self.img3Grey = pygame.image.load("IMAGES/player_grey/player_walk3.png").convert_alpha()
		self.img4Grey = pygame.image.load("IMAGES/player_grey/player_walk4.png").convert_alpha()
		self.imgDeadGrey = pygame.image.load("IMAGES/player_grey/player_dead.png").convert_alpha()
		self.imgDeadFallGrey = pygame.image.load("IMAGES/player_grey/player_fall.png").convert_alpha()

		self.img1Red = pygame.image.load("IMAGES/player_red/player_walk1.png").convert_alpha()
		self.img2Red = pygame.image.load("IMAGES/player_red/player_walk2.png").convert_alpha()
		self.img3Red = pygame.image.load("IMAGES/player_red/player_walk3.png").convert_alpha()
		self.img4Red = pygame.image.load("IMAGES/player_red/player_walk4.png").convert_alpha()
		self.imgDeadRed = pygame.image.load("IMAGES/player_red/player_dead.png").convert_alpha()
		self.imgDeadFallRed = pygame.image.load("IMAGES/player_red/player_fall.png").convert_alpha()

		self.imgsBlue = [self.img1Blue,self.img2Blue,self.img3Blue,self.img4Blue,self.img3Blue,self.img2Blue]
		self.imgsGreen = [self.img1Green,self.img2Green,self.img3Green,self.img4Green,self.img3Green,self.img2Green]
		self.imgsGrey = [self.img1Grey,self.img2Grey,self.img3Grey,self.img4Grey,self.img3Grey,self.img2Grey]
		self.imgsRed = [self.img1Red,self.img2Red,self.img3Red,self.img4Red,self.img3Red,self.img2Red]

		self.imgNumber = 0
		self.img = self.imgsBlue[self.imgNumber]
		self.updateImg = 0

		# self.rect
		self.isJumping = False
		self.hasLanded = False
		self.impulsion = 3
		self.g = 0.02

	def update(self):
		if self.updateImg > 5:
			self.imgNumber += 1
			self.updateImg =0
		if self.imgNumber > 5:
			self.imgNumber = 0

		if self.player == "player_blue":
			self.img = self.imgsBlue[self.imgNumber]
		elif self.player == "player_green":
			self.img = self.imgsGreen[self.imgNumber]
		elif self.player == "player_grey":
			self.img = self.imgsGrey[self.imgNumber]
		elif self.player == "player_red":
			self.img = self.imgsRed[self.imgNumber]

		screen.blit(self.img,(self.posX,self.posY))

		if self.lives <= 0 and not self.isdead:
			self.isdead = True
			self.isDead()

		if self.isJumping:
			self.Jump_Fall()

		if not self.hasLanded and not self.isJumping:
			self.impulsion = 0
			self.Jump_Fall()

		if self.posY>=400 and self.posX<1000: #ATTERISSAGE
			self.hasLanded = True
			self.isJumping = False
			if player.player=="player_green":
				self.impulsion = 5
				self.g = 0.04
			else:
				self.impulsion = 3
				self.g = 0.02
			self.imgNumber = 0

	def move(self,dir):
		self.updateImg += 1
		self.posX += self.speed*((dir=="right")-(dir=="left"))	#deplacement latéral

	def Jump_Fall(self): 
		self.posY-=self.impulsion
		self.impulsion -= self.g #impulsion est positive puis négative (impulsion [3 --> -3])

	def isDead(self):
		self.img = self.imgDeadBlue
		screen.fill((196,233,242))
		for cloud in clouds:
			cloud.update()
		game.update()
		game.UI()
		screen.blit(self.img,(self.posX,self.posY))
		pygame.display.update()
		time.sleep(2)
		self.img = self.imgDeadFall
		self.impulsion = 1.5

		while self.posY<height_screen:
			screen.fill((196,233,242))
			for cloud in clouds:
				cloud.update()
			game.update()
			game.UI()
			screen.blit(self.img,(self.posX,self.posY))
			pygame.display.update()
			self.Jump_Fall()
		inGame = False
		inMenu = True


class GAME():
	def __init__(self):
		self.heartFull = pygame.image.load("IMAGES/heartFull.png").convert_alpha()
		self.heartEmpty = pygame.image.load("IMAGES/heartEmpty.png").convert_alpha()
		self.coin = pygame.image.load("IMAGES/coin.png").convert_alpha()
		self.numbers = []
		for i in range(10):
			self.numbers.append(pygame.image.load("IMAGES/"+str(i)+".png"))
		self.discSymbol = pygame.image.load("IMAGES/DiscSymbol.png").convert_alpha()
		self.jumpSymbol = pygame.image.load("IMAGES/JumpSymbol.png").convert_alpha()

	def UI(self):
		x = 10
		live = 0
		for live in range(int(player.lives)):
			screen.blit(self.heartFull,(x,10))
			x+=60
		x = 130
		for live_empty in range(2-live):
			screen.blit(self.heartEmpty	,(x,10))
			x-=60

		screen.blit(self.coin,(width_screen*.95,10))
		screen.blit(self.numbers[int(player.coins)],(width_screen*.92,15))
		if player.player=="player_green":
			screen.blit(self.jumpSymbol,(10,height_screen-60))
		elif player.player=="player_grey":
			screen.blit(self.discSymbol,(10,height_screen-70))
		elif player.player=="player_red":
			pass			

	def update(self):	#fonctionne pas???
		print("si si je fonctionne") #ah bah nan ca marche pas..
		self.updateEnemies()
		self.updateBlocks()
		self.updateOthers()
		self.UI()

	def RandomGeneration(self):
		pass

	def updateEnemies(self):
		pass

	def updateBlocks(self):
		pass

	def updateOthers(self):
		pass

	def update(self):
		pass

	def ReadMap(self):
	    map = np.loadtxt("map.txt",delimiter=None,dtype=str)
	    for y in range(0,15):
        		block = map[y]
        		time, size = block.split(".")
        		platform = PLATFORM(int(time),int(size),y)
        		platforms.append(platform)

class PLATFORM():
	def __init__(self,time,size,y):
		self.time = time
		self.size = size
		self.img = pygame.image.load("IMAGES/tileGreen_27.png").convert_alpha()
		self.posX = 1366
		self.posY = y
		self.t = 0

	def update(self):
		self.t+=0.01
		if self.t>self.time:
			self.posX -= speed
			x = 0
			for i in range(self.size):
				screen.blit(self.img,(self.posX+x,self.posY*50))
				x += 64

class CLOUD():
	def __init__(self,x,y,speed):
		self.speed = speed/random.uniform(35,45)
		self.posX = x
		self.dir = 1
		self.posY = y
		self.img = pygame.image.load("IMAGES/cloud"+str(random.randint(1,8))+".png").convert_alpha()

	def update(self):
		self.posX += self.dir*self.speed
		screen.blit(self.img,(self.posX,self.posY))
		if self.posX>width_screen+1000:
			self.posX=-random.randint(-500,0)
			self.posY = random.randint(0,height_screen)
			self.speed = random.randint(1,10)/40

class DISC(): #disque d'attaque de grey
	def __init__(self):
		self.speed = 5
		self.posX = player.posX + 10
		self.posY = player.posY + 10
		self.img = pygame.image.load("IMAGES/disc.png").convert_alpha()

	def update(self):
		self.posX += self.speed
		screen.blit(self.img,(self.posX,self.posY))
		if self.posX > width_screen: #on le supprime si il est sorti de l'écran
			discs.remove(self)
			del self

	def __del__(self):
		pass

discs = []
clouds = []
platforms = []
player = PLAYER()
game = GAME()
# game.ReadMap()

def ScreenDisplay(): #on update l'ecran
    screen.fill((196,233,242))
    # for platform in platforms:
    	# platform.update()
    for cloud in clouds:
    	cloud.update()
    game.update()
    game.UI()
    player.update()
    for disc in discs:
    	disc.update()
    pygame.display.update()

for i in range(10):
	cloud = CLOUD(random.randint(-500,0),random.randint(0,height_screen*2/3),random.randint(1,10)) #(x,y,speed)
	clouds.append(cloud)

#BOUCLE PRINCIPALE
while Game:
	while inMenu:
		print("menu")
	while inGame:
	    for event in pygame.event.get(): #pile des évènements
	        if event.type == QUIT or event.type==KEYDOWN and event.key == K_ESCAPE: #on quitte le jeu
	            inGame = False
	            inMenu = False
	            Game = False
	        if event.type == KEYDOWN:
	        	if event.key == K_LEFT:
	        		player.move("left")
	        	if event.key == K_RIGHT:
	        		player.move("right")
	        	if event.key == K_UP and player.hasLanded: #on saute si on est déja à terre
	        		player.isJumping = True
	        	if event.key == K_DOWN and player.impulsion>0:
	        		player.impulsion = -1 #impulsion<0 donc phase de chute, on donne -1 pour qu'il ait déja une vitesse de chute
	        	if event.key == K_SPACE and player.player=="player_grey" and len(discs)<1: #une attaque de grey à la fois
	        		disc = DISC()
	        		discs.append(disc)
	        	if event.key == K_TAB: #changer de joueur
	        		if player.player=="player_blue":
	        			player.player="player_green"
	        		elif player.player=="player_green":
	        			player.player="player_grey"
	        		elif player.player=="player_grey":
	        			player.player="player_red"
	        		elif player.player=="player_red":
	        			player.player="player_blue"
	    ScreenDisplay()

pygame.quit()
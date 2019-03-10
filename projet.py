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
colors = ["Blue","Green","Grey","Red"]
sprite_number = ["1","2","3","4","Dead","DeadFall"]
sprite_type = ["walk","walk","walk","walk","",""]
sens = random.randint(0,1)
discs = []
clouds = []
platforms = []


#DECLARATION DES CLASSES
class PLAYER():
	def __init__(self):
		self.posX = int(width_screen*1/4) #Position en X (Par rapport au Left)
		self.posY = int(height_screen/2) #Position en Y (par rapport au Top)
		self.speed = 5 #Vitesse du joueur
		self.lives = 3 #Nombre de vies
		self.isdead = False #Qualité de la vie
		self.coins = 0 #Money Money Money (ABBA)
		self.player = "player_Blue"
		for color in colors:
			for number in sprite_number:
				self."img"+number+color=pygame.image.load("IMAGES/player_"+str(color).lower()+"/player_"+str(sprite_type[sprite_number.index(number)]).lower()+str(number).lower()+".png").convert_alpha()


		self.imgsBlue = [self.img1Blue,self.img2Blue,self.img3Blue,self.img4Blue,self.img3Blue,self.img2Blue] #Ordre d'apparition des Sprites
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
		self.g = 0.02*(height_screen/768) #Paramétré proportionnellement a l'ordi d'Etienne

	def update(self):
		if self.updateImg > 5:
			self.imgNumber += 1
			self.updateImg =0
		if self.imgNumber > 5:
			self.imgNumber = 0

		if self.player == "player_Blue":
			self.img = self.imgsBlue[self.imgNumber]
		elif self.player == "player_Green":
			self.img = self.imgsGreen[self.imgNumber]
		elif self.player == "player_Grey":
			self.img = self.imgsGrey[self.imgNumber]
		elif self.player == "player_Red":
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

		if self.posY>=1/4*height_screen and self.posX<=height_screen*3/4: #ATTERISSAGE
			self.hasLanded = True
			self.isJumping = False
			if player.player=="player_Green":
				self.impulsion = 5
				self.g = 0.04*(height_screen/768)
			else:
				self.impulsion = 3
				self.g = 0.02*(height_screen/768)
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
		x = 60
		for live in range(player.lives):
			screen.blit(self.heartFull,(width_screen*2/32+(live-1)*x,height_screen*1/15))
		for live_empty in range(2-live):
			screen.blit(self.heartEmpty	,(width_screen*2/32+(live-1)*x,height_screen*1/15))

		screen.blit(self.coin,(width_screen*15/16,height_screen*1/15))
		screen.blit(self.numbers[int(player.coins)],(width_screen*29/32,height_screen*1/15))
		if player.player=="player_Green":
			screen.blit(self.jumpSymbol,(10,height_screen*15/16))
		elif player.player=="player_Grey":
			screen.blit(self.discSymbol,(10,height_screen*15/16))
		elif player.player=="player_Red":
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
		self.posX = width_screen
		self.posY = y
		self.t = 0

	def update(self):
		self.t+=0.01
		if self.t>self.time:
			self.posX -= speed
			x = width_screen
			for i in range(self.size):
				screen.blit(self.img,(self.posX+x,self.posY*int(height_screen/15)))
				x += 64

class CLOUD():
	def __init__(self,x,y,speed):
		self.speed = (speed-2*sens*speed)/random.randint(30,50)
		self.posX = x
		self.posY = y
		self.img = pygame.image.load("IMAGES/cloud"+str(random.randint(1,8))+".png").convert_alpha()

	def update(self):
		self.posX += self.speed
		if self.posX>width_screen or self.posX<-98:
			self.posX=-98+sens*(width_screen+98)
			self.posY = random.randint(0,height_screen*2/3)
			self.speed = (random.randint(8,15)-2*sens*random.randint(8,15))/random.randint(30,50)
			self.img = pygame.image.load("IMAGES/cloud"+str(random.randint(1,8))+".png").convert_alpha()
		screen.blit(self.img,(self.posX,self.posY))

class DISC(): #disque d'attaque de grey
	def __init__(self):
		self.speed = 5*(width_screen/768)
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

player = PLAYER()
game = GAME()
# game.ReadMap()


for i in range(random.randint(10,20)):
	cloud = CLOUD(random.randint(0,width_screen),random.randint(0,height_screen*2/3),random.randint(8,15)) #(x,y,speed)
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
				if event.key == K_SPACE and player.player=="player_Grey" and len(discs)<1: #une attaque de grey à la fois
					disc = DISC()
					discs.append(disc)
				if event.key == K_TAB: #changer de joueur
					if player.player=="player_Blue":
						player.player="player_Green"
					elif player.player=="player_Green":
						player.player="player_Grey"
					elif player.player=="player_Grey":
						player.player="player_Red"
					elif player.player=="player_Red":
						player.player="player_Blue"
		ScreenDisplay()

pygame.quit()
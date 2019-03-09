#IMPORTATIONS
import pygame, os, numpy as np,time	
from pygame.locals import*

#INITIALISATIONS DE LA FENETRE ET PYGAME
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)
pygame.init()
py_info=pygame.display.Info() #1366/768 dimensions écran etienne
width_screen,height_screen=py_info.current_w,py_info.current_h
pygame.display.set_caption("Jumper")
screen=pygame.display.set_mode((width_screen,height_screen-30))

pygame.key.set_repeat(1,10) 
pygame.display.update()

#INITIALISATION DES VARIABLES
Game=True
inGame=True
inMenu=False

#DECLARATION DES CLASSES
class PLAYER():
	def __init__(self):
		self.posX = width_screen*1/4
		self.posY = 400
		self.speed = 5
		self.lives = 3
		self.coins = 0
		self.img1 = pygame.image.load("playerBlue_walk1.png").convert_alpha()
		self.img2 = pygame.image.load("playerBlue_walk2.png").convert_alpha()
		self.img3 = pygame.image.load("playerBlue_walk3.png").convert_alpha()
		self.img4 = pygame.image.load("playerBlue_walk4.png").convert_alpha()

		self.imgs = [self.img1,self.img2,self.img3,self.img4,self.img3,self.img2,]
		self.imgNumber = 0
		self.img = self.imgs[self.imgNumber]
		self.updateImg = 0

		# self.rect
		self.isJumping = False
		self.hasLanded = False
		self.impulsion = 3

	def update(self):
		if self.updateImg > 5:
			self.imgNumber += 1
			self.updateImg =0
		if self.imgNumber > 5:
			self.imgNumber = 0
		self.img = self.imgs[self.imgNumber]

		screen.blit(self.img,(self.posX,self.posY))

		if self.isJumping:
			self.Jump_Fall()

		if not self.hasLanded and not self.isJumping:
			self.impulsion = 0
			self.Jump_Fall()

		if self.posY>=400 and self.posX<1000: #ATTERISSAGE
			self.hasLanded = True
			self.isJumping = False
			self.impulsion = 3
			self.imgNumber = 0
		# else:
			# self.hasLanded = False
			# self.impulsion = 0
			# self.Jump_Fall()
			# self.impulsion -= g


	def move(self,dir):
		self.updateImg += 1
		self.posX += self.speed*((dir=="right")-(dir=="left"))	#deplacement latéral

	def Jump_Fall(self): 
		self.posY-=self.impulsion
		self.impulsion -= g #impulsion est positive puis négative (impulsion [3 --> -3])


class GAME():
	def __init__(self):
		self.heartFull = pygame.image.load("heartFull.png").convert_alpha()
		self.heartEmpty = pygame.image.load("heartEmpty.png").convert_alpha()
		self.coin = pygame.image.load("coin.png").convert_alpha()
		self.numbers = []
		for i in range(10):
			self.numbers.append(pygame.image.load(str(i)+".png"))

	def UI(self):
		x = 10
		for live in range(player.lives):
			screen.blit(self.heartFull,(x,10))
			x+=60
		x = 130
		for live_empty in range(2-live):
			screen.blit(self.heartEmpty	,(x,10))
			x-=60

		screen.blit(self.coin,(1300,10))
		screen.blit(self.numbers[int(player.coins)],(1250,10))

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
		self.img = pygame.image.load("tileGreen_27.png").convert_alpha()
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

global speed
speed = 2
global platforms
platforms = []
player = PLAYER()
game = GAME()
g = 0.02
# game.ReadMap()



#BOUCLE PRINCIPALE
while Game:
	while inMenu:
		pass
	while inGame:
	    for event in pygame.event.get(): #pile des évènements
	        if event.type == QUIT or event.type==KEYDOWN and event.key == K_ESCAPE:
	            inGame = False
	            Game=False
	        if event.type == KEYDOWN:
	        	if event.key == K_LEFT:
	        		player.move("left")
	        	if event.key == K_RIGHT:
	        		player.move("right")
	        	if event.key == K_UP and player.hasLanded: #on saute si on est déja à terre
	        		player.isJumping = True
	        	if event.key == K_DOWN and player.impulsion>0:
	        		player.impulsion = -1 #impulsion<0 donc phase de chute, on donne -1 pour qu'il ait déja une vitesse de chute

	    screen.fill((196,233,242))
	    for platform in platforms:
	    	platform.update()
	    game.update()
	    game.UI()
	    player.update()
	    pygame.display.update()

pygame.quit()

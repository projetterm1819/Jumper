#IMPORTATIONS
import pygame, os, numpy, time, random
from pygame.locals import*

#INITIALISATIONS DE LA FENETRE ET PYGAME

pygame.init()
py_info=pygame.display.Info() #1366/768 dimensions écran etienne
width_screen,height_screen=(py_info.current_w),(py_info.current_h)
pygame.display.set_caption("Jumper")
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,int(3.5/100*height_screen))#placage de la fenetre par rapport au top left
screen=pygame.display.set_mode((int(width_screen),int(height_screen-3.5/100*height_screen)))
pygame.key.set_repeat(1,10) # accepte un evenement clavier toutes les millisecondes
pygame.display.update() #affiche

#INITIALISATION DES VARIABLES
Game=True # Boucle principale "Main"
inGame=True #Boucle de jeu
inMenu=False #Boucle de menu

#DECLARATION DES CLASSES
class CLOUDS():

	def __init__(self):
		if sens_Nuage==0:
			self.speed = random.uniform(-1.2,-.5)
		else:
			self.speed =random.uniform(0.5,1.2)
		if cloudGen==0:
			self.posX = random.randint(0,width_screen)
		else:
			self.posX = (sens_Nuage*(width_screen+500)-500)
		self.posY = random.randint(0,int(height_screen/2))

		self.image = pygame.image.load("cloud"+str(random.randint(1,8))+".png").convert_alpha()
		self.size = size =(random.randint(0,5/100*width_screen))

	def update(self):
		self.posX+=self.speed
		screen.blit(self.image,(self.posX,self.posY))

	def generator(self):
		nuage=CLOUDS()
		nuages.append(nuage)
class PLAYER():
	def __init__(self):
		self.posX = int(width_screen*1/4)
		self.posY = int(height_screen/2)
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

		if self.posY>=1/4*height_screen and self.posX<=height_screen*3/4: #ATTERISSAGE
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
		x = 60
		for live in range(player.lives):
			screen.blit(self.heartFull,(width_screen*2/32+(live-1)*x,height_screen*1/15))
		for live_empty in range(2-live):
			screen.blit(self.heartEmpty	,(width_screen*2/32+(live-1)*x,height_screen*1/15))

		screen.blit(self.coin,(width_screen*15/16,height_screen*1/15))
		screen.blit(self.numbers[int(player.coins)],(width_screen*29/32,height_screen*1/15))

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
		self.posX = width_screen
		self.posY = y
		self.t = 0

	def update(self):
		self.t+=0.01
		if self.t>self.time:
			self.posX -= speed
			x = 0
			for i in range(self.size):
				screen.blit(self.img,(self.posX+x,self.posY*int(height_screen/15)))
				x += 64

global speed
speed = 2
global platforms
platforms = []
player = PLAYER()
game = GAME()
g = 0.02*height_screen/768
global cloudGen
cloudGen=False
global sens_Nuage
sens_Nuage=random.randint(0,1)
global nuages
nuages=[]
for n in range(random.randint(10,20)):
	nuage=CLOUDS()
	nuages.append(nuage)

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
		cloudGen=True
		nuage=CLOUDS()
		nuages.append(nuage)
		cloudGen=False
		for nuage in nuages:
			nuage.update()
		for platform in platforms:
			platform.update()
		game.update()
		game.UI()
		player.update()
		pygame.display.update()

pygame.quit()
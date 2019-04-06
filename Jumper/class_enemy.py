#Types : Flying, Walking, Floating

class ENEMY():
	def __init__(self,EnemyType,x,y,speed,direction):
		self.posX = x
		self.posY = y
		self.initialX = x
		self.initialY = y
		self.speed = speed
		self.direction = direction
		
		self.types = ["Flying","Walking","Floating"]
		self.type = EnemyType

		self.sprites = ["1","2","3","dead"]

		for Type in self.types:
			for sprite_name in self.sprites:
				image="IMAGES/enemy_"+Type+"/"+sprite_name+".png"
				setattr(self, str("img"+sprite_name+Type),pygame.image.load(image).convert_alpha())

		self.imgsFlying = [self.img1Flying,self.img2Flying,self.img3Flying,self.img2Flying]
		self.imgsWalking = [self.img1Walking,self.img2Walking,self.img3Walking,self.img2Walking]
		self.imgsFloating = [self.img1Floating,self.img2Floating,self.img3Floating,self.img2Floating]

		self.enemies = {"Flying":self.imgsFlying,"Walking":self.imgsWalking,"Floating":self.imgsFloating}

		self.imgNumber = 0
		self.img = self.enemies[self.type][self.imgNumber]
		self.imgPersistance = {"Flying":0.04,"Walking":0.02,"Floating":0.02}
		self.animations = {"Flying":"self.flying()","Walking":"self.walking()","Floating":"self.floating()"}

	def update(self):
		self.img = self.enemies[self.type][int(self.imgNumber)]
		self.imgNumber+=self.imgPersistance[self.type]
		if self.imgNumber>4:
			self.imgNumber = 0
		screen.blit(self.img,(self.posX,self.posY))
		exec(self.animations[self.type])

	def die(self):
		pass

	def attack(self):
		pass

	def flying(self):
		self.posY += (self.direction==-1)*0.25 - (self.direction==1)*0.25
		if self.posY>self.initialY+30 or self.posY<self.initialY-30:
			self.direction = -self.direction

	def walking(self):
		self.posX += (self.direction==-1)*0.25 - (self.direction==1)*0.25
		if self.posX>self.initialX+30 or self.posX<self.initialX-30:
			self.direction = -self.direction

	def floating(self):
		self.posY += (self.direction==-1)*0.25 - (self.direction==1)*0.25
		if self.posY>self.initialY+10 or self.posY<self.initialY-10:
			self.direction = -self.direction

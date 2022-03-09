import pygame as pg

pg.init()
clock = pg.time.Clock()

sf = 2
width, height = 640, 360
screen = pg.display.set_mode((width * sf, height * sf))

running = True

fps = 60

black = (0, 0, 0)
white = (255, 255, 255)
lightGray = (205, 205, 205)
darkGray = (55, 55, 55)
red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 200)
orange = (255, 145, 0)
lightRed = (184, 39, 39)
lightGreen = (0, 255, 48)
lightBlue = (20, 152, 215)
pink = (204, 126, 183)
lightBlack = (45, 45, 45)
darkWhite = (215, 215, 215)


class Vehicle:
	def __init__(self, x, y, maxSpeed, color):
		self.pos = pg.Vector2(x, y)
		self.vel = pg.Vector2(0, 0)
		self.acc = pg.Vector2(0, 0)
		
		self.maxSpeed = maxSpeed
		self.maxDamp = 1000
		self.dampning = 50

		self.maxForce = 1

		self.color = color

	def Draw(self):
		pg.draw.aaline(screen, self.color, self.pos, self.pos + self.vel)

	def Seek(self, target):
		force = target - self.pos
		force -= self.vel
		try:
			force.scale_to_length(self.maxSpeed)
		except:
			pass

		self.ApplyForce(force)

	def Arrive(self, target):
		desired = target - self.pos
		d = desired.magnitude()
		if d < 50:
			m = ((d / self.maxDamp) * self.dampning) - 1
			try:
				desired.scale_to_length(m)
			except:
				pass
		else:
			desired.scale_to_length(self.maxSpeed)

		steer = desired + self.vel
		try:
			steer.scale_to_length(self.maxForce)
		except:
			pass
		self.ApplyForce(steer)


	def ApplyForce(self, force):
		self.acc += force

	def Update(self):
		self.vel += self.acc
		try:
			self.vel.scale_to_length(self.maxSpeed)
		except:
			pass
		self.pos += self.vel * clock.get_time()/100
		self.acc.update(0, 0)




def DrawLoop():
	screen.fill(darkGray)

	v.Draw()

	pg.draw.circle(screen, black, (width, height), 1)

	pg.display.update()


v = Vehicle(10, 20, 50, lightRed)

while running:
	clock.tick_busy_loop(fps)
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				running = False

	v.Update()
	v.Arrive(pg.Vector2(pg.mouse.get_pos()))

	DrawLoop()

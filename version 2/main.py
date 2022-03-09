import os
import sys

os.chdir(sys.path[0])
sys.path.insert(1, "P://Python Projects/assets/")

from GameObjects import *


class Agent(Vec2):
	allAgents = []

	def __init__(self, x, y, color, radius):
		super().__init__(x, y)
		self.vel = Vec2(0, 0)
		self.acc = Vec2(0, 0)

		self.maxSpeed = 5
		self.maxForce = 10

		self.color = color
		self.radius = radius
		
		Agent.allAgents.append(self)

	def Draw(self):
		pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)

	def ApplyForce(self, force):
		self.acc = self.acc.Add(force)

	def Update(self):
		self.vel = self.vel.Add(self.acc).SetMagnitude(self.maxSpeed)
		pos = self.Add(self.vel)
		self.x, self.y = pos.x, pos.y
		self.acc = Vec2(0, 0)

	def Edges(self, bounce=False):
		if not bounce:
			if self.y > height - self.radius:
				self.y = self.radius

			if self.y < self.radius:
				self.y = height - self.radius
			
			if self.x > width - self.radius:
				self.x = self.radius

			if self.x < self.radius:
				self.x = width - self.radius
		else:
			if self.y >= height - self.radius:
				self.y = height - self.radius
				self.vel.y *= -1

			if self.y <= self.radius:
				self.y = self.radius
				self.vel.y *= -1

			if self.x >= width - self.radius:
				self.x = width - self.radius
				self.vel.x *= -1

			if self.x <= self.radius:
				self.x = self.radius
				self.vel.x *= -1

	def Seek(self, target):
		force = target.Sub(self)
		force = force.SetMagnitude(self.maxSpeed)
		force = force.Sub(self.vel)
		force = force.Limit(self.maxForce)

		return force

	def Flee(self, target):
		return self.Seek(target).Multiply(-1)

	def Pursue(self, vehicle):
		target = vehicle.Copy()
		vel = vehicle.vel.Multiply(10)
		target = target.Add(vel)

		return self.Seek(target)

	def Evade(self, vehicle):
		return self.Pursue(vehicle).Multiply(-1)

	def Arrive(self, target):
		force = target.Sub(self)
		slowRadius = 100
		mag = force.Magnitude()
		if mag < slowRadius:
			m = Map(mag, 0, slowRadius, 0, self.maxSpeed)
			force = force.SetMagnitude(round(m))
		else:
			force = force.SetMagnitude(self.maxSpeed)

		force = force.Sub(self.vel)
		force = force.Limit(self.maxForce)

		return force



def DrawLoop():
	screen.fill(darkGray)

	for agent in Agent.allAgents:
		agent.Draw()

	DrawAllGUIObjects()

	pg.display.update()



def HandleEvents(event):
	HandleGui(event)


def Update():
	
	for agent in Agent.allAgents:
		agent.ApplyForce(agent.Seek(Vec2(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])))
		agent.Update()
		agent.Edges(False)

a = Agent(10, 10, white, 5)

while running:
	clock.tick_busy_loop(fps)

	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				running = False

		HandleEvents(event)

	Update()

	DrawLoop()

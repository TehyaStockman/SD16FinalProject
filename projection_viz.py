import sys, os, random, math
import pygame
from pygame.locals import *
import numpy as np
import scipy
from colorTrack import Tracker
from threading import Thread


class Model(object):
	'''The model class will contain functions of interactions between the different classes,
	how the different Creatures and Schools interact with wach other and respond to outside 
	stimuli.'''


	def __init__(self, screen_size, tracker, creatureNum = 10, forceConstant = 80):
		self.creature_list = []
		color = pygame.Color('green')
		self.creatureNum = creatureNum
		self.tracker = tracker

		for i in xrange(creatureNum):
			vx = random.randint(0,1)
			vy = random.randint(0,1)
			self.creature_list.append(Creature(i*30+500, i*30+500, vx, vy, color))
		self.forceConstant = forceConstant
		self.school = School
		#self.mouse_pos = Controller.mouse_pos

	def forces(self, creature1, creature2):
		# the distanc.e vectore between the two fish. Vector from creature1 to creature 2
		xdist = creature1.x - creature2.x
		ydist = creature1.y - creature2.y
		displacement = math.sqrt(xdist**2 + ydist**2)


		if xdist == 0 or ydist == 0:                #cannot divide by zero
			xdist = 0.0001
			ydist = 0.0001
		xForce = creature1.mass * creature2.mass / ((xdist) * self.forceConstant)
		yForce = creature1.mass * creature2.mass / ((ydist) * self.forceConstant)

		if displacement < max([creature1.repulsion_r, creature2.repulsion_r]) and displacement > min([creature1.orientation_r, creature2.orientation_r]):
			xForce = 0
			yForce = 0

		if displacement < max([creature1.orientation_r, creature2.orientation_r]):
			#force reverses if goes below this range
			xForce *= -1
			yForce *= -1

		creature1.vx -= int(xForce)
		creature1.vy -= int(yForce)

		creature2.vx += int(xForce)
		creature2.vy += int(yForce)

	def school_force(self, creature1, school):

		xdist = creature1.x - school.x
		ydist = creature1.y - school.y


	def tracker_force(self, creature):
	#The force between the tracked object and a fishy

		xlocation = self.tracker.center[0]
		ylocation = self.tracker.center[1]

		xdist = creature.x - xlocation
		ydist = creature.y - ylocation
		displacement = math.sqrt(xdist**2 + ydist**2)


		if xdist == 0 or ydist == 0:                #cannot divide by zero
			xdist = 0.0001
			ydist = 0.0001
		xForce = creature.mass  / ((xdist) * 1000)
		yForce = creature.mass  / ((ydist) * 1000)

		

		creature.vx -= int(xForce)
		creature.vy -= int(yForce)


	def update(self):
		for creature1 in self.creature_list:
			for creature2 in self.creature_list:
				if not creature1 is creature2:
					self.forces(creature1, creature2)
			self.tracker_force(creature1)
		for creature in self.creature_list:
			creature.update()

class School(object):
	def __init__(self, x, y, vx, vy, r):
		'''A school is made up of many creatures. Each of the creatures both attract and 
		repel the other creatures in their school.'''
		self.x, self.y, self.r = x, y, r
		self.vx, self.vy = vx, vy
		self.mass = 50
		self.boundary = 2 * math.pi * r**2  #current boundary of the school is a circle. I don't think this should be a very strict boundary
		creature_positions = []
		self.creature_list = model.creature_list

	def update(self):
		pass


class Creature(pygame.sprite.Sprite):
	def __init__(self, x, y, vx, vy, color, mass = 20, r = 20):
		'''Creatures are currently represented by dots. Each creature belongs to a school. 
		A creature can attract and repel other creatures of a school. There are different 
		radii and magnitudes for attraction, repulsion, and orientation.'''
		self.x, self.y, self.mass, self.r = x, y, mass, r
		self.vx, self.vy = vx, vy
		self.color = color

		self.attraction_r = self.r + 30  #numbers for these are not final and will most likely be changed
		self.orientation_r = self.r + 30
		self.repulsion_r = self.r + 5
		self.attraction_weight = 1.5   #weights will be used in calculating angular direction
		self.repulsion_weight = 0.7
		#self.rect = pygame.Rect(x-r/math.sqrt(2), y-r/math.sqrt(2), 2*r/math.sqrt(2), 2*r/math.sqrt(2))

		pygame.sprite.Sprite.__init__(self)
	def accelerate(self, force, force_angle):
		self.vx += force*math.cos(force_angle)
		self.vy += force*math.sin(force_angle)

	def update(self):
		self.move()
		#self.rect.centerx, self.rect.centery = self.x, self.y

	def move(self):
		self.x += self.vx
		self.y += self.vy


class View(object):
	'''The View class is the visual representation of the model.'''
	def __init__(self, screen_size, model):
		self.screen = pygame.display.set_mode(screen_size)
		self.screen.fill(pygame.Color('blue'))
		for creature in model.creature_list: 
			pygame.draw.circle(self.screen, creature.color, (creature.x, creature.y), creature.r)

		pygame.display.update()

	def update(self, model):
		self.screen.fill(pygame.Color('blue'))
		for creature in model.creature_list: 
			pygame.draw.circle(self.screen, creature.color, (creature.x, creature.y), creature.r)
		pygame.display.update()


class Controller(object):
	'''The Controller class is a stand-in for the Audio/Video classes.''' 
	def __init__(self):
		mouse_pos = pygame.mouse.get_pos()

	def update(self, events, model):
		mouse_pos = pygame.mouse.get_pos()
		mouse_posx = mouse_pos[0]
		mouse_posy = mouse_pos[1]

class Audio(object):
	'''Audio will first be implemented with pressing keys. 
	It will then be changed to make the model update due to the sound input.
	'''
	def __init__(self):
		pass

class Video(object):
	def __init__(self):
		pass


def main():
	pygame.init()
	clock = pygame.time.Clock()
	screen_size = (1920, 1080) #pygame.display.list_modes()[0]
	
	# initializes the color tracker and has it run the tracking function
	tracka = Tracker()



	# initialize our model
	model = Model(screen_size, tracka)
	
	controller = Controller()
	view = View(screen_size, model)
	running = True


	def runLoop():
		while running:
			tracka.track
			model.update()
			view.update(model)
			clock.tick(20)
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()

	t1 = Thread(target = tracka.track)
	t2 = Thread(target = runLoop)

	t1.start()
	t2.start()

if __name__ == '__main__': main()


"""
Things to work on:
+We need to add in:
	+multiple creatures
	+forces between the creatures
	+make school classes/interactions
+Make the fish more complex:
	+make them into multiple circles (from large circle for head to increasingly smaller tail circles)
	+find a way to make the circles move together/look fishy-like in movement 
	+find nice-looking fish colors/transparencies
	+make shapes more complicated instead of circles 
+It would be cool to have a background that looks like shimmery water.
+Integrate across collected data and visual representation
	+Develop the Audio/Video classes for the inputted data
	+Make creatures respond to these inputs
	+Input more types of data for creatures to respond to
"""

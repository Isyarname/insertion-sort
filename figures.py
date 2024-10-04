from math import sin, cos, pi
import pygame

class Cell:
	def __init__(self, surf, width, color, number, pos):
		self.number = number
		self.x = pos[0]
		self.x0 = self.x
		self.x1 = self.x
		self.y = pos[1]
		self.y0 = self.y
		self.y1 = self.y
		self.width = width
		self.color = color
		self.v = 0.01
		self.moving = False
		self.shift = 0
		self.surface = surf
		fontSize = round(self.width * 1.5)
		self.font = pygame.font.SysFont("roboto", fontSize)
		self.selected = False
		self.selectedTime = 0
		self.isNext = False

	def lower(self):
		self.moving = True
		self.y1 = self.y + self.width*2

	def setpos(self, pos):
		self.moving = True
		self.x0 = self.x
		self.y0 = self.y
		self.x1 = pos[0]
		self.y1 = pos[1]

	def move(self):
		if self.moving:
			if abs(self.x - self.x1) < 1 and abs(self.y - self.y1) < 1:
				self.moving = False
				self.x0 = self.x = self.x1
				self.y0 = self.y = self.y1
			else:
				self.x += self.v * (self.x1-self.x0)
				self.y += self.v * (self.y1-self.y0)

	def draw(self):
		self.move()
		x = round(self.x)
		y = round(self.y)
		if self.selected:
			w = self.width+3
			sForm = [(x-w, y-w), (x-w, y+w), 
			(x+w, y+w), (x+w, y-w)]
			sColor = (255,255,255)
			pygame.draw.polygon(self.surface, sColor, sForm)
		form = [(x-self.width, y-self.width), (x-self.width, y+self.width), 
		(x+self.width, y+self.width), (x+self.width, y-self.width)]
		pygame.draw.polygon(self.surface, self.color, form)
		####
		textColor = (0,0,0)
		text = self.font.render(str(self.number), True, textColor)
		place = text.get_rect(topleft=(self.x-self.width/2, self.y-self.width/2))
		self.surface.blit(text, place)
		####

class Triangle(Cell):
	def __init__(self, surf, width, color, number, pos):
		self.number = number
		self.x = pos[0]
		self.x0 = self.x
		self.x1 = self.x
		self.y = pos[1]
		self.y0 = self.y
		self.y1 = self.y
		self.width = width
		self.color = color
		self.v = 0.05
		self.moving = False
		self.surface = surf

	def setpos(self, pos):
		self.moving = True
		self.x0 = self.x
		self.y0 = self.y
		self.x1 = pos[0]
		self.y1 = pos[1]

	def move(self):
		if self.moving:
			if abs(self.x - self.x1) < 1 and abs(self.y - self.y1) < 1:
				self.moving = False
				self.x0 = self.x = self.x1
				self.y0 = self.y = self.y1
			else:
				self.x += self.v * (self.x1-self.x0)
				self.y += self.v * (self.y1-self.y0)
	def draw(self):
		self.move()
		x = round(self.x)
		y = round(self.y)
		#c = 3
		#w = self.width + c
		#form1 = [(x-w-2*c,y-w),(x+w+2*c,y-w),(x,y+2*c)]
		#pygame.draw.polygon(self.surface, (0,0,0), form1)
		form2 = [(x-self.width, y-self.width), (x+self.width, y-self.width), (x, y)]
		pygame.draw.polygon(self.surface, self.color, form2)
import pygame
import random
import time
import sys
from figures import *
from color_generator import *

clock = pygame.time.Clock()
pygame.init()

Width = 1500
cellsNumber = 100
border = Width/cellsNumber
gap = (Width - 2*border) / (cellsNumber-1)
width = round(gap/2)

Height = 200 + width * 5
sc = pygame.display.set_mode((Width, Height))

def getpos(i):
	return border+i*gap, Height/3

def trianglePos(i):
	return (border+cur*gap, Height/3 - width*2)

def _qiut():
	pygame.quit()
	sys.exit()

def events():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			_qiut()
		elif event.type == pygame.KEYDOWN:
			pass

def allCellsNotSelected(d = 0):
	for cell in cells:
		if cell.selected:
			if False:#time.time() - cell.selectedTime < d:
				return False
			else:
				cell.selected = False
	return True

def allCellsNotMoving():
	for cell in cells:
		if cell.moving:
			return False
	return not temp.moving

indices = list(range(cellsNumber))
random.shuffle(indices)
#start = 10
#indices = random.sample(range(start, cellsNumber+start), cellsNumber)
colors = genColors(max(indices), min(indices), 0, type_=2)
cells = []
for i, e in enumerate(indices):
	cells.append(Cell(sc, width, colors[e], e, getpos(i)))

cur = 1
triangle = Triangle(sc, width/2, (255,255,255), 0, trianglePos(cur))

temp = cells[1]
temp.selected = True
prevTempI = -1
i = 0
isSorted = False
def play():
	global i
	global cellsNumber
	global cur
	global temp
	global prevTempI
	global isSorted
	if temp.isNext and not cells[prevTempI].moving:
			cells[prevTempI].selected = False
			cells[prevTempI-1].selected = False
			temp.lower()
			temp.isNext = False
			temp.selected = True
	if not isSorted and cur >= cellsNumber:
		isSorted = True

	if allCellsNotMoving() and not isSorted and allCellsNotSelected():
		if i >= 0:
			cells[i].selected = True
			cells[i].selectedTime = time.time()
		if i == -1 or temp.number > cells[i].number:
			temp.setpos(getpos(i+1))
			cells[i+1] = temp
			prevTempI = i + 1
			cur += 1
			triangle.setpos(trianglePos(cur))
			if cur < cellsNumber:
				temp = cells[cur]
				temp.isNext = True
			i = cur - 1
		else: # если номер i-й клетки больше номера текущей проверяемой клетки
			cells[i].setpos(getpos(i+1))
			cells[i+1] = cells[i]
			i -= 1

	

startTime = time.time()
while True:
	sc.fill((20,40,80))
	events()

	if time.time() - startTime > 2:
		if time.time() - startTime < 2.1 and not temp.moving:
			temp.lower()
		play()

	for cell in cells:
		cell.draw()
	temp.draw()
	triangle.draw()

	clock.tick(60 + cellsNumber)
	pygame.display.set_caption(str(clock))
	pygame.display.update()
	pygame.display.flip()
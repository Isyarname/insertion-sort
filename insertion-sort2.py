import pygame
import random
import time
import sys
from screeninfo import get_monitors
from figures import *
from color_generator import *

clock = pygame.time.Clock()
pygame.init()
monitors = get_monitors()
while monitors == []: # так надо, не трогать
	monitors = get_monitors()

Width = monitors[0].width # 1500
Height = monitors[0].height // 1.1 # 700
numberOfCells = 45
numberOfLines = numberOfCells // 30

lineLength = 2
gap = Width / (lineLength+1)
width = round(gap/2)

def cellpos(i):
	x = gap + (i%lineLength) * gap
	y = width*3 + (i//lineLength) * width*5
	return (x, y)

while cellpos(numberOfCells-1)[1] > Height - width*3:
		lineLength += 1
		gap = Width / (lineLength+1)
		width = round(gap/2)



sc = pygame.display.set_mode((Width, Height))

def trianglePos(x):
	cp = cellpos(x)
	return (cp[0], cp[1]-width*2)

def _qiut():
	pygame.quit()
	sys.exit()

def events():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			_qiut()
		elif event.type == pygame.KEYDOWN:
			pass

def allCellsNotMoving():
	for cell in cells:
		if cell.moving:
			return False
	return not temp.moving

indices = list(range(numberOfCells))
random.shuffle(indices)
#start = 10
#indices = random.sample(range(start, numberOfCells+start), numberOfCells)
colors = genColors(max(indices), min(indices), type_=2)
cells = []
for i, e in enumerate(indices):
	cells.append(Cell(sc, width, colors[e], e, cellpos(i)))

cur = 1
triangle = Triangle(sc, width/2, (255,255,255), 0, trianglePos(cur))

temp = cells[1]
temp.selected = True
prevTempI = -1
i = 0
isSorted = False
def play():
	global i
	global numberOfCells
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

	if not isSorted and cur >= numberOfCells:
		isSorted = True
		for cell in cells:
			cell.selected = False
	
	if allCellsNotMoving() and not isSorted:
		for cell in cells:
			cell.selected = False
		if i >= 0:
			cells[i].selected = True
			cells[i].selectedTime = time.time()
		if i == -1 or temp.number > cells[i].number:
			temp.setpos(cellpos(i+1))
			cells[i+1] = temp
			prevTempI = i + 1
			cur += 1
			triangle.setpos(trianglePos(cur))
			if cur < numberOfCells:
				temp = cells[cur]
				temp.isNext = True
			i = cur - 1
		else: # если номер i-й клетки больше номера текущей проверяемой клетки
			cells[i].setpos(cellpos(i+1))
			cells[i+1] = cells[i]
			i -= 1

	

startTime = time.time()
while True:
	sc.fill((20,40,80))
	events()

	if time.time() - startTime > 1:
		if time.time() - startTime < 1.1 and not temp.moving:
			temp.lower()
		play()

	for cell in cells:
		cell.draw()
	temp.draw()
	triangle.draw()

	clock.tick(60 + numberOfCells)
	pygame.display.set_caption(str(clock))
	pygame.display.update()
	pygame.display.flip()
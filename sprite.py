from PIL import Image, ImageDraw, ImageEnhance, ImageFont
from random import randint

#must be even
totalGrid = 8

enlargeOutput = True

xdim = int(totalGrid /2)
ydim = totalGrid
maxNumOfPixels = ((xdim * ydim) / 2) #36
numOfPixels = randint((int(maxNumOfPixels / 3)),maxNumOfPixels) #12, 36
usedGrid = [(-1, -1), (-1, -1)]

#returns random rgb
def getColour():
	r = randint(0, 255)
	g = randint(0, 255)
	b = randint(0, 255)
	return [r, g, b]

#returns co-ordinates, does not care if duplicates
def getGridAny(usedX, usedY, xdim, ydim):
	xGrid = -1
	yGrid = -1
	
	xGrid = randint(0, xdim - 1)
	yGrid = randint(0, ydim - 1)

	return xGrid, yGrid

#returns unique co-ordinates
def getGridUnique(usedX, usedY, xdim, ydim):
	isOK = False

	while isOK == False:
		tempGrid = getGridAny(usedX, usedY, xdim, ydim)
		print('generating - testing ' + str(tempGrid) + ' ' + str(usedGrid))
		for i in range(0, len(usedGrid)):

			if tempGrid[0] == usedGrid[i][0]:
				if tempGrid[1] == usedGrid[i][1]:
					isOK = False
			else:
				isOK = True

	usedGrid.append((tempGrid[0], tempGrid[1]))
	return tempGrid[0], tempGrid[1]


#flips image and joins to create symmetry
def complete(img):

	flippedImg = img.transpose(Image.FLIP_LEFT_RIGHT)

	output = Image.new(mode = "RGB", size = (totalGrid, totalGrid), color = "black")

	output.paste(img)
	output.paste(flippedImg, (xdim, 0))

	output.resize((100, 100))

	output.save('spriteOut.png')




img = Image.new(mode = "RGB", size = (xdim, ydim), color = "black")

for i in range(0, numOfPixels):
	pixColour = getColour()
	pixGrid = getGridUnique(usedGrid[0], usedGrid[1], xdim, ydim)
	print('Painting pixel position ' +  str(pixGrid[0]) + ',' + str(pixGrid[1]))

	img.putpixel( (pixGrid[0], pixGrid[1]), (pixColour[0], pixColour[1], pixColour[2]) )



complete(img)





"""
#1 bit color
from PIL import Image
from PIL.ImageOps import posterize
img = Image.open('obama.jpg')
pimg = posterize(img, bits=1)
"""
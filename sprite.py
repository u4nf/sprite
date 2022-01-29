from PIL import Image, ImageDraw, ImageEnhance, ImageFont
from random import randint, choice

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
def getGridAny():
	xGrid = randint(0, xdim - 1)
	yGrid = randint(0, ydim - 1)

	return xGrid, yGrid


#returns unique co-ordinates
def getGridUnique():
	isOK = False

	while isOK == False:
		tempGrid = getGridAny()
		print('generating - testing ' + str(tempGrid) + ' against list - ' + str(usedGrid))
		for i in range(0, len(usedGrid)):

			if tempGrid[0] == usedGrid[i][0]:
				if tempGrid[1] == usedGrid[i][1]:
					isOK = False
			else:
				isOK = True

	usedGrid.append((tempGrid[0], tempGrid[1]))
	return tempGrid[0], tempGrid[1]


def getGridTouching(xcurr, ycurr):

	#generate refernce to neighboring pixel and verify validity
	isOK = False	
	while not isOK:

		rand = choice([-1, 1])
		if (xcurr + rand) > 0 and (xcurr + rand) < xdim:
			tempx = xcurr + rand
			rand = choice([-1, 1])
			if (ycurr + rand) > 0 and (ycurr + rand) < ydim:
				tempy = ycurr + rand

				#check if co-ords have been used
				for i in range(0, len(usedGrid) - 1):
					print('tempx ' + str(tempx) + ' tempy ' + str(tempy))
					if not tempx == usedGrid[i][0]:
						print('checking if ' + str(tempx) + ' = ' + str(usedGrid[i][0]))
						if not tempy == usedGrid[i][1]:
							isOK = False
						else:
							isOK = True


	usedGrid.append((tempx, tempy))
	return currentPixel


#flips image and joins to create symmetry
def complete(img):

	flippedImg = img.transpose(Image.FLIP_LEFT_RIGHT)

	output = Image.new(mode = "RGB", size = (totalGrid, totalGrid))
	output.paste(img)
	output.paste(flippedImg, (xdim, 0))

	if enlargeOutput:
		output = output.resize((1000, 1000), resample=Image.NEAREST)

	output.save('spriteOut.png')


img = Image.new(mode = "RGB", size = (xdim, ydim))

#initial pixel to build from
currentPixel = getGridUnique()

for i in range(0, numOfPixels):
	pixColour = getColour()
	#curretPixel = getGridAny()
	#currentPixel = getGridUnique()
	currentPixel = getGridTouching(currentPixel[0], currentPixel[1])

	print('Painting pixel position ' +  str(currentPixel[0]) + ',' + str(currentPixel[1]))
	img.putpixel( (currentPixel[0], currentPixel[1]), (pixColour[0], pixColour[1], pixColour[2]) )

complete(img)


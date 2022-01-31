from PIL import Image, ImageDraw, ImageEnhance, ImageFont
from random import randint, choice

#must be even
totalGrid = 10

# use this pallete.  If false, use 8bit colour
spaceInvaders = True
enlargeOutput = True

xdim = int(totalGrid / 2)
ydim = totalGrid
maxNumOfPixels = int(((xdim * ydim) / 2))
minNumOfPixels = int(maxNumOfPixels / 4) 
numOfPixels = randint(minNumOfPixels, maxNumOfPixels)
usedGrid = []


def getColour():
	"""returns rgb values as tuple"""
	if spaceInvaders:
		return choice([(248, 59, 58), (235, 223, 100), (98, 222, 109), (219, 85, 221), (83, 83, 241), (66, 233, 244)])

	r = randint(0, 255)
	g = randint(0, 255)
	b = randint(0, 255)
	return [r, g, b]


def firstPixel():
	"""ensures first pixel is centered"""
	pixColour = getColour()

	usedGrid.append((xdim -1, randint(0, ydim -1)))
	img.putpixel((usedGrid[0][0], usedGrid[0][1]), (pixColour[0], pixColour[1], pixColour[2]))

	print('first pixel painted at ' + str(usedGrid[0][0]) + str(usedGrid[0][1]))


def getGridAny():
	"""returns co-ordinates as tuple, does not care if duplicates"""
	x = randint(0, xdim - 1)
	y = randint(0, ydim - 1)

	return (x, y)


def getGridUnique():
	"""returns unused co-ordinates as tuple"""
	isOK = False
	while not isOK:
		xy = getGridAny()
		isOK = isUnused(xy)

	return (xy)


def getGridTouching():
	"""returns co-ordinates that touch previous co-ordinates"""
	while True:
		# select random used pixel and attempt to build off it
		rand = randint(0, len(usedGrid) - 1)
		x = usedGrid[rand][0]
		y = usedGrid[rand][1]

		# generate refernce to neighboring pixel and verify validity
		rand = choice([-1, 0, 1])

		if (x + rand) >= 0 and (x + rand) < xdim:
			tempx = x + rand
			rand = choice([-1, 0, 1])

			if (y + rand) >= 0 and (y + rand) < ydim:
				tempy = y + rand

				if isUnused((tempx, tempy)):
					return (tempx, tempy)


def isUnused(xy):
	"""returns True if tuple xy is not in usedGrid list"""
	for i in range(0, len(usedGrid)):
		if ((xy[0] == usedGrid[i][0]) and (xy[1] == usedGrid[i][1])):
			return False

	usedGrid.append(xy)
	return True


def complete(img):
	"""flips a copy of img horzontally, and joins it to the orginal img to create a symmetrical image"""
	flippedImg = img.transpose(Image.FLIP_LEFT_RIGHT)

	output = Image.new(mode = "RGB", size = (totalGrid, totalGrid))
	output.paste(img)
	output.paste(flippedImg, (xdim, 0))

	if enlargeOutput:
		output = output.resize((500, 500), resample=Image.NEAREST)

	output.save('spriteOut.png')


# initial pixel to build from
img = Image.new(mode = "RGB", size = (xdim, ydim))
firstPixel()


for i in range(0, numOfPixels - 1):
	pixColour = getColour()
	#currentPixel = getGridAny()
	#currentPixel = getGridUnique()
	currentPixel = getGridTouching()

	print('Painting pixel position ' +  str(currentPixel[0]) + ',' + str(currentPixel[1]))
	img.putpixel((currentPixel[0], currentPixel[1]), (pixColour[0], pixColour[1], pixColour[2]))

complete(img)
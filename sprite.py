from PIL import Image, ImageDraw, ImageEnhance, ImageFont
from random import randint, choice

#must be even
totalGrid = 12

#use this pallete.  If false, use 8bit colour
spaceInvaders = True
enlargeOutput = True

firstPixel = True
xdim = int(totalGrid /2)
ydim = totalGrid
maxNumOfPixels = ((xdim * ydim) / 2)
numOfPixels = randint((int(maxNumOfPixels / 3)), maxNumOfPixels)
usedGrid = [(-1, -1)]


#returns rgb
def getColour():

	if spaceInvaders:
		return choice([(248, 59, 58), (235, 223, 100), (98, 222, 109), (219, 85, 221), (83, 83, 241), (66, 233, 244)])

	r = randint(0, 255)
	g = randint(0, 255)
	b = randint(0, 255)
	return [r, g, b]


#returns co-ordinates, does not care if duplicates
def getGridAny():
	xGrid = randint(0, xdim - 1)
	yGrid = randint(0, ydim - 1)

	if firstPixel:
		xGrid = xdim -1

	return xGrid, yGrid


#returns unique co-ordinates
def getGridUnique():
	isOK = False

	while isOK == False:
		tempGrid = getGridAny()
		for i in range(0, len(usedGrid)):
			if tempGrid[0] == usedGrid[i][0]:
				if tempGrid[1] == usedGrid[i][1]:
					isOK = False
			else:
				isOK = True

	return tempGrid[0], tempGrid[1]


#returns co-ordinates that touch each other
def getGridTouching():

	isOK = False

	#select random used pixel and attempt to build off it
	rand = randint(1, len(usedGrid) - 1)
	xcurr = usedGrid[rand][0]
	ycurr = usedGrid[rand][1]

	while not isOK:
		#generate refernce to neighboring pixel and verify validity
		rand = choice([-1, 0, 1])
		if (xcurr + rand) >= 0 and (xcurr + rand) < xdim:
			tempx = xcurr + rand
			rand = choice([-1, 0, 1])
			if (ycurr + rand) >= 0 and (ycurr + rand) < ydim:
				tempy = ycurr + rand


				print(len(usedGrid) - 1)
				#check if co-ords have been used
				for i in range(0, len(usedGrid) - 1):

					print(str(tempx) + ' ' + str(tempy))
					print(usedGrid)

					if (tempx == usedGrid[i][0]) and (tempy == usedGrid[i][1]):
						isOK = False
					else:
						isOK = True
						break

	return (tempx, tempy)


#flips image and joins to create symmetry
def complete(img):

	flippedImg = img.transpose(Image.FLIP_LEFT_RIGHT)

	output = Image.new(mode = "RGB", size = (totalGrid, totalGrid))
	output.paste(img)
	output.paste(flippedImg, (xdim, 0))

	if enlargeOutput:
		output = output.resize((500, 500), resample=Image.NEAREST)

	output.save('spriteOut.png')


#initial pixel to build from
img = Image.new(mode = "RGB", size = (xdim, ydim))
usedGrid.append(getGridUnique())


for i in range(0, numOfPixels):
	pixColour = getColour()
	#curretPixel = getGridAny()
	#currentPixel = getGridUnique()
	currentPixel = getGridTouching()

	usedGrid.append(currentPixel)
	print('Painting pixel position ' +  str(currentPixel[0]) + ',' + str(currentPixel[1]))
	img.putpixel((currentPixel[0], currentPixel[1]), (pixColour[0], pixColour[1], pixColour[2]))

complete(img)


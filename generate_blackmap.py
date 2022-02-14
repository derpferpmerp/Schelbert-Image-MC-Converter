import os

import numpy as np
import requests
from keras.preprocessing import image
from matplotlib import pyplot as plt
from tqdm import tqdm, trange

from parser import compressData
import argparse

parser = argparse.ArgumentParser(
	description='Generate MC Conversion'
)

parser.add_argument(
	'-u',
	dest="url",
	type=str,
	nargs=1,
	help='Supply the URL for the Image'
)

parser.add_argument(
	'-v',
	'--verbose',
	dest="verbose",
	action='store_true',
	default=False,
	help='add verbose cli'
)
args = parser.parse_args()

IMG_URL = "https://images3.alphacoders.com/209/20979.jpg" if not args.url else args.url
VERBOSE = args.verbose
print(args)

def removeIfExists(filename):
	if os.path.exists(filename):
		os.remove(filename)


removeIfExists("IMAGE.jpg")
removeIfExists("DATADUMP.txt")

img_data = requests.get(IMG_URL).content


with open('IMAGE.jpg', 'wb') as handler:
	handler.write(img_data)


X_test = image.load_img(
	"IMAGE.jpg",
	color_mode="grayscale",
)

X_test = image.img_to_array(X_test)  # convert image into array

def Mag( vec:np.ndarray ):
	m = 0
	for x in vec:
		m += x * x
	return np.sqrt(m)
	


def closestTo( ITEM:np.ndarray, b=(0,255), invert=False):
	# Invert Parameter:
	# [ True  ] : Break Black Pixels
	# [ False ] : Break White Pixels
	
	
	distances_255 = float(b[1]) - ITEM
	
	# Check if Item Should be Identified as White
	CASE = bool( Mag(distances_255) > Mag(ITEM) )
	
	# Check Breakable Boolean
	Breakable = not CASE if invert else CASE
	return Breakable

boolean = np.array([], dtype=bool)
LO = []

for x in [ tqdm(X_test) if VERBOSE else X_test ][0]:
	TMP = []
	for y in x:
		TMP.append(closestTo(y))
	LO.append(np.array(TMP))
	
LO = np.array(LO)
LO = np.expand_dims(LO, axis=0)[0]
LCOORDS = []

for x in [ trange(len(LO)) if VERBOSE else range(len(LO)) ][0]:
	for y in range(x):
		LCOORDS.append( [ x, y, LO[x][y] ] )

compressData(LCOORDS)

plt.imshow(LO, cmap="binary")
plt.savefig(os.path.join(os.path.dirname(__file__), "MAP", "out.png"))

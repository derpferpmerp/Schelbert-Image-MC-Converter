import os

import numpy as np
import requests
from keras.preprocessing import image
from matplotlib import pyplot as plt
from tqdm import tqdm, trange

from parser import compressData
import argparse
print("\n\n")
parser = argparse.ArgumentParser(
	description='Generate MC Conversion'
)

inputGroup = parser.add_mutually_exclusive_group()

inputGroup.add_argument(
	'-u',
	dest="url",
	type=str,
	nargs=1,
	help='Supply the URL for the Image',
	default="None"
)

inputGroup.add_argument(
	'-f',
	dest="inFile",
	type=str,
	help='Supply the Input File for the Image',
	default="None"
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
print(args)
if args.inFile == "None" and args.url == "None":
	parser.print_help()
	parser.exit()

IMG_URL = "https://images3.alphacoders.com/209/20979.jpg" if not args.url else args.url
TRANSFER_PROTOCOL = "file" if args.inFile != "None" else ("url" if args.url != "None" else "invalid")
VERBOSE = args.verbose

if TRANSFER_PROTOCOL == "file":
	if os.path.exists(args.inFile):
		X_test = image.load_img(
			args.inFile,
			color_mode="grayscale",
		)
	else:
		raise FileNotFoundError(f"The File {args.inFile} does not exist in the current directory")
elif TRANSFER_PROTOCOL == "url":
	img_data = requests.get(IMG_URL).content
	with open('IMAGE.jpg', 'wb') as handler:
		handler.write(img_data)
	X_test = image.load_img(
		"IMAGE.jpg",
		color_mode="grayscale",
	)
else:
	raise ValueError(f"Fatal Error. Arguments: \n{args}")
def removeIfExists(filename):
	if os.path.exists(filename):
		os.remove(filename)

removeIfExists("IMAGE.jpg")
removeIfExists("DATADUMP.txt")

X_test = image.img_to_array(X_test)  # convert image into array

def Mag( vec:np.ndarray ) -> np.float64:
	m = 0
	for x in vec:
		m += x * x
	return np.sqrt(m)
	


def closestTo( ITEM:np.ndarray, b=(0,255), THRESH=2.5, invert=True) -> bool:
	# Invert Parameter:
	# [ True  ] : Break Black Pixels
	# [ False ] : Break White Pixels
	distances_255 = 255.0 - ITEM
	
	# Check if Item Should be Identified as White
	CASE = Mag(distances_255) * THRESH > Mag(ITEM)
	
	# Check Breakable Boolean
	Breakable = not CASE if invert else CASE
	return Breakable

def hidePlotBounds(ax):
	'''
	Function: hidePlotBounds
	Summary: Hides the Matplotlib Plot Bounds
	Examples: hidePlotBounds(plt)
	Attributes:
		@param (ax): Matplotlib Axis Object
	Returns: None
	'''
	ax.spines["top"].set_visible(False)
	ax.spines["right"].set_visible(False)
	ax.spines["bottom"].set_visible(False)
	ax.spines["left"].set_visible(False)

	ax.set_xticklabels([])
	ax.set_yticklabels([])

	ax.set_xticks([])
	ax.set_yticks([])

	ax.axes.get_xaxis().set_visible(False)
	ax.axes.get_yaxis().set_visible(False)


boolean = np.array([], dtype=bool)
LO = []
L_NEG = []

for x in [ tqdm(X_test) if VERBOSE else X_test ][0]:
	TMP = []
	TMP2 = []
	for y in x:
		TMP.append(closestTo(y, THRESH=1))
		TMP2.append(closestTo(y, THRESH=2.5))
	LO.append(np.array(TMP))
	L_NEG.append(np.array(TMP2))
	
LO = np.array(LO)
L_NEG = np.array(L_NEG)

LO = np.expand_dims(LO, axis=0)[0]
L_NEG = np.expand_dims(L_NEG, axis=0)[0]

LCOORDS = []
LCOORDS_NEG = []

for x in [ trange(len(LO)) if VERBOSE else range(len(LO)) ][0]:
	for y in range(len(LO)):
		if not LO[x,y]:
			L_NEG[x][y] = True
		LCOORDS.append( [ x, y, LO[x][y] ] )
		LCOORDS_NEG.append( [ x, y, L_NEG[x][y] ] )

compressData(LCOORDS)
plt.style.use("dark_background")
N = len(LCOORDS_NEG)/100
fig, ax = plt.subplots(1, 1, figsize=(30, 30))

ax.imshow(L_NEG, cmap="binary")
hidePlotBounds(ax)
plt.savefig(os.path.join(os.path.dirname(__file__), "MAP", "out.png"))

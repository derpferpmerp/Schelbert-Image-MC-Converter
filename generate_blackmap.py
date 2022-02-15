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

def Mag( vec:np.ndarray ):
	m = 0
	for x in vec:
		m += x * x
	return np.sqrt(m)
	


def closestTo( ITEM:np.ndarray, b=(0,255), invert=False):
	# Invert Parameter:
	# [ True  ] : Break Black Pixels
	# [ False ] : Break White Pixels
	THRESH = 1.1
	distances_255 = 255.0 - ITEM
	
	# Check if Item Should be Identified as White
	CASE = Mag(distances_255) * THRESH > Mag(ITEM)
	
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

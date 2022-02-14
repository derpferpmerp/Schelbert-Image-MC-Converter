import pickle
from pickle import HIGHEST_PROTOCOL as HIGH
import os

def removeIfExists(filename):
	if os.path.exists(filename):
		os.remove(filename)

def compressData(data, outpath="MAP/COMP.bin"):
	removeIfExists(outpath)
	with open(outpath, "xb+") as out:
		pickle.dump(data, out, protocol=HIGH)
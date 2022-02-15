import pickle
import os

FILE = os.path.join(".", "MAP", "COMP.bin")

with open(FILE, "rb") as fileobject:
	DATA = pickle.load(fileobject)

toPrint = [
	"-- Data Binary Loaded --",
	f"Amount of Items: {len(DATA)}",
	f"First Item: {DATA[0]}"
]

print(*toPrint, sep="\n")
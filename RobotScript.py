import random
import pickle

L = []

def beta(x):
    return x

for x_i in range(10):
	tmp = []
	for y_i in range(10):
		CHOICE = bool(random.randint(0, 1))
		L.append([x_i, y_i, True])

LS = sorted(L, key=lambda x: x[1])
CX, CZ, CY = beta(agent.position)
agent.say(str(CX))
for x, y, delete in L:
	agent.say(str(CX+x))
	agent.say(str(CY+y))
	agent.teleport([CX+x, CZ, CY+y])
	#player.teleport([CX+x, CZ, CY+y])
	if delete:
		agent.destroy("DOWN")



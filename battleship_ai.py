import random

# Prints the map in readable form
def printmap (map):
    print (" ")
    for i in range (0, 10):
         print (map[i][0],map[i][1],map[i][2],map[i][3],map[i][4],map[i][5],map[i][6],map[i][7],map[i][8],map[i][9])

# Find the maximum value of the map
def mapmax (map):
	result = 0
	for i in range (0,10):
		for j in range (0,10):
		   if map [i][j] > result:

			   result = map [i][j]
	return result

# Find the coordinates of the target in the map
# This and mapmax are used to help AI locate target
def maxcoordinates (map, target):
	coordinates = []
	for i in range (0,10):
	  for j in range (0,10):
	     if map [i][j] == target:
	         coordstring = str(i) + str(j)
	         coordinates.append(coordstring)

	result = random.choice(coordinates)
	return result

# Declaring the board

# Worlds represented as a two-dimensional array:

# Map of the player, as seen by the AI:
# Number on each cell represents priority. Cells
# with higher priority get taken out first.
global playervague
playervague = []
newpv = []
for i in range (0, 10):
 for j in range (0, 10):
     newpv.append(5)
 playervague.append(newpv)
 newpv = []

# Encourage Hunt-and-Target - make even
# cells a slightly higher priority
# It has 6's in one row, 5's in the next and so on
# Will be fixed for the final version
for i in range (0, 10):
# x = (i-1)*2
 for j in range (0, 5):
    y = (j-1)*2
    playervague [i][y] = 6

printmap (playervague)

# Map of the AI, as seen by the player
# H stands for hit, M stands for miss,
# X stands for unknown
global aivague
aivague = []
newav = []
for i in range (0, 10):
 for j in range (0, 10):
     newav.append("X")
 aivague.append(newav)
 newav = []

printmap (aivague)

# Map of the player as seen by the player:
# A stands for ship, O stands for Unoccupied,
# X stands for hit
global playermap
playermap = []
newpm = []
for i in range (0, 10):
 for j in range (0, 10):
     newpm.append("O")
 playermap.append(newpm)
 newpm = []

# Map of the AI as seen by the AI:
# A stands for ship, O stands for Unoccupied,
# X stands for hit
global aimap
aimap = []
newam = []
for i in range (0, 10):
 for j in range (0, 10):
     newam.append("O")
 aimap.append(newam)
 newam = []

# Populate the maps:
# Later, we will of course enable the player
# to choose his own locations and randomize AI's
# locations, but for now, the code below gives them
# static locations

playermap[0][0] = "A"
playermap[0][1] = "A"
playermap[0][2] = "A"
playermap[0][3] = "A"
playermap[0][4] = "A"

playermap[1][0] = "A"
playermap[1][1] = "A"
playermap[1][2] = "A"
playermap[1][3] = "A"

playermap[2][5] = "A"
playermap[3][5] = "A"
playermap[4][5] = "A"

playermap[7][7] = "A"
playermap[8][7] = "A"
playermap[9][7] = "A"

playermap[8][9] = "A"
playermap[9][9] = "A"

printmap (playermap)

# Same arrangement for AI map -
# doesn't really matter for now

aimap[0][0] = "A"
aimap[0][1] = "A"
aimap[0][2] = "A"
aimap[0][3] = "A"
aimap[0][4] = "A"

aimap[1][0] = "A"
aimap[1][1] = "A"
aimap[1][2] = "A"
aimap[1][3] = "A"

aimap[2][5] = "A"
aimap[3][5] = "A"
aimap[4][5] = "A"

aimap[7][7] = "A"
aimap[8][7] = "A"
aimap[9][7] = "A"

aimap[8][9] = "A"
aimap[9][9] = "A"

printmap (aimap)

# THIS LAST SECTION MAKES THE MOVES
# COPY AND PASTE OVER AND OVER AGAIN TO
# MAKE MORE MOVES.

# This will be fixed in the final version of course.
# Also, enter valid numbers, or the code will crash.
# This will also be fixed.

# Prompt a move: enter 11 to hit cell 1, 1
# Count starts from 0. Read in the move.

var = input("Make a move: ")
xc = int(var[:-1])
yc = int(var[1:])

# Update corresponding maps
if (aimap [xc][yc] == "A"):
	aivague [xc][yc] = "H"
else:
	aivague [xc] [yc] = "M"
aimap [xc][yc] = "X"

# Have the AI make a move:
# Print the move:
maxcoord = maxcoordinates(playervague, mapmax(playervague))
xai = int (maxcoord[:-1])
yai = int (maxcoord[1:])
print ("The computer makes a move:", xai, yai)

# Update corresponding maps
playervague [xai][yai] = 0
if playermap [xai][yai] == "A":
	if xai > 0:
	  if playervague[xai-1][yai] > 0:	
	           playervague[xai-1][yai] = 9
	if xai < 9:
	  if playervague[xai+1][yai] > 0:	
	           playervague[xai+1][yai] = 9
	if yai > 0:
	   if playervague[xai][yai-1] > 0:	
	           playervague[xai][yai-1] = 9
	if yai < 9:
	   if playervague[xai][yai+1] > 0:	
	           playervague[xai][yai+1] = 9
playermap [xai][yai] = "X"

# Print current state of four boards
printmap (playervague)
printmap (playermap)
printmap (aivague)
printmap (aimap)


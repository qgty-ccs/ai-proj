mport random

# Collective health of all ships:
# Game over once one of them reaches 0
playerhealth = 17
aihealth = 17
gameover = 0

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

# Applies the resetmap to the playervague
# Needed for the reset function
def applyreset (resmap, plmap):
      for i in range (0,10):
       for j in range (0,10):
        if resmap[i][j]>0:
           resmap[i][j] = resmap[i][j]-1
           if (plmap[i][j]>2) and (plmap[i][j]<8):
               plmap[i][j] = plmap[i][j]+1


# Map of the reset: used in reset function
global resetmap
resetmap = []
newres = []
for i in range (0, 10):
 for j in range (0, 10):
     newres.append(0)
 resetmap.append(newres)
 newres = []

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

# Linear bombardment - crucial part of the AI
def linbombard (x, y, direction):

    # Horizontal directions
    if (direction == 1):
        if (x == 0):
            for i in range(1,10):
                targetarray.append([i,y])
                
    # Vertical directions        
    if (direction == -1):

# Declaring the board

# Worlds represented as a two-dimensional array:

# Map of the player, as seen by the AI:
# Number on each cell represents priority. Cells
# with higher priority get taken out first.
global playervague

def playervaguemethod():
 lrrandom = random.randint(1,2)
 playervaguemap = []
 newpv = []
 if (lrrandom == 1):
    for i in range (0, 10):
     for j in range (0, 10):
         newpv.append(2)
     playervaguemap.append(newpv)
     newpv = []

    # Encourage Hunt-and-Target - make even
    # cells a slightly higher priority
    for x in range (0, 5):
        i = 2*x
        playervaguemap [i] [0] = 2
        playervaguemap [i] [2] = 2
        playervaguemap [i] [4] = 2
        playervaguemap [i] [6] = 2
        playervaguemap [i] [8] = 2
        playervaguemap [i-1] [1] = 2
        playervaguemap [i-1] [3] = 2
        playervaguemap [i-1] [5] = 2
        playervaguemap [i-1] [7] = 2
        playervaguemap [i-1] [9] = 2

 if (lrrandom == 2):
    for i in range (0, 10):
     for j in range (0, 10):
         newpv.append(2)
     playervaguemap.append(newpv)
     newpv = []

    # Encourage Hunt-and-Target - make even
    # cells a slightly higher priority
    for x in range (0, 5):
        i = 2*x
        playervaguemap [i] [0] = 3
        playervaguemap [i] [2] = 3
        playervaguemap [i] [4] = 3
        playervaguemap [i] [6] = 3
        playervaguemap [i] [8] = 3
        playervaguemap [i-1] [1] = 3
        playervaguemap [i-1] [3] = 3
        playervaguemap [i-1] [5] = 3
        playervaguemap [i-1] [7] = 3
        playervaguemap [i-1] [9] = 3


 return playervaguemap


playervague = playervaguemethod()
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

#var = " "

while gameover == 0:

    # Prompt a move: enter 11 to hit cell 1, 1
    # Count starts from 0. Read in the move.
    var = input("Make a move: ")

    # Check input length
    if ((len(var)>0) and (len(var)<3)):
        xc = int(var[:-1])
        yc = int(var[1:])

    # Check input validity
    if (aimap [xc][yc] != "X"):
    
        # Update corresponding maps
        if (aimap [xc][yc] == "A"):
            aivague [xc][yc] = "H"
            aihealth = (aihealth - 1)
        else:
            aivague [xc] [yc] = "M"
        aimap [xc][yc] = "X"

        # Have the AI make a move:
        # Print the move:
        maxcoord = maxcoordinates(playervague, mapmax(playervague))
        if targetarray == []:
            xai = int (maxcoord[:-1])
            yai = int (maxcoord[1:])
        else:
            xai = targetarray[0][0]
            yai = targetarray[0][1]            
        print ("The computer makes a move:", xai, yai)

        # Update corresponding maps and target array
        if playermap [xai][yai] == "A":
            playervague [xai][yai] = 1
            playerhealth = (playerhealth - 1)
            if xai > 0:
              if playervague[xai-1][yai] > 0:   
                       playervague[xai-1][yai] = 8
            if xai < 9:
              if playervague[xai+1][yai] > 0:   
                       playervague[xai+1][yai] = 8
            if yai > 0:
               if playervague[xai][yai-1] > 0:  
                       playervague[xai][yai-1] = 8
            if yai < 9:
               if playervague[xai][yai+1] > 0:  
                       playervague[xai][yai+1] = 8

        else:
            playervague [xai][yai] = 0
        playermap [xai][yai] = "X"

        # Print current state of four boards
        printmap (playervague)
        printmap (aivague)
        printmap (playermap)
        printmap (aimap)

    else:
        print ("Invalid input!")

    # Check for game over
    if playerhealth == 0:
        print ("Defeat!")
        gameover = 1
    if aihealth == 0:
        print ("Victory!")
        gameover = 1
'''
CS 5100 Proj:   Battleship
Team:           BigLeg
Last Modified:  04/03/2014
'''

import copy
import random
# import randomgen.assignailoc

MAPSIZE = 10
HEALTH = 17
EXPLORED = ' '
UNEXPLORED = '-'
OCCUPIED = 'X'
HIT = 'H'
MISS = 'M'

available = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,8), (0,9), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9),(2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (2,9),(3,0), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (3,7), (3,8), (3,9),(4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (4,7), (4,8), (4,9),(5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7), (5,8), (5,9),(6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6), (6,7), (6,8), (6,9),(7,0), (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7), (7,8), (7,9),(8,0), (8,1), (8,2), (8,3), (8,4), (8,5), (8,6), (8,7), (8,8), (8,9),(9,0), (9,1), (9,2), (9,3), (9,4), (9,5), (9,6), (9,7), (9,8), (9,9)]


# An arrangement of ships for testing.
TEST_ARRANGEMENT = [
    (0,0), (0,1), (0,2), (0,3), (0,4),
    (1,0), (1,1), (1,2), (1,3),
    (2,5), (3,5), (4,5),
    (7,7), (8,7), (9,7),
    (8,9), (9,9)]

TEST_FLEET = {
    'Carrier':      [(0,0), (0,1), (0,2), (0,3), (0,4)],
    'Battleship':   [(1,0), (1,1), (1,2), (1,3)],
    'Submarine':    [(2,5), (3,5), (4,5)],
    'Cruiser':      [(7,7), (8,7), (9,7)],
    'Destroyer':    [(8,9), (9,9)]
}

FLEET_HEALTH = {
    'Carrier':      5,
    'Battleship':   4,
    'Submarine':    3,
    'Cruiser':      3,
    'Destroyer':    2
        }

class Map:

    m = None
    size = 0

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def generate_player_map(self, occupied):
        ''' Generate player map for human or agent.
            Take a list of ship arrangement as input
            and mark them as occupied.
        '''
        map_range = range(0, self.size)
        row = [EXPLORED for i in map_range]
        self.m = [row[:] for i in map_range]
        for (x,y) in occupied:
            self.m[x][y] = OCCUPIED

    def generate_ai_enemy_map(self):
        ''' Generate enemy map for agent.
        '''
        map_range = range(0, self.size)
        row = [0 for i in map_range]
        self.m = [row[:] for i in map_range]
        # Encourage Hunt-and-Target - make even
        # cells a slightly higher priority
        even = False
        for i in map_range:
            for j in map_range:
                if even:
                    self.m[i][j] = 1
                even = not even
            even = not even

    def generate_human_enemy_map(self):
        ''' Generate enemy map for human.
        '''
        map_range = range(0, self.size)
        row = [UNEXPLORED for i in map_range]
        self.m = [row[:] for i in map_range]

    def print_map(self):
        ''' Prints the map in readable form.
        '''
        for i in range(0, self.size):
            for j in range(0, self.size):
                print self.m[i][j],
            print ''

    def mark_adjacent_coords(self, (x,y), score):
        ''' Hunt-and-Target
            For agent enemy map: find unexplored adjacent coordinates
            and mark them with the given score.
        '''
        for (ax,ay) in self.find_adjacent_by_xy((x,y)):
            if self.m[ax][ay] > -1:
                self.m[ax][ay] = score

    def find_adjacent_by_xy(self, (x,y)):
        ''' Find adjacent neighbors of a given coordinate.
        '''
        nbs = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        for nb in nbs:
            if not self.in_range(nb):
                nbs.remove(nb)
        return nbs

    def in_range(self, (x,y)):
        ''' Tell if a coordinate is in map range
        '''
        if (0 <= x < self.size) and (0 <= y < self.size):
            return True
        return False

    def get(self, (x,y)):
        ''' getter of (x,y) coordinate
        '''
        return self.m[x][y]

    def set(self, (x,y), val):
        ''' setter of (x,y) coordinate
        '''
        self.m[x][y] = val


class Player:

    my_map = None
    enemy_map = None
    fleet = {'Carrier': [],
             'Battleship': [],
             'Submarine': [],
             'Cruiser': [],
             'Destroyer': []}

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def attack(self, enemy, (x,y)):
        ''' Attack an enemy coordinate and mark result on
            own enemy map.
        '''
        result = enemy.hit((x,y))
        self.enemy_map.set((x,y), result['result'])
        return result

    def hit(self, (x,y)):
        ''' Takes a hit from enemy, calculate score
            and return result to enemy.
        '''
        if self.my_map.get((x,y)) == OCCUPIED:
            self.my_map.set((x,y), ' ')
            sunk_ship = self.update_fleet((x,y))
            return {'result': HIT,
                    'sunk_ship': sunk_ship}
        return {'result': MISS,
                'sunk_ship': None}

    def update_fleet(self, (x,y)):
        for k,ship in self.fleet.items():
            if (x,y) in ship:
                self.fleet[k].remove((x,y))
                if not ship:
                    del self.fleet[k]
                    return k
        return None

    def lose(self):
        ''' Tell if the player lost the game.
        '''
        return False if self.fleet else True

    def gethealth(self):
        result = 0
        for v in self.fleet.values():
            result = result + len(v)
        return result

    def getfleet(self):
        result = []
        for k, v in self.fleet.items():
            string = k + ': 1'
            result.append(string)
        return result


class Agent(Player):

    # target mode parameters

    # direction:
    # -1 - up 
    # 1 - down
    # -2 - left 
    # 2 - right
    direction = None 
    candidates = [] # direction candidates
    wrong_direction = False
    r_edge = False
    r_end = False
    base = None
    current = None # the cell under hit at this round
    streak = 0
    sunk_ship = None

    hunt_mode = True
    enemy_fleet = ['Carrier', 'Battleship', 'Submarine', 'Cruiser',
                    'Destroyer']

    def arrangement(self):
        '''
        Generate a randomized sparse arrangement of fleet.
        '''
        # return TEST_ARRANGEMENT   
        return assignailoc() 

    def attack(self, enemy, (x,y)):
        ''' Attack a coordinate in Hunt-and-Target mode.
        '''
        self.current = (x,y)
        result = enemy.hit((x,y))
        feedback = result['result']
        sunk_ship = result['sunk_ship']
        if feedback == HIT:

            print 'hit'
            self.streak = self.streak + 1

            if self.hunt_mode:
                # hunt mode - hit, enter target mode
                self.hunt_mode = False
                self.base = (x,y)

            elif sunk_ship:
                # return to hunt mode
                self.enemy_fleet.remove(sunk_ship)
                self.to_hunt_mode(sunk_ship)

            elif self.reached_edge():
                self.r_edge = True

        else:
            print 'miss'
            if not self.hunt_mode:
                # target mode - miss
                if self.streak > 1:
                    # reach end
                    self.r_end = True
                else:
                    # wrong direction
                    self.wrong_direction = True

        # mark coordinate as visited
        self.enemy_map.set((x,y), -1)
        return result

    def reached_edge(self):
        ''' Tell if the current direction reaches the map edge.
        '''
        x, y = self.current
        direction = self.direction
        if direction == -1 and y == 0:
            return True
        elif direction == 1 and y == MAPSIZE - 1:
            return True
        elif direction == -2 and x == 0:
            return True
        elif direction == 2 and x == MAPSIZE - 1:
            return True
        return False

    def find_target(self):
        ''' Find the next target for attack.
        '''
        if self.hunt_mode:
            return self.hunt()
        else:
            return self.target()

    def hunt(self):
        ''' Hunt mode
        '''
        print 'hunt'
        return self.choice(0)

    def target(self):
        '''
        keep track of cell discovered, possible directions, remaining ships
        and find the best candidate to attack.
        '''
        m = self.enemy_map
        base = self.base
        next = None

        if self.direction is None:
            # if direction is not determined yet
            next = self.set_direction()
            print 'set direction to', self.direction

        elif self.wrong_direction:
            print 'wrong direction'
            next = self.choose_random_direction()
            print 'set direction to', self.direction
            self.wrong_direction = False

        elif self.r_edge:
            print 'reached the edge of map'
            print self.current
            next = self.opposite_direction()
            if not next:
                # no sunken ship, reached edge, no opposite direction.
                # TODO mark part of ships
                next = self.to_hunt_mode(None)
            self.r_edge = False

        elif self.r_end:
            print 'reach end of a ship'
            next = self.opposite_direction()
            if not next:
                # no sunken ship, reached end, no opposite direction.
                # TODO mark part of ships
                next = self.to_hunt_mode(None)
            self.r_end = False

        else:
            # if everything alright, continue
            next = self.moveon()
            print 'move on direction', self.direction
            # remove all candidates except the opposite
            for c in self.candidates:
                if self.determine_direction(c, base) != -self.direction:
                    self.candidates.remove(c)

        return next

    def opposite_direction(self):
        base = self.base
        chosen = None
        self.direction = -self.direction
        for c in self.candidates:
            if self.determine_direction(c, base) == self.direction:
                chosen = c
                self.candidates.remove(c)
        return chosen

    def set_direction(self):
        m = self.enemy_map
        base = self.base

        # find undiscovered spaces around the base.
        adjacent = m.find_adjacent_by_xy(base)
        undiscovered_adjacent = [a for a in adjacent if m.get(a) > -1]

        # find all feasible directions.
        self.candidates = [u for u in undiscovered_adjacent \
            if self.evaluate_direction(u, base)]
        
        # choose one as next direction randomly.
        return self.choose_random_direction()

    def choose_random_direction(self):
        ''' choose a random direction from candidates.
        '''
        base = self.base
        chosen = random.choice(self.candidates)
        self.candidates.remove(chosen)
        self.direction = self.determine_direction(chosen, base)
        return chosen

    def to_hunt_mode(self, ship):
        ''' Return to hunt mode
        '''
        self.hunt_mode = True

        # clear target mode parameters
        self.direction = None
        if ship in self.enemy_fleet:
            self.enemy_fleet.remove(ship)
        self.streak = 0
        self.candidates = []
        self.base = None
        self.sunk_ship = None
        self.reach_end = False
        self.reach_edge = False
        return self.hunt()

    def determine_direction(self, (x,y), base):
        ''' Determine the direction from (x,y) to base.
        '''
        bx, by = base
        if y == by - 1:
            return -1
        elif y == by + 1:
            return 1
        elif x == bx - 1:
            return -2
        elif x == bx + 1:
            return 2
        return None

    def evaluate_direction(self, (x,y), base):
        ''' Tell if the given direction is applicable.
        '''
        bx, by = base
        direction = self.determine_direction((x,y), base)
        for ship in self.enemy_fleet:
            valid = self.have_continous_cells(direction, base, FLEET_HEALTH[ship], MAPSIZE)
            if valid:
                return True
        return False

    def have_continous_cells(self, direction, base, length, size):
        ''' Tell if a direction has <length> continous undiscovered cells
            in a row starting from base.
        '''
        bx, by = base
        m = self.enemy_map
        if direction == -1:
            if by > length - 2:
                discovered = [i for i in range(by + 1 - length, by) if m.get((bx,i)) == -1]
                if not discovered:
                    return True
        elif direction == 1:
            if by < size - length + 1:
                discovered = [i for i in range(by + 1, by + length) if m.get((bx,i)) == -1]
                if not discovered:
                    return True
        elif direction == -2:
            if bx > length - 2:
                discovered = [i for i in range(bx + 1 - length, bx) if m.get((i,by)) == -1]
                if not discovered:
                    return True
        elif direction == 2:
            if bx < size - length + 1:
                discovered = [i for i in range(bx + 1, bx + length) if m.get((i,by)) == -1]
                if not discovered:
                    return True

        return False

    def moveon(self):
        ''' Continue moving to current direction.
        '''
        direction = self.direction
        x, y = self.current
        if direction == -1:     # up
            return (x, y - 1)
        elif direction == 1:    # down
            return (x, y + 1)
        elif direction == -2:   # left
            return (x - 1, y)
        elif direction == 2:    # right
            return (x + 1, y)
        return None


    def find_highest_priority(self):
        ''' Find the maximum value of the map for agent
        '''
        size = self.enemy_map.size
        m = self.enemy_map.m
        result = 0
        for i in range(0, size):
            for j in range(0, size):
               if m[i][j] > result:
                   result = m[i][j]
        return result

    def choice(self, highest):
        ''' Choose the coordinates of the target in the map for agent
            This and find_highest_priority are used to help AI locate target
        '''
        size = self.enemy_map.size
        m = self.enemy_map.m
        candidates = []
        for i in range(0, size):
          for j in range(0, size):
             if m[i][j] == highest:
                 candidates.append((i,j))
        return random.choice(candidates)


class Human(Player):

    def attacked_before(self, (x,y)):
        ''' Tell if a coordinate was attacked before
        '''
        return False if self.enemy_map.get((x,y)) == UNEXPLORED else True


def init_human(mapsize, arrangement, fleet):
    ''' Init human object.
    '''
    my_map = Map(size=mapsize)
    my_map.generate_player_map(arrangement)
    enemy_map = Map(size=mapsize)
    enemy_map.generate_human_enemy_map()
    return Human(my_map=my_map, enemy_map=enemy_map, fleet=fleet)


def init_agent(mapsize, arrangement, fleet):
    ''' Init agent.
    '''
    my_map = Map(size=mapsize)
    my_map.generate_player_map(arrangement)
    enemy_map = Map(size=mapsize)
    enemy_map.generate_ai_enemy_map()
    return Agent(my_map=my_map, enemy_map=enemy_map, fleet=fleet)


def array_to_arrangement(array):
    ''' Convert two-dimension array to arrangement.
    '''
    arrangement = []
    for i in range(0, MAPSIZE):
        for j in range(0, MAPSIZE):
            if array[i][j] == '1':
                arrangement.append((i,j))
    return arrangement

def assignship(length, dir):

    startav = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,8), (0,9), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9),(2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (2,9),(3,0), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (3,7), (3,8), (3,9),(4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (4,7), (4,8), (4,9),(5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7), (5,8), (5,9),(6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6), (6,7), (6,8), (6,9),(7,0), (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7), (7,8), (7,9),(8,0), (8,1), (8,2), (8,3), (8,4), (8,5), (8,6), (8,7), (8,8), (8,9),(9,0), (9,1), (9,2), (9,3), (9,4), (9,5), (9,6), (9,7), (9,8), (9,9)]

    random.shuffle(startav)
    start = startav[0]

    if (length == 5):
        if (dir == 'r'):
          if ((available.count(start) > 0) and (available.count((start[0]+1, start[1])) > 0) and (available.count((start[0]+2, start[1])) > 0) and (available.count((start[0]+3, start[1])) > 0) and (available.count((start[0]+4, start[1])) > 0)):
 
                                        shiplocarray = [start, (start[0]+1, start[1]), (start[0]+2, start[1]), (start[0]+3, start[1]), (start[0]+4, start[1])]
                                        available.remove(start)
                                        available.remove((start[0]+1, start[1]))
                                        available.remove((start[0]+2, start[1]))
                                        available.remove((start[0]+3, start[1]))
                                        available.remove((start[0]+4, start[1]))
                                        return shiplocarray
          else:
                                        startav.remove(start)
                                        return assignship(length, dir)
                    

        if (dir == 'd'):
          if ((available.count(start) > 0) and (available.count((start[0], start[1]+1)) > 0) and (available.count((start[0], start[1]+2)) > 0) and (available.count((start[0], start[1]+3)) > 0) and (available.count((start[0], start[1]+4)) > 0)):

                                        shiplocarray = [start, (start[0], start[1]+1), (start[0], start[1]+2), (start[0], start[1]+3), (start[0], start[1]+4)]
                                        available.remove(start)
                                        available.remove((start[0], start[1]+1))
                                        available.remove((start[0], start[1]+2))
                                        available.remove((start[0], start[1]+3))
                                        available.remove((start[0], start[1]+4))
                                        return shiplocarray
          else:
                                        startav.remove(start)
                                        return assignship(length, dir)

    if (length == 4):
     if (dir == 'r'):
      if ((available.count(start) > 0) and (available.count((start[0]+1, start[1])) > 0) and (available.count((start[0]+2, start[1])) > 0) and (available.count((start[0]+3, start[1])) > 0)):

                                    shiplocarray = [start, (start[0]+1, start[1]), (start[0]+2, start[1]), (start[0]+3, start[1])]
                                    available.remove(start)
                                    available.remove((start[0]+1, start[1]))
                                    available.remove((start[0]+2, start[1]))
                                    available.remove((start[0]+3, start[1]))
                                    return shiplocarray
      else:
                                    startav.remove(start)
                                    return assignship(length, dir)
                

     if (dir == 'd'):
      if ((available.count(start) > 0) and (available.count((start[0], start[1]+1)) > 0) and (available.count((start[0], start[1]+2)) > 0) and (available.count((start[0], start[1]+3)) > 0)):

                                    shiplocarray = [start, (start[0], start[1]+1), (start[0], start[1]+2), (start[0], start[1]+3)]
                                    available.remove(start)
                                    available.remove((start[0], start[1]+1))
                                    available.remove((start[0], start[1]+2))
                                    available.remove((start[0], start[1]+3))
                                    return shiplocarray
      else:
                                    startav.remove(start)
                                    return assignship(length, dir)

    if (length == 3):
     if (dir == 'r'):
      if ((available.count(start) > 0) and (available.count((start[0]+1, start[1])) > 0) and (available.count((start[0]+2, start[1])) > 0)):

                                    shiplocarray = [start, (start[0]+1, start[1]), (start[0]+2, start[1])]
                                    available.remove(start)
                                    available.remove((start[0]+1, start[1]))
                                    available.remove((start[0]+2, start[1]))
                                    return shiplocarray
      else:
                                    startav.remove(start)
                                    return assignship(length, dir)
                

     if (dir == 'd'):
      if ((available.count(start) > 0) and (available.count((start[0], start[1]+1)) > 0) and (available.count((start[0], start[1]+2)) > 0)):

                                    shiplocarray = [start, (start[0], start[1]+1), (start[0], start[1]+2)]
                                    available.remove(start)
                                    available.remove((start[0], start[1]+1))
                                    available.remove((start[0], start[1]+2))
                                    return shiplocarray
      else:
                                    startav.remove(start)
                                    return assignship(length, dir)

    if (length == 2):
     if (dir == 'r'):
      if ((available.count(start) > 0) and (available.count((start[0]+1, start[1])) > 0)):
                                    shiplocarray = [start, (start[0]+1, start[1])]
                                    available.remove(start)
                                    available.remove((start[0]+1, start[1]))
                                    return shiplocarray
      else:
                                    startav.remove(start)
                                    return assignship(length, dir)
                

     if (dir == 'd'):
      if ((available.count(start) > 0) and (available.count((start[0], start[1]+1)) > 0)):

                                    shiplocarray = [start, (start[0], start[1]+1)]
                                    available.remove(start)
                                    available.remove((start[0], start[1]+1))
                                    return shiplocarray
      else:
                                    startav.remove(start)
                                    return assignship(length, dir)

def assignailoc():

    cadirection = random.choice('dr')
    badirection = random.choice('dr')
    sudirection = random.choice('dr')
    crdirection = random.choice('dr')
    dedirection = random.choice('dr')

    ca = assignship(5, cadirection)
    ba = assignship(4, badirection)
    su = assignship(3, sudirection)
    cr = assignship(3, crdirection)
    de = assignship(2, dedirection)

    dict = {'Carrier':ca, 'Battleship':ba, 'Submarine':su, 'Cruiser':cr, 'Destroyer':de}
    # print (dict)
    return dict

def fleet_to_array(fleet):
    result = []
    for v in fleet.values():
        result.extend(v)
    return result


if __name__ == '__main__':

    human = init_human(MAPSIZE, TEST_ARRANGEMENT, TEST_FLEET)
    agent = init_agent(MAPSIZE, TEST_ARRANGEMENT, TEST_FLEET)
    human_turn = True

    while True:
        print 'human map'
        human.my_map.print_map()
        print 'agent map from human perspective'
        human.enemy_map.print_map()
        print 'agent map'
        agent.my_map.print_map()
        print 'human map from agent perspective'
        agent.enemy_map.print_map()
        if human_turn:
            # Prompt a move: enter 11 to hit cell 1, 1
            # Count starts from 0. Read in the move.
            var = raw_input("Make a move: ")

            # Check input length
            if not ((len(var) > 0) and (len(var) < 3)):
                print 'Please enter valid coordinates'
                continue
            x, y = int(var[:-1]), int(var[1:])
            # Check if that coordinate was attacked before
            if human.attacked_before((x,y)):
                print var, 'was attacked before.'
                continue

            # Update corresponding maps
            human.attack(agent, (x,y))

            if agent.lose():
                print 'Human won'
                break

            human_turn = not human_turn
        else:
            # Have the AI make a move
            target = agent.find_target()
            print 'AI attacked', target
            agent.attack(human, target)
            if human.lose():
                print 'AI won'
                break

            human_turn = not human_turn
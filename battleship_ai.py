'''
CS 5100 Proj:   Battleship
Team:           BigLeg
Last Modified:  03/28/2014
'''

import copy
import random

MAPSIZE = 10
HEALTH = 17
EXPLORED = ' '
UNEXPLORED = '-'
OCCUPIED = 'X'
HIT = 'H'
MISS = 'M'

# An arrangement of ships for testing.
TEST_ARRANGEMENT = [
    (0,0), (0,1), (0,2), (0,3), (0,4),
    (1,0), (1,1), (1,2), (1,3),
    (2,5), (3,5), (4,5),
    (7,7), (8,7), (9,7),
    (8,9), (9,9)]

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

    # def mapmax(self):
    #     ''' Find the maximum value of the map for agent
    #     '''
    #     result = 0
    #     for i in range(0, self.size):
    #         for j in range(0, self.size):
    #            if self.m[i][j] > result:
    #                result = self.m[i][j]
    #     return result

    # def maxcoordinates(self, target):
    #     ''' Find the coordinates of the target in the map for agent
    #         This and mapmax are used to help AI locate target
    #     '''
    #     coordinates = []
    #     for i in range(0, self.size):
    #       for j in range(0, self.size):
    #          if self.m[i][j] == target:
    #              coordinates.append((i,j))
    #     return random.choice(coordinates)

    def mark_adjacent_coords(self, (x,y), score):
        ''' Hunt-and-Target
            For agent enemy map: find unexplored adjacent coordinates
            and mark them with score.
        '''
        for (ax,ay) in self.find_adjacent_by_xy((x,y)):
            if self.m[ax][ay] > -1:
                self.m[ax][ay] = score

    def find_adjacent_by_xy(self, (x,y)):
        ''' Find neighbors of a given coordinate.
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
        ''' getter
        '''
        return self.m[x][y]

    def set(self, (x,y), val):
        ''' setter
        '''
        self.m[x][y] = val


class Player:

    my_map = None
    enemy_map = None
    health = 0

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def attack(self, enemy, (x,y)):
        ''' Attack an enemy coordinate and mark result on
            own enemy map.
        '''
        result = enemy.hit((x,y))
        self.enemy_map.set((x,y), result)
        return result

    def hit(self, (x,y)):
        ''' Takes a hit from enemy, calculate score
            and return result to enemy.
        '''
        if self.my_map.get((x,y)) == OCCUPIED:
            self.my_map.set((x,y), ' ')
            self.health = self.health - 1
            return HIT
        return MISS

    def lose(self):
        ''' Tell if player is defeated.
        '''
        return True if self.health == 0 else False


class Agent(Player):

    # target mode parameters
    direction = None   # -1 - up 1 - down -2 - left 2 - right
    candidates = [] # direction candidates
    wrong_direction = False
    reach_end = False
    remain_ships = [5, 4, 3, 3, 2]
    base = None
    current = None # the cell currently being hit
    streak = 0

    hunt_mode = True    

    def attack(self, enemy, (x,y)):
        ''' Attack a coordinate in Hunt-and-Target mode.
        '''
        self.current = (x,y)
        result = enemy.hit((x,y))
        if result == HIT:
            # hit
            self.streak = self.streak + 1
            print 'streak', self.streak
            if self.hunt_mode:
                # enter target mode
                self.hunt_mode = False
                self.base = (x,y)
            else:
                # target mode & hit
                if self.reach_edge():
                    # if edge is reached, set reach_end = True
                    self.reach_end = True

        else:
            # miss
            print 'miss'
            if not self.hunt_mode:
                # target mode: miss
                if self.streak > 1:
                    # reach end
                    self.reach_end = True
                else:
                    # wrong direction
                    self.wrong_direction = True

            # self.enemy_map.mark_adjacent_coords((x,y), 2)
        self.enemy_map.set((x,y), -1)
        return result

    def reach_edge(self):
        ''' Tell if the current direction reaches the map edge.
        '''
        x, y = self.current
        direction = self.direction
        if direction == -1:
            if y == 0:
                return True
        elif direction == 1:
            if y == MAPSIZE - 1:
                return True
        elif direction == -2:
            if x == 0:
                return True
        elif direction == 2:
            if x == MAPSIZE - 1:
                return True
        return False

    def find_target(self):
        ''' Find the next target for attack.
        '''
        if self.hunt_mode:
            return self.hunt()
        else:
            return self.target()

        # return self.choice(self.find_highest_priority())

    def hunt(self):
        ''' Hunt mode
        '''
        print 'hunt'
        return self.choice(0)

    def target(self):
        '''
        keep track of cell discovered, possible directions, remaining ships
        and find the best candidate to attack.
        TODO tear into sub-methods
        '''
        m = self.enemy_map
        base = self.base
        next = None

        if self.direction is None:
            # if direction is not determined yet
            # find undiscovered spaces around the base.
            adjacent = m.find_adjacent_by_xy(base)
            undiscovered_adjacent = [a for a in adjacent if m.get(a) > -1]
            # find all applicable directions.
            for u in undiscovered_adjacent:
                if self.evaluate_direction(u, base):
                    self.candidates.append(u)
            
            # choose one as next direction.
            chosen = random.choice(self.candidates)
            self.candidates.remove(chosen)
            self.direction = self.determine_direction(chosen, base)
            next = chosen
            print 'set direction to', self.direction

        elif self.wrong_direction:
            print 'wrong direction'
            # direction is wrong, choose another one
            chosen = random.choice(self.candidates)
            self.candidates.remove(chosen)
            self.direction = self.determine_direction(chosen, base)
            next = chosen
            self.wrong_direction = False

        elif self.reach_end:
            print 'reach end'
            # reached the edge of map, or hit empty space after a streak > 1.

            # if streak reaches max val in remain_ship
            # sunk a ship. enter hunt mode
            max_ship = max(self.remain_ships)
            if self.streak == max_ship:
                print 'ship', str(max_ship), 'sunk'
                self.hunt_mode = True
                self.direction = None
                self.remain_ships.remove(max_ship)
                self.streak = 0
                print 'streak reset to 0'
                print 'streak', self.streak
                self.candidates = []
                self.base = None
                next = self.hunt()
                print 'remain ships', self.remain_ships
            else:
                # reach end, try the opposite direction
                # may or may not discover more parts of ship as agent
                # doesnt know the ship type.
                self.direction = -self.direction

                chosen = None
                for c in self.candidates:
                    if self.determine_direction(c, base) == self.direction:
                        chosen = c

                if not chosen:
                    # if no opposite option
                    # if streak > 1:
                    # sunk a ship. enter hunt mode
                    if self.streak > 1:
                        print 'ship', str(self.streak), 'sunk'
                        self.hunt_mode = True
                        self.direction = None
                        for s in self.remain_ships:
                            if s == self.streak:
                                self.remain_ships.remove(s)
                        self.streak = 0
                        print 'streak reset to 0'
                        print 'streak', self.streak
                        self.candidates = []
                        self.base = None
                        next = self.hunt()
                        print 'remain ships', self.remain_ships
                    else:
                        # choose another random direction and continue
                        chosen = random.choice(self.candidates)
                        self.candidates.remove(chosen)
                        self.direction = self.determine_direction(chosen, base)
                        next = chosen
                        print 'reset direction to', self.direction
                else:
                    # pursue the opposite direction
                    self.candidates.remove(chosen)
                    next = chosen
                    print 'go to opposite', self.direction

            self.reach_end = False

        else:
            # if everything alright, continue
            next = self.moveon()
            print 'move on direction', self.direction
            # remove all candidates except the opposite
            for c in self.candidates:
                if self.determine_direction(c, base) != -self.direction:
                    self.candidates.remove(c)

        return next

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
        for ship in self.remain_ships:
            valid = self.have_continous_cells(direction, base, ship, MAPSIZE)
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
        if direction == -1: # up
            return (x, y - 1)
        elif direction == 1: # down
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


def init_human(mapsize, arrangement, health):
    ''' Init human object.
    '''
    my_map = Map(size=mapsize)
    my_map.generate_player_map(arrangement)
    enemy_map = Map(size=mapsize)
    enemy_map.generate_human_enemy_map()
    return Human(my_map=my_map, enemy_map=enemy_map, health=health)

def init_agent(mapsize, arrangement, health):
    ''' Init agent.
    '''
    my_map = Map(size=mapsize)
    my_map.generate_player_map(arrangement)
    enemy_map = Map(size=mapsize)
    enemy_map.generate_ai_enemy_map()
    return Agent(my_map=my_map, enemy_map=enemy_map, health=health)

def array_to_arrangement(array):
    ''' Convert two-dimension array to arrangement.
    '''
    arrangement = []
    for i in range(0, MAPSIZE):
        for j in range(0, MAPSIZE):
            if array[i][j]:
                arrangement.append((i,j))
    return arrangement


if __name__ == '__main__':

    human = init_human(MAPSIZE, TEST_ARRANGEMENT, HEALTH)
    agent = init_agent(MAPSIZE, TEST_ARRANGEMENT, HEALTH)
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
'''
CS 5100 Proj:   Battleship
Team:           BigLeg
Last Modified:  03/21/2014
'''
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

    def mapmax(self):
        ''' Find the maximum value of the map for agent
        '''
        result = 0
        for i in range(0, self.size):
            for j in range(0, self.size):
               if self.m[i][j] > result:
                   result = self.m[i][j]
        return result

    def maxcoordinates(self, target):
        ''' Find the coordinates of the target in the map for agent
            This and mapmax are used to help AI locate target
        '''
        coordinates = []
        for i in range(0, self.size):
          for j in range(0, self.size):
             if self.m[i][j] == target:
                 coordinates.append((i,j))
        return random.choice(coordinates)

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
        if (0 <= x <= self.size) and (0 <= y <= self.size):
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
        self.enemy_map.set((x,y), enemy.hit((x,y)))

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

    def attack(self, enemy, (x,y)):
        ''' Attack a human coordinate and mark priority score
            on own enemy map.
        '''
        if enemy.hit((x,y)) == HIT:
            self.enemy_map.mark_adjacent_coords((x,y), 2)
        self.enemy_map.set((x,y), -1)

    def find_target(self):
        ''' Find the next target for attack.
        '''
        return self.enemy_map.maxcoordinates(self.enemy_map.mapmax())


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
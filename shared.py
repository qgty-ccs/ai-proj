MAPSIZE = 10

class Ship:

    coords = []
    t = None
    horizontal = None
    head = None

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def length(self):
        return len(self.coords)

    def find_head(self):
        if not self.head:
            # find head first
            self.head = list(self.coords)[0]
            xory = 0 if self.horizontal else 1
            for c in self.coords:
                if c[xory] < self.head[xory]:
                    self.head = c
        return self.head


def grid_to_array(grid):
    array = []
    for i in range(0, MAPSIZE):
        for j in range(0, MAPSIZE):
            if grid[i][j] == '1':
                array.append((i,j))
    return array

def fleet_to_array(fleet):
    ''' Convert a list of ships into array.
    '''
    result = []
    [result.extend(s.coords) for s in fleet]
    return result
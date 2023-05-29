import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

number_of_cells = int(input())  # amount of hexagonal cells in this map
all_cells = []

class Cell:
    def __init__(self, i, _type, init_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5):
        self.resource_type = _type
        self.index = i
        self.init_resources = init_resources

        self.neigh_0 = neigh_0
        self.neigh_1 = neigh_1
        self.neigh_2 = neigh_2
        self.neigh_3 = neigh_3
        self.neigh_4 = neigh_4
        self.neigh_5 = neigh_5

        self.resources = init_resources
        self.my_ants = 0
        self.opp_ants = 0

    def set_curr(self, resources, my_ants, opp_ants):
        self.resources = resources
        self.my_ants = my_ants
        self.opp_ants = opp_ants


values = {}
resource_type = {}
for i in range(number_of_cells):
    # _type: 0 for empty, 1 for eggs, 2 for crystal
    # initial_resources: the initial amount of eggs/crystals on this cell
    # neigh_0: the index of the neighbouring cell for each direction
    _type, initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [int(j) for j in input().split()]
    all_cells.append(Cell(i, _type, initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5))
    # print(f"{i}: {neigh_0}, {neigh_1}, {neigh_2}, {neigh_3}, {neigh_4}, {neigh_5}", file=sys.stderr, flush=True)
    if initial_resources:
        values[i]=initial_resources
        resource_type[i] = _type

number_of_bases = int(input())
my_base_index = []
for i in input().split():
    my_base_index.append(int(i))
opp_base_index = []
for i in input().split():
    opp_base_index.append(int(i))

print(f"mybase: {my_base_index[0]}", file=sys.stderr, flush=True)

# get all cell distance
all_cell_dist = []
all_cell_dist.append(my_base_index)
flatten_all_cell_dist = [element for sublist in all_cell_dist for element in sublist]
print(f"len(all_cells): {len(all_cells)}", file=sys.stderr, flush=True)
while len(flatten_all_cell_dist) != len(all_cells):
    l_tmp = []
    for c in all_cell_dist[-1]:
        print(f"c: {c}", file=sys.stderr, flush=True)
        if all_cells[c].neigh_0 >= 0 and all_cells[c].neigh_0 not in flatten_all_cell_dist:
            if all_cells[all_cells[c].neigh_0].index not in l_tmp:
                l_tmp.append(all_cells[all_cells[c].neigh_0].index)
        if all_cells[c].neigh_1 >= 0 and all_cells[c].neigh_1 not in flatten_all_cell_dist:
            if all_cells[all_cells[c].neigh_1].index not in l_tmp:
                l_tmp.append(all_cells[all_cells[c].neigh_1].index)
        if all_cells[c].neigh_2 >= 0 and all_cells[c].neigh_2 not in flatten_all_cell_dist:
            if all_cells[all_cells[c].neigh_2].index not in l_tmp:
                l_tmp.append(all_cells[all_cells[c].neigh_2].index)
        if all_cells[c].neigh_3 >= 0 and all_cells[c].neigh_3 not in flatten_all_cell_dist:
            if all_cells[all_cells[c].neigh_3].index not in l_tmp:
                l_tmp.append(all_cells[all_cells[c].neigh_3].index)
        if all_cells[c].neigh_4 >= 0 and all_cells[c].neigh_4 not in flatten_all_cell_dist:
            if all_cells[all_cells[c].neigh_4].index not in l_tmp:
                l_tmp.append(all_cells[all_cells[c].neigh_4].index)
        if all_cells[c].neigh_5 >= 0 and all_cells[c].neigh_5 not in flatten_all_cell_dist:
            if all_cells[all_cells[c].neigh_5].index not in l_tmp:
                l_tmp.append(all_cells[all_cells[c].neigh_5].index)
    all_cell_dist.append(l_tmp[:])
    flatten_all_cell_dist = [element for sublist in all_cell_dist for element in sublist]

print(f"all_cell_dist: {all_cell_dist}", file=sys.stderr, flush=True)
for i in range(len(all_cell_dist)):
    for c in all_cell_dist[i]:
        all_cells[c].distance = i

# game loop
dist_crystal = {}
pre_dest = []

while True:
    values.clear()
    dist_crystal.clear()
    total_my_ants = 0
    for i in range(number_of_cells):
        # resources: the current amount of eggs/crystals on this cell
        # my_ants: the amount of your ants on this cell
        # opp_ants: the amount of opponent ants on this cell
        resources, my_ants, opp_ants = [int(j) for j in input().split()]
        all_cells[i].set_curr(resources, my_ants, opp_ants)
        total_my_ants += my_ants
    for i in range(number_of_cells):
        if all_cells[i].resources:
            values[i]=all_cells[i].resources*(100/total_my_ants if resource_type[i]==1 else 1)*1.0/all_cells[i].distance
            dist_crystal[i]=all_cells[i].distance
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    # Only do re-calculate if one of the pre_dest is done

    sorted_crystal = dict(sorted(values.items(), key=lambda x: x[1], reverse=True))
    sorted_dist_crystal = dict(sorted(dist_crystal.items(), key=lambda x: x[1]))
    iterator = iter(sorted_crystal)
    print(f"crystal: {values}", file=sys.stderr, flush=True)
    if all(key in values for key in pre_dest) and len(set(pre_dest)) == 3:
        dest = pre_dest[:]
    else:
        dest = []
        dest.append(next(iterator))
        if len(values) > 1:
            dest.append(next(iterator))
        if len(values) > 2:
            dest.append(next(iterator))
        #dest.append(next(iter(sorted_dist_crystal)))

    act = ""
    for i in dest:
        act += f"LINE {my_base_index[0]} {i} 1;"
    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
    print(f"{act}")
    pre_dest = dest[:]

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

        self.neighs = [neigh_0,neigh_1,neigh_2,neigh_3,neigh_4,neigh_5]

        self.resources = init_resources
        self.my_ants = 0
        self.opp_ants = 0

    def set_curr(self, resources, my_ants, opp_ants):
        self.resources = resources
        self.my_ants = my_ants
        self.opp_ants = opp_ants

def get_distance(i1, i2):
    if i1 == i2:
        return 0
    distance_list = {i1}
    i = 0
    while i2 not in distance_list:
        i += 1
        curr_list = set()
        for c in distance_list:
            for n in all_cells[c].neighs:
                curr_list.add(n)
        if i2 in curr_list:
            break
        else:
            distance_list = curr_list
            curr_list = set()
    return i

def find_closest_resource(s):
    check_list = [s]
    already_checked = [s]
    while True:
        next_check_list = []
        for i in check_list:
            # print(f"check_list: {check_list}", file=sys.stderr, flush=True)
            # print(f"already_checked: {already_checked}", file=sys.stderr, flush=True)
            for n in all_cells[i].neighs:
                if n >= 0 and all_cells[n].resources > 0:
                    return n
                elif n >= 0 and n not in already_checked:
                    next_check_list.append(n)
                    already_checked.append(n)
        check_list = next_check_list[:]

values = {}
resource_type = {}
target_number = 0
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
        target_number += initial_resources if _type == 2 else 0

target_number /= 2

number_of_bases = int(input())
my_base_index = []
for i in input().split():
    my_base_index.append(int(i))
opp_base_index = []
for i in input().split():
    opp_base_index.append(int(i))

# print(f"mybase: {my_base_index[0]}", file=sys.stderr, flush=True)


# get all cell distance
all_cell_dist = []
all_cell_dist.append(my_base_index)
flatten_all_cell_dist = [element for sublist in all_cell_dist for element in sublist]
print(f"len(all_cells): {len(all_cells)}", file=sys.stderr, flush=True)
while len(flatten_all_cell_dist) != len(all_cells):
    l_tmp = []
    for c in all_cell_dist[-1]:
        #print(f"c: {c}", file=sys.stderr, flush=True)
        for n in all_cells[c].neighs:
            if n >= 0 and n not in flatten_all_cell_dist:
                if all_cells[n].index not in l_tmp:
                    l_tmp.append(all_cells[n].index)

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
    total_crystals = 0
    total_eggs = 0
    myScore, oppScore = [int(j) for j in input().split()]
    for i in range(number_of_cells):
        # resources: the current amount of eggs/crystals on this cell
        # my_ants: the amount of your ants on this cell
        # opp_ants: the amount of opponent ants on this cell
        resources, my_ants, opp_ants = [int(j) for j in input().split()]
        all_cells[i].set_curr(resources, my_ants, opp_ants)
        total_my_ants += my_ants
        total_crystals += (resources if resources > 0 and resource_type[i] == 2 else 0)
        total_eggs += (resources if resources > 0 and resource_type[i] == 1 else 0)

    for i in range(number_of_cells):
        if all_cells[i].resources:
            # factor = (100/total_my_ants*total_crystals/total_eggs if resource_type[i]==1 else 1)
            factor = pow(10, pow((target_number - myScore)/target_number, 2))
            # print(f"factor:{factor}", file=sys.stderr, flush=True)
            values[i]=(factor if resource_type[i]==1 else 1)*1.0/all_cells[i].distance #all_cells[i].resources*
            dist_crystal[i]=all_cells[i].distance
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    # Only do re-calculate if one of the pre_dest is done

    sorted_crystal = dict(sorted(values.items(), key=lambda x: x[1], reverse=True))
    sorted_dist_crystal = dict(sorted(dist_crystal.items(), key=lambda x: x[1]))
    iterator = iter(sorted_crystal)
    print(f"crystal: {values}", file=sys.stderr, flush=True)

    dest = []
    finished_list = []
    double_strength = -1
    for i in pre_dest:
        if all_cells[i].resources > 0 and all_cells[i].my_ants > 0:
            dest.append(i)
        if all_cells[i].resources == 0:
            finished_list.append(i)
    print(f"finished: {finished_list}", file=sys.stderr, flush=True)
    for i in finished_list:
        closest_resource = find_closest_resource(i)
        if closest_resource not in dest:
            dest.append(closest_resource)
    for i in iterator:
        if len(dest) >= math.floor(total_my_ants/10):
            break
        b = False
        for d in dest:
            if all_cells[d].opp_ants >= all_cells[d].my_ants \
            and all_cells[d].my_ants:
                double_strength = d
                b = True
        if b:
            break
        if i not in dest:
            dest.append(i)

    # Add dest neigh
    dest_neigh = []
    for i in dest:
        for n in all_cells[i].neighs:
            if all_cells[n].resources > 0 and n not in dest and n >= 0:
                dest_neigh.append(n)

    act = ""
    strength = len(dest)
    for i in dest:
        strength = 1
        src_0 = get_distance(my_base_index[0], i)
        if len(my_base_index) > 1:
            src_1 = get_distance(my_base_index[1], i)
        else:
            src_1 = 99999
        # print(f"dest: {i} {src_0} {src_1}", file=sys.stderr, flush=True)
        act += f"LINE {my_base_index[0] if src_0 < src_1 else my_base_index[1]} {i} {strength if i != double_strength else strength};"
        strength -= 1
    for i in dest_neigh:
        act += f"BEACON {i} 1;"
    #for k, y in sorted_crystal.items():
    #    act += f"LINE {my_base_index[0]} {k} {round(y)};"
    #print(f"act: {act}", file=sys.stderr, flush=True)
    #final_act = ';'.join(act.split(';')[:round(total_my_ants/10)])

    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
    print(f"{act}")
    pre_dest = dest[:]

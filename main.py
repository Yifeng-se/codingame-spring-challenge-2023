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
        self.distance_to_sources = []
        self.distance_to_opp_base = 9999

    def set_curr(self, resources, my_ants, opp_ants):
        self.resources = resources
        self.my_ants = my_ants
        self.opp_ants = opp_ants

class Base:
    def __init__(self, i):
        self.index = i

        self.dest = []

    def add_dests(self, i):
        self.dest.append(i)

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
                if n >= 0:
                    curr_list.add(n)
        if i2 in curr_list:
            break
        else:
            distance_list = curr_list
            curr_list = set()
    return i

def get_wish_list(s, factor):
    check_list = [s]
    already_checked = set()
    already_checked.add(s)
    wish_list = {}
    found_crystal = False
    found_egg = False
    dist_to_s = 1

    while len(check_list) > 0:
        next_check_list = []

        for i in check_list:
            # print(f"already_checked: {already_checked}", file=sys.stderr, flush=True)

            for n in all_cells[i].neighs:
                if n >= 0 and all_cells[n].resources > 0 and n not in already_checked:
                    if all_cells[n].resource_type==1:
                        found_egg = True
                    if all_cells[n].resource_type==2:
                        found_crystal = True

                    wish_list[n] = (factor if all_cells[n].resource_type==1 else 1)*1.0/dist_to_s
                if n >= 0 and n not in already_checked:
                    next_check_list.append(n)
                    already_checked.add(n)

        check_list = next_check_list[:]
        dist_to_s += 1
        # print(f"check_list: {check_list}, {dist_to_s}", file=sys.stderr, flush=True)
        if (found_egg and factor<=1) \
        or (found_crystal and factor >=1) \
        or (found_crystal and found_egg) \
        or (dist_to_s >= all_cells[s].distance):
            break
    # print(f"wish_list: {wish_list}", file=sys.stderr, flush=True)
    return wish_list


def find_closest_resource(s, factor):
    wish_list = get_wish_list(s, factor)
    if len(wish_list) > 0:
        max_value = max(wish_list.values())
        max_keys = [key for key, value in wish_list.items() if value == max_value]
        sub_list = [all_cells[i] for i in max_keys]
        sub_list.sort(key=lambda obj: (obj.distance, -obj.resources))
        n = sub_list[0].index
        print(f"{s} is done, wish {wish_list}, found new target {n}", file=sys.stderr, flush=True)
        return n


def find_closest_resources(s, factor):
    wish_list = get_wish_list(s, factor)
    max_keys = []
    if len(wish_list) > 0:
        max_value = max(wish_list.values())
        max_keys = [key for key, value in wish_list.items() if value == max_value]

        #sub_list_closer_than_distance = [all_cells[i] for i in sub_list if i.distance > get_distance(s, i)]

    print(f"{s} sub-routes {max_keys}", file=sys.stderr, flush=True)
    return max_keys

values = {}
resource_type = {}
target_number = 0
for r in range(number_of_cells):
    # _type: 0 for empty, 1 for eggs, 2 for crystal
    # initial_resources: the initial amount of eggs/crystals on this cell
    # neigh_0: the index of the neighbouring cell for each direction
    _type, initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [int(j) for j in input().split()]
    all_cells.append(Cell(r, _type, initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5))
    # print(f"{i}: {neigh_0}, {neigh_1}, {neigh_2}, {neigh_3}, {neigh_4}, {neigh_5}", file=sys.stderr, flush=True)
    if initial_resources:
        values[r]=initial_resources
        resource_type[r] = _type
        target_number += initial_resources if _type == 2 else 0

target_number /= 2

number_of_bases = int(input())
my_base_index = []
for r in input().split():
    my_base_index.append(Base(int(r)))
opp_base_index = []
for r in input().split():
    opp_base_index.append(Base(int(r)))

# get all cell distance, each resource belongs to one base
for c in all_cells:
    for b in my_base_index:
        c.distance_to_sources.append(get_distance(c.index, b.index))
    for b in opp_base_index:
        c.distance_to_opp_base = min(c.distance_to_opp_base, get_distance(c.index, b.index))
    c.belongs_to = c.distance_to_sources.index(min(c.distance_to_sources))
    c.distance = min(c.distance_to_sources)
    if c.resources > 0 \
        and (c.resource_type != 1 or c.distance*1.0/c.distance_to_opp_base < 1.5 ):
        my_base_index[c.belongs_to].dest.append(c.index)
    # print(f"Cell: {c.index} {c.distance_to_sources} {c.distance} {c.belongs_to}", file=sys.stderr, flush=True)

# game loop
pre_routes = []
my_pre_score = 0
opp_pre_score = 0
while True:
    values.clear()
    total_my_ants = 0
    total_oop_ants = 0
    total_crystals = 0
    total_eggs = 0
    myScore, oppScore = [int(j) for j in input().split()]
    my_delta_score = myScore - my_pre_score
    opp_delta_score = oppScore - opp_pre_score
    my_pre_score = myScore
    opp_pre_score = oppScore
    for r in range(number_of_cells):
        # resources: the current amount of eggs/crystals on this cell
        # my_ants: the amount of your ants on this cell
        # opp_ants: the amount of opponent ants on this cell
        resources, my_ants, opp_ants = [int(j) for j in input().split()]
        all_cells[r].set_curr(resources, my_ants, opp_ants)
        total_my_ants += my_ants
        total_oop_ants += opp_ants
        total_crystals += (resources if resources > 0 and resource_type[r] == 2 else 0)
        total_eggs += (resources if resources > 0 and resource_type[r] == 1 else 0)

    factor = pow(10, pow(2*((target_number - myScore)/target_number - 0.4), 1))
    print(f"factor:{round(factor,2)} {round((target_number - myScore)/target_number,2)}", file=sys.stderr, flush=True)
    for r in range(number_of_cells):
        if all_cells[r].resources:
            # factor = (100/total_my_ants*total_crystals/total_eggs if resource_type[i]==1 else 1)
            all_cells[r].value=(factor if resource_type[r]==1 else 1)*1.0/all_cells[r].distance #all_cells[i].resources*
        elif all_cells[r].resource_type != 0:
            # there is no resource, remove from Base dest
            if r in my_base_index[all_cells[r].belongs_to].dest:
                my_base_index[all_cells[r].belongs_to].dest.remove(r)
            if r in my_base_index[all_cells[r].belongs_to].sorted_dest:
                my_base_index[all_cells[r].belongs_to].sorted_dest.remove(r)

    for b in my_base_index:
        tmp_dest = [all_cells[d] for d in b.dest]
        sorted_tmp_dest = sorted(tmp_dest, key=lambda obj: obj.value, reverse=True)
        b.sorted_dest = [d.index for d in sorted_tmp_dest]

        print(f"Base: {b.index} {b.dest} {b.sorted_dest}", file=sys.stderr, flush=True)

    sorted_crystal = dict(sorted(values.items(), key=lambda x: x[1], reverse=True))

    iterator = iter(sorted_crystal)
    # print(f"crystal: {values}", file=sys.stderr, flush=True)

    # routes contains tuples, like [(0,35), (1, 25)], means "line 0 35" and "line 1 25"
    # routes can be from cell to cell, not necessary to be base to cell
    routes = []
    finished_routes = []
    routes_length = 0
    double_strength = set()
    max_opp_ants = 0
    for r in pre_routes:
        max_opp_ants = max(max_opp_ants, all_cells[r[1]].opp_ants if all_cells[r[1]].my_ants else 0)
        if all_cells[r[1]].resources > 0 \
            and (all_cells[r[1]].opp_ants <= all_cells[r[1]].my_ants \
                 or total_my_ants > total_oop_ants \
                    or all_cells[r[1]].resource_type == 2): # and all_cells[i].my_ants > 0:
            routes.append(r)
        if all_cells[r[1]].resources == 0 and all_cells[r[1]].my_ants > 0:
            finished_routes.append(r)

    for r in pre_routes:
        if r not in routes:
            for d in my_base_index[all_cells[r[1]].belongs_to].sorted_dest:
                new_route = (my_base_index[all_cells[r[1]].belongs_to].index, d)
                if new_route not in routes \
                    and (all_cells[d].opp_ants <= all_cells[d].my_ants \
                         or total_my_ants > total_oop_ants
                         #\ or all_cells[r[1]].resource_type == 2
                        ):
                    print(f"new_route: {new_route}", file=sys.stderr, flush=True)
                    routes.append(new_route)
                    break

    for r in routes:
        routes_length += get_distance(r[0], r[1])
    base_has_dest = [obj for obj in my_base_index if len(obj.dest) > 0]
    route_add = 0
    new_route_threshold = max(3, max_opp_ants)
    print(f"finished: {finished_routes}, routes: {routes} threshold: {new_route_threshold}", file=sys.stderr, flush=True)

    def routes_length_check(new_route):
        return routes_length == 0 \
            or total_my_ants / (routes_length + get_distance(new_route[0], new_route[1])) >= new_route_threshold+1

    while route_add < max([len(b.sorted_dest) for b in base_has_dest])\
            and (all(all_cells[r[1]].my_ants >= new_route_threshold for r in routes) \
                 or any(all_cells[r[1]].resources / all_cells[r[1]].my_ants <= 3 for r in routes if all_cells[r[1]].my_ants)):
        for b in base_has_dest:
            # find the target from b.index
            if len(b.sorted_dest) > route_add \
                and (b.index, b.sorted_dest[route_add]) not in routes\
                    and (all_cells[b.index].opp_ants <= all_cells[b.index].my_ants \
                         or total_my_ants > total_oop_ants \
                            or all_cells[b.index].resource_type == 2) \
                        and routes_length_check((b.index, b.sorted_dest[route_add])):
                print(f"new_route2: {(b.index, b.sorted_dest[route_add])}", file=sys.stderr, flush=True)
                routes.append((b.index, b.sorted_dest[route_add]))
                routes_length += get_distance(b.index, b.sorted_dest[route_add])

        route_add += 1

    #route_add = 0
    #while (routes_length == 0) \
    #    or (total_my_ants / routes_length >= new_route_threshold+1 \
    #        and route_add < max([len(b.sorted_dest) for b in base_has_dest])\
    #        and (all(all_cells[r[1]].my_ants >= new_route_threshold for r in routes) \
    #             or any(all_cells[r[1]].my_ants >= 2*new_route_threshold for r in routes))):
    #    for b in base_has_dest:
    #        # find the target from b.index
    #        if len(b.sorted_dest) > route_add \
    #            and (b.index, b.sorted_dest[route_add]) not in routes :
    #            print(f"new_route3: {(b.index, b.sorted_dest[route_add])}", file=sys.stderr, flush=True)
    #            routes.append((b.index, b.sorted_dest[route_add]))
    #            routes_length += get_distance(b.index, b.sorted_dest[route_add])
    #    route_add += 1
    # print(f"find final routes: {routes} threshold: {new_route_threshold}", file=sys.stderr, flush=True)

    child_routes = []
    for d in routes:
        print(f"d: {d} oop: {all_cells[d[1]].opp_ants}, my_ants: {all_cells[d[1]].my_ants}", file=sys.stderr, flush=True)
        if all_cells[d[1]].opp_ants and all_cells[d[1]].my_ants:
            double_strength.add(d)
        if all_cells[d[1]].opp_ants >= all_cells[d[1]].my_ants \
            and total_my_ants <= total_oop_ants \
            and all_cells[d[1]].opp_ants > 0:
            double_strength.add(d)
            continue

        # Add child routes
        sub_d = find_closest_resources(d[1], 1)
        for s in sub_d:
            if s not in [r[1] for r in routes] \
            and s not in [r[1] for r in child_routes]:
                if all_cells[s].distance <= get_distance(d[1], s):
                    new_route = (my_base_index[all_cells[s].belongs_to].index, s)
                else:
                    new_route = (d[1], s)

                if routes_length_check(new_route):
                    child_routes.append(new_route)


    print(f"my_ants {total_my_ants} routes: {routes} routes_length {routes_length} child_routes: {child_routes} double: {double_strength}", file=sys.stderr, flush=True)

    act = ""
    strength = len(routes)
    for r in routes:
        strength = 1
        act += f"LINE {r[0]} {r[1]} {strength*2 if r in double_strength else strength};"
        strength -= 1
    for r in child_routes:
        strength = 1
        #if all_cells[r[0]].my_ants > 0:
        act += f"LINE {r[0]} {r[1]} {strength};"

    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
    print(f"{act}")
    pre_routes = routes[:]

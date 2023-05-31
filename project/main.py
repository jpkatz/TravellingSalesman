import json
from algorithm.milp_tsp import TSP

read_file = 'project/test_bank/size_5_version_1.json'

file = open(read_file)
graph = json.load(file)
file.close()

tsp = TSP(graph)
tsp.build_mip()
tsp.solve_mip()
optimal_tour = tsp.get_dict_solution()

from pprint import pprint
pprint(optimal_tour)
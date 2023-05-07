import pyscipopt as popt
import json


def solve_mip(model):
    model.optimize()
    for v in model.getVars():
        if model.getVal(v) > 0.5:
            print("%s: %d" % (v, round(model.getVal(v))))


def build_mip(graph):
    model = generate_model()
    x_ij = build_variables(model, graph)
    build_constraints(model, graph, x_ij)
    build_objective(model, graph, x_ij)
    return model


def generate_model():
    model = popt.Model()
    return model


def build_variables(model, graph):
    x_ij = {}
    for first_city, connections in graph.items():
        for second_city, distance in connections.items():
            x_ij[first_city, second_city] = model.addVar(vtype='B', name="x_(%s,%s)" % (first_city, second_city))
    return x_ij


def build_constraints(model, graph, x_ij):
    # one exit from city
    for city_i, connections in graph.items():
        terms = []
        for city_j in connections.keys():
            term = x_ij[city_i, city_j]
            terms.append(term)
        model.addCons(popt.quicksum(terms) == 1)

    # one entrance to city
    for city_i, connections in graph.items():
        terms = []
        for city_j in connections.keys():
            term = x_ij[city_j, city_i]
            terms.append(term)
        model.addCons(popt.quicksum(terms) == 1)


def build_objective(model, graph, x_ij):
    obj_terms = []
    for first_city, connections in graph.items():
        for second_city, distance in connections.items():
            term = distance * x_ij[first_city, second_city]
            obj_terms.append(term)
    model.setObjective(popt.quicksum(obj_terms), "minimize")


if __name__ == '__main__':
    path_to_test = '../test_bank/3_city_test.json'
    f = open(path_to_test)
    test_problem = json.load(f)
    model = build_mip(test_problem)
    solve_mip(model)

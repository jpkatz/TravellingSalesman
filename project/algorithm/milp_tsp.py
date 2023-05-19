import pyscipopt as popt
import json

class TspConsHandler(popt.Conshdlr):
    def __init__(self, variables):
        self.variables = variables
        self.nodes = None

    def add_node_names(self, nodes):
        self.nodes = nodes

    def find_subtours(self, solution=None):
        xij = self.variables
        total_cycle_len = len(self.nodes)
        # TODO: guard against infeasible solutions based on existing constraints? Presolve problem?
        keep_traversing = True
        len_local_cycle = 0
        initial_source = next(iter(self.nodes.keys()))
        source = initial_source
        while keep_traversing:
            for destination in self.nodes[source].keys():
                mip_variable = xij[source, destination]
                variable_value = self.model.getSolVal(solution, mip_variable)
                if variable_value > 0.5:
                    source = destination
                    len_local_cycle += 1
                    if source == initial_source:
                        keep_traversing = False
                    break
            else:
                return solution
        if len_local_cycle < total_cycle_len:
            return solution
        return None

    def conscheck(self, constraints, solution, check_integrality,
                  check_lp_rows, print_reason, completely):
        if self.find_subtours(solution):
            return {"result": popt.SCIP_RESULT.INFEASIBLE}
        else:
            return {"result": popt.SCIP_RESULT.FEASIBLE}

    def consenfolp(self, constraints, n_useful_conss, solinfeasible):
        # TODO: Figure out what this does
        subtours = self.find_subtours()
        if subtours:
            x = self.variables
            for subset in subtours:
                # self.model.addCons(popt.quicksum(x[i, j] for (i, j) in pairs(subset))
                #                    <= len(subset) − 1)
                # print("cut: len (%s) <= %s" % (subset, len(subset) − 1))
                return {"result": popt.SCIP_RESULT.CONSADDED}
        else:
            return {"result": popt.SCIP_RESULT.FEASIBLE}

    def conslock(self, constraint, locktype, nlockspos, nlocksneg):
        x = self.variables
        for x_var in x.values():
            self.model.addVarLocks(x_var, nlocksneg, nlockspos)

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

    constraint_hanlder = TspConsHandler(x_ij)
    constraint_hanlder.add_node_names(graph)
    model.includeConshdlr(constraint_hanlder, 'TSP', 'TSP Subtour Elimination', needscons=False)

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
    path_to_test = '../test_bank/4_city_test.json'
    f = open(path_to_test)
    test_problem = json.load(f)
    model = build_mip(test_problem)
    solve_mip(model)

import pyscipopt as popt
import json

class SHP:
    def __init__(self, graph) -> None:
        self.graph = graph
        self.model = self.generate_model()

        self.x_ij = {}
        self.si = {}
        self.ei = {}

    def solve_mip(self):
        self.model.optimize()
        for v in self.model.getVars():
            if self.model.getVal(v) > 0.5:
                print("%s: %d" % (v, round(self.model.getVal(v))))


    def build_mip(self):
        self.build_variables()
        self.build_constraints()
        self.build_objective()


    def generate_model(self):
        model = popt.Model()
        return model


    def build_variables(self):
        for first_city, connections in self.graph.items():
            for second_city, distance in connections.items():
                self.x_ij[first_city, second_city] = self.model.addVar(vtype='B', 
                                                                       name="x_(%s,%s)" 
                                                                       % (first_city, second_city)
                                                                       )
        for city in self.graph.keys():
            self.si[city] = self.model.addVar(vtype='B',
                                              name='s_(%s)' % (city)
                                              )
            self.ei[city] = self.model.addVar(vtype='B',
                                              name='e_(%s)' % (city)
                                              )


    def build_constraints(self):
        # one exit from city
        for city_i, connections in self.graph.items():
            terms = []
            for city_j in connections.keys():
                term = self.x_ij[city_i, city_j]
                terms.append(term)
            self.model.addCons(popt.quicksum(terms) == 1 - self.si[city_i])

        # one entrance to city
        for city_i, connections in self.graph.items():
            terms = []
            for city_j in connections.keys():
                term = self.x_ij[city_j, city_i]
                terms.append(term)
            self.model.addCons(popt.quicksum(terms) == 1 - self.ei[city_i])

        # one city doesnt have exit
        self.model.addCons(popt.quicksum(self.si[city] for city in self.graph.keys()) == 1)

        # one city doesnt have entrance
        self.model.addCons(popt.quicksum(self.ei[city] for city in self.graph.keys()) == 1)

    def build_objective(self):
        obj_terms = []
        for first_city, connections in self.graph.items():
            for second_city, distance in connections.items():
                term = distance * self.x_ij[first_city, second_city]
                obj_terms.append(term)
        self.model.setObjective(popt.quicksum(obj_terms), "minimize")


if __name__ == '__main__':
    path_to_test = './project/test_bank/4_city_test.json'
    f = open(path_to_test)
    test_problem = json.load(f)
    shp = SHP(test_problem)
    shp.build_mip()
    shp.solve_mip()

import pyscipopt as popt
import json

class SHP:
    def __init__(self, graph) -> None:
        self.graph = graph
        self.model = self.generate_model()

        self.x_ij = {}
        self.si = {}
        self.ei = {}

    def solve_n_mip(self, n):
        self.model.hideOutput()
        self.solve_mip()
        for iter in range(n):
           starting_var = [x for x in self.ei.values() if self.model.getVal(x) > 0.5][0]
           ending_var = [x for x in self.si.values() if self.model.getVal(x) > 0.5][0]
           self.model.freeTransform()
           self.model.addCons(starting_var + ending_var <= 1)
           self.model.freeTransform()
           self.solve_mip()



    def solve_mip(self):
        self.model.optimize()
        self.print_path()

    def print_path(self):
        for starting_name, starting_var in self.ei.items():
            if self.model.getVal(starting_var) > 0.5:
                print('The starting position: {}'.format(starting_name))
                break
        for ending_name, ending_var in self.si.items():
            if self.model.getVal(ending_var) > 0.5:
                print('The ending position: {}'.format(ending_name))
                break
        print('---')
        print('The path is as follows:')
        total_path_len = len(self.graph.keys()) - 1
        keep_traversing = True
        len_path = 0
        initial_source = starting_name
        source = initial_source
        max_iter = total_path_len + 1
        iter = 0
        while keep_traversing:
            print('Current position: {}'.format(source))
            for destination in self.graph[source].keys():
                mip_variable = self.x_ij[source, destination]
                variable_value = self.model.getVal(mip_variable)
                if variable_value > 0.5:
                    source = destination
                    len_path += 1
                    
                    break
            else:
                if source != ending_name:
                    print('Unable to find connecting city: {}'
                        .format(source))
                else:
                    print('---')
                    print('Completed, Ending city: {}'.format(ending_name))
                keep_traversing = False
            
            iter += 1
            if iter > max_iter:
                print('Exceeded max iterations')
                break

        if len_path < total_path_len:
            print('The path is not complete it seems: path {} vs total {}'
                  .format(len_path, total_path_len))


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
    shp.solve_n_mip(2)

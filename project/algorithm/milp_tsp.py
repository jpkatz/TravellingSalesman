import pyscipopt as popt


def main():
    model = popt.Model()
    model.hideOutput()
    x = model.addVar("x", "B")
    y = model.addVar("y", "B")
    z = model.addVar("z", "B")
    r = model.addVar("r", "B")
    model.addConsAnd([x, y, z], r)
    model.addCons(x == 1)
    model.setObjective(r, sense="minimize")
    model.optimize()
    print("* %s *" % 'AND')
    objSet = bool(model.getObjective().terms.keys())
    print("* Is objective set? %s" % objSet)
    if objSet:
        print("* Sense: %s" % model.getObjectiveSense())
    for v in model.getVars():
        if v.name != "n":
            print("%s: %d" % (v, round(model.getVal(v))))
    print("\n")
    print('Hello there')


if __name__ == '__main__':
    main()

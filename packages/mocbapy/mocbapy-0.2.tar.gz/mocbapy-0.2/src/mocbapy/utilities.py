# coding=utf-8
import optlang
from collections import defaultdict
from cobra.util import solver as list_solvers
from warnings import warn
from tqdm import tqdm


def choose_optlang_interfase(solver=None):
    """Returns a solver instance"""
    avail = [sol.lower() for sol, exist in optlang.available_solvers.items() if exist]
    if solver is None:
        warn("Warning: No solver selected. Available solvers: {}".format(str(avail)))
        if len(avail) == 0:
            raise RuntimeError("No solvers available. Try to install glpk or scipy packages")
        warn("Picking {} as solver".format(avail[0]))
        solver = avail[0]
    solver = solver.lower()
    if solver not in avail:
        raise RuntimeError("Solver \'{}\' not available. Available solvers: {}".format(solver, str(avail)))
    #TODO: Remove dependence on cobra.util if possible
    return list_solvers.solvers[solver]


def get_common_mets(model_list):
    """
        Naive implementation of getting common exchange metabolites, using their id's.
        It assumes that identical metabolites have the same id.
    """
    common_mets = defaultdict(dict)
    for model in model_list:
        for rxn_ex in model.exchanges:
            for met_ex in rxn_ex.metabolites:
                common_mets[(met_ex.id, model)] = met_ex.id
    return dict(common_mets)


def sum_from_list(list_expr):
    """ Dichotomous construction of expressions"""
    def sum_from_list_p(le, a, b):
        if a == b:
            return 0
        else:
            if b - a == 1:
                return le[a]
            else:
                middle = int((a+b)/2)
                return sum_from_list_p(le, a, middle) + sum_from_list_p(le, middle, b)

    return sum_from_list_p(list_expr, 0, len(list_expr))


def build_base_opt_model(ecomodel, solver=None):
    """ Builds the underlying base optimization problem Sv = 0, lb <= v <= ub """
    interfase = choose_optlang_interfase(solver)
    model = interfase.Model(name='Base Solver Model')
    m, n = ecomodel.Ssigma.shape
    assert m == len(ecomodel.sysmetabolites)
    assert n == len(ecomodel.sysreactions)
    # Create flux variables
    flux_variables = [interfase.Variable(rxn, lb=ecomodel.lb[i], ub=ecomodel.ub[i]) for i, rxn in
                      enumerate(ecomodel.sysreactions)]
    model.add(flux_variables, sloppy=True)
    model.update()
    for i in tqdm(range(m)):
        terms_const = [flux_variables[j] * ecomodel.Ssigma[i, j] for j in range(n) if ecomodel.Ssigma[i, j] != 0]
        mass_const = interfase.Constraint(sum_from_list(terms_const), lb=0, ub=0)
        model.add(mass_const, sloppy=True)
    model.update()
    model.objective = interfase.Objective(0, direction="max")
    return model

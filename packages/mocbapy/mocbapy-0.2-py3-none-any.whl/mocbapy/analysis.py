import pandas
from warnings import warn
from benpy import solve as bensolve
from .utilities import choose_optlang_interfase, build_base_opt_model
from tqdm import tqdm


def mo_fba(ecosystem_model, **kwargs):
    """Solve the Ecosystem Model using bensolve procedure"""
    vlp_eco = ecosystem_model.to_vlp(**kwargs)
    return bensolve(vlp_eco)

#TODO: Check cobra code for a speed up
def mo_fva(ecosystem_model, fba=None, reactions=None, alpha=0.9, solver=None):
    """Calculate the MO-FVA near the Pareto Front """
    # optlang usage:
    # x1 = interfase.Variable("x1", lb=0, ub=20)
    # x2 = interfase.Variable("x2", lb=0, ub=10)
    # c1 = interfase.Constraint(2 * x1 - x2, lb=0, ub=0)  # Equality constraint
    # model.add([x1, x2, c1])
    # model.objective = interfase.Objective(x1 + x2, direction="max")
    if fba is None:
        raise RuntimeError("No MO-FBA restriction were given")
    interfase = choose_optlang_interfase(solver)
    warn("Building base optimization model")
    base_model = build_base_opt_model(ecosystem_model, solver=solver)
    base_model.update()
    rxn_dict = {r.name: r for r in base_model.variables}
    if reactions is None:
        warn("No selected reactions for FVA")# Go for all
        reactions = rxn_dict.keys()
    fva_res = {rxn: {} for rxn in reactions}
    for obj_id, value in fba.items():
        var = rxn_dict[obj_id]
        base_model.add(interfase.Constraint(var, ub=value, lb=value * alpha))
        print("Adding Constraint {}*{} <= {} <= {}".format(alpha, value, obj_id, value))
    base_model.update()

    for senses in ("minimum", "maximum"):
        synonyms = {"minimum": "min", "maximum": "max"}
        print("Solving {} optimizations".format(senses))
        for rxn in tqdm(reactions):
            flux = rxn_dict[rxn]
            base_model.objective = interfase.Objective(flux, direction=synonyms[senses])
            base_model.update()
            base_model.optimize()
            fva_res[rxn][senses] = flux.primal

    return pandas.DataFrame.from_dict(fva_res, orient='index')

# mocbapy test file
import cobra.io
import mocbapy.utilities
import mocbapy.analysis
#import mocbapy.draw
import numpy as np
import re
from mocbapy.EcosystemModel import create_model, bensolve_default_options

test_arr = list()
n_test = 2
for i in range(n_test):
    model = cobra.io.load_model("textbook")
    model.id = model.id + '_' + str(i+1)
    test_arr.append(model)

common_mets = mocbapy.utilities.get_common_mets(test_arr)
test_EcoSys = create_model(model_array=test_arr, metabolic_dict=common_mets)

index_gluc_pool = test_EcoSys.sysreactions.index("EX_glc__D_e:pool")
test_EcoSys.lb[index_gluc_pool] = -5

bensolve_opts = bensolve_default_options()
bensolve_opts['message_level'] = 0
sol_mofba = mocbapy.analysis.mo_fba(test_EcoSys, options=bensolve_opts)
print(sol_mofba)

#Extract extreme points
ext_points = np.asarray([v for i, v in enumerate(sol_mofba.Primal.vertex_value) if sol_mofba.Primal.vertex_type[i] == 1])

#Max values of each model in the pareto front
max_vals = np.amax(ext_points,0)

#test = mocbapy.draw.draw2d(sol_mofba)

#fig, ax = mocbapy.draw.draw2d(sol_mofba)
#fig.savefig('test2D.png')

#fba_res = {obj: 0.5 for obj in test_EcoSys.objectives}
fba_res = {'{}:{}'.format(v[0][0],k): 0.5 for k, v in test_EcoSys.objectives.items()}
ex_rxn = [r for r in test_EcoSys.sysreactions if re.match('.*:pool',r)]
fva_test = mocbapy.analysis.mo_fva(test_EcoSys, fba=fba_res, reactions=ex_rxn)

#fig, ax = mocbapy.draw.draw3d(sol_mofba.Primal,norm_facts=max_vals)
#fig.savefig('test_norm.png')

#Objective reactions:
#test_EcoSys.sysreactions[7]
#test_EcoSys.sysreactions[2590]

#base_problem = build_base_opt_model(test_EcoSys, solver='glpk')
#Pick up one extrme point
#pext_3=sol_mofba.Primal.vertex_value[3]
#fva_dict = {test_EcoSys.sysreactions[7]:pext_3[0], test_EcoSys.sysreactions[2590]:pext_3[1]}
#fva_res_pext3 = mocbapy.mo_fva(test_EcoSys, fba=fva_dict, solver='gurobi')

#pext_4=sol_mofba.Primal.vertex_value[4]
#fva_dict = {test_EcoSys.sysreactions[7]:pext_4[0], test_EcoSys.sysreactions[2590]:pext_4[1]}
#fva_res_pext4 = mocbapy.mo_fva(test_EcoSys, fba=fva_dict, solver='glpk')

# -*- coding: utf-8 -*-
"""
Created on Thu May  4 15:35:50 2017
Construct Ecosystem model
@author: mbudinich
"""
from benpy import vlpProblem
from collections import OrderedDict, defaultdict
from warnings import warn

from cobra.util.array import create_stoichiometric_matrix
from numpy import zeros
from scipy.sparse import lil_matrix, block_diag, eye


# TODO: Speed up FVA (using chached model?)
class EcosystemModel:

    def _construct_ecosystem_pool( self ):
        """Check all metabolites used in import/export exchanges and construct the pool compartment"""
        # TODO: Skip all reactions not EX (see Thiele et the thousand authors COBRA conventions)
        pooldict = defaultdict(list)
        for model in self.models:
            for rxn_ex in model.exchanges:
                for met_ex in rxn_ex.metabolites:
                    if (met_ex.id, model) in self.metabolic_dict:
                        met_name = self.metabolic_dict[(met_ex.id, model)]
                        pooldict[met_name].append((model, rxn_ex, rxn_ex.get_coefficient(met_ex.id)))
        self._pooldict = dict(pooldict)

    def _populate_ecosystem_model( self ):
        """Calculate the object attributes after pool construction"""
        self.pool_ex_rxns = []
        self.pool_ex_mets = []
        pool_ub = []
        pool_lb = []
        cnt=0
        for key in self._pooldict.keys(): #pooldict.keys() are met, so the medium dict must be based on met too.
            self.pool_ex_rxns.append("EX_{}:pool".format(key))
            self.pool_ex_mets.append("{}:pool".format(key))
            if self.medium != None and key in self.medium.keys():
                pool_lb.append(self.medium[key][0])
                pool_ub.append(self.medium[key][1])
                cnt = cnt+1
            else:
                pool_lb.append(-1000)
                pool_ub.append(1000) 
        print('nb of bounds modified by medium : ',cnt)
        self.sysreactions = []
        self.sysmetabolites = []
        self.lb = []
        self.ub = []
        self.objectives = OrderedDict()
        for model in self.models:
            self.objectives[model] = []
        for model in self.models:
            for r in model.reactions:
                new_name = "{}:{}".format(r.id, model.id)
                self.sysreactions.append(new_name)
                self.lb.append(r.lower_bound)
                self.ub.append(r.upper_bound)
                if r.objective_coefficient != 0:
                    self.objectives[model].append((r.id, r.objective_coefficient))
            for m in model.metabolites:
                self.sysmetabolites.append("{}:{}".format(m.id, model.id))
        self.sysreactions.extend(self.pool_ex_rxns)
        self.sysmetabolites.extend(self.pool_ex_mets)
        self.lb.extend(pool_lb)
        self.ub.extend(pool_ub)

        array_form = block_diag([create_stoichiometric_matrix(model, array_type="lil")
                                 for model in self.models],
                                format="lil")

        self.Ssigma = block_diag([array_form, -eye(len(self.pool_ex_rxns))], format="lil")
        for met in self._pooldict.keys():
            met_name = "{}:pool".format(met)
            met_idx = self.sysmetabolites.index(met_name)
            for model, reaction, coeff in self._pooldict[met]:
                rxn_name = "{}:{}".format(reaction.id, model.id)
                rxn_idx = self.sysreactions.index(rxn_name)
                self.Ssigma[met_idx, rxn_idx] = -coeff

    def __init__( self, model_array=None, metabolic_dict=None, medium=None ):
        """Instantiate the EcosystemModel object model_array is an array of cobra models to connect
        metabolic_dict is a dictionary such as:
            * Its keys correspond to tuples (metabolite_id,model)
            * Its value correspond to the id that will be used in the model
        """

        self.models = model_array
        self.models_ids = [getattr(m, 'id', 'model_{}'.format(model_array.index(m))) for m in model_array]
        self.metabolic_dict = metabolic_dict
        self.medium = medium
        self._pooldict = None
        self.pool_ex_rxns = None
        self.pool_ex_mets = None
        self.Ssigma = None
        self.sysreactions = None
        self.sysmetabolites = None
        self.lb = None
        self.ub = None
        self.objectives = None
        if model_array is not None and metabolic_dict is not None:
            self._construct_ecosystem_pool()
            self._populate_ecosystem_model()
        elif model_array is None:
            warn("Models array is empty")
        elif metabolic_dict is None:
            warn("No metabolic dictionary is given")

    def add_compartment( self, model ):
        """Utility function to add a new agent to models.
        Pretty inefficient, re-runs all the steps again for each addition"""
        self.__init__(self.models.add(model), self.metabolic_dict)

    def add_pool_reaction( self, name, reaction, lb=-1000, ub=1000):
        """Adds manually a reaction to the pool.
        Require a dictionary of pool metabolites:stoichiometric coefficient"""
        # First, we check reactions and metabolites to add. Reaction is sure to be new, metabolites need to be checked
        if name in self.pool_ex_rxns:
            raise RuntimeError("Reaction already included")
        (nm, nr) = self.Ssigma.shape
        self.sysreactions.append(name)
        nr = nr + 1
        self.lb.append(lb)
        self.ub.append(ub)
        rxn_idx = self.sysreactions.index(name)
        for met in reaction.keys():
            if met not in self.sysmetabolites:
                self.sysmetabolites.append(met)
                nm = nm + 1

        # Copy of old values
        new_Ssigma = lil_matrix((nm, nr))
        (l1, l2) = self.Ssigma.nonzero()
        for im, ir in zip(l1, l2):
            new_Ssigma[im, ir] = self.Ssigma[im, ir]

        # new stoich. index in new_Ssigma
        for met in reaction.keys():
            met_idx = self.sysmetabolites.index(met)
            new_Ssigma[met_idx, rxn_idx] = reaction[met]
        # Replacement of Ssigma
        self.Ssigma = new_Ssigma

    def to_vlp( self, **kwargs ):
        """Returns a vlp problem from EcosystemModel"""
        # We are using bensolve-2.0.1:
        # B is coefficient matrix
        # P is objective Marix
        # a is lower bounds for B
        # b is upper bounds for B
        # l is lower bounds of variables
        # s is upper bounds of variables
        # opt_dir is direction: 1 min, -1 max
        # Y,Z and c are part of cone definition. If empty => MOLP
        vlp = vlpProblem(**kwargs)
        m, n = self.Ssigma.shape
        q = len(self.models)
        vlp.B = self.Ssigma
        vlp.a = zeros((1, m))[0]
        vlp.b = zeros((1, m))[0]
        vlp.l = self.lb
        vlp.s = self.ub
        vlp.P = lil_matrix((q, n))
        vlp.opt_dir = -1
        for i in range(q):
            for rxn, coeff in self.objectives[self.models[i]]:
                new_name = "{}:{}".format(rxn, self.models[i].id)
                k = self.sysreactions.index(new_name)
                print((i, k))
                vlp.P[i, k] = coeff
        vlp.Y = None
        vlp.Z = None
        vlp.c = None
        return vlp


def create_model( model_array=None, metabolic_dict=None, medium=None ):
    """Returns ans EcosystemModel from parameters"""
    return EcosystemModel(model_array=model_array, metabolic_dict=metabolic_dict, medium=medium)


def bensolve_default_options():
    """Returns default options for bensolve """
    return vlpProblem().default_options

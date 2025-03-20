import numpy as np
import pandas as pd

class CGE_IO_Data(object):
    def __init__(self, sam, Ind, Com, Fac, Con):
        # Intermediate input QX
        self.intermediate_matrix = sam.loc[Com, Ind]
        # Total output X
        self.total_production = sam.loc['Total', Ind]
        # Commodity matrix XQ
        self.commodity_matrix = sam.loc[Ind, Com]
        # Factor input V
        self.factor = sam.loc[Fac, Ind]
        # Final demand FD
        self.final_demand = sam.loc[Com, Con].T
        # Total demand
        self.total_demand = self.final_demand.sum(axis=1)
        # Factor endowment
        self.factor_endow = self.factor.sum(axis=1)
        # Total income:
        self.income = self.factor_endow

        # generate dict
        self.intermediate_matrix = self.intermediate_matrix.stack().to_dict()
        self.final_demand = self.final_demand.stack().to_dict()
        self.factor = self.factor.stack().to_dict()
        self.total_production = self.total_production.to_dict()
        self.commodity_matrix = self.commodity_matrix.stack().to_dict()
        self.income = self.income.to_dict()

class CGE_Exo_Param(object):
    def __init__(self, CGE_IO_Data, Ind, Com, Fac, Con):
        # Initial elasticity value
        self.elas_subs_utility = 0.5
        self.elas_subs_prod = 0.5

        # Initial price value
        self.price_commodity = {key: 1 for key in Com}
        self.price_factor = {key: 1 for key in Ind}
        self.price_utility = 1
        self.price_ind = {key: 1 for key in Ind}

        # Calibrated parameters
        self.share_param_utility = {}
        for cc in Com:
            self.share_param_utility[cc] = (self.price_commodity[cc] * CGE_IO_Data.final_demand['Gov', cc]) ** (1 / self.elas_subs_utility) / sum(
                self.price_commodity[cc] * CGE_IO_Data.final_demand['Gov', cc] ** (1 / self.elas_subs_utility) for cc in Com)

        self.share_param_inter_prod = {}
        for ind in Ind:
            for cc in Com:
                self.share_param_inter_prod[cc, ind] = (self.price_commodity[cc] * CGE_IO_Data.intermediate_matrix[cc, ind]) ** (1 / self.elas_subs_prod) / (sum((self.price_commodity[cc]
                                                                       * CGE_IO_Data.intermediate_matrix[cc, ind] ** (1 / self.elas_subs_prod) for cc in Com))
                                                                       + (self.price_factor[ind] * CGE_IO_Data.factor['Fac', ind]) ** (1 / self.elas_subs_prod))

        self.share_param_factor_prod = {}
        for ind in Ind:
            self.share_param_factor_prod[ind] = (self.price_factor[ind] * CGE_IO_Data.factor['Fac', ind]) ** (1 / self.elas_subs_prod) / (sum((self.price_commodity[cc]
                                                                     * CGE_IO_Data.intermediate_matrix[cc, ind] ** (1 / self.elas_subs_prod) for cc in Com))
                                                                      + (self.price_factor[ind] * CGE_IO_Data.factor['Fac', ind]) ** (1 / self.elas_subs_prod))

        self.share_production_to_com = {}
        for ind in Ind:
            for cc in Com:
                self.share_production_to_com[ind, cc] = CGE_IO_Data.commodity_matrix[ind, cc] / CGE_IO_Data.total_production[ind]

        self.scale_utility = 1/self.price_utility * sum((self.share_param_utility[cc]**self.elas_subs_utility) * (
                                self.price_commodity[cc]**(1-self.elas_subs_utility)) for cc in Com)**(1/(1-self.elas_subs_utility))

        self.scale_prod_ces = {}
        for ind in Ind:
            self.scale_prod_ces[ind] = CGE_IO_Data.total_production[ind] / (sum(self.share_param_inter_prod[cc, ind] * CGE_IO_Data.intermediate_matrix[cc, ind] ** (1 - 1 / self.elas_subs_prod) for cc in Com)
                                                           + self.share_param_factor_prod[ind] * CGE_IO_Data.factor['Fac', ind] ** (1 - 1 / self.elas_subs_prod)) ** (self.elas_subs_prod / (self.elas_subs_prod - 1))
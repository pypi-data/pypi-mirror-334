import numpy as np
import pandas as pd
from scipy import optimize as opt

import Code.Calibration as Calibration
import Code.Consumer as Cons
import Code.Producer as Prod
import Code.MacroEconomy as Macro
import Code.CGESystem as CGE

sam_table = pd.read_excel(r"D:\OneDriveSyn\OneDrive - The University of Hong Kong - Connect\SynJunex\Project\HKU\CGE\Data\SAM.xlsx")
sam_table = sam_table.set_index('Cat')
# Define sets in the model
Ind = ['Pri', 'Sec', 'Ter']
Com = ['Com1', 'Com2', 'Com3']
Fac = ['Fac']
Con = ['Gov']

def execute():

    error_term = 100
    iteration = 0
    max_iteration = 5000
    max_tolerance = 1e-10
    adjust_rate = 0.1

    vars = Calibration.CGE_IO_Data(sam_table, Ind, Com, Fac, Con)
    params = Calibration.CGE_Exo_Param(vars, Ind, Com, Fac, Con)

    price_commodity_array = np.array(list(params.price_commodity.values()))
    #price_commodity_array = np.array([1.0, 3.0, 3.0])
    price_ind_init = params.price_commodity
    #price_factor_init = params.price_factor
    price_factor_init = {key: 5 for key in Ind}
    price_utility_init = params.price_utility

    factor = vars.factor
    total_production = vars.total_production

    while (error_term > max_tolerance) & (iteration < max_iteration):
        iteration += 1
        cge_args = [vars, params, Ind, Com, Fac, Con, factor, total_production]

        print('Iteration =', iteration)
        print('Initialized product price =', price_commodity_array)

        results = opt.root(CGE.cge_system, price_commodity_array, args=cge_args, method='lm', tol=1e-5)
        price_commodity_array = results.x
        price_commodity_array[0] = 1.0
        price_commodity = dict(zip(Com, price_commodity_array))

        #price_ind = Prod.price_production(params.share_production_to_com, price_commodity, Ind, Com)
        #total_final_demand = Cons.agg_final_demand(final_demand, Com)
        price_util = Cons.price_utility(params.scale_utility, params.share_param_utility, params.elas_subs_utility, params.price_commodity, Com)
        marginal_cost = Prod.marginal_prod_cost(params.scale_prod_ces, params.share_param_inter_prod, params.elas_subs_prod, price_commodity, params.share_param_factor_prod, params.price_factor, Ind, Com)
        factor = Prod.factor_demand(total_production, params.scale_prod_ces, params.share_param_factor_prod, marginal_cost, params.price_factor, params.elas_subs_prod, Ind, Com)
        factor_endow = Cons.factor_endowment(factor, Ind)
        income = Cons.labour_income(params.price_factor, factor, Ind)
        final_demand = Cons.final_consumption(params.share_param_utility, params.price_commodity, params.elas_subs_utility, params.price_utility, params.scale_utility, income, Com)
        intermediate_matrix = Prod.intermediate_demand(total_production, params.scale_prod_ces, params.share_param_inter_prod, marginal_cost, params.price_commodity, params.elas_subs_prod, Ind, Com)

        total_production_process = Prod.total_production(params.scale_prod_ces, params.share_param_inter_prod, intermediate_matrix, params.share_param_factor_prod, factor, params.elas_subs_prod, Ind, Com)
        price_commodity_process = Prod.price_commodity(marginal_cost, params.share_production_to_com, Ind, Com)
        print("production", total_production_process)
        utility_cons = Cons.consumer_utility(params.scale_utility, params.share_param_utility, final_demand, params.elas_subs_utility, Com)

        GDP1 = Macro.gdp_use(params.share_production_to_com, params.price_commodity, vars.total_production, intermediate_matrix, Ind, Com)
        GDP2 = Macro.gdp_consumption(params.price_commodity, final_demand, Com)
        GDP3 = Macro.gdp_value_added(params.price_factor, factor, Ind)
        final_price_commodity = price_commodity
        final_total_production = total_production_process

        price_commodity = (adjust_rate * price_commodity_process[cc] + (1-adjust_rate) * price_commodity[cc] for cc in Com)
        total_production = (adjust_rate * total_production_process[ind] + (1-adjust_rate) * total_production[ind] for ind in Ind)

        print("Model solved, price = ", price_commodity_array)
        return final_price_commodity, utility_cons, income, final_demand, final_total_production, intermediate_matrix, price_util, marginal_cost, GDP1, GDP2, GDP3

if __name__ == '__main__':
    price_commodity, utility_cons, income, final_demand, total_production, intermediate_matrix, price_util, marginal_cost, GDP1, GDP2, GDP3 = execute()
    print(price_commodity)
    print(total_production)
    print([GDP1, GDP2, GDP3])

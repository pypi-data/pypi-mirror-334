import Code.Calibration as Calibration
import Code.Consumer as Cons
import Code.Producer as Prod
import Code.MacroEconomy as Macro

def cge_system(price_commodity_array, args):
    (vars, params, Ind, Com, Fac, Con, factor, total_production) = args
    price_commodity = dict(zip(Com, price_commodity_array))
    price_ind = Prod.price_production(params.share_production_to_com, price_commodity, Ind, Com)
    marginal_cost = Prod.marginal_prod_cost(params.scale_prod_ces, params.share_param_inter_prod, params.elas_subs_prod, price_commodity, params.share_param_factor_prod, params.price_factor, Ind, Com)
    price_commodity = Prod.price_commodity(marginal_cost, params.share_production_to_com, Ind, Com)
    factor = Prod.factor_demand(vars.total_production, params.scale_prod_ces, params.share_param_factor_prod, marginal_cost, params.price_factor, params.elas_subs_prod, Ind, Com)
    factor_endow = Cons.factor_endowment(factor, Ind)
    income = Cons.labour_income(params.price_factor, factor, Ind)
    price_util = Cons.price_utility(params.scale_utility, params.share_param_utility, params.elas_subs_utility, params.price_commodity, Com)
    intermediate_matrix = Prod.intermediate_demand(vars.total_production, params.scale_prod_ces, params.share_param_inter_prod, marginal_cost, price_commodity, params.elas_subs_prod, Ind, Com)
    final_demand = Cons.final_consumption(params.share_param_utility, price_commodity,
                                          params.elas_subs_utility, price_util, params.scale_utility, income, Com)

    error_factor = Macro.factor_clearing(factor_endow, factor, Ind)
    error_com = Macro.commodity_clearing(params.share_production_to_com, vars.total_production, intermediate_matrix, final_demand, Com, Ind)

    error_commodity = [error_com[cc] for cc in Com]
    return error_commodity


def agg_value_balance(share_production_to_com, price_commodity, total_production, intermediate_matrix, final_demand, Ind, Com):
    agg_value_error = (sum(share_production_to_com[ind, cc] * price_commodity[cc] * total_production[ind] for ind in Ind for cc in Com)
                        - sum(intermediate_matrix[cc, ind] * price_commodity[cc] for ind in Ind for cc in Com)
                        - sum(final_demand[cc] * price_commodity[cc] for cc in Com))
    return agg_value_error
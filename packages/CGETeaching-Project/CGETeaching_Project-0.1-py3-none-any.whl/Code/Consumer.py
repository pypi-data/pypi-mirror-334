def consumer_utility(scale_utility, share_param_utility, final_demand, elas_subs_utility, Com):
    utility_cons = scale_utility * sum(share_param_utility[cc] * (final_demand[cc]**(1-1/elas_subs_utility))
                                              for cc in Com)**(elas_subs_utility/(elas_subs_utility-1))
    return utility_cons

def price_utility(scale_utility, share_param_utility, elas_subs_utility, price_commodity, Com):
    price_util = (1/scale_utility) *sum(share_param_utility[cc]**elas_subs_utility * price_commodity[cc]**(1-elas_subs_utility) for cc in Com)**(1/(1-elas_subs_utility))
    return price_util

def final_consumption(share_param_utility, price_commodity, elas_subs_utility, price_utility, scale_utility, income, Com):
    final_demand = {}
    for cc in Com:
        final_demand[cc] = (share_param_utility[cc]/price_commodity[cc]) ** elas_subs_utility * price_utility**(elas_subs_utility-1)*scale_utility**(elas_subs_utility-1) * income
    return final_demand

def agg_final_demand(final_demand, Com):
    total_final_demand = sum(final_demand[cc] for cc in Com)
    return total_final_demand

def labour_income(price_factor, factor, Ind):
    factor_income = sum(price_factor[ind]*factor[ind] for ind in Ind)
    return factor_income

def factor_endowment(factor, Ind):
    factor_endow = sum(factor[ind] for ind in Ind)
    return factor_endow
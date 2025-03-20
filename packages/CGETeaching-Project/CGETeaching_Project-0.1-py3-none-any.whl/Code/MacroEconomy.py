def gdp_use(share_production_to_com, price_commodity, total_production, intermediate_matrix, Ind, Com):
    gdp1 = sum(share_production_to_com[ind, cc] * price_commodity[cc] * total_production[ind] for ind in Ind for cc in Com) - sum(
                intermediate_matrix[cc, ind] * price_commodity[cc] for ind in Ind for cc in Com)
    return gdp1

def gdp_value_added(price_factor, factor, Ind):
    value_added = sum(price_factor[ind]*factor[ind] for ind in Ind)
    return value_added

def gdp_consumption(price_commodity, final_demand, Com):
    gdp2 = sum(price_commodity[cc]*final_demand[cc] for cc in Com)
    return gdp2

def factor_clearing(factor_endow, factor, Ind):
    factor_clear = factor_endow - sum(factor[ind] for ind in Ind)
    return factor_clear

def commodity_clearing(share_production_to_com, total_production, intermediate_matrix, final_demand, Com, Ind):
    error_commodity = {}
    for cc in Com:
        error_commodity[cc] = sum(share_production_to_com[ind, cc] * total_production[ind] for ind in Ind) - sum(intermediate_matrix[cc, ind] for ind in Ind) - final_demand[cc]
    return error_commodity
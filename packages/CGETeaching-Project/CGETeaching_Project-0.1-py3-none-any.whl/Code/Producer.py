def price_commodity(marginal_cost, share_production_to_com, Ind, Com):
    price_commodity = {}
    for cc in Com:
        if cc == 'Com1':
            price_commodity[cc] = 1.0
        else:
            price_commodity[cc] = sum(marginal_cost[ind] * share_production_to_com[ind, cc] for ind in Ind)
    return price_commodity

def intermediate_demand(total_production, scale_prod_ces, share_param_inter_prod, marginal_cost, price_commodity, elas_subs_prod, Ind, Com):
    intermediate_matrix = {}
    for ind in Ind:
        for cc in Com:
            intermediate_matrix[cc, ind] = total_production[ind] / scale_prod_ces[ind] * (share_param_inter_prod[cc, ind] * scale_prod_ces[ind] *
                                                                                          marginal_cost[ind] / price_commodity[cc])**elas_subs_prod
    return intermediate_matrix

def factor_demand(total_production, scale_prod_ces, share_param_factor_prod, marginal_cost, price_factor, elas_subs_prod, Ind, Com):
    factor = {}
    for ind in Ind:
        factor[ind] = total_production[ind] / scale_prod_ces[ind] * (share_param_factor_prod[ind] *
                                                                     scale_prod_ces[ind] * marginal_cost[ind] / price_factor[ind])**elas_subs_prod
    return factor

def price_production(share_com_ind, price_commodity, Ind, Com):
    price_ind = {}
    for ind in Ind:
        price_ind[ind] = sum(price_commodity[cc]*share_com_ind[ind, cc] for cc in Com)
    return price_ind

def marginal_prod_cost(scale_prod_ces, share_param_inter_prod, elas_subs_prod, price_commodity, share_param_factor_prod, price_factor, Ind, Com):
    marginal_cost = {}
    for ind in Ind:
        marginal_cost[ind] = 1/scale_prod_ces[ind] * (sum(share_param_inter_prod[cc, ind]**elas_subs_prod * price_commodity[cc]**(1-elas_subs_prod) for cc in Com)
        + share_param_factor_prod[ind]**elas_subs_prod * price_factor[ind] ** (1-elas_subs_prod))**(1/(1-elas_subs_prod))
    return marginal_cost

def total_production(scale_prod_ces, share_param_inter_prod, intermediate_matrix, share_param_factor_prod, factor, elasticity_subs_prod, Ind, Com):
    total_production = {}
    for ind in Ind:
        total_production[ind] = scale_prod_ces[ind] * (sum(share_param_inter_prod[cc, ind] * intermediate_matrix[cc, ind] ** (1-1/elasticity_subs_prod) for cc in Com) +
                                                       share_param_factor_prod[ind] * factor[ind] ** (1-1/elasticity_subs_prod))**(elasticity_subs_prod/(elasticity_subs_prod-1))
    return total_production

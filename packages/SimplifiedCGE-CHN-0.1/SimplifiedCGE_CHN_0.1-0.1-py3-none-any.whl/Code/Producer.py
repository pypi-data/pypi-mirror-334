def price_commodity(total_production, share_production_to_com, intermediate_matrix, final_demand, invest_goods, Ind, Com):
    price_commodity = {}
    for cc in Com:
        if cc == 'Com1':
            price_commodity[cc] = 1.0
        else:
            price_commodity[cc] = sum(share_production_to_com[ind,cc] * total_production[ind] for ind in Ind) / (sum(intermediate_matrix[cc, ind] for ind in Ind) + final_demand[cc] + invest_goods[cc])
    return price_commodity

def intermediate_demand(total_production, scale_prod_ces, share_param_inter_prod, marginal_cost, price_commodity, elas_subs_prod, Ind, Com):
    intermediate_matrix = {}
    for ind in Ind:
        for cc in Com:
            intermediate_matrix[cc, ind] = total_production[ind] / scale_prod_ces[ind] * (share_param_inter_prod[cc, ind] * scale_prod_ces[ind] *
                                                                                          marginal_cost[ind] / price_commodity[cc])**elas_subs_prod[ind]
    return intermediate_matrix

def labour_demand(total_production, scale_prod_ces, share_param_labour_prod, marginal_cost, price_labour, elas_subs_prod, Ind, Com):
    labour_input = {}
    for ind in Ind:
        labour_input[ind] = total_production[ind] / scale_prod_ces[ind] * (share_param_labour_prod[ind] *
                                                                     scale_prod_ces[ind] * marginal_cost[ind] / price_labour[ind])**elas_subs_prod[ind]
    return labour_input

def price_labour(labour_input, total_labour, Ind):
    wage_labour = {}
    for ind in Ind:
        wage_labour[ind] = total_labour / sum(labour_input[ind] for ind in Ind)
    return wage_labour
def capital_demand(total_production, scale_prod_ces, share_param_capital_prod, marginal_cost, price_capital, elas_subs_prod, Ind, Com):
    capital_input = {}
    for ind in Ind:
        capital_input[ind] = total_production[ind] / scale_prod_ces[ind] * (share_param_capital_prod[ind] *
                                                                     scale_prod_ces[ind] * marginal_cost[ind] / price_capital[ind])**elas_subs_prod[ind]
    return capital_input

def price_capital(capital_input, total_capital,Ind):
    rent_capital = {}
    for ind in Ind:
        rent_capital[ind] = total_capital / sum(capital_input[ind] for ind in Ind)
    return rent_capital

def price_production(marginal_cost, Ind):
    price_ind = {}
    for ind in Ind:
        price_ind[ind] = marginal_cost[ind]
    return price_ind

def marginal_prod_cost(scale_prod_ces, share_param_inter_prod, elas_subs_prod, price_commodity, share_param_labour_prod, share_param_capital_prod, price_labour, price_capital,Ind, Com):
    marginal_cost = {}
    for ind in Ind:
        marginal_cost[ind] = 1/scale_prod_ces[ind] * (sum(share_param_inter_prod[cc, ind]**elas_subs_prod[ind] * price_commodity[cc]**(1-elas_subs_prod[ind]) for cc in Com)
                            + share_param_labour_prod[ind]**elas_subs_prod[ind] * price_labour[ind] ** (1-elas_subs_prod[ind])
                             + share_param_capital_prod[ind]**elas_subs_prod[ind] * price_capital[ind] ** (1-elas_subs_prod[ind]))**(1/(1-elas_subs_prod[ind]))
    return marginal_cost

def total_production(scale_prod_ces, share_param_inter_prod, intermediate_matrix, share_param_labour_prod, share_param_capital_prod,labour_input, capital_input,elasticity_subs_prod, Ind, Com):
    total_production = {}
    for ind in Ind:
        total_production[ind] = scale_prod_ces[ind] * (sum(share_param_inter_prod[cc, ind] * intermediate_matrix[cc, ind] ** (1-1/elasticity_subs_prod[ind]) for cc in Com) +
                                                       share_param_labour_prod[ind] * labour_input[ind] ** (1-1/elasticity_subs_prod[ind]) +
                                                       share_param_capital_prod[ind] * capital_input[ind] ** (1-1/elasticity_subs_prod[ind]))**(elasticity_subs_prod[ind]/(elasticity_subs_prod[ind]-1))
    return total_production

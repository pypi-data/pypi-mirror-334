import numpy as np
import Calibration as Calibration
import Consumer as Cons
import Producer as Prod
import MacroEconomy as Macro

def cge_system(price_commodity_array, args):
    #(vars, params, Ind, Com, Fac, Con, factor, total_production) = args
    (vars, params, Ind, Com, Fac, Con, price_commodity_array, total_production, labour_input, capital_input, wage_labour, rent_capital) = args
    price_commodity = dict(zip(Com, price_commodity_array))

    price_utility = Cons.price_utility(params.scale_utility, params.share_param_utility, params.elas_subs_utility, price_commodity, Com)
    income = Cons.total_income(wage_labour, labour_input, rent_capital, capital_input, Ind)
    final_demand = Cons.final_consumption(params.share_param_utility, price_commodity, params.elas_subs_utility, price_utility, params.scale_utility, params.saving_rate, income, Com)
    utility_cons = Cons.consumer_utility(params.scale_utility, params.share_param_utility, final_demand, params.elas_subs_utility, Com)
    total_savings = Cons.total_saving(params.saving_rate, income)
    total_invest = Cons.total_investment(total_savings)
    invest_goods = Cons.investment_goods(params.share_param_invest, total_invest, Com)

    marginal_cost = Prod.marginal_prod_cost(params.scale_prod_ces, params.share_param_inter_prod, params.elas_subs_prod, price_commodity, params.share_param_labour_prod, params.share_param_capital_prod, wage_labour, rent_capital, Ind, Com)
    intermediate_matrix = Prod.intermediate_demand(total_production, params.scale_prod_ces, params.share_param_inter_prod, marginal_cost, price_commodity, params.elas_subs_prod, Ind, Com)
    labour_input = Prod.labour_demand(total_production, params.scale_prod_ces, params.share_param_labour_prod, marginal_cost, wage_labour, params.elas_subs_prod, Ind, Com)
    capital_input = Prod.capital_demand(total_production, params.scale_prod_ces, params.share_param_capital_prod, marginal_cost, rent_capital, params.elas_subs_prod, Ind, Com)

    error_labour = Macro.labour_clearing(labour_input, vars.total_labour, Ind)
    error_capital = Macro.capital_clearing(capital_input, vars.total_capital, Ind)
    error_com = Macro.commodity_clearing(params.share_production_to_com, total_production, price_commodity, intermediate_matrix, final_demand, invest_goods, Com, Ind)
    error_commodity = [error_com[cc] for cc in Com]
    error_list = np.append(error_commodity, [error_labour, error_capital])
    return error_list
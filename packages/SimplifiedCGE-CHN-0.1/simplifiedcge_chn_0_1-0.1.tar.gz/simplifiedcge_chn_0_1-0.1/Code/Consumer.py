def consumer_utility(scale_utility, share_param_utility, final_demand, elas_subs_utility, Com):
    utility_cons = scale_utility * sum(share_param_utility[cc] * (final_demand[cc]**(1-1/elas_subs_utility))
                                              for cc in Com)**(elas_subs_utility/(elas_subs_utility-1))
    return utility_cons

def price_utility(scale_utility, share_param_utility, elas_subs_utility, price_commodity, Com):
    price_util = (1/scale_utility) *sum(share_param_utility[cc]**elas_subs_utility * price_commodity[cc]**(1-elas_subs_utility) for cc in Com)**(1/(1-elas_subs_utility))
    return price_util

def final_consumption(share_param_utility, price_commodity, elas_subs_utility, price_utility, scale_utility, saving_rate, income, Com):
    final_demand = {}
    for cc in Com:
        final_demand[cc] = (share_param_utility[cc] * scale_utility * price_utility / price_commodity[cc]) ** elas_subs_utility * (1-saving_rate) * income / (price_commodity[cc] * scale_utility)
    return final_demand

def agg_final_demand(final_demand, Com):
    total_final_demand = sum(final_demand[cc] for cc in Com)
    return total_final_demand

def total_income(price_labour, labour_input, price_capital, capital_input,Ind):
    income = sum(price_labour[ind]*labour_input[ind] + price_capital[ind]*capital_input[ind] for ind in Ind)
    return income

def total_saving(saving_rate, income):
    total_savings = saving_rate * income
    return total_savings

def total_investment(total_savings):
    total_invest = total_savings
    return total_invest

def investment_goods(share_param_invest, total_investment, Com):
    invest_goods = {}
    for cc in Com:
        invest_goods[cc] = share_param_invest[cc] * total_investment
    return invest_goods
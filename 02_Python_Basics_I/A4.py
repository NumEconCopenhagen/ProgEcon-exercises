basket_items = ["Food", "Energy", "Transport"]
last_year_costs = [500.0, 300.0, 200.0]

this_year_costs = last_year_costs.copy()
this_year_costs[1] = 330.0

last_year_total = sum(last_year_costs)
this_year_total = sum(this_year_costs)
inflation_rate = (this_year_total - last_year_total) / last_year_total * 100

if inflation_rate > 2:
    inflation_label = "Inflation above 2 percent"
elif inflation_rate > 0:
    inflation_label = "Positive inflation"
else:
    inflation_label = "No inflation"

print("Last year's costs:", last_year_costs)
print("This year's costs:", this_year_costs)
print("Last year's total:", last_year_total)
print("This year's total:", this_year_total)
print("Inflation rate:", inflation_rate, "percent")
print("Classification:", inflation_label)

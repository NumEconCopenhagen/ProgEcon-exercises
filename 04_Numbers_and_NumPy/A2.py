print("Categories:", consumption_categories.shape, consumption_categories.dtype)
print("Prices:", prices.shape, prices.dtype)
print("Quantities:", quantities.shape, quantities.dtype)

spending_by_category = prices * quantities
total_spending = np.sum(spending_by_category)
budget_shares = spending_by_category / total_spending * 100
above_eight_percent = budget_shares > 8

print("Spending by category:", spending_by_category)
print("Total spending:", total_spending)
print("Budget shares:", budget_shares)
print("Selected categories:", consumption_categories[above_eight_percent])
print("Selected shares:", budget_shares[above_eight_percent])

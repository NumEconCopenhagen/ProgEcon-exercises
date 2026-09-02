print("Number of categories:", len(spending_categories))

higher_energy_spending = baseline_spending.copy()
higher_energy_spending[2] *= 1.25
budget_scenario = {
    "categories": spending_categories,
    "baseline": baseline_spending,
    "higher_energy": higher_energy_spending,
}

print("Affected category:", budget_scenario["categories"][2])
print("Baseline energy spending:", budget_scenario["baseline"][2])
print("Higher energy spending:", budget_scenario["higher_energy"][2])

baseline_total = sum(budget_scenario["baseline"])
higher_energy_total = sum(budget_scenario["higher_energy"])
print("Baseline total:", baseline_total)
print("Higher-energy total:", higher_energy_total)
print("Extra monthly spending:", higher_energy_total - baseline_total)
print("Unchanged baseline:", baseline_spending)

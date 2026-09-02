import numpy as np

household_names = np.array(["Household A", "Household B", "Household C"])
income_by_year = np.array([
    [18000.0, 20000.0],
    [25000.0, 26000.0],
    [14000.0, 15000.0],
])

baseline_income = income_by_year[:, 0]
policy_income = baseline_income.copy()
policy_income[policy_income < 20000.0] += 2000.0

still_below_threshold = (policy_income > 0) & (policy_income < 20000.0)
average_income_by_year = np.mean(income_by_year, axis=0)

print("Baseline income:", baseline_income)
print("Income after support:", policy_income)
print("Still below the threshold:", household_names[still_below_threshold])
print("Average income by year:", average_income_by_year)

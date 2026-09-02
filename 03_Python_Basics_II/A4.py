def calculate_debt_path(initial_debt, annual_budget_deficits):
    debt = initial_debt
    debt_path = [initial_debt]

    for deficit in annual_budget_deficits:
        debt += deficit
        debt_path.append(debt)

    return debt_path


initial_debt = 100
annual_budget_deficits = [10, 15, -5]
print("Government debt path:", calculate_debt_path(initial_debt, annual_budget_deficits))

def budget_balances(tax_revenue, government_spending, interest_payments=0.0):
    primary_balance = tax_revenue - government_spending
    overall_balance = primary_balance - interest_payments
    return primary_balance, overall_balance


primary, overall = budget_balances(tax_revenue, government_spending)
print("Without interest payments:", primary, overall)

primary, overall = budget_balances(
    tax_revenue, government_spending, interest_payments=80.0
)
print("With interest payments:", primary, overall)

interest_payments = 500.0
primary, overall = budget_balances(tax_revenue, government_spending)
print("After changing the global variable:", primary, overall)

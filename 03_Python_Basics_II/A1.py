trade_balances = []
for export, imported in zip(exports, imports):
    trade_balances.append(export - imported)

surplus_count = 0
for position, country in enumerate(countries):
    balance = trade_balances[position]
    print(country, position, balance)
    if balance > 0:
        surplus_count += 1

print("Trade balances:", trade_balances)
print("Total trade balance:", sum(trade_balances))
print("Countries with a surplus:", surplus_count)

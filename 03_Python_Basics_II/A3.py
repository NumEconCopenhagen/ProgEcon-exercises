class Economy:

    def __init__(self, name, gdp, population, government_debt):
        self.name = name
        self.gdp = gdp
        self.population = population
        self.government_debt = government_debt

    def gdp_per_capita(self):
        return self.gdp / self.population

    def debt_to_gdp(self):
        return self.government_debt / self.gdp * 100


denmark = Economy(economy_name, gdp, population, government_debt)
print("Name:", denmark.name)
print("GDP per capita:", denmark.gdp_per_capita())
print("Debt-to-GDP ratio:", denmark.debt_to_gdp())

denmark.gdp = 3_150_000_000_000
print("GDP per capita after GDP rises:", denmark.gdp_per_capita())
print("Debt-to-GDP ratio after GDP rises:", denmark.debt_to_gdp())

print("Original wage:", weekly_wage_last_year_text)
print("Original type:", type(weekly_wage_last_year_text))

weekly_wage_last_year = float(weekly_wage_last_year_text)
weekly_wage_growth = (weekly_wage_this_year / weekly_wage_last_year - 1) * 100
inflation_rate = (price_index_this_year / price_index_last_year - 1) * 100
real_weekly_wage_last_year = weekly_wage_last_year / price_index_last_year * 100
real_weekly_wage_this_year = weekly_wage_this_year / price_index_this_year * 100
real_weekly_wage_growth = (real_weekly_wage_this_year / real_weekly_wage_last_year - 1) * 100
purchasing_power_increased = real_weekly_wage_this_year > real_weekly_wage_last_year

print("Nominal wage growth:", weekly_wage_growth, "percent")
print("Inflation rate:", inflation_rate, "percent")
print("Real wage last year:", real_weekly_wage_last_year)
print("Real wage this year:", real_weekly_wage_this_year)
print("Real wage growth:", real_weekly_wage_growth, "percent")
print("Purchasing power increased:", purchasing_power_increased)

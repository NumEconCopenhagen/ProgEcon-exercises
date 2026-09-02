n_countries, n_years = nominal_wage_growth.shape
print("Shape:", nominal_wage_growth.shape)
print("Countries and years:", n_countries, n_years)
print("Sweden:", nominal_wage_growth[1, :])
print("2024:", nominal_wage_growth[:, 1])

real_wage_growth = nominal_wage_growth - inflation_by_year
average_by_country = np.mean(real_wage_growth, axis=1)
average_by_year = np.mean(real_wage_growth, axis=0)
print("Real wage growth:", real_wage_growth)
print("Average by country:", average_by_country)
print("Average by year:", average_by_year)

above_1_5_percent = average_by_country > 1.5
print("Countries above 1.5 percent:", country_names[above_1_5_percent])

negative_positions = np.where(real_wage_growth < 0)
print("Negative positions:", negative_positions)
print("Negative country and year:", country_names[negative_positions[0]], growth_years[negative_positions[1]])

real_wage_one = nominal_wage / cpi * 100
real_wage_two = nominal_wage * (100 / cpi)
real_wage_three = 100 * nominal_wage / cpi

equal_one_two = real_wage_one == real_wage_two
equal_one_three = real_wage_one == real_wage_three
print("Real wages:", real_wage_one, real_wage_two, real_wage_three)
print("First versus second:", equal_one_two, "disagreements:", np.sum(~equal_one_two))
print("Years and positions:", wage_years[~equal_one_two], np.where(~equal_one_two))
print("First versus third:", equal_one_three, "disagreements:", np.sum(~equal_one_three))
print("Years and positions:", wage_years[~equal_one_three], np.where(~equal_one_three))

print("isclose, first versus second:", np.isclose(real_wage_one, real_wage_two))
print("isclose, first versus third:", np.isclose(real_wage_one, real_wage_three))
print("allclose:", np.allclose(real_wage_one, real_wage_two), np.allclose(real_wage_one, real_wage_three))

difference_one_two = real_wage_one - real_wage_two
difference_one_three = real_wage_one - real_wage_three
print("Differences:", difference_one_two, difference_one_three)
print("Relative differences:", difference_one_two / real_wage_one, difference_one_three / real_wage_one)

rounded_one = np.round(real_wage_one, 2)
rounded_two = np.round(real_wage_two, 2)
rounded_three = np.round(real_wage_three, 2)
print("Rounded real wages:", rounded_one, rounded_two, rounded_three)
print("Rounded comparisons:", rounded_one == rounded_two, rounded_one == rounded_three)

nominal_wage_growth = (nominal_wage[-1] / nominal_wage[0] - 1) * 100
real_wage_growth = (real_wage_one[-1] / real_wage_one[0] - 1) * 100
print("Nominal wage growth:", nominal_wage_growth, "percent")
print("Real wage growth:", real_wage_growth, "percent")

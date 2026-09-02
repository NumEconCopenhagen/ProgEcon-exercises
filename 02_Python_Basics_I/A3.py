print(quarter_labels[-2], quarterly_gdp_growth[-2])
print(quarter_labels[-1], quarterly_gdp_growth[-1])

technical_recession = quarterly_gdp_growth[-2] < 0 and quarterly_gdp_growth[-1] < 0
if technical_recession:
    print("Two consecutive quarters of falling GDP")
elif quarterly_gdp_growth[-1] < 0:
    print("GDP fell in the latest quarter")
else:
    print("GDP did not fall in the latest quarter")

quarterly_gdp_growth[-2] = 0.1
technical_recession = quarterly_gdp_growth[-2] < 0 and quarterly_gdp_growth[-1] < 0
if technical_recession:
    print("Two consecutive quarters of falling GDP")
elif quarterly_gdp_growth[-1] < 0:
    print("GDP fell in the latest quarter")
else:
    print("GDP did not fall in the latest quarter")

quarterly_gdp_growth[-1] = 0.2
technical_recession = quarterly_gdp_growth[-2] < 0 and quarterly_gdp_growth[-1] < 0
if technical_recession:
    print("Two consecutive quarters of falling GDP")
elif quarterly_gdp_growth[-1] < 0:
    print("GDP fell in the latest quarter")
else:
    print("GDP did not fall in the latest quarter")

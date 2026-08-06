# a. load
nah1_api = DstApi('NAH1')
params = nah1_api._define_base_params(language='en')
nah1_true = nah1_api.get_data(params=params)

# b. rename columns
nah1_true = nah1_true.rename(columns=columns_dict)

# c. replace data
for key,value in var_dict.items():
   nah1_true.variable = nah1_true.variable.replace(key,value)

for key,value in unit_dict.items():
   nah1_true.unit = nah1_true.unit.replace(key,value)

# d. keep if in var_dict
I = nah1_true.variable.isin(var_dict.values())
nah1_true = nah1_true[I].copy() # .copy() -> avoid working on a view

# e. convert values to numeric
nah1_true.value = nah1_true.value.astype('float')

# f. add the two private consumption categories (households and NPISH) together
nah1_true = nah1_true.groupby(['variable','unit','year'],as_index=False)['value'].sum()

# g. GDP from NAN1
params = {
    'table': 'NAN1',
    'format': 'BULK',
    'lang': 'en',
    'variables': [
        {'code': 'TRANSAKT', 'values': ['B1GQK']},
        {'code': 'PRISENHED', 'values': ['V_M','LAN_M']},
        {'code': 'Tid', 'values': ['*']},
        ]
    }
gdp_true = DstApi('NAN1').get_data(params=params)
gdp_true = gdp_true.rename(columns=columns_dict)

gdp_true['variable'] = 'Y'

# the unit labels have the unit appended -> strip it, then use unit_dict
gdp_true['unit'] = gdp_true['unit'].str.replace(', (bill. DKK.)','',regex=False)
for key,value in unit_dict.items():
    gdp_true.unit = gdp_true.unit.replace(key,value)

# NAN1 is in bill. DKK, NAH1 in mio. DKK
gdp_true['value'] = gdp_true['value'].astype('float')*1000

nah1_true = pd.concat([nah1_true,gdp_true[['variable','unit','year','value']]],ignore_index=True)

# h. check the national account identity
check = nah1_true.pivot_table(index=['unit','year'],columns='variable',values='value')
check['C+G+I+X-M'] = check['C']+check['G']+check['I']+check['X']-check['M']
check['diff'] = check['Y']-check['C+G+I+X-M']

print('largest absolute deviation from the identity (mio. DKK):')
display(check.groupby('unit')['diff'].apply(lambda x: x.abs().max()))

# In *current prices* the identity holds exactly (the deviation of ~50 mio. DKK out of a
# GDP of ~3,000,000 mio. DKK is rounding in the published figures).
#
# In *2020-prices* it does NOT hold - the deviation is more than 2 pct. of GDP. The reason
# is that the real figures are CHAINED values: each year is linked to the previous one
# using that year's prices. Chained values are therefore not additive, and the components
# do not sum to the total in any year other than the base year (2020).

# i. summary statistics
display(nah1_true.groupby(['variable','unit']).describe())

# j. sort by year
nah1_true = nah1_true.sort_values(by='year')
nah1_true

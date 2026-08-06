ages = [f'{age} years' for age in range(18,65+1)]

assert set(ages) <= set(BEFOLK1.ALDER.unique()), 'some age labels did not match'

working_pop = BEFOLK1[BEFOLK1.ALDER.isin(ages)].groupby('year')[['population']].sum()
working_pop = working_pop.rename(columns={'population':'working_population'})

merged_true = pd.merge(nah1_true, working_pop, how='left', on=['year'], validate='m:1')
merged_true = pd.merge(merged_true, pop, how='left', on=['year'], validate='m:1')

fig = plt.figure(figsize=(6,4))
ax = fig.add_subplot(1,1,1)

# the values are in mio. DKK -> multiply by 1e6 to get DKK per person
merged_true['value_pop'] = merged_true.value/merged_true.population*1e6
merged_true['value_working_pop'] = merged_true.value/merged_true.working_population*1e6

I = merged_true.unit == 'real'
I &= merged_true.variable == 'Y'

df = merged_true[I].set_index('year')
ax.plot(df.value_pop, label='per capita')
ax.plot(df.value_working_pop, label='per working-age (18-65)')

ax.set_xlabel('year')
ax.set_ylabel('DKK per person, 2020-prices')
ax.set_title('Real GDP per person')
ax.legend()

merged_true = pd.merge(nah1_true,pop,how='left',on=['year'],validate='m:1')
merged_true.tail(10)

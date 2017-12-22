import pandas as pd

columns = ['NPI', 'Name', 'Score']
entries = []

df_names = pd.read_csv('Healthgrade List.csv')

df_prov = pd.read_csv('prov_NE.csv')

hN = df_names.Name.tolist()
pN = df_prov.Full_Name.tolist()

match = list(set(hN).intersection(pN))
npi = []
score = []

for x in match:
	npi.append(df_prov.loc[df_prov['Full_Name'] == x, 'npi'].iloc[0])
	score.append(df_names.loc[df_names['Name'] == x, 'Rating'].iloc[0])

print(match[5], npi[5], score[5])
print(match[50], npi[50], score[50])

for x in range(len(match)):
	entries.append([npi[x], match[x], score[x]])

df = pd.DataFrame(entries, columns = columns)
df = df.sort_values(by = 'Score', ascending = True)
df.to_csv('MatchNames.csv', index=False)

'''
matchNames = csv.writer(open("matchNames.csv",'w', newline = ''))
for item in match:
	matchNames.writerow([item])


END - CSV
NPI | Name | Score
XXXX,  A B,   5.0
'''


'''
df_prov['provNames'] = df_prov['nppes_provider_first_name'] + ' ' + df_prov['nppes_provider_last_org_name']
df_prov = df_prov['provNames']
#pN = df_prov.provNames.tolist()
#print(pN[0])

df = pd.concat([df_prov, df_names], ignore_index = True, axis = 1)
df.columns = ['pN', 'hN', 'c', 'd']
keepcol = ['pN', 'hN']
df = df[keepcol]

for x in range(len(df.hN)):
	for y in range(len(df.pN)):
		if df.at[x, 'hN'] == df.at[y, 'pN']: 
			print(df.iat[x, 'hN'])
'''


'''
df_prov.drop(df_prov.columns[[0]], axis = 1, inplace = True)
#print(df_prov.columns.values)
#print(df_names.columns.values)

#df = pd.merge(df_prov, df_names, left_index = True, right_index = True)

df = df_prov.merge(df_names, how = 'left', left_on = 'npi', right_on = 'Name')
#keepcol = ['nppes_provider_last_org_name','nppes_provider_first_name','Name']
#df = df[keepcol]
print(df.head(4))


print(df.columns.values)
print()
print(df.tail(3))
print()

df['provNames'] = df['nppes_provider_first_name'] + ' ' + df['nppes_provider_last_org_name']
df.drop(df.columns[[0, 1]], axis = 1, inplace = True)

print(df.columns.values)
#print(df.Name)
'''
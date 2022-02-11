# Write a separate python program that accepts few search words and uses the file produced by Task 1.
# The words given by users will be matched against any words in the Columns 1,2 and the most closely matched company's Standard Name will be produced as output.

# Assumptions
# 1. a user could enter single or multiple words
# 2. the output could be a list of companies incase the word matches equally with multiple companies
# 3. since the idea is to find the most closely matched company and not the max number of matches with a company summary,
#    we can assume n=1 in difflib.get_close_matches
# 4. set the cutoff in the above mentioned function to a value close to 1 to more strictly with the company information
import difflib
import pandas as pd
# pd.set_option('display.max_colwidth',100)
# pd.set_option('display.max_columns',6)
df_cmp = pd.read_csv('companies.csv')
# print(df_cmp)
search_words = input('Enter one or a few words separated by commas: ')
searchL = [x.strip().lower() for x in search_words.split(',')]
df_cmp['matchedL'] = df_cmp.apply(lambda x: [difflib.get_close_matches(searchL[i],(x['Standard Name'] + x['Summary']).lower().split(),n=1, cutoff=0.8) for i in range(len(searchL))], axis=1)
df_cmp['flattenList'] = df_cmp.apply(lambda x: [val for sublist in x.matchedL for val in sublist], axis=1)
df_cmp['flattenLength'] = df_cmp.apply(lambda x: len([val for sublist in x.matchedL for val in sublist]), axis=1)
# print(df_cmp)
# print(df_cmp['flattenLength'].max())
print('Company(ies) that most closely matched--', df_cmp[df_cmp['flattenLength']== df_cmp['flattenLength'].max()]['Standard Name'].tolist())

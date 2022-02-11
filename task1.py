
# Task 1. Write a python program that parses wiki-pedia web pages using standard open source WikiPedia API.
# The objective is to follow links of major Canadian companies recursively and produces the output in below CSV format.


import wikipedia
import pandas as pd
from bs4 import BeautifulSoup as bsp
import warnings
warnings.catch_warnings()
warnings.simplefilter("ignore")
pgName = wikipedia.page('List_of_companies_of_Canada', auto_suggest=False)
print('URL-', pgName.url)
print('Title-', pgName.title)

# print(pgName.links)
# pgName.links result in a list company names from 'Notable firms' section. However, it does return some random links like
# '2016 Canadian census' from other sections of the same page which do not represent any specific company and hence irrelevant.
# Therefore using html method below to then later find the table data by parsing it through BeautifulSoup module
# wikipedia api has a few limitations:
# limitation 1. the html() method cannot be used further within the scope of wikipedia API

cmpHtml = pgName.html()
cmptbody = bsp(cmpHtml,'html.parser').find_all('tbody')[1]
cmpList =[]
for tr in cmptbody.find_all('tr')[1:]:
    cmpList.append(tr.find_all('td')[0].text.strip())
# print(cmpList)
nameL = []
summaryL=[]
#limitation 2. there are certain companies names that are so common that wikipedia API throws DisambiguationError Exception
# As a workaround we could use the URL(href attribute in html element a of the tbody) but the API again has no methods to
# take the URL and search for respective page content. Therefore had to handle a few exceptions and bypass the data capture of
# such companies
for i, name in enumerate(cmpList):
    try:
        # if i == 15:
        #     break
        print(i, name)
        nameL.append(wikipedia.page(name, auto_suggest=False).title)
        summaryL.append(wikipedia.summary(name, auto_suggest=False))
    except wikipedia.exceptions.DisambiguationError as e:
        continue
    except wikipedia.exceptions.PageError as e:
        continue
df_cmp = pd.DataFrame({'Standard Name': nameL, 'Summary': summaryL})
df_cmp.to_csv('companies.csv')
# print(df_cmp)
# print('DONE')

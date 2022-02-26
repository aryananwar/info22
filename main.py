import requests as r
from bs4 import BeautifulSoup 

api = 'https://mdallsky.astro.umd.edu/masn01-archive/'
r.get(api).text
html = BeautifulSoup(r.get(api).text, 'html.parser')

table = html.find('table')
links = table.findAll('tr')

for i in links:
    print(i)







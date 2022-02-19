import csv
import requests
from bs4 import BeautifulSoup

#YEAR = '21'
YEAR = '22'

url = 'https://www.umpd.umd.edu/stats/arrest_report.cfm?year=20'+YEAR
response = requests.get(url, headers={'User-Agent': 'Rachel Logan'}) 
html = response.content 

soup = BeautifulSoup(html, features="html.parser")
#print(soup.prettify())

table = soup.find('table').find_all('tr')

row_list = []
cell_list = []

for row_index in range(0,len(table)):
	#print(table[row_index],'\n')
	if (not row_index): 
		header_row = [cell.text.strip() for cell in table[0].find_all('th')]
		header_row.append('DESCRIPTION')
		#print(header_row)
		row_list.append(header_row)
	elif (row_index % 2):
		cell_list = [cell.text.strip() for cell in table[row_index].find_all('td')]
	else:
		cell_list.append(table[row_index].find('td').text.strip())
		row_list.append(cell_list)
		cell_list = []

out_url = './data/scraped-umd-police-arrest-log-'+YEAR+'.csv'
outfile = open(out_url,"w",newline="")
writer = csv.writer(outfile)
writer.writerows(row_list)
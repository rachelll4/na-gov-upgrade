import csv
from csv import reader
import requests
from bs4 import BeautifulSoup
from datetime import date
from pathlib import Path
import pandas as pd

#Can loop through, append these to download larger sets



MONTH = str(date.today().month)
YEAR = str(date.today().year)

#for YEAR in range(2021,2023):
#    YEAR = str(YEAR)
#    for MONTH in range(1,13):
#        MONTH = str(MONTH)
        

url = 'https://www.umpd.umd.edu/stats/incident_logs.cfm?year=' + YEAR + '&month=' + MONTH
#url = 'https://www.umpd.umd.edu/stats/incident_logs.cfm?year=2022&month=2
response = requests.get(url, headers={'User-Agent': 'Rachel Logan'}) 
html = response.content 

soup = BeautifulSoup(html, features="html.parser")
#print(soup.prettify())
#print(soup.find('table').find_all('tr'))

table = soup.find('table').find_all('tr')

row_list = []
cell_list = []

for row_index in range(0,len(table)):
    #print(table[row_index],'\n')
    if (not row_index): 
        #there is the issue of removing <br> leaves no space-- 
        #could replace <br> with ' ' before pulling text, but not as clean
        header_row = [cell.text.strip() for cell in table[0].find_all('th')]
        header_row.append('LOCATION')
        #print(header_row)
        row_list.append(header_row)
    elif (row_index % 2):
        cell_list = [cell.text.strip() for cell in table[row_index].find_all('td')]
    else:
        cell_list.append(table[row_index].find('td').text.strip())
        row_list.append(cell_list)
        # for cell in cell_list: 
        # 	print(cell,'\n')
        # print('-----------')
        cell_list = []

        
path = Path('./data/all-police-activity.csv')

if not path.is_file():
    outfile = open(path,"w",newline="")
    writer = csv.writer(outfile)
    writer.writerows(row_list)

else:
    with open(path, 'r') as prev_data_stream:
        csv_reader = reader(prev_data_stream)
        prev_data = list(csv_reader)
    
    all_data = prev_data + row_list
    pd_all_data = pd.DataFrame(all_data).drop_duplicates(keep = 'first')
    pd_all_data.to_csv(path, index = False, index_label = False, header = False)
    

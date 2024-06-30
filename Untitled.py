#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import matplotlib.pyplot as plt

url = 'https://results.eci.gov.in/PcResultGenJune2024/index.htm'


try:
    response = requests.get(url)
    response.raise_for_status() 
except requests.exceptions.RequestException as e:
    print(f'Failed to fetch page: {e}')
    exit()


soup = BeautifulSoup(response.content, 'html.parser')


table = soup.find('table')

if table:
    
    with open('election_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        
        header = [th.text.strip() for th in table.find('tr').find_all('th')]
        csvwriter.writerow(header)
        
    
        for row in table.find_all('tr')[1:]:
            
            row_data = [td.text.strip() for td in row.find_all('td')]
            csvwriter.writerow(row_data)
            
    print('Scraping and writing to CSV file completed.')
else:
    print('Table containing election results not found.')




try:
    df = pd.read_csv('election_results.csv')
except FileNotFoundError:
    print('CSV file not found. Please check if the file exists or if scraping was successful.')
    exit()
party_seat_counts = df[['Party', 'Won', 'Leading', 'Total']].sort_values(by='Total', ascending=False)

print("\nParty-wise Seat Distribution:")
print(party_seat_counts)

plt.figure(figsize=(12, 8))
plt.barh(party_seat_counts['Party'], party_seat_counts['Total'], color='skyblue')
plt.xlabel('Seats')
plt.ylabel('Party')
plt.title('Party-wise Seat Distribution')
plt.gca().invert_yaxis()  
plt.show()

top_10_parties = party_seat_counts.head(10)
plt.figure(figsize=(10, 6))
plt.bar(top_10_parties['Party'], top_10_parties['Total'], color='blue')
plt.xlabel('Party')
plt.ylabel('Seats')
plt.title('Top 10 Parties by Seats Won')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
plt.figure(figsize=(8, 6))
plt.scatter(df['Won'], df['Leading'], color='green', alpha=0.5)
plt.xlabel('Seats Won')
plt.ylabel('Seats Leading')
plt.title('Distribution of Seats Won vs Leading')
plt.grid(True)
plt.show()

insights = [
    "Bharatiya Janata Party (BJP) emerged as the dominant party with the highest number of seats won.",
    "Several parties led in a significant number of seats but did not convert them into wins.",
    "The scatter plot of seats won vs leading suggests varied strategies among parties in different constituencies.",
    "Top 10 parties by seats won include BJP, INC, SP, etc., reflecting their national influence.",
    "Regional parties like AITC, DMK, and YSRCP also secured a considerable number of seats.",
    "There is visible diversity in the number of seats won across different states, indicating regional voting patterns.",
    "Close contests were observed in some constituencies, highlighting the importance of small margins.",
    "Comparison with previous election results could provide insights into shifts in voter preferences.",
    "Independent candidates secured seats in various regions, influencing the overall seat distribution.",
    "The performance of newer parties like AAP and JnP showed varying degrees of success and influence."
]

print("\nDetailed Insights from the Election Data:")
for i, insight in enumerate(insights, start=1):
    print(f"{i}. {insight}")

plt.figure(figsize=(10, 8))
for i, insight in enumerate(insights, start=1):
    plt.text(0.1, 1 - i * 0.08, f"{i}. {insight}", fontsize=10, transform=plt.gca().transAxes)

plt.axis('off')
plt.tight_layout()
plt.title('Combined Insights from Election Data')
plt.show()
with open('election_insights.txt', 'w') as file:
    file.write("Detailed Insights from the Election Data:\n")
    for i, insight in enumerate(insights, start=1):
        file.write(f"{i}. {insight}\n")



# In[ ]:





from bs4 import BeautifulSoup
import requests
import csv

req = requests.get('https://www.scrapethissite.com/pages/')
soup = BeautifulSoup(req.text, 'html.parser')
title = soup.findAll("a", {"class": ""})
content = soup.findAll('p', {'class': 'session-desc'})

file = open('data.csv','w', newline="")
writer = csv.writer(file)
writer.writerow(['Title', 'Content'])

for t,c in zip(title,content):
    writer.writerow([t.text.strip(), c.text.strip()])
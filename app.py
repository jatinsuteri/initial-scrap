from bs4 import BeautifulSoup
import requests
import csv

# Make the request to the correct URL
req = requests.get('https://m.manganelo.com/genre-all')
soup = BeautifulSoup(req.text, 'html.parser')

# Find all the manga titles based on the class in the <a> tag
titles = soup.findAll("a", {"class": "tooltip a-h text-nowrap hastool"})
print(titles)

# Write the titles to a CSV file
file = open('data.csv', 'w', newline="")
writer = csv.writer(file)
writer.writerow(['Titles'])

# Write each title into the CSV
for t in titles:
    writer.writerow([t.text.strip()])

file.close()


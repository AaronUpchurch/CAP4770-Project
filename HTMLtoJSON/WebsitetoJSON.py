from lxml import html
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

"""

Creating the dictionary of country names to country codes for file names

"""


url = 'https://en.wikipedia.org/wiki/List_of_FIPS_country_codes'
codes_website = requests.get(url)
doc = html.fromstring(codes_website.content)
soup = BeautifulSoup(codes_website.text, 'lxml')

table = soup.find_all('table')
df = pd.read_html(str(table))[0]


names = []
gec = []
for i in range(0,len(table)):
    df = pd.read_html(str(table))[i]
    if df.columns[0] != 'Code':
        break
    gec.append(df[df.columns[0]])
    names.append(df[df.columns[1]])
    
country = []
iso = []
for i in range(0,len(names)):
    for j in names[i]:
        country.append(j)
    for j in gec[i]:
        iso.append(j)

"""

Scraping the data from the webpages into json files

"""


urls = []
for i in country:
    # Manually fixing the country names to append to the URL
    name = i.lower()
    name = name.replace(",", "")
    name = name.replace("(", "")
    name = name.replace(")", "")
    name = name.replace(" ", "-")
    
    # Manually fixing the country names to the correct URL name
    if (name == "congo-brazzaville"):
        name = "congo-republic-of-the"
    elif (name == "congo-kinshasa"):
        name = "congo-democratic-republic-of-the"
    elif (name == "czech-republic"):
        name = "czechia"
    elif (name == "côte-d'ivoire"):
        name = "cote-divoire"
    elif (name == "curaçao"):
        name = "curacao"
    elif (name == "united-states-virgin-islands"):
        name = "virgin-islands"
    elif (name == "vatican-city"):
        name = "holy-see-vatican-city"
    urls.append('https://www.cia.gov/the-world-factbook/countries/' + name)

# Manually Appending the World
urls.append('https://www.cia.gov/the-world-factbook/countries/world/')


country_datas = []
for i in urls:
    page = requests.get(i)
    if(page.status_code == 404):
        continue
    
    soup = BeautifulSoup(page.text, 'lxml')

    classes = ["introduction", "geography", "people-and-society", "environment", "government", "economy", "energy", "communications", "transportation", "military-and-security", "terrorism", "transnational-issues"]
    sections = []
    for i in range(0,12):
        sections.append(soup.find_all(id=classes[i]))
        

    data = {}
    for section in sections:
        if(len(section) == 0):
            continue
        divs = section[0].find_all('div')
        data_section = {}
        for i in range(0,len(divs)):
            header = divs[i].find('h3')
            paragraphs = divs[i].find_all('p')
            if (header != None):
                temp_dict = {}
                for p in paragraphs:
                    subsections = p.find_all('strong')
                    if(len(subsections) != 0):
                        text = {}
                        for i in range(0, len(subsections)):
                            temp_text_dict = {}
                            temp_text_dict["text"] = str(subsections[i].next_sibling)
                            #print(type(subsections[i].next_sibling))
                            temp_dict[subsections[i].get_text()] = temp_text_dict
                    else:
                        text = ""
                        text += p.get_text()
                        temp_dict["text"] = text
                data_section[header.get_text()] = temp_dict
        data[section[0].find_all('h2')[0].get_text()] = data_section
    
    country_datas.append(data)
 
"""

Converting the json files into output files

"""

import os
directory = os.getcwd()

for country in country_datas:
    try:
        world = country['Geography']['Map references']['text']
        if (world == "Physical Map of the World"):
            s = "world"
            region = "world"
        else:
            s = country['Government']['Country name']['conventional short form: ']['text']
            s = s.replace(" ", "")
            s = s.lower()
            region = country['Geography']['Map references']['text']
            region = region.replace(" ", "-")
            region = region.lower()
               
        file_path = 'C:/Users/TheNicMachine/Desktop/Country Datas/countries2022/' + s + '.json' 
        json_data = json.dumps(country, indent=2)

        if(s == "none"):
            continue
    
        with open(file_path, "x") as outfile:
            outfile.write(json_data)
    except:
        continue




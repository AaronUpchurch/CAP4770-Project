import json
from bs4 import BeautifulSoup
import os

directory = os.fsencode("C:/Users/TheNicMachine/Desktop/Country Datas/factbook-2017/geos")

urls = []
for filename in os.listdir(directory):
    f = os.fsdecode(filename)
    if f.endswith(".html") and "countrytemplate" not in f and "print_" not in f:
        urls.append("C:/Users/TheNicMachine/Desktop/Country Datas/factbook-2017/geos/" + f)
        

for url in urls:
    with open(url, 'rb') as html_data:
        soup = BeautifulSoup(html_data, 'lxml')
        
        
    code = ".." + url[58:]
    print(code)
    # URLs of Pages that can't be parsed
    # I have no idea why some of them can't be parsed
    broken_pages = ["../geos/bu.html", "../geos/lg.html", "../geos/xx.html"]
    if code in broken_pages:
        continue

    # World Page has unique code to find country name
    country_name = soup.find_all('span', {"class": "region_name1"})[0].get_text()

    country_name = country_name.upper()

    table = soup.find_all('ul', {"class": "expandcollapse"})[0]
    rows = table.find_all('li')
    
    headers = []
    info = []
    for row in rows:
        text = row.get_text()
        if country_name in text:
            header = text.split(':')[0]
            headers.append(header)
        else:
            info.append(row.find_all('div'))

    final_data = {}
    i = 0
    for divs in info:
        temp_data = {}
        
        current_header = ""
        current_div = {}
        
        for div in divs:
            div_text = div.get_text()
            
            length = len(div_text)
            if length > 0 and div_text[length-1] == ":":
                div_text = div_text.replace(":","")
                
                current_header = div_text
                temp_data[div_text] = {}
            else:
                if len(div) > 1:

                    if len(div_text.split(':')) < 2:
                        continue
                    
                    head = div_text.split(':')[0]
                    body = div_text.split(':')[1]
                    while len(body) > 0 and body[0] == ' ':
                        body = body[1:]
                    temp_body = {"text": body}
                    
                    # Make copy of the current DICT under this header then add a new entry to it
                    temp_area = temp_data[current_header]
                    temp_area[head] = temp_body
                    temp_data[current_header] = temp_area
                    
                else:
                    # Make copy of the current DICT under this header then add a new entry to it
                    temp_area = temp_data[current_header]
                    temp_area["text"] = div_text
                    temp_data[current_header] = temp_area
                    
        
        final_data[headers[i]] = temp_data
        i += 1


    file_name = code[8:10]
    file_path = 'C:/Users/TheNicMachine/Desktop/Country Datas/countries2017/' + file_name + '.json' 
    json_data = json.dumps(final_data, indent=2)
    with open(file_path, "w") as outfile:
        outfile.write(json_data)




import json
from bs4 import BeautifulSoup
import os


directory = os.fsencode("C:/Users/TheNicMachine/Desktop/Country Datas/factbook-2013/geos")

urls = []
for filename in os.listdir(directory):
    f = os.fsdecode(filename)
    if f.endswith(".html") and "countrytemplate" not in f and "print_" not in f:
        urls.append("C:/Users/TheNicMachine/Desktop/Country Datas/factbook-2013/geos/" + f)

urls.remove("C:/Users/TheNicMachine/Desktop/Country Datas/factbook-2013/geos/ip.html")

for url in urls:
    with open(url, 'rb') as html_data:
        soup = BeautifulSoup(html_data, 'lxml')
        
    # Unable to easily pull section names from code :( So manually it is
    sections = ["Introduction", "Geography", "People and Society", "Government", "Economy", "Energy","Communications",
                "Transportation", "Military", "Transnational Issues"]
        
    code = ".." + url[58:]
    print(code)
    
   
    # These files have missing categories
    # Manually sort out those categories
    if code == "../geos/at.html":
        sections.remove("Energy")
        sections.remove("People and Society")
    elif code == "../geos/av.html":
        sections.remove("Energy")
    elif code == "../geos/ax.html":
        sections.remove("Energy")
        sections.remove("Transnational Issues")
        sections.remove("Transportation")
    elif code == "../geos/ay.html":
        sections.remove("Energy")
        sections.remove("Transportation")
    elif code == "../geos/bq.html":
        sections.remove("Energy")
        sections.remove("Communications")
    elif code == "../geos/bv.html":
        sections.remove("Energy")
    elif code == "../geos/cc.html":
        sections.remove("Transnational Issues")
        sections.remove("Communications")
    elif code == "../geos/ck.html":
        sections.remove("Energy")
    elif code == "../geos/cr.html":
        sections.remove("Energy")
    elif code == "../geos/dx.html":
        sections.remove("Transnational Issues")
        sections.remove("Communications")
        sections.remove("Energy")
    elif code == "../geos/dq.html":
        continue
    elif code == "../geos/fq.html":
        continue
    elif code == "../geos/im.html":
        sections.remove("Energy")
    elif code == "../geos/io.html":
        sections.remove("Energy")
    elif code == "../geos/fs.html":
        sections.remove("Energy")
    elif code == "../geos/ip.html":
        sections.remove("Communications")
    elif code == "../geos/gk.html":
        sections.remove("Energy")
    elif code == "../geos/hm.html":
        sections.remove("Energy")
    elif code == "../geos/hq.html":
        continue
    elif code == "../geos/hq.html":
        continue
    elif code == "../geos/jn.html":
        continue
    elif code == "../geos/jq.html":
        continue
    elif code == "../geos/kq.html":
        continue
    elif code == "../geos/kt.html":
        continue
    elif code == "../geos/lq.html":
        continue
    elif code == "../geos/ls.html":
        sections.remove("Energy")
    elif code == "../geos/mf.html":
        continue
    elif code == "../geos/mn.html":
        sections.remove("Energy")
    elif code == "../geos/mq.html":
        sections.remove("Energy")
        sections.remove("Communications")
        sections.remove("Economy")
    elif code == "../geos/nf.html":
        continue
    elif code == "../geos/od.html":
        sections.remove("Energy")
    elif code == "../geos/oo.html":
        sections.remove("Communications")
        sections.remove("People and Society")
        sections.remove("Government")
        sections.remove("Transnational Issues")
        sections.remove("Military")
    elif code == "../geos/pc.html":
        continue
    elif code == "../geos/pf.html":
        continue
    elif code == "../geos/pg.html":
        continue
    elif code == "../geos/ps.html":
        continue
    elif code == "../geos/rn.html":
        sections.remove("Transnational Issues")
        sections.remove("Energy")
    elif code == "../geos/rm.html":
        sections.remove("Transnational Issues")
        sections.remove("Energy")
    elif code == "../geos/sk.html":
        sections.remove("Transnational Issues")
    elif code == "../geos/sm.html":
        sections.remove("Energy")
    elif code == "../geos/ss.html":
        continue
    elif code == "../geos/sv.html":
        sections.remove("Energy")
    elif code == "../geos/sx.html":
        continue
    elif code == "../geos/tb.html":
        sections.remove("Transnational Issues")
        sections.remove("Energy")
    elif code == "../geos/tv.html":
        sections.remove("Energy")
    elif code == "../geos/um.html":
        sections.remove("Communications")
        sections.remove("Energy")
    elif code == "../geos/vt.html":
        sections.remove("Transportation")
        sections.remove("Energy")
    elif code == "../geos/xo.html":
        sections.remove("Communications")
        sections.remove("People and Society")
        sections.remove("Government")
        sections.remove("Military")
        sections.remove("Energy")
    elif code == "../geos/xq.html":
        sections.remove("Communications")
        sections.remove("People and Society")
        sections.remove("Government")
        sections.remove("Military")
        sections.remove("Energy")
    elif code == "../geos/xx.html":
        continue
    elif code == "../geos/wf.html":
        continue
    elif code == "../geos/wq.html":
        continue
    elif code == "../geos/zh.html":
        sections.remove("Communications")
        sections.remove("People and Society")
        sections.remove("Government")
        sections.remove("Military")
        sections.remove("Energy")
    elif code == "../geos/zn.html":
        sections.remove("Communications")
        sections.remove("People and Society")
        sections.remove("Government")
        sections.remove("Military")
        sections.remove("Energy")
        
        

        
    tables = soup.find_all('div', {"class": "CollapsiblePanel"})
    if len(tables) == 0:
        continue
    
    final_data = {}
    for i in range(0, len(sections)):
        table = tables[i]
        table_data = {}
        
        
        current_header = ""
        temp_data = {}
        
        rows = table.find_all('div')
        for row in rows:
            header = row.find_all("a")
            if len(header) > 0:
                current_header = header[0].get_text()
                current_header = current_header.lstrip()
                table_data[current_header] = {}
            else:
                info = row.get_text()
                if ":" in info:
                    title = info.split(":")[0]
                    info = info.split(":")[1]
                    
                    title = title.lstrip()
                    info = info.lstrip()
                    
                    if title == "note":
                        temp_data[title] = info
                        table_data["note"] = info
                    else:
                        temp_data = table_data[current_header]
                        temp_data[title] = {"text": info}
                        table_data[current_header] = temp_data
                else:
                    temp_data = table_data[current_header]
                    temp_data["text"] = info
                    table_data[current_header] = temp_data
        
        #table_data.pop("")
        final_data[sections[i]] = table_data

    file_name = code[8:10]
    file_path = 'C:/Users/TheNicMachine/Desktop/Country Datas/countries2013/' + file_name + '.json' 
    json_data = json.dumps(final_data, indent=2)
    with open(file_path, "w") as outfile:
        outfile.write(json_data)
        
        




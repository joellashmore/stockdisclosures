# All code credit to Part Time Larry from youtube
import csv, json, zipfile
import requests, PyPDF2, datetime, os, tabula

# Make empty list to hold the URLs for financial discloure info to scrape - these contain document IDs for further forms that have the individual trades listed
zipfile_urls = []
zipfile_names = []
year = datetime.datetime.today().year

#Get the last five years of data, plus the current one
years = list(range(year, year , -1))
print(years)

zipfile_base_url ="https://disclosures-clerk.house.gov/public_disc/financial-pdfs/"
zipfile_ext = "FD.zip"
pdf_base_url = "https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/"

for i in years:
    print(i)
    fullurl = str(zipfile_base_url) + str(i) + str(zipfile_ext)
    filename = str(i) + str(zipfile_ext)
    zipfile_urls.append(fullurl)
    zipfile_names.append(filename)

for file in zipfile_urls:
    r = requests.get(file)
    for name in zipfile_names:
        with open(name, 'wb') as f:
            f.write(r.content)
            with zipfile.ZipFile(name) as z:
                z.extractall('.')     
                
                
for filename in os.listdir('/Users/joellashmore/stockdisclosures'):
    if filename.endswith(".txt"): 
        print(filename)
        with open(filename) as o:
            for line in csv.reader(o, delimiter='\t'):
                
                date = line[7]
                fst_name = [2]
                lst_name = [1]
                doc_id = line[8]
                r = requests.get(f"{pdf_base_url}{filename[:4]}/{doc_id}.pdf")
                # Only save file if it found a doc for a correct id
                if r.status_code == 200:
                    with open(f"data/{doc_id}.pdf", 'wb') as pdf_file:
                        pdf_file.write(r.content)
                    
                    
                 #   tabula.convert_into(r.content, f"{doc_id}_{date}_{lst_name}_{fst_name}.csv", output_format="csv", pages='all')
#
#                    with open(f"data/{doc_id}.pdf", 'wb') as pdf_file:
#                        pdf_file.write(r.content)
#_{lst_name}_{fst_name}_{date}
#                
                

 



    
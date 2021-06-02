import PyPDF2, fitz, pdfplumber
import csv, os, glob, re
import pandas as pd
import json
import tabula
import parse
from collections import namedtuple
from pathlib import Path

# Periodic Transaction Reports come in two flavors, the pdfs that are text-readable, i.e. you can highlgight the text in them, and those that are just images
# To get the relevant data out of each, you have to programmatically detect which are images and which already contain text. This is easy to do, because apparently the image ones all start with an '8' in their file name.


# What file extension to find, and where to look from
ext = "*.pdf"
PATH = "/Users/joellashmore/stockdisclosures"

# Find all the files with that extension
files = []
for dirpath, dirnames, filenames in os.walk(PATH):
    files += glob.glob(os.path.join(dirpath, ext))
    
print(files)

# Names of fields you're trying to scrape from the PTR's.
Line = namedtuple('Line', 'name asset transaction_type date_group amount')
lines= []
date_re = re.compile(r'\d{2}/\d{2}/\d{4} ')

for file in files:
#    read_pdf = fitz.open(file)
    if Path(file).stem[0] != '8':
        with pdfplumber.open(file) as pdf:
            pages = pdf.pages
            for page in pdf.pages:
                text = page.extract_text()
                try:
                    for line in text.split('\n'):
                        if 'Name: ' in line:
                            name = line.split("Name: ",1)[1]
                        if date_re.search(line)  and re.search('\$', line):
                            date_group = re.findall(r'\d{2}/\d{2}/\d{4}', line)
                        if re.search('\$', line):
                            if re.search('\$[0-9][0-9],[0-9][0-9][0-9]',line):
                                amount = re.findall('\$[0-9][0-9],[0-9][0-9][0-9]',line) 
                            elif re.search('\$[0-9][0-9][0-9],[0-9][0-9][0-9]',line):
                                amount = re.findall('\$[0-9][0-9][0-9],[0-9][0-9][0-9]',line)  
                            elif re.search('\$[0-9][0-9].[0-9][0-9]',line):
                                amount = re.findall('\$[0-9][0-9].[0-9][0-9]',line)
                        if re.search('\$', line) and ( ' P ' in line or ' S ' in line):
                            transaction_type_1 = re.findall(' P ', line)
                            transaction_type_2 = re.findall(' S ', line)
                            if transaction_type_1:
                                transaction_type = 'Purchased'
                                asset = (line[0:line.find(' P ')])
                            else:
                                transaction_type = 'Sold'
                                asset = (line[0:line.find(' S ')])

                            lines.append(Line(name, asset, transaction_type, date_group, amount))
                except:
                    print('No line or EOL detected')
                        

              
#df = pd.DataFrame(lines)                        
#                      
#print(df.head())
  
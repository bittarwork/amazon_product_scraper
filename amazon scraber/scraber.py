import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import json
import csv


# csv 
filecsv = open('SouqDataapple.csv', 'w',encoding='utf8')
# url 
url = 'https://www.amazon.sa/s?k=apple&dc&page='
# json
file = open('SouqDataapple.json','w',encoding='utf8')
file.write('[\n')
# init data
data = {}
# csv data 
csv_columns = ['name','price','img']
# for loop for scrabing each page : 
for page in range(40):
    # go to the page 
    print('---', page, '---')
    r = requests.get(url + str(page))
    # print url
    print(url + str(page))
    # sou object
    soup = BeautifulSoup(r.content, "html.parser")
    # all elements in this page 
    divs=soup.find_all('div',{'class' : 'sg-col-inner'})
    # writer object :
    writer = csv.DictWriter(filecsv, fieldnames=csv_columns)
    i=0
    writer.writeheader()
    for div in  divs:
        # retrive information from each div 
        name=div.find('span', {'class' : 'a-size-base-plus a-color-base a-text-normal'})
        itemPrice=div.find('span', {'class' : 'a-price-whole'})
        img=div.find('img', {'class' : 's-image'})
        # condition to write all information 
        if img and name and itemPrice:      
            # csv writing 
            writer.writerow({'name': name.text.replace('                    ', '').strip('\r\n'), 'price': itemPrice.text, 'img': img.get('src')})
            # jason data writing 
            data['name'] =name.text.replace('                    ', '').strip('\r\n')
            data['price'] =itemPrice.text
            data['img'] =img.get('src')
            json_data = json.dumps(data,ensure_ascii=False)
            file.write(json_data)
            file.write(",\n") 
# finish and close :
file.write("\n]")
filecsv.close()
file.close()
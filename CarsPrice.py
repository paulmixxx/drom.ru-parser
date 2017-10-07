import urllib.request
import urllib.parse

import csv
import time

from bs4 import BeautifulSoup

import http.client
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

#Insert your URL
BASE_URL = 'http://moscow.drom.ru/toyota/camry/?fueltype=1&transmission=2&ph=1&pts=2&damaged=2&w=2&go_search=2'
#Insert your NAME File
NAME_FILE = "Cars"

def get_html(url):
    try:
        content_page = urllib.request.urlopen(url).read().decode('windows-1251')
        return content_page
    except http.client.IncompleteRead:
        return False

def remove_char(string, chars):
    string_new = ""
    for c in string:
        if c not in chars:
            string_new = string_new + c
    return string_new

def parse_html(html_page):
    list_object = BeautifulSoup(html_page, 'html.parser')

    list_cars = []
    
    for x in list_object.find_all('a', {'class' : 'b-advItem'}):
        list_cars.append(x)
        
    var = []
    
    for x in list_cars:
        var.append({"URL" : x['href'],
                    "date" : x.find_all('div', {'class' : 'b-advItem__param'})[-1]
                              .text
                              .replace("\xa0", " "),
                    "year" : x.find_all("div", {'class' : 'b-advItem__title'})[0]
                              .text
                              .split(", ")[1],
                    "price" : x.find_all('div', {'class' : 'b-advItem__price '})[0]
                               .text
                               .replace("\n", "")
                               .replace("\xa0", "")
                               .strip()
                               .replace("q", ""),
                    "city" : x.find_all('div', {'class' : 'b-advItem__param'})[-2]
                              .text
            })
        
    print(var)
    return var

def result_print(data):
    for x in data:
        print("{0}; {1}; {2}".format(x['date'], convert_data(x['date']), x['value']))

def save(namefile, data):
    with open("{0}.txt".format(namefile), "w") as f:
        f.write("Date ; UTC ; Value")
        for x in data:
            f.write("{0}; {1}; {2}".format(x['date'], convert_data(x['date']), x['value']))
            
def save_csv(namefile, data):
    with open("{0}.csv".format(namefile), "a", encoding='utf-8') as f:
        spamwriter = csv.writer(f, dialect='excel')
        for x in data:
            spamwriter.writerow((x['year'], x['price'], x['URL'], x['date'], x['city']))

def create_csv(namefile):
    with open("{0}.csv".format(namefile), "w", encoding='utf-8') as f:
        spamwriter = csv.writer(f, dialect='excel')
    
def count_page(current_link):
    
    count = 1
    create_csv(NAME_FILE)
    
    while 1:
        time.sleep(1)
        print(count)

        if count % 5 == 0:
            time.sleep(15)

        if count % 10 == 0:
            time.sleep(30)

        content = get_html(current_link)
        
        
        content_page = BeautifulSoup(content, 'html.parser')
        #print(content_page)
        var = content_page.find("a", {"class" : "b-pagination__item_next"})
        if var is None:
            print(("Pages: {0}".format(count)))
            x = parse_html(content)
            save_csv(NAME_FILE, x)
            break
        else:
            count +=1
            current_link = var['href']
            content = parse_html(get_html(current_link))
            save_csv(NAME_FILE, content)

count_page(BASE_URL)

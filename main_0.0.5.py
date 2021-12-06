# -*- coding: iso-8859-1 -*-
# import re
import redis
import hashlib
import re
from selenium import webdriver
# "/usr/local/bin/chromedriver"
from bs4 import BeautifulSoup


def redis_con():
    redis_client = redis.Redis(host='localhost', port=6379, db=0, password=123456789, decode_responses=True)

    return redis_client


def seitenanzahl():
    mainurl = "https://home.mobile.de/regional"

    url_list = ["/bayern/0.html", "/baden-württemberg/0.html", "/rheinland-pfalz/0.html", "/saarland/0.html",
                "/hessen/0.html", "/thüringen/0.html", "/sachsen/0.html", "/sachsen-anhalt/0.html",
                "/nordrhein-westfalen/0.html", "/niedersachsen/0.html", "/brandenburg/0.html", "/berlin/0.html",
                "/bremen/0.html", "/schleswig-holstein/0.html", "/hamburg/0.html", "/mecklenburg-vorpommern/0.html"]

    for i in range(0, 16):

        url = mainurl + url_list[i]

        driver = webdriver.Chrome()
        driver.get(url)
        html = driver.page_source

        soup = BeautifulSoup(html, 'lxml')
        # Seitenanzahl
        seite = soup.find("ol", {"class": "num"})

        pagelist_row = []
        for nex in seite.findChildren('li'):
            pagelist_row.append(nex.text)

        pagelist_last_item = pagelist_row[-1]

        last_item_to_int = (int(pagelist_last_item))
        seiten_zahl = last_item_to_int - 1

        redis_client = redis_con()

        # seitenlink in redis speichern
        for n in range(0, seiten_zahl):
            link = url[:-6] + (str(n)) + ".html"
            link_hash = hashlib.md5(str(link).encode('utf-8', 'ignore')).hexdigest()

            # abrage ob linkhash bereits existiert
            if not redis_client.exists(link_hash):
                reg = "tpl_regioLinks"
                redis_client.hset(reg, link_hash, link)
            else:
                pass

#seitenanzahl()


def crwal_delaer():
    redis_client = redis_con()
    links = redis_client.hvals("tpl_regioLinks")

    for i in links:
        url = i
        driver = webdriver.Chrome()
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        # Seitenanzahl

        seite = soup.find_all('h3')

        h3content = str(seite)
        sauce2 = h3content
        soup2 = BeautifulSoup(sauce2, "lxml")

        # suche nach http://home.mobile.de
        for a_tag in soup2.select('a[href*="/home.mobile.de"]'):
            link = a_tag['href']
            link_hash = hashlib.md5(str(link).encode('utf-8', 'ignore')).hexdigest()

            # abrage ob linkhash bereits existiert
            if not redis_client.exists(link_hash):
                reg = "tpl_dealer_urls"
                redis_client.hset(reg, link_hash, link)
            else:
                pass

#crwal_delaer()


def crwal_cars():

    global h3_c
    redis_client = redis_con()
    links = redis_client.hvals("tpl_dealer_urls")

    for i in links:
        url = i
        driver = webdriver.Chrome()
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        # car_build


        # Titel crwal
        crawl1 = soup.findAll("li", {"class": "listing odd"})
        h3content = str(crawl1)
        sauce2 = h3content
        soup2 = BeautifulSoup(sauce2, "lxml")

        List_hash = []
        List_URL = []
        List_title= []
        List_km = []
        List_price = []
        List_ez = []
        List_power = []

        for tag in soup2.find_all(class_="listing odd"):
            car_id = tag.get('id')
            url_para = "#des_"
            car_link = url + url_para + car_id
            link_hash = hashlib.md5(str(car_link).encode('utf-8', 'ignore')).hexdigest()
            List_hash.append(link_hash)
            List_URL.append(car_link)
            # lencheck
            checklen1 = (len(List_URL))


        for a in soup2.find_all('h3'):
            h3_c = a.text
            #print(h3_c)
            List_title.append(h3_c)
            # lencheck
            checklen2 = (len(List_title))


        for c in soup2.find_all("div", {"class": "vehiclePrice pull-right"}):
            price_c = c.text
            #print(price_c)
            List_price.append(price_c)

        for d in soup2.find_all("span", {"class": "firstReg"}):
            ez_span = d.text
            #print(ez_span)
            List_ez.append(ez_span)
            # lencheck
            checklen4 = (len(ez_span))

        for e in soup2.find_all("span", {"class": "mileage"}):
            km_span = e.text
            #print(km_span)
            List_km.append(km_span)
            checklen5 = (len(km_span))

        checklen1 = (len(List_URL))
        checklen2 = (len(List_title))

        checklen3 = (len(List_price))
        checklen4 = (len(ez_span))
        checklen5 = (len(km_span))

        # URL mit Title
        if checklen1 == checklen2:
            pass
        else:
            List_title.append("NODE")

        # Title mit Price
        if checklen2 == checklen3:
            pass
        else:
            List_title.append("NODE")

        # ez mit Price
        if checklen4 == checklen5:
            pass
        else:
            List_title.append("NODE")

        carInserats = List_hash + List_URL + List_title + List_km + List_price + List_ez

        #print(len(carInserats))

        print(len(List_URL))
        print(len(List_title))
        print(len(List_price))
        print(len(ez_span))
        print(len(km_span))

        print(carInserats)

crwal_cars()


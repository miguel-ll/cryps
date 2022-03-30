# depends on rate.sx
from flask import Flask
import requests
import re

app = Flask(__name__)

@app.route('/')
def default():
    return "<h1>Example:  url/btc</h1><h2>If you want to see the list of supported cryptocurrencies, go to url/list.</h2>"

@app.route('/<cryptocoin>')
def crypto(cryptocoin):
    url = f"http://rate.sx/{cryptocoin}?T"
    resp = requests.get(url).text
    name = resp.splitlines()[:2] 
    name = re.search('[A-Z].*\(', name[1]).group()[:-2]
    form_resp = resp.splitlines()[-5:]
    begin_end = form_resp[0]
    begin_price = begin_end.split()[1]
    # dates according to UTC
    date_begin = re.search('\(.*\)', begin_end).group()[1:]
    date_begin = f"{date_begin.split()[0]} {date_begin.split()[1]} {date_begin.split()[2][:-1]}"
    end_price = begin_end.split()[7]
    date_end = re.search('end.*\)', begin_end).group()
    date_end = f"{date_end.split()[2][1:]} {date_end.split()[3]} {date_end.split()[4][:-1]}"
    high_low = form_resp[1]
    highest_price = high_low.split()[1]
    date_highest = re.search('\(.*\)', high_low).group()[1:]
    date_highest = f"{date_highest.split()[0]} {date_highest.split()[1]} {date_highest.split()[2][:-1]}"
    lowest_price = high_low.split()[7]
    date_lowest = re.search('low.*\)', high_low).group()
    date_lowest = f"{date_lowest.split()[2][1:]} {date_lowest.split()[3]} {date_lowest.split()[4][:-1]}"
    avg_med = form_resp[2]
    average = avg_med.split()[1]
    median = avg_med.split()[4]
    # change in 24h
    change_value = avg_med.split()[7]
    change_perc = avg_med.split()[8][:-1][1:]
    return {"name": name, "begin_price": begin_price, "date_begin": date_begin, "end_price": end_price, "date_end": date_end, "highest_price": highest_price, "date_highest": date_highest, "lowest_price": lowest_price, "date_lowest": date_lowest, "average": average, "median": median, "change_value": change_value, "change_perc": change_perc} 

@app.route('/list')
def list():
    import json
    url = "http://rate.sx/:coins"
    resp = requests.get(url).text
    li1 = []
    li2 = []
    for i in resp.splitlines():
        li1.append(i.split()[0])
        li2.append(i.split()[1])
    lii = {li1[i]: li2[i] for i in range(len(li1))}
    return lii

if __name__ == '__main__':
   app.run()

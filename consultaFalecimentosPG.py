from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
from datetime import date
from datetime import timedelta

def consultaFalecimentos(fullData):
    URL = "http://app.pontagrossa.pr.gov.br/sisppg/servico_funerario/internet/mostra_hoje.php"
    param = "ontem=" + fullData
    try:
        r = requests.get(url = URL, params = param)
        if r.status_code == 200:
            tables = pd.read_html(r.content,flavor='bs4')
            count = 0
            for nome in tables[1][0]:
                if isinstance(nome, float):
                    break
                if nome != "Nome":
                    count+=1                         
        else:
            raise Exception("URL return status is not 200")        
        return count
    except :
        print("An error happened whilte requesting URL", URL)
        return False

def extract_data(years_to_compare, starting_day, starting_month, ending_day, ending_month):
    resulting_data = {}

    for year in years_to_compare:
        actual_date = datetime.datetime(year, starting_month, starting_day)
        ending_date = datetime.datetime(year, ending_month, ending_day)
        resulting_data[year] = { 'x': [], 'y': []}

        while actual_date <= ending_date:
            date_str = actual_date.strftime('%d/%m/%Y')
            day_month_str = actual_date.strftime('%d/%m')
            resulting_data[year]['x'].append(day_month_str)
            resulting_data[year]['y'].append(consultaFalecimentos(date_str))
            actual_date = actual_date + timedelta(days=1)
        
    return resulting_data

def calculate_moving_average(years_to_compare, resulting_data, moving_size):
    for year in years_to_compare:
        resulting_data[str(year)+"-ma"] = { 'x': [], 'y': []}
        moving_sum = 0
        for index in range(len(resulting_data[year]['y'])):
            moving_sum += resulting_data[year]['y'][index]
            if index >= moving_size:
                resulting_data[str(year)+"-ma"]['y'].append(moving_sum/min(index+1,moving_size))
                resulting_data[str(year)+"-ma"]['x'].append(resulting_data[year]['x'][index])
                moving_sum -= resulting_data[year]['y'][index-moving_size]
            index += 1
    return resulting_data


startDate = datetime.datetime(2020, 8, 1)


i = 0
diasCount = 1

while i < diasCount:
    startDate = startDate + timedelta(days=1)
    data_em_texto = startDate.strftime('%d/%m/%Y')
    totalDia = consultaFalecimentos(data_em_texto)
    print (data_em_texto,",", totalDia,",",sep="")
    i += 1

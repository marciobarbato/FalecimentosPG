from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
from datetime import date
from datetime import timedelta

def consultaFalecimentos(fullData):
    URL = "http://app.pontagrossa.pr.gov.br/sisppg/servico_funerario/internet/mostra_hoje.php"
    param = "ontem=" + fullData
    r = requests.get(url = URL, params = param)

    if r.status_code == 200:
        tables = pd.read_html(r.content,flavor='bs4')
        count = 0
        for nome in tables[1][0]:
            if isinstance(nome, float):
                break
            if nome != "Nome":
                count+=1                         
                
    
        #print("total de nomes",count)
        return count
    else:
        print('An error has occurred.')
        return False

data_comeco_ano = datetime.datetime(2020, 5, 1)
data_atual = data_comeco_ano


i = 0
diasCount = 1

while i<diasCount:
    data_atual = data_atual + timedelta(days=1)
    data_em_texto = data_atual.strftime('%d/%m/%Y')
    #print ("consulta dia: ", data_em_texto)
    totalDia = consultaFalecimentos(data_em_texto)
    print (data_em_texto,",", totalDia,",",sep="")
    i += 1
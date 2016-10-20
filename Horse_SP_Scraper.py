# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 11:30:20 2015

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 15:46:30 2015

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 13:16:33 2015

@author: Administrator
"""
import fractions
from bs4 import BeautifulSoup
import winsound
import requests

from datetime import datetime
startTime = str(datetime.now())
date = startTime[:10]
import xlwt
from tempfile import TemporaryFile
book = xlwt.Workbook()
sheet1 = book.add_sheet('sheet1')

race_url_list = []

alphabet = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
for letter in alphabet:
    results_url = "http://www.irishracing.com/result-index?starting-with=" + letter

    r  = requests.get(results_url)

    data = r.text

    soup = BeautifulSoup(data)

    links = []
    race_url_letter = []

    for link in soup.find_all('a'):
        links.append(link.get('href'))

    for href in links:
        if href[0:33] == "http://www.irishracing.com/result":
            race_url_letter.append(href[33:])

    race_url_list.extend(race_url_letter)
row_number=0
if row_number < len(race_url_list):
    for ending in race_url_list:
     
        race_url = "http://www.irishracing.com/result" + ending
    
        r  = requests.get(race_url)
    
        data = r.text
    
        soup = BeautifulSoup(data)
    
        SP = []
        odds_list = []
    
        for strong_tag in soup.find_all('strong'):
            SP.append(strong_tag.text)
            sp = SP
    
        for d in sp:
            if str(d[0:2]) == "SP":  #to pick out what ones are odds
                odds_list.append(str(d[3:])) #to pick out the odds themselves
    
        decimal_list = []    #converting the fractions to decimal
        decimal_list.append(ending)      
        for i in odds_list:
            b = str(i)  
            try:
                c = float(fractions.Fraction(b))
            except ValueError:
                try:        
                    b = b[:-3]   #to get rid of fav at end of odds
                    c = float(fractions.Fraction(b))
                except ValueError:
                    b = b[:-1]   #to get rid of Jfav
                    c = float(fractions.Fraction(b))
            decimal_list.append(c)
        
        for column_number, item in enumerate(decimal_list):  #writing each race result and odds into a column, the order is the order in which they finished                
            sheet1.write(row_number, column_number, item)  
        
        name = "Hodds " + date + ".xls"
        book.save(name)
        book.save(TemporaryFile())
        
        row_number=row_number+1
winsound.Beep(1000,1000)    
#d = unicodedata.numeric(u'odds_list[0]')
#i = float(odds_list[0])

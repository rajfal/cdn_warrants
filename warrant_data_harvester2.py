#!/usr/bin/env python
#----------------START IMPORT LIBRARIES -------------------------------#
from bs4 import BeautifulSoup

import pandas as pd

import requests

import csv #not used yet

import sys

import os

import datetime

import re

#------------------END IMPORT LIBRARIES -------------------------------#

#------------------START CONSTANTS ------------------------------------#

url = "http://www.financialpost.com/markets/data/group-warrants.html";
#url = "file:///home/xyz/learning.python/Warrants/warrants_nov.html";

url_tmx = "http://web.tmxmoney.com/quote.php?qm_symbol=";
url_tmx_combo_xt = "http://web.tmxmoney.com/getquote.php?symbols%5B%5D=NDM.WT.B&symbols%5B%5D=LYD.WT&symbols%5B%5D=MQR.WT.A"
url_tmx_combo= "file:///home/xyz/learning.python/Warrants/warrants_multi_quotes.html"

#--------------------END CONSTANTS ------------------------------------#

def get_daily_tmx_data(warrant_symbol):
    #warrant_symbol = "JDL.WT"
    print ("...fetching closing price for " + warrant_symbol)
    my_soup = open_page(url_tmx + warrant_symbol)
    table = my_soup.find(class_="quote-price priceLarge")
    #skip first two table header rows and the very last, else None object appears
    for row in table.find_all('span'):
        
        return(row.string)

    #print("-------------------------------------tmx price updated");

def get_tmx_warrants_daily_close(page_url= "all"):
    """retrieve warrant symbol and its daily closing price
       return data as dictionary
    """    

    warrant_prices = {}
    page = open_page(url_tmx_combo) 
    table = get_soup_table_(page,"tbody") # tbody tag contains all required data
    
    for row in table.find_all("tr"):
        s = row.get_text().split("\n")
        warrant_prices[s[1]] = s[3].replace(" ","")
        #print ("...fetching closing price for... " + s[1])
    #for key, value in warrant_prices.items():
    #    print(key + ":" + value)

    return warrant_prices


def make_multi_arg_url(warrant_symbols= ""):
    """pass in a tuple of warrant_symbols and
       return a url string where those warrant_symbols are passed as args
       example: http://web.tmxmoney.com/getquote.php?symbols%5B%5D=NDM.WT.B&symbols%5B%5D=LYD.WT&symbols%5B%5D=MQR.WT.A
    """    
    
    arg_string = ""
    pre_string = "&symbols%5B%5D="
    page = "http://web.tmxmoney.com/getquote.php?" 

    for item in warrant_symbols:
        arg_string += pre_string + item
        
    url = (page + arg_string).replace("?&", "?")

    return url



##https://www.crummy.com/software/BeautifulSoup/bs4/doc
##http://chrisalbon.com/python/beautiful_soup_scrape_table.html 
##pandas.pydata.org documentation

def get_page_content(url):
    #page = urllib2.urlopen(url)
    #return urllib3.urlopen(url)
    response = requests.get(url)
    return response.content
    
    

def get_soup_table_(page= '', tag= '', parser= 'lxml'):
    soup = BeautifulSoup(page, parser)
    table = soup.find(tag)
    return table
 
def get_soup_table(page= '', page_class= '', parser= 'html.parser'):
    soup = BeautifulSoup(page, parser)
    table = soup.find(class_= page_class)
    return table

def extract_monthly_data(table= ''):
    """ return 
    """
    company = []
    stock_close = []
    warrant_symbol = []
    warrant_exercise_price = []
    warrant_close = []
    leverage = []
    years_left = []
    warrant_expiry_date = []
    
    #my_soup = open_page(url)
    #table = my_soup.find(class_="data")


    #exclude first two table header rows and the very last, else None object appears
    for row in table.find_all('tr')[2:-1]:
 
        # Create a variable of all the <td> tag pairs in each <tr> tag pair,
        col = row.find_all('td')
        
        #col[0] in some rows only 1 character and missing full co. name...fill it in with previous string
        if len(col[0].string) == 1: 
            col[0].string.replace_with(previous_co_name)

        #only warrants with at least 4 years to expiry need to be included
        if int((col[12].string.strip().split(', ')[1]))> (datetime.datetime.now().year +2):
            # Create a variable of the string inside 1st <td> tag pair,
            company.append(col[0].string) # company name
            stock_close.append(col[1].string or 0) # stock close
            warrant_symbol.append(col[3].string) # symbol            
            warrant_exercise_price.append(col[5].string) # exercise price
            
            #print col[6].get_text()
            try:
                col[6].sup.decompose()
            except AttributeError:
                pass
                
            ##warrant_end_of_day_close = get_daily_tmx_data(col[3].string) 
            warrant_end_of_day_close = col[6].get_text() or 0 # warrant close                                               
            warrant_close.append(warrant_end_of_day_close)  

            #if col[6].string is None:
            #    print("none")
        #else:
            #    print(list(col[6].string))
 
            #print(str(col[6].string) + " " + company[-1])  
            #sometimes stock/warrant close is in US$, so need to strip it down to '0123456789.' to calc leverage against warrant close

                
            warrant_close_numeric = re.sub('[^0-9^.]','', col[6].get_text(), flags=re.U) #
            stock_close_numeric = re.sub('[^0-9^.]','', str(stock_close[-1]))
            
            stock_warrant_leverage = float(stock_close_numeric)/float(warrant_close_numeric)
            
            #stock_warrant_leverage = col[10].string # leverage
            #print(col[10].string)
            leverage.append(stock_warrant_leverage) 
            #leverage.append(col[10].string) # leverage

            years_left.append(col[11].string) # years left
            #x = col[12].string.strip().split(', ')[1] # expiry date - reports only the year part of the column, for filtering
            warrant_expiry_date.append(col[12].string) # expiry date
            #print(col[12].string)
            

        previous_co_name = col[0].string
        #print(previous_co_name)   
        #print(str(len(col[0].string)) + " " + col[0].string)

    columns = ({'1-company': company, '2-stock_close': stock_close, '3-symbol': warrant_symbol, '4-exercise_price': warrant_exercise_price,
               '5-close': warrant_close, '6-leverage': leverage, '7-years_left': years_left, '8-expiry_date': warrant_expiry_date})
    #for c in columns.items():
    #   print(c)
 
    return columns

def mainx():
    """Main entry point for script
    """
    #pass
    os.system('clear') #play on a clean screen :)    
    print("try combo")
    warrants = ('LYD.WT','MQR.WT.A','NDM.WT.B')

    make_multi_arg_url(warrants)
    data = get_tmx_warrants_daily_close(warrants)
    print("end combo")
 
def main():
    """Main entry point for script
    """
    #pass
    os.system('clear') #play on a clean screen :)    
        
    page = get_page_content(url)
    
    table = get_soup_table(page,"data")

    data_as_columns = extract_monthly_data(table)

    pd.set_option('display.width', pd.util.terminal.get_terminal_size()[0])
    df = pd.DataFrame(data_as_columns) 

    #indexed_df = df.set_index(['1-company']) # add index

    print(df)
    #-----
    #print(df[['1-company', '3-symbol']]); #show two cols only

    #print(df[:2]); # show first two rows of DataFrame

    #print(df[df['6-leverage'] > 3]); # show all rows where leverage > 3
 
    #print(indexed_df.ix['JDL Gold Corp']); # show 1 row based on index reference
 
    #print(indexed_df.ix[:, '7-years_left']); # show 1 column based on index reference

    #print(indexed_df.ix['Blackbird Energy Inc', '3-symbol']); # show value based on row and column

    
if __name__ == '__main__':
    """report any processing error to the shell??
    """
    sys.exit(main())


 





















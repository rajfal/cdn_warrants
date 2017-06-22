#!/usr/bin/env python
#----------------START IMPORT LIBRARIES -------------------------------#
from bs4 import BeautifulSoup

import pandas as pd

import requests # to open files on remote servers

import csv #not used yet

import sys

import os

import datetime

import re

#------------------END IMPORT LIBRARIES -------------------------------#

#------------------START CONSTANTS ------------------------------------#

url_remote = "http://www.financialpost.com/markets/data/group-warrants.html";
url_local = "/home/ithilien/Documents/misc/Warrants-Data-2017-06.html";

url_tmx = "http://web.tmxmoney.com/quote.php?qm_symbol=";
url_tmx_combo_xt = "http://web.tmxmoney.com/getquote.php?symbols%5B%5D=NDM.WT.B&symbols%5B%5D=LYD.WT&symbols%5B%5D=MQR.WT.A"
url_tmx_combo= "file:///home/xyz/learning.python/Warrants/warrants_multi_quotes.html"

#--------------------END CONSTANTS ------------------------------------#

#-----------START GLOBAL VARIABLES ------------------------------------#
current_file_date = ''
#-------------END GLOBAL VARIABLES ------------------------------------#


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


def get_local_page_content(path):
    #for files stored locally
    with open(path, "r") as f:
        page = f.read()
    return page

def get_remote_page_content(url):
    # on http://... server
    response = requests.get(url)
    return response.content
    
def get_page(source):
    if source == 'local':
        page = get_local_page_content(url_local)
    else:
        page = get_page_content(url_remote)
    return page    
        
def get_soup_table_(page= '', tag= '', parser= 'lxml'):
    soup = BeautifulSoup(page, parser)
    table = soup.find(tag)
    return table
 
def get_soup_table(page= '', page_class= '', parser= 'html.parser'):
    soup = BeautifulSoup(page, parser)
    table = soup.find(class_= page_class)
    return table
    
def remove_html_tags(html_element, tag_list):
    """
        remove_html_tags(row, ['span', 'sup'])
    """
    for tag in html_element(tag_list):
            try:
                tag.decompose()                
            except AttributeError:
                pass    

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
    currency = []
    
    prices = [] # hold cols that may contain US$ 
     
    for header in table.find_all('tr')[0:1]:
        # save name for eventual CSV file name
        col = header.find_all('td')
        global current_file_date 
        # assign to global variable
        current_file_date = get_num_value(col[0])
        print(current_file_date)    
        
        
    # for warrants data body, exclude first two table header rows and the very last, else None object appears
    for row in table.find_all('tr')[2:-1]:
        
        # clear superscript references
        remove_html_tags(row, ['sup'])
        
        # create a variable of all the <td> tag pairs in each <tr> tag pair,
        col = row.find_all('td')
        
        #col[0] in some rows only 1 character and missing full co. name...fill it in with previous string
        if len(col[0].string) == 1: 
            col[0].string.replace_with(previous_co_name)

        #only warrants with at least 4 years to expiry need to be included
        # =>>
        if int((col[12].string.strip().split(', ')[1]))> (datetime.datetime.now().year +0):
            
            
            # Create a variable of the string inside 1st <td> tag pair,
            company.append(col[0].string) # company name
            
            stock_close.append(get_num_value(col[1]) or 0) # stock close 
            
            warrant_symbol.append(col[3].string) # symbol
                        
            warrant_exercise_price.append(get_num_value(col[5]) or 0) # exercise price
                            
            warrant_close.append(get_num_value(col[6]) or 0)                                            
            
            stock_warrant_leverage = float(stock_close[-1])/float(warrant_close[-1])
            
            # return one decimal place
            leverage.append('{:.1f}'.format(stock_warrant_leverage)) 
            
            years_left.append(get_num_value(col[11])) # years left
            
            """
            if float(yrs_left)>3.5 and stock_warrant_leverage>40.0: 
            ##if float(col[11].string)>3.5 and stock_warrant_leverage>40.0:     
                print(col[3].string + ' - ' + col[0].string)
                print('to expiry ' + col[11].string + ' years')
                # print('leverage ' + str(stock_warrant_leverage)) # "%8.2f" %
                print('leverage ' + '{:.1f}'.format(stock_warrant_leverage))
            """    
            
            warrant_expiry_date.append(col[12].string) # expiry date
            
            #check whether US$ is present in following columns
            prices = [ col[1].string, col[5].string, col[6].get_text() ]            
            currency.append(get_trade_currency('US$', prices))
         
        previous_co_name = col[0].string
        
    columns = ({'1-company': company, '2-stk_close': stock_close, '3-symbol': warrant_symbol, '4-exercise_price': warrant_exercise_price,
               '5-wrt_close': warrant_close, '6-leverage': leverage, '7-years_left': years_left, '8-expiry_date': warrant_expiry_date, 
               '9-currency': currency})
    #for c in columns.items():
    #   print(c)
    
    return columns
    
def get_trade_currency( other_currency, price_list ):
    #check whether other_currency is present, default is CDN
    trade_currency = 'CDN'
    
    if any(other_currency in p for p in price_list):
        trade_currency = 'USD'
    return trade_currency

def get_num_value( in_str ):
    # obtain numeric value of passed in string
    # col[6].get_text()
    return re.sub('[^0-9^.]','', in_str.get_text(), flags=re.U)

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
    
    # 'local' by default, else 'remote' 
    datasource = 'local'   
    page = get_page(datasource)
    
    table = get_soup_table(page,"data")

    data_as_columns = extract_monthly_data(table)

    pd.set_option('display.width', pd.util.terminal.get_terminal_size()[0])
    
    df = pd.DataFrame(data_as_columns) 

    #indexed_df = df.set_index(['1-company']) # add index

    ##print(df)
    ##print(df.to_csv('warrants_data_' + str(get_num_value(col[5])) + '.csv'))
    
    global current_file_date
    print('file date : ' + current_file_date)
    df.to_csv('warrants_market_data_' + str(current_file_date) + '.csv', index=False)
    
    print('{:*^30}'.format(' end '))
    print("Data from: " + datasource )
    print('{:*^30}'.format(' end '))
    # https://docs.python.org/2/library/string.html
    
    
    
    
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


 





















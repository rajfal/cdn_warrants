#!/usr/bin/env python
#------------------CODE INFORMATION -----------------------------------#
"""
by: Rafal Jacyna
email: rafal@jacyna.net

purpose: scrape warrant data, prep it and save as CSV file

refs:
##https://www.crummy.com/software/BeautifulSoup/bs4/doc
##http://chrisalbon.com/python/beautiful_soup_scrape_table.html 
##pandas.pydata.org documentation
## https://docs.python.org/2/library/string.html
##https://leemendelowitz.github.io/blog/any-all-in-python.html
##https://kaijento.github.io/2017/03/30/beautifulsoup-removing-tags/

"""
#------------------CODE INFORMATION -----------------------------------#


#----------------START IMPORT LIBRARIES -------------------------------#
from utils import untangle_date, get_days_to_expiry # custom package

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
#--------------------END CONSTANTS ------------------------------------#

#-----------START GLOBAL VARIABLES ------------------------------------#
current_file_date = ''
#-------------END GLOBAL VARIABLES ------------------------------------#


def get_local_page_content(path):
    # for local files
    with open(path, "r") as f:
        page = f.read()
    return page

def get_remote_page_content(url):
    # for files on http://... server
    response = requests.get(url)
    return response.content
    
def get_page(source):
    if source == 'local':
        page = get_local_page_content(url_local)
    else:
        page = get_remote_page_content(url_remote)
    return page    
        
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
                
def get_trade_currency( other_currency, price_list ):
    # check if another_currency is present, default is CDN
    trade_currency = 'CDN'
    
    if any(other_currency in p for p in price_list):
        trade_currency = 'USD'
    return trade_currency

def get_num_value( in_str ):
    # obtain numeric value of passed in string
    # col[6].get_text()
    return re.sub('[^0-9^.]','', in_str.get_text(), flags=re.U)                

def get_pct_to_exercise_warrant(intrinsic_value, price_common):
    """ 
        calculate percentage a warrant needs to increase to be exercised
        input: intrinsic value of warrant, closing price of common stock
        usage: get_perc_to_exercise_warrant(x, y)
    """
    # if warrant's intrinsic value is 0 or less, then warrant can be exercised
    f = (lambda x,y: float(x)/float(y) if float(x) > 0 else 0)
    return f(intrinsic_value,price_common)


def extract_monthly_data(table= ''):
    """ 
        => better descriptor for function collate...?
        return input and calculated columns for a DataFrame 
    """
    company = []
    stock_close = []
    
    warrant_symbol = []
    warrant_exercise_price = []
    warrant_close = []
    
    leverage = []
    
    warrant_expiry_date = []
    years_2_expiry = []
    days_2_expiry = []
    
    w_intrinsic_value = []
    w_percent_to_exercise = []
    w_time_price_gain_factor = []
    
    currency = []
    
    prices = [] # hold cols that may contain US$ 
     
    for header in table.find_all('tr')[0:1]:
        # save name for eventual CSV file name
        col = header.find_all('td')
        
        global current_file_date 
        # assign to global variable
        current_file_date = get_num_value(col[0])
        ##print(current_file_date)    
        
        
    # for warrants data body, exclude first two table header rows and the very last, else None object appears
    for row in table.find_all('tr')[2:-1]:
        
        # clear superscript references
        remove_html_tags(row, ['sup'])
        
        # create a variable of all the <td> tag pairs in each <tr> tag pair,
        col = row.find_all('td')
        
        # col[0] in some rows only 1 character and missing full co. name...fill it in with previous string
        if len(col[0].string) == 1: 
            col[0].string.replace_with(previous_co_name)

        # only warrants with at least 4 years to expiry need to be included
        # =>>
        if int((col[12].string.strip().split(', ')[1]))> (datetime.datetime.now().year +0):
            
            
            # create a variable of the string inside 1st <td> tag pair,
            company.append(col[0].string) # company name
            
            stock_close.append(get_num_value(col[1]) or 0) # stock close 
            
            warrant_symbol.append(col[3].string) # symbol
                        
            warrant_exercise_price.append(get_num_value(col[5]) or 0) # exercise price
                            
            warrant_close.append(get_num_value(col[6]) or 0)                                            
            
            # stock warrant leverage
            sw_leverage = float(stock_close[-1])/float(warrant_close[-1])
            
            # return one decimal place
            leverage.append('{:.1f}'.format(sw_leverage)) 
            
            warrant_expiry_date.append(untangle_date(col[12].string))
            
            years_2_expiry.append(get_num_value(col[11])) # 
            
            days_2_expiry.append(get_days_to_expiry(warrant_expiry_date[-1]))
                                  
            intrinsic_val = float(warrant_exercise_price[-1]) - float(stock_close[-1])           
            w_intrinsic_value.append('{:.2f}'.format(intrinsic_val))
            
            pct_increase = get_pct_to_exercise_warrant(w_intrinsic_value[-1], stock_close[-1])
            w_percent_to_exercise.append('{:.2f}'.format(pct_increase))
           
            #w_time_price_gain_factor = [] '{:.2f}'.format(
            
            
            #ccheck whether US$ is present in following columns
            prices = [ col[1].string, col[5].string, col[6].get_text() ]            
            currency.append(get_trade_currency('US$', prices))
         
        previous_co_name = col[0].string
        
    columns = ({'01-company': company, '02-stk_close': stock_close, '03-symbol': warrant_symbol, '04-exercise_price': warrant_exercise_price,
               '05-wrt_close': warrant_close, '06-leverage': leverage, '07-yrs_to_expiry': years_2_expiry, '08-expiry_date': warrant_expiry_date, 
               '09-currency': currency, '10-days_to_expiry': days_2_expiry,'11-intrinsic_value': w_intrinsic_value, '12-%_to_go_to_exercise': w_percent_to_exercise})
    
    return columns
    
 
def main():
    """
        Main entry point for script
    """
    
    # play on a clean screen :) unless in tmux
    os.system('clear')    
    
    # 'local' by default, else 'remote' 
    datasource = 'local'   
    page = get_page(datasource)
    
    table = get_soup_table(page,"data")

    data_as_columns = extract_monthly_data(table)

    pd.set_option('display.width', pd.util.terminal.get_terminal_size()[0])
    
    df = pd.DataFrame(data_as_columns) 

    ##print(df)
    
    global current_file_date
    
    # save to CSV file
    df.to_csv('warrants_market_data_' + str(current_file_date) + '.csv', index=False)
    
    """
    print('file date : ' + current_file_date)
    print('{:*^30}'.format(' end '))
    print("Data from: " + datasource )
    print('{:*^30}'.format(' end '))
    """
        
if __name__ == '__main__':
    """report any processing error to the shell??
    """
    sys.exit(main())


 





















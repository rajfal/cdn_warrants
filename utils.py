#!/usr/bin/env python
#------------------CODE INFORMATION -----------------------------------#
"""
by: Rafal Jacyna
email: rafal@jacyna.net

purpose: functions to manipulate dates

refs:
#http://strftime.org/

"""
#------------------CODE INFORMATION -----------------------------------#

#----------------START IMPORT LIBRARIES -------------------------------#
from datetime import datetime
import time
import csv

#------------------END IMPORT LIBRARIES -------------------------------#



def untangle_date(date_mash):
    """
       format strings like, ' Jan. 2, 2022 ', 'Mar. 7, 2022'
       into '02/01/2022', '07/03/2022'
       usage: date_cleaner(' Jan. 2, 2022 ')
    """
    # remove outer whitespace, commas, periods
    cleaner_date = ''.join( c for c in date_mash.strip() if  c not in ',.' )
    
    date_elements = cleaner_date.split(' ')
    # turn Jan to 01 - some months like July, June are written out in full
    clean_month = datetime.strptime(date_elements[0][0:3],'%b').strftime('%m')
    # turn 1 to 01
    clean_day = datetime.strptime(date_elements[1],'%d').strftime('%d')
    # turn '2022' to 2022 - an integer
    clean_year = datetime.strptime(date_elements[2],'%Y').strftime('%Y')
    return clean_day + '/' + clean_month + '/' + clean_year 


def say_hello(somestring):
    
    return somestring

def get_days_to_expiry(warrant_expiry_date):
    """
       how many days from today to expiry?
       usage: get_days_to_expiry('02/02/2022')
    """   
    date_format = "%d/%m/%Y"
    a = datetime.strptime(warrant_expiry_date, date_format)
    today = time.strftime(date_format)
    b = datetime.strptime(today, date_format)
        
    return (a-b).days

def gen_alert_signal(warrant_symbol):
    """
       calculate a value that will indicate whether the warrant warrants further investigation
       any figure greater than 0.80 is a positive territory
       usage: gen_alert_signal('AEF.WT')
       note:  warrant symbol is unique
    """ 
    
    # define some key parameters
    # -------------------------------------------------------------
    # not to be changed without further system testing!
    _p_Leverage = 0.31
    _p_TimePriceGain = 0.47
    _p_WarrantPriceLevel = 0.22
    # -------------------------------------------------------------  
      
      
    date_format = "%d/%m/%Y"
    a = datetime.strptime(warrant_expiry_date, date_format)
    today = time.strftime(date_format)
    b = datetime.strptime(today, date_format)
        
    return alert_signal

def read_selection_csv():
    """
        usage: s = read_selection_csv() 
        note: inside python console use, [print(s[0][i]+'\n') for i in range(len(s[0]))]
        
        [print(s[i][2]+'\n') for i in range(len(s))] # print a list of warrant symbols
        
        │01-company                   
        │02-stk_close                 
        │03-symbol                    
        │04-exercise_price            
        │05-wrt_close                 
        │06-leverage                  
        │07-yrs_to_expiry             
        │08-expiry_date               
        │09-currency                  
        │10-days_to_expiry            
        │11-intrinsic_value           
        │12-%_til_exercise            
        │13-price_time_gain_factor 
        
        len(s) will give number of rows
        len(s[0]) will give number of columns
        print(str(len(s)) + ' rows by ' + str(len(s[0])) + ' columns')
        
        # print out all warrant symbols, ignore header
        [print(s[i][2]) for i in range(1,len(s))] 
        w = [s[i][2] for i in range(1,len(s))] # make list of warrant symbols
        
    """
    
    with open('warrants_filtered_selection.csv', 'rb') as f:
        reader = csv.reader(f)
        your_list = list(reader)

    return your_list

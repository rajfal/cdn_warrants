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



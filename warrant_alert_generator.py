#!/usr/bin/env python
#------------------CODE INFORMATION -----------------------------------#
"""
by: Rafal Jacyna
email: rafal@jacyna.net

purpose: to generate alert signals for warrants that show signs of 
         profitability

refs:


"""
#------------------CODE INFORMATION -----------------------------------#


#----------------START IMPORT LIBRARIES -------------------------------#
import sys

import os

import csv
#------------------END IMPORT LIBRARIES -------------------------------#

#------------------START CONSTANTS ------------------------------------#
# ---
#--------------------END CONSTANTS ------------------------------------#

#-----------START GLOBAL VARIABLES ------------------------------------#
# ---
#-------------END GLOBAL VARIABLES ------------------------------------#

def gen_alert():
    #def gen_alert_signal(warrant_symbol):
    """
       calculate a value that will indicate whether the warrant warrants further investigation
       any figure greater than 0.80 is a positive territory
       usage: gen_alert_signal('AEF.WT')
       note:  warrant symbol is unique
    """ 
   
    # ================================>> make this function available to Jupyter notebook to run calcs on each row of the DataFrame and 
    
    # define some key parameters
    # -------------------------------------------------------------
    # not to be changed without further system testing!
    _p_Leverage = 0.31
    _p_TimePriceGain = 0.47
    _p_WarrantPriceLevel = 0.22
    # -------------------------------------------------------------  
      
    s = read_selection_csv()
    
    for warrant in range(1, len(s)):
        
        print(s[warrant][2])
        #get_subsignal_leverage
        l = get_subsignal_leverage(s[warrant][5])
        #print(l)
        
        #get_subsignal_timepricegain
        g = get_subsignal_timepricegain(s[warrant][12])
        #print(g)
        
        #get_subsignal_warrantpricelevel
        p = get_subsignal_warrantpricelevel(s[warrant][4])
        #print(p)
        
        alert = '{:.2f}'.format((l*_p_Leverage + g*_p_TimePriceGain + p*_p_WarrantPriceLevel)) 
        
        print(alert)
         
    return 1
    
def get_subsignal_leverage(leverage):
    """ 
        assign rating to warrant's leverage 
        input: leverage
        usage: get_subsignal_leverage(s[warrant][5])
    """
    rating = rate_leverage(float(leverage))
    return rating    
    
def rate_leverage(n):
    # assign rating levels
    if n >= 4 : return 1
    elif n >= 3 : return 0.75
    elif n >= 2 : return 0.5
    else:
        return 0

def get_subsignal_timepricegain(timepricegain):
    """ 
        assign rating to warrant's timepricegain  
        input: timepricegain
        usage: get_subsignal_timepricegain(s[warrant][5])
    """
    rating = rate_timepricegain(float(timepricegain))
    return rating    
    
def rate_timepricegain(g):
    # note 1 = 100%
    # assign rating levels
    if g >= 5.5 : return 0
    elif g >= 2.5 : return 0.25
    elif g >= 1 : return 0.5
    else:
        return 1 - g

def get_subsignal_warrantpricelevel(price):
    """ 
        assign rating to warrant's price 
        input: price
        usage: get_subsignal_warrantpricelevel(s[warrant][4])
        
    """
    rating = rate_warrantprice(float(price))
    return rating    
    
def rate_warrantprice(p):
    # assign rating levels
    if p >= 5 : return 0
    elif p >= 2 : return 0.25
    elif p >= 1 : return 0.5
    else:
        return 1 - p



def read_selection_csv():
    """
        usage: s = read_selection_csv() 
        note: inside python console use, [print(s[0][i]+'\n') for i in range(len(s[0]))]
        
        [print(s[i][2]+'\n') for i in range(len(s))] # print a list of warrant symbols
        
        │0 - 01-company                   
        │1 - 02-stk_close                 
        │2 - 03-symbol                    
        │3 - 04-exercise_price            
        │4 - 05-wrt_close                 
        │5 - 06-leverage                  
        │6 - 07-yrs_to_expiry             
        │7 - 08-expiry_date               
        │8 - 09-currency                  
        │9 - 10-days_to_expiry            
        │10 - 11-intrinsic_value           
        │11 - 12-%_til_exercise            
        │12 - 13-price_time_gain_factor 
        
        len(s) will give number of rows
        len(s[0]) will give number of columns
        print(str(len(s)) + ' rows by ' + str(len(s[0])) + ' columns')
        
        # print out all warrant symbols, ignore header
        [print(s[i][2]) for i in range(1,len(s))] 
        w = [s[i][2] for i in range(1,len(s))] # make list of warrant symbols
        
    """
    
    with open('warrants_filtered_selection.csv', 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)

    return your_list

def main():
    """
        Main entry point for script
    """
    
    # play on a clean screen :) unless in tmux
    os.system('clear')    
    
    #global current_file_date
    
    gen_alert()
    
        
if __name__ == '__main__':
    """report any processing error to the shell??
    """
    sys.exit(main())

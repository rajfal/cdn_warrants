#!/usr/bin/env python
#------------------CODE INFORMATION -----------------------------------#
"""
by: Rafal Jacyna
email: rafal@jacyna.net

purpose: to determine avealeva warrant leverage
         is it more profitable to invest in commonn stock or 
         its stock warrant?

refs:
# http://www.scipy-lectures.org/intro/numpy/array_object.html
# https://chrisalbon.com/#Python
# http://treyhunner.com/2015/12/python-list-comprehensions-now-in-color/

"""
#------------------CODE INFORMATION -----------------------------------#


#----------------START IMPORT LIBRARIES -------------------------------#
import numpy as np

import sys

import os

#------------------END IMPORT LIBRARIES -------------------------------#

#------------------START CONSTANTS ------------------------------------#
# ---
#--------------------END CONSTANTS ------------------------------------#

#-----------START GLOBAL VARIABLES ------------------------------------#
# ---
#-------------END GLOBAL VARIABLES ------------------------------------#

def gen_avealeva(common_price, warrant_price, warrant_xrs_price):
    """
    # list setup:
    # a - price_target_defs
    # b - price_targets
    # c - common_profits
    # d - common_ROI
    # e - warrant_intrinsic_values
    # f - warrant_profits
    # g - warrant_ROI
    # h - leverage (warrants/commons)
    # 
    # purpose: to calculate aevaleva, average leverage of a warrant cf. common stock over a range of price targets
    #
    
    """

    # define a list of price targets
    a = [1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]

    # -> get price targets
    b = [a[price_target]*warrant_xrs_price for price_target in range(len(a))]
    #print(b)
    # -> get common stock profits
    c = [(b[price_target]-common_price) for price_target in range(len(b))]
    #print(c)
    # -> get common stock ROI
    d = [(c[price_target]/common_price) for price_target in range(len(c))]
    #print(d)
    # -> get warrant intrinsic values
    e = [(b[price_target] - warrant_xrs_price) for price_target in range(len(b))]
    #print(e)
    # -> get warrant profits
    f = [(e[price_target] - warrant_price) for price_target in range(len(e))]
    #print(f)
    # -> get warrant ROI
    g = [(f[price_target] / warrant_price) for price_target in range(len(f))]
    #print(g)
    # -> get ROI Leverage
    h = [(g[price_target] / d[price_target]) for price_target in range(len(g))]
    #print(h)
    # calcuate Average Leverage - AevaLeva
    avg_leverage = '{:.2f}'.format((sum(h) / len(h)))
    print('--->' + avg_leverage)
    return avg_leverage

def main(): 
    """
        Main entry point for script
        
    """
    
    # play on a clean screen :) unless in tmux
    os.system('clear')    
    
    # set up numbers for Acasta Enterprises Inc market instruments 
    # AEF.WT stock warrant
    #==============================================================
    warrant_symbol = 'AEF.WT'
    common_price = 8.88
    warrant_price = 1.20
    warrant_xrs_price = 11.50
    #==============================================================
    
    avg_leverage = gen_avealeva(common_price, warrant_price, warrant_xrs_price)
    
    print('Warrant symbol : ' + warrant_symbol)
    print('{:*^30}'.format(' end '))
    print("Warrant AevaLeva: " + '{:.2f}'.format(avg_leverage) )
    print('{:*^30}'.format(' end '))
    
        
if __name__ == '__main__':
    """report any processing error to the shell??
    """
    sys.exit(main())

#!/usr/bin/env python
#------------------CODE INFORMATION -----------------------------------#
"""
by: Rafal Jacyna
email: rafal@jacyna.net

purpose: to calculate Root Mean Square of values in a list

refs:
# http://simplestatistics.readthedocs.io/en/latest/#min
# https://en.wikipedia.org/wiki/Root_mean_square

#  simplestatistics.root_mean_square(x)[source]

    Root mean square (RMS) is the square root of the sum of the squares of values in a list divided by the length of the list. 
    It is a mean function that measures the magnitude of values in the list regardless of their sign.
    Parameters:	x – A list or tuple of numerical objects.
    Returns:	A float of the root mean square of the list.

"""
#------------------CODE INFORMATION -----------------------------------#


#----------------START IMPORT LIBRARIES -------------------------------#
import math

import sys

import os

#------------------END IMPORT LIBRARIES -------------------------------#

#------------------START CONSTANTS ------------------------------------#
# ---
#--------------------END CONSTANTS ------------------------------------#

#-----------START GLOBAL VARIABLES ------------------------------------#
# ---
#-------------END GLOBAL VARIABLES ------------------------------------#

def gen_rms(list_of_values = 0):
    """

    # 
    # purpose: to calculate root mean square of a list of values
    #
    
    """
    if list_of_values == 0:
        # list of test values
        a = [1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]
    else:
        a = list_of_values
    
        
    # -> square each value
    b = [a[each_value]**2 for each_value in range(len(a))]
    #print(b)
    # -> derive mean, sum all squared values and divide by their number
    c = (sum(b) / len(b))
    #print(c)
    # -> find square root
    d = math.sqrt(c)
    #print(d)
    
    # calcuate Average Leverage - AevaLeva
    rms = '{:.2f}'.format(d)
    #print('--->' + rms)
    #print(" ".join([str(x) for x in a] ))
    return rms

def main(): 
    """
        Main entry point for script
        
    """
    
    # play on a clean screen :) unless in tmux
    os.system('clear')    
    
    # set up 
    #==============================================================
    warrant_symbol = 'sample run'
    sample_values = [-1.0,1.0,-1.0,1.0]
    #==============================================================
    
    root_mean_square = gen_rms() # sample_values)
    
    #print('Warrant symbol : ' + warrant_symbol)
    print('{:*^30}'.format(' end '))
    print("Root Mean Square: " + str(root_mean_square) )
    print('{:*^30}'.format(' end '))
    
    
        
if __name__ == '__main__':
    """report any processing error to the shell??
    """
    sys.exit(main())

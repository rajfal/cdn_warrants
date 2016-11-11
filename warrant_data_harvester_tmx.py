from bs4 import BeautifulSoup
import pandas as pd
import urllib2
import csv
import sys
import os
import datetime


url = "http://web.tmxmoney.com/quote.php?qm_symbol=";
#url = "file:///home/ithilien/learning.python/warrants_NDM.WT.A.html";


def open_page(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'lxml')
    return soup


def extract_table_data():
    
    warrant="JDL.WT"
    my_soup = open_page(url + warrant)
    table = my_soup.find(class_="quote-price priceLarge")
    #skip first two table header rows and the very last, else None object appears
    for row in table.find_all('span'):
        print(row.string)

    print("-------------------------------------table data is out now");



def soup():
   """extract soup ingredients
   """
   #warrant="NDM.WT.A"
   #my_soup = open_page(url + warrant)
   my_soup = open_page(url)
   table = my_soup.find(class_="quote-price priceLarge")
   
   #print(my_soup.get_text());   
   #print(my_soup.prettify());
   return table


def main():
    """Main entry point for script
    """
    #pass
    os.system('clear') #play on a clean screen :)    
     
    #data_table = soup()
    #print(data_table);
    extract_table_data()



if __name__ == '__main__':
    """report any processing error to the shell??
    """
    sys.exit(main())


 




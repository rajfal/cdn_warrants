from bs4 import BeautifulSoup
import pandas as pd
import urllib2
import csv
import sys
import os
import datetime

#url = "http://www.financialpost.com/markets/data/group-warrants.html";
url = "file:///home/ithilien/learning.python/warrants_nov.html";

url_tmx = "http://web.tmxmoney.com/quote.php?qm_symbol=";



##https://www.crummy.com/software/BeautifulSoup/bs4/doc
##http://chrisalbon.com/python/beautiful_soup_scrape_table.html

def open_page(url):
    page = urllib2.urlopen(url)
    #soup = BeautifulSoup(page, 'html.parser')
    soup = BeautifulSoup(page, 'lxml')

    return soup


def get_daily_tmx_data(warrant_symbol):
    
    #warrant_symbol = "JDL.WT"
    print ("...fetching closing price for " + warrant_symbol)
    my_soup = open_page(url_tmx + warrant_symbol)
    table = my_soup.find(class_="quote-price priceLarge")
    #skip first two table header rows and the very last, else None object appears
    for row in table.find_all('span'):
        
        return(row.string)

    #print("-------------------------------------tmx price updated");



def extract_table_data():
    company = []
    stock_close = []
    warrant_symbol = []
    warrant_exercise_price = []
    warrant_close = []
    leverage = []
    years_left = []
    warrant_expiry_date = []
    
    my_soup = open_page(url)
    table = my_soup.find(class_="data")
    #skip first two table header rows and the very last, else None object appears
    for row in table.find_all('tr')[2:-1]:
 
        # Create a variable of all the <td> tag pairs in each <tr> tag pair,
        col = row.find_all('td')
        
        #col[0] in some rows only 1 character and missing full co. name...fill it in with previous string
        if len(col[0].string) == 1:
            col[0].string.replace_with(previous_co_name)

        #only warrants with at least 4 years to expiry need to be included
        if int((col[12].string.strip().split(', ')[1]))> (datetime.datetime.now().year +3):
            # Create a variable of the string inside 1st <td> tag pair,
            #x = col[0].string # company
            company.append(col[0].string)
            stock_close.append(col[1].string or 0) # stock close
            warrant_symbol.append(col[3].string) # symbol            
            warrant_exercise_price.append(col[5].string) # exercise price
            ##warrant_end_of_day_close = get_daily_tmx_data(col[3].string) 
            warrant_end_of_day_close = col[6].string # recent close                                               
            warrant_close.append(warrant_end_of_day_close) # recent close 
            stock_warrant_leverage = float(stock_close[-1])/float(warrant_close[-1])
            leverage.append(stock_warrant_leverage) # leverage
            ##leverage.append(col[10].string) # leverage
            years_left.append(col[11].string) # years left
            #x = col[12].string.strip().split(', ')[1] # expiry date - reports only the year part of the column, for filtering
            warrant_expiry_date.append(col[12].string) # expiry date
            #print(col[12].string)
        previous_co_name = col[0].string
        #print(previous_co_name)   
        #print(str(len(col[0].string)) + " " + col[0].string)

    columns = ({'company': company, 'stock_close': stock_close, 'warrant_symbol': warrant_symbol, 'warrant_exercise_price': warrant_exercise_price,
               'warrant_close': warrant_close, 'leverage': leverage, 'years_left': years_left, 'warrant_expiry_date': warrant_expiry_date}
              ) 
    df = pd.DataFrame(columns)  
    print(df);
    #df.head(20);
    print("-------------------------------------table data is out now");



def soup():
   """extract soup ingredients
   """
   #pass
   #print("I am in main");
   my_soup = open_page(url)
   table = my_soup.find(class_="data")
   
   #print(my_soup.get_text());   
   #print(my_soup.prettify());
   return table


def main():
    """Main entry point for script
    """
    #pass
    os.system('clear') #play on a clean screen :)    
    #print(soup());
    #print("web soup printed");
    #data_table = soup()
    #print(data_table);
    extract_table_data()



if __name__ == '__main__':
    """report any processing error to the shell??
    """
    sys.exit(main())


 




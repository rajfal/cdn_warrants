from bs4 import BeautifulSoup
import pandas as pd
import urllib2
import csv
import sys
import os
import datetime

url = "http://www.financialpost.com/markets/data/group-warrants.html";
#url = "file:///home/ithilien/learning.python/warrants_nov.html";


def open_page(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    return soup

def df_sample():
    """test for a DataFrame
    """
    
    #print("I am in main");

    raw_data = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'],
        'last_name': ['Miller', 'Jacobson', 'Ali', 'Milner', 'Cooze'],
        'age': [42, 52, 36, 24, 73],
        'preTestScore': [4, 24, 31, 2, 3],
        'postTestScore': [25, 94, 57, 62, 70]}

    #print(raw_data);

    # Create a dataframe
    raw_df = pd.DataFrame(raw_data, columns = ['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])

    # View a dataframe
    #raw_df
    return(raw_df.head(5));


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
            stock_close.append(col[1].string) # stock close
            warrant_symbol.append(col[3].string) # symbol
            warrant_exercise_price.append(col[5].string) # exercise price
            warrant_close.append(col[6].string) # recent close
            leverage.append(col[10].string) # leverage
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


 




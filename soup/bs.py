#Import libraries
from urllib import request
from bs4 import BeautifulSoup as BS
import re
import pandas as pd
import time
#Start measuring program execution time
start = time.time()

#List for column names and also  these are the names of the information, which i am scraping
columns=['Nazwa oferty','Cena','Data dodania','Lokalizacja','Marka','Model','Typ nadwozia','Rok','Kilometry','Skrzynia biegów']
#Create DataFrame to save information
df_result=pd.DataFrame(columns=columns)
cond=0
#Condition that when true only 100 pages are scraped
limit=True
#Main website from starting webscraping
main_url = 'https://www.gumtree.pl/s-samochody-osobowe/v1c9026p' 
#In this case there are 50 pages of car ads
for i in range(1,51):
    links=[]
    #Checking a condition - only 100 website can scraped
    if(cond==100 and limit==True):
        break
    else:
        #Scraping links to offers
        html = request.urlopen(main_url+str(i)) 
        cond=cond+1
        print(main_url+str(i))
        bs = BS(html.read(), 'html.parser')
        tags = bs.find_all('a', {'class':re.compile('href-link*')})
        links=['https://www.gumtree.pl'+tag['href'] for tag in tags]
        
        # For every link do scrap needed information
        for link in links:
            result=[]
            #Checking a condition - only 100 website can scraped
            if(cond==100 and limit==True):
                break
            else:
            #For unwanted situations we use try
                try:
                    new_html = request.urlopen(link)
                    cond=cond+1
                    bs = BS(new_html.read(), 'html.parser')
                    #Information about offer name and price
                    offer=bs.find('div',{'class':'vip-title clearfix'})
                    offer_name=offer.find('span',{'class':'myAdTitle'}).text
                    offer_value=offer.find('span',{'class':'value'}).text
                    #Add to list with values
                    result.append(offer_name)
                    result.append(offer_value)
                    #Details about offer
                    others = bs.find('ul', {'class':'selMenu'}).find_all('div',{'class':'attribute'})
                 
                    for col in columns[2:11]:
                        j=0
                        for other in others:
                            #Checking if the information is available 
                             if other.find('span',{'class':'name'}).text==col:
                                 result.append(other.find('span',{'class':'value'}).text)
                                 break
                             else:
                                 j=j+1
                        #If there is no information in others add None to result
                        if(j==len(others)):
                            result.append(None)
                    #Add list of result as row to dataframe                            
                    df_result=df_result.append(pd.DataFrame(data=[result],columns=columns))
                #If there is a problem with the link go to the next
                except:
                    continue
df_result=df_result.reset_index(drop=True)
print(df_result)
#Print a program execution time
print(" Program executed in %s seconds " % (time.time() - start))

#Import libraries
from selenium import webdriver
import time
import os
import pandas as pd
#Start measuring program execution time
start = time.time()
#List for column names and also  these are the names of the information, which i am scraping

columns=['Nazwa oferty','Cena','Data dodania','Lokalizacja','Marka','Model','Typ nadwozia','Rok','Kilometry','Skrzynia biegów']
#Create DataFrame to save information
df_result=pd.DataFrame(columns=columns)
#Set path to geckodriver. For me geckodriver is in the same folder as this script.
gecko_path = os.getcwd()+'\geckodriver'
#Change of option related to tracking what happens during program operation
options = webdriver.firefox.options.Options()
options.headless = True
driver = webdriver.Firefox(options = options, executable_path = gecko_path)

#Condition that when true only 100 pages are scraped
cond=0
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
        driver.get(main_url+str(i))
        cond=cond+1
        print(main_url+str(i))
        tags=driver.find_elements_by_class_name('href-link.tile-title-text')
        links=[tag.get_attribute('href') for tag in tags]
        
        # For every link do scrap needed information
        for link in links:
            #Checking a condition - only 100 website can scraped
            if(cond==100 and limit==True):
                break
            else:
                #For unwanted situations we use try
                try:
                    result=[]
                    driver.get(link)
                    cond=cond+1
                    #Information about offer name and price
                    offer_name=driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[3]/section/div/div[1]/div[3]/div[2]/div[2]/h1/span').text
                    offer_value=driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[3]/section/div/div[1]/div[3]/div[2]/div[2]/div/span').text
                    #Add to list with values
                    result.append(offer_name)    
                    result.append(offer_value)
                    #Details about offer 
                    others = driver.find_elements_by_class_name('attribute')
                   
                    for col in columns[2:11]:
                        j=0
                        for other in others:
                            #Checking if the information is available
                             if other.find_element_by_class_name('name').text==col:
                                 result.append(other.find_element_by_class_name('value').text)
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

# Close browser:
driver.quit()

df_result=df_result.reset_index(drop=True)
print(df_result)
#Print a program execution time
print(" Program executed in %s seconds " % (time.time() - start))                

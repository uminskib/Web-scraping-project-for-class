#!/usr/bin/env python
# coding: utf-8

# In[27]:


import scrapy
from scrapy import Selector
from urllib import request
import pandas as pd
import time
pd.set_option("display.max_rows",None)


# In[28]:


start=time.time()
#We create 2 list one for links of pages with ofers and second for specific ofers
url=[]
urls=[]
#List of links of pages with ofers
for i in range(1,51):
    url.append('https://www.gumtree.pl/s-samochody-osobowe/page-'+str(i)+'/v1c9026p'+str(i))
#List of links of specific ofers
for i in range(50):
    html=request.urlopen(url[i])
    sel= Selector(text=html.read(),type='html')
    xpath='//div[re:test(@class, "title")]//@href'
    urls=urls+sel.xpath(xpath).getall()
for i in range(len(urls)):
    urls[i]='https://www.gumtree.pl'+urls[i]
#Creating empty dataframe 
column_names=["Nazwa oferty","Cena","Data dodania oferty","Lokalizacja","Rok produkcji","Kilometry","Skrzynia biegów","Marka","Model","Nadwozie"]
Auta=pd.DataFrame(columns=column_names)
#We set xpath for data that we want to scrap
nazwa_xpath='//span[re:test(@class, "myAdTitle")]/text()'
cena_xpath='//span[re:test(@class, "amount")]/text()'
data_xpath='//span[text()="Data dodania"]/following-sibling::*/text()'
lokalizacja_xpath='//div[re:test(@class, "location")]/a/text()'
rok_xpath='//span[text()="Rok"]/following-sibling::*/text()'
kilometry_xpath='//span[text()="Kilometry"]/following-sibling::*/text()'
skrzynia_xpath='//span[text()="Skrzynia biegów"]/following-sibling::*/text()'
marka_xpath='//span[text()="Marka"]/following-sibling::*/span/text()'
model_xpath='//span[text()="Model"]/following-sibling::*/span/text()'
nadwozie_xpath='//span[text()="Typ nadwozia"]/following-sibling::*/text()'
#Seting limit for pages that we want to scrap
limit=True
iteration=0

for i in range(len(urls)):
    if(iteration==100 and limit==True):
        break
    else:
        iteration=iteration+1
        #Creating list where all informations about offer will be stored
        auto=[]
        urll=urls[i]
        html=request.urlopen(urll)
        sel=Selector(text=html.read(),type="html")
        #Download name of offer
        nazwa=sel.xpath(nazwa_xpath).getall()
        nazwa=''.join(nazwa)
        nazwa=nazwa.replace(u'\xa0',u'')
        auto.append(nazwa)
        #Download price of offer
        cena=sel.xpath(cena_xpath).get()
        try:
            cena=cena.replace(u'\xa0',u'')
        except AttributeError:
            cena=cena
        auto.append(cena)
        #Download date when the offer was issued
        data=sel.xpath(data_xpath).getall()
        data=''.join(data)
        auto.append(data)
        #Download localization
        lokalizacja=sel.xpath(lokalizacja_xpath).getall()
        lokalizacja=', '.join(lokalizacja)
        auto.append(lokalizacja)
        #Download year
        rok=sel.xpath(rok_xpath).getall()
        rok=''.join(rok)
        auto.append(rok)
        #Download kilometers
        kilometry=sel.xpath(kilometry_xpath).getall()
        kilometry=''.join(kilometry)
        auto.append(kilometry)
        #Download type of gearbox
        skrzynia=sel.xpath(skrzynia_xpath).getall()
        skrzynia=''.join(skrzynia)
        auto.append(skrzynia)
        #Download brand
        marka=sel.xpath(marka_xpath).getall()
        marka=''.join(marka)
        auto.append(marka)
        #Dwonload model
        model=sel.xpath(model_xpath).getall()
        model=''.join(model)
        auto.append(model)
        #Dwonload type of car body
        nadwozie=sel.xpath(nadwozie_xpath).getall()
        nadwozie=''.join(nadwozie)
        auto.append(nadwozie)
        #Add list to dataframe
        Auta.loc[len(Auta)]=auto
print(" Program executed in %s seconds " % (time.time() - start))


# In[101]:


#Export to CSV
Auta.to_csv('Auta_scrapy.csv')
Auta


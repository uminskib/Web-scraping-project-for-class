#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#Path to scraped data
Auta = pd.read_csv ('Auta_scrapy.csv')


# In[9]:


#We count how many cars are there with automatic and manual transmission 
count1=Auta['Skrzynia biegów'].value_counts()
#And visualize results
typy_skrzyń=["Manual 81","No data 10","Automatic 9"]
liczby=np.array(['81','10','9']).astype(np.float)
fig= plt.figure(figsize =(10, 7))
plt.pie(liczby,labels=typy_skrzyń)
plt.show()
#The number of cars produced in the given years
count2=Auta['Rok produkcji'].value_counts()
#And visualize results
liczby=[11,8,8,6,6,5,5,5,4,4,4,4,3,3,3,3,3,3,2,2,2,1,1,1,1,1,1]
lata=['2006 11','2005 8','2004 8','Brak danych 6', '2007 6','2008 5','2010 5','2002 5','2012 4','2001 4','2003 4','2000 4','2015 3','2013 3','2011 3','2018 3','2009 3','2016 3','1999 2','2014 2','1998 2','1995 1','2019 1','1990 1','1994 1','2017 1','1997 1']
fig= plt.figure(figsize =(10, 7))
plt.pie(liczby,labels=lata)
plt.show()
#Brands of cars put up for sale and number of offers
count3=Auta['Marka'].value_counts()
#Type of cars put up for sale and number of offers
count4=Auta['Nadwozie'].value_counts()
#And visualize results
liczby=[54,28,6,5,3,3,1]
nadwozie=['Unspecified type of car 54', 'Hatchbeck 28','Sedan 6', 'Wagon 5', 'Minivan 3', 'Coupe 3', 'Open roof 1']
fig= plt.figure(figsize =(10, 7))
plt.pie(liczby,labels=nadwozie)
plt.show()
#We change type of price data
Auta['Cena']=Auta['Cena'].str.replace('zł','')
Auta['Cena']=Auta['Cena'].astype(int)
#Price histogram
Auta['Cena'].plot.hist(stacked=True, bins=30)
#We summarize price 
print(Auta["Cena"].describe())
#We change type of kilometers data
Auta['Kilometry']=Auta['Kilometry'].replace(r'^\s*$', np.nan, regex=True)
Auta['Kilometry']=Auta['Kilometry'].astype('float64')
#Kilomiters histogram
Auta['Kilometry'].plot.hist(stacked=True, bins=30)
#We summarize kilomiters 
print(Auta['Kilometry'].describe())


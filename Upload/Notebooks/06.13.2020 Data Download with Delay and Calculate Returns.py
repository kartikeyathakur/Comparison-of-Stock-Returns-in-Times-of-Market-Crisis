#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  05 19:23:06 2020

@author: KartikeyaThakur
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import Workbook
import time
from datetime import datetime
import os

#Dot Com Bubble January 1 2000 to March 31 2003
#Housing Crisis July 1 2007 to March 31 2009
#Coronavirus February 15 2020 to Present

datePerformed = str(datetime.now()).replace('-','.')[:10]
#creates necessary folders
homeDir = str(os.getcwd()).split('\\Notebook')[0]
print(homeDir)
if not os.path.exists(homeDir + '\Data\Stock Data'):
    os.makedirs(homeDir + '\Data\Stock Data')
if not os.path.exists(homeDir + '\\Data\\Stock Data\\' + datePerformed):
    os.makedirs(homeDir + '\\Data\\Stock Data\\' + datePerformed)
if not os.path.exists(homeDir + '\\Output'):
    os.makedirs(homeDir + '\\Output')
if not os.path.exists(homeDir + '\\Output\\' + datePerformed):
    os.makedirs(homeDir + '\\Output\\' + datePerformed)
    
def getPriceData(stock, p):
    if stock.history(period=p).empty:
        data = pd.DataFrame({'Date' : [], 'Open' : [], 'High' : [], 'Low' : [], 'Close' : [], 'Volume' : [], 'Dividends' : [], 'Stock Splits' : []})
        data = data.set_index('Date')
        return data 
    else:
        return stock.history(period=p)

# show actions (dividends, splits)
def getCompanyActions(stock):
    if stock.actions.empty:
        actionData = pd.DataFrame({'Date' : [], 'Dividends' : [], 'Stock Splits' : []})
        actionData = actionData.set_index('Date')
        return actionData
    else:
        return stock.actions

def plotPriceChart(data):
    data['Close'].plot(figsize=(16, 9))

def saveStockData(symbol, data, actionData):
    path = homeDir + "/Data/Stock Data/" + datePerformed + "/" + symbol + ".xlsx"
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    workbook=writer.book
    worksheet=workbook.add_worksheet('Prices')
    writer.sheets['Prices'] = worksheet
    data.to_excel(writer,sheet_name='Prices',startrow=0 , startcol=0)
    worksheet=workbook.add_worksheet('Actions')
    writer.sheets['Actions'] = worksheet
    actionData.to_excel(writer,sheet_name='Actions',startrow=0 , startcol=0)
    writer.save()
    writer.close()

def loadPriceData(symbol):
    if symbol in files:
        data = pd.read_excel(homeDir + "/Data/Stock Data/" + datePerformed + "/" + symbol + ".xlsx", sheet_name='Prices', header=0)
        data = data.set_index('Date')
        data = data.dropna()
    else:
        data = pd.DataFrame({'Date' : [], 'Open' : [], 'High' : [], 'Low' : [], 'Close' : [], 'Volume' : [], 'Dividends' : [], 'Stock Splits' : []})
        data = data.set_index('Date')
    return data
    
#Collections
returns = "Symbol~Security~CoronaVirus~HousingCrisis~HousingCrisisRecovery15M~HousingCrisisRecovery2Y~DotComBubble~DotComBubbleRecovery15M~DotComBubbleRecovery2Y~Signal\n"
#stocks that are now at 2/3 of their pre-Coronavirus values
coronaTwoThree = []
#stocks that are now at 4/5 of their pre-Coronavirus values
coronaFourFive = []
#stocks that are now at 1/2 of their pre-Coronavirus values
coronaHalf = []
#stocks that are now at 1/3 of their pre-Coronavirus values
coronaThird = []
#stocks that are now at 1/4 of their pre-Coronavirus values
coronaFourth = []
#stocks that are now at 1/5 of their pre-Coronavirus values
coronaFifth = []
#stocks that are now at 1/10 of their pre-Coronavirus values
coronaTenth = []

path = homeDir + "/Data/Stock Data/" + datePerformed + "/"

files = []
for r, d, f in os.walk(path):
    for file in f:
        if '.xlsx' in file:
            files.append(str(os.path.join(r, file)).replace('.xlsx', '').replace(path,''))
            
#to indicate if you want to evaluate all the stocks or SNP or Russell or Dow or NYSE or Nasdaq or AMEX
#Leave as is for all stocks or provide a valid value from ['Russell', 'NYSE', 'Nasdaq', 'AMEX', 'SNP', 'Dow']
index = ""
if index in ['Russell', 'NYSE', 'Nasdaq', 'AMEX', 'SNP', 'Dow']:
    index  = index + " "
else:
    index  = ""
    
tickers = pd.read_excel(homeDir + "/Data/Symbol List/06.13.2020 " + index + "Symbol List.xlsx")

for i in tickers.index.values:
    symbol = tickers['Symbol'][i]
    security = tickers['Description'][i]
    if symbol not in files:
        stock = yf.Ticker(symbol)    
        
        data = getPriceData(stock, "max")
        data = data.dropna()
        if data.empty:
            print('No data found for: ' + symbol)
        else:
            actionData = getCompanyActions(stock)
            actionData = actionData.dropna()
            saveStockData(symbol, data, actionData)
            
        time.sleep(2.5)
    else:
        data = loadPriceData(symbol)
        
    if data.empty:
            print('No data found for: ' + symbol)
    else:
        #returns
        #change in Price since February 15 2020
        coronaVirusReturn = 0
        #change in Price during the Housing Crisis
        housingCrisisReturn = 0
        #change in Price during the DotCom bubble
        dotcomBubbleReturn = 0
        #change in Price 15 months after the Housing Crisis
        housingCrisisRecovery = 0
        #change in Price 15 months After the DotCom Bubble
        dotcomBubbleRecovery = 0
        #change in Price 2 years after the Housing Crisis
        housingCrisisRecovery2y = 0
        #change in Price 2 years after the DotCom Bubble 
        dotcomBubbleRecovery2y = 0

        #calculate returns
        coronaVirus = data[data.index>'2020-2-15']
        if len(coronaVirus) > 0:
            coronaVirusReturn = (coronaVirus['Close'][coronaVirus.index.values[-1]]-coronaVirus['Close'][0])/coronaVirus['Close'][0]
        housingCrisis = data[(data.index>'2007-7-1') & (data.index<='2009-3-31')]
        if len(housingCrisis) > 0:
            housingCrisisReturn = (housingCrisis['Close'][housingCrisis.index.values[-1]]-housingCrisis['Close'][0])/housingCrisis['Close'][0]
        dotcomBubble = data[(data.index>='2000-1-1') & (data.index<='2003-3-31')]
        if len(dotcomBubble) > 0:
            dotcomBubbleReturn = (dotcomBubble['Close'][dotcomBubble.index.values[-1]]-dotcomBubble['Close'][0])/dotcomBubble['Close'][0]
        housingCrisis = data[(data.index>'2009-3-31') & (data.index<='2010-6-30')]
        if len(housingCrisis) > 0:
            housingCrisisRecovery = (housingCrisis['Close'][housingCrisis.index.values[-1]]-housingCrisis['Close'][0])/housingCrisis['Close'][0]
        dotcomBubble = data[(data.index>='2003-3-31') & (data.index<='2004-6-30')]
        if len(dotcomBubble) > 0:
            dotcomBubbleRecovery = (dotcomBubble['Close'][dotcomBubble.index.values[-1]]-dotcomBubble['Close'][0])/dotcomBubble['Close'][0]
        housingCrisis = data[(data.index>'2009-3-31') & (data.index<='2011-3-31')]
        if len(housingCrisis) > 0:
            housingCrisisRecovery2y = (housingCrisis['Close'][housingCrisis.index.values[-1]]-housingCrisis['Close'][0])/housingCrisis['Close'][0]
        dotcomBubble = data[(data.index>='2003-3-31') & (data.index<='2005-3-31')]
        if len(dotcomBubble) > 0:
            dotcomBubbleRecovery2y = (dotcomBubble['Close'][dotcomBubble.index.values[-1]]-dotcomBubble['Close'][0])/dotcomBubble['Close'][0]
        
        #Signal to buy or sell calculated using a 125 day moving average and a 28 day moving average
        #buy if short term moving average is higher than the long term moving average, sell if lower
        if len(data)>=125:
            if data['Close'][-125:].mean() > data['Close'][-28:].mean():
                signal = 'Sell'
            elif data['Close'][-125:].mean() < data['Close'][-28:].mean():
                signal = 'Buy'
            else:
                signal = 'Neutral'
        else:
            signal = ''
        
        returns = returns + symbol + "~" + security + "~" + str(coronaVirusReturn) + "~" + str(housingCrisisReturn) + "~" + str(housingCrisisRecovery) + "~" + str(housingCrisisRecovery2y) + "~" + str(dotcomBubbleReturn) + "~" + str(dotcomBubbleRecovery) + "~" + str(dotcomBubbleRecovery2y) + "~" + str(signal) + "\n"

        if len(coronaVirus) > 0:
            if coronaVirus['Close'][coronaVirus.index.values[-1]]/coronaVirus['Close'][0] <= 0.8:
                coronaFourFive.append(symbol)
            if coronaVirus['Close'][coronaVirus.index.values[-1]]/coronaVirus['Close'][0] <= 0.66:
                coronaTwoThree.append(symbol)
            if coronaVirus['Close'][coronaVirus.index.values[-1]]/coronaVirus['Close'][0] <= 0.5:
                coronaHalf.append(symbol)
            if coronaVirus['Close'][coronaVirus.index.values[-1]]/coronaVirus['Close'][0] <= 0.33:
                coronaThird.append(symbol)
            if coronaVirus['Close'][coronaVirus.index.values[-1]]/coronaVirus['Close'][0] <= 0.25:
                coronaFourth.append(symbol)
            if coronaVirus['Close'][coronaVirus.index.values[-1]]/coronaVirus['Close'][0] <= 0.2:
                coronaFifth.append(symbol)
            if coronaVirus['Close'][coronaVirus.index.values[-1]]/coronaVirus['Close'][0] <= 0.1:
                coronaTenth.append(symbol)
        
f = open(homeDir + "Output/" + datePerformed + "/Returns " + index + " " + str(datetime.now()).replace(':','-')[:19] + ".csv", 'w+')
f.write(returns)
f.close()

f = open(homeDir + "/Output/" + datePerformed + "/Returns " + index + " " + str(datetime.now()).replace(':','-')[:19] + ".txt", 'w+')
f.write("Four Fifths: " + str(coronaFourFive) + '\n')
f.write("Two Thirds: " + str(coronaTwoThree) + '\n')
f.write("Half: " + str(coronaHalf) + '\n')
f.write("Third: " + str(coronaThird) + '\n')
f.write("Fourth: " + str(coronaFourth) + '\n')
f.write("Fifth: " + str(coronaFifth) + '\n')
f.write("Tenth: " + str(coronaTenth) + '\n')
f.close()

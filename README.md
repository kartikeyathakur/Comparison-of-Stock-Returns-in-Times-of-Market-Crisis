# Comparison-of-Stock-Returns-in-Times-of-Market-Crisis
In short, the Python program downloads all the stock data for all the stocks listed on Nasdaq, NYSE and AMEX from Yahoo Finance using the yFinance module and then looks at the changes in prices during and after the DotCom Bubble, the Housing Crisis and the current Coronavirus pandemic. This can help you download stock data for all the stocks on the Russell, Dow, SNP any any other indices.

I got the list of stocks from the Nasdaq website. Then ran a loop to download all the data available for each ticker symbol from Yahoo Finance. Then I calculated reurns for each stocks during and after the three most recent market crises. I set up the periods for and after these crises by looking at the movement of the SNP 500. For the Dot Com Bubble - January 1 2000 to March 31 2003, for the Housing Crisis July 1 2007 to March 31 2009 and for the Coronavirus pandemic February 15 2020 to Present.

You can use either the iPython notebook or the .py file provided. They both do the same job. The script will create necessary folders and already contains all the information it needs to run such as tickers for the stocks. Please do not change the folder structure to ensure that the program runs as is.

Periods of analysis and the crises can be changed as needed. 

I included a buy and sell signal based on moving averages. If the short term (28 day) moving average was higher than the long term (125 day) moving average a buy signal is saved whereas a sell signal is saved in the opposite scenario. The periods of evaluation of these moving averages can also be changed in the programs.

The programs downloads stock data for more than 8,000 stocks listed in the United States, so it may take a while hours even. Please be patient. Sometimes your IP may get busted for making too many requests despite the delay I have included in the program or for some other reason program may error out. In that case, it can be re-run and it is programed to skip over the stocks for thich the data has already been downloaded. Alternativeyly, you can provide an index value in the "tickers" dataframe to skip over the files already downloaded but this will also skip over calculating the returns for the skipped tickers. So the best option is to re-run the file.

Other possible uses of the script include:
  Download all histrorical stock prices for NYSE stocks
  Download all histrorical stock prices for Nasdaq stocks
  Download all histrorical stock prices for AMEX stocks
  Download all histrorical stock prices for SNP500 stocks
  Download all histrorical stock prices for Dow stocks
  Download all histrorical stock prices for Russell 2000 stocks

I have included files containing the list of tickers for these groups. Merely changing the value of the "index" variable will change the list of stocks to be evaluated. The program makes sure that a valid index value is set.


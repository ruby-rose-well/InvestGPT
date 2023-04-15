import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

def get_portfolio(reit_keys):
    """
    Calculate the optimal portfolio given a list of REIT keys
    :param reit_keys: a list of REIT keys
    :return: a list of weights (matching the order of reit_keys)
    """
    first = yf.Ticker(reit_keys[0])
    portfolio = first.history(start="2021-01-01", end="2021-04-02", interval="1d")
    portfolio = portfolio.drop(portfolio.columns[0:], axis=1)
    for asset in reit_keys:
        temp = yf.Ticker(asset)
        temp_historical = temp.history(start="2021-01-01", end="2021-04-02", interval="1d")
        close = temp_historical['Close']
        portfolio[asset] = close
    returns = portfolio/portfolio.shift(1)
    logReturns = np.log(returns)
    
    #number of portfolios
    
    noOfPortfolios = 10000
    weight = np.zeros((noOfPortfolios,len(reit_keys)))
    expectedReturn = np.zeros((noOfPortfolios))
    expectedVolatility = np.zeros((noOfPortfolios))
    sharpeRatio = np.zeros((noOfPortfolios))
    meanLogRet = logReturns.mean()
    Sigma = logReturns.cov()
    
    # get expectedReturn
    
    for k in range(noOfPortfolios):
        w = np.array(np.random.random(len(reit_keys)))
        w = w/np.sum(w)
        weight[k,:] = w
        expectedReturn[k] = np.sum(meanLogRet* w)
        expectedVolatility[k] = np.sqrt(np.dot(w.T, np.dot(Sigma,w)))
        sharpeRatio[k] = expectedReturn[k]/expectedVolatility[k]
    maxIndex = sharpeRatio.argmax()

    return weight[maxIndex,:]
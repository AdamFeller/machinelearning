# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 11:54:47 2016

@author: fella
"""

import connection
#import pyodbc
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np
from operator import itemgetter
import matplotlib
from scipy.stats.stats import pearsonr 
import collections
import seaborn as sns
matplotlib.style.use('ggplot')

#-------------------------------------------------
#Queery

connection_str =    """
Driver={SQL Server Native Client 11.0};
Server=BDPRADA;
Database=ADA_MB;
Trusted_Connection=yes;
"""

table   = ['[ZAP_Beta].[fella].[SP500GICS_sp500_bloomberg_gicsl1l2_tr_d]']

query =   """ select * from %s """


#-------------------------------------------------
#Extract

i = 0
while i < len(table):

    utility = connection.UtilitiesDatabase(connection_str,query, table[i])

    all_data  = utility.extract_results_db()

    data_work = all_data["data"]
    description = all_data["description"]

    columns = map(itemgetter(0), description)   ## build a list with name of columns

    df = pd.DataFrame.from_records(data_work, columns = columns)
    
#    try:
#        globals()['df{}'.format(i)] = df.set_index(['datadate']).sort_index()
#        
#    except:
    globals()['df{}'.format(i)] = df
    
    i += 1
    
#-------------------------------------------------
#Extract
    
SPX = df0[df0.ticker == 'SPX Index'].sort('datadate').values
     
TR_USD = np.array(SPX[:,[0,6]])

toWhat=3000
i=1

patternAr = np.zeros(shape=((toWhat-30-30-1),30))
dataAr = pd.DataFrame(np.zeros(((toWhat-30-30-1),6)),
                      columns = ['Date', 'Avg(Diff)', 'E(r)5', 'E(r)6-15', 'E(r)6-20', 'Pattern'])

while i<(toWhat-30-30-1):
    patternAr[i-1] = TR_USD[i:30+i,1]
    dataAr.iloc[i-1,0] = TR_USD[i:30+i,0][-1]
    dataAr.iloc[i-1,1] = np.sum(abs(TR_USD[i:30+i,1]-TR_USD[toWhat-30:toWhat,1]))/30
    dataAr.iloc[i-1,2] = np.sum(TR_USD[i+30:i+35,1])/5
    dataAr.iloc[i-1,3] = np.sum(TR_USD[i+35:i+45,1])/10
    dataAr.iloc[i-1,4] = np.sum(TR_USD[i+35:i+50,1])/15
    dataAr.iloc[i-1,5] = TR_USD[i:30+i,1]
    
    i += 1
    
dataAr.sort('Avg(Diff)')

dataAr[ dataAr.Date == '1993-12-29 00:00:00', :] 

patternAr 

dataAr.assign(TR_USD[i:30+i,1])
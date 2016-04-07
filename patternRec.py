# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 21:54:03 2016

@author: adam
"""

import pandas as pd
import numpy as np
from datetime import datetime
import scipy.sparse as sparse
import matplotlib.pyplot as plt


parse = lambda x: datetime.strptime(x, '%d/%m/%Y')

df = pd.read_csv(r'/home/adam/Dropbox/Machine Learning/SP500GICSlv1lv2.csv', parse_dates =['datadate'] , date_parser=parse)


SPX = df[df.ticker == 'SPX Index'].sort('datadate').values
     
TR_USD = np.array(SPX[:,[0,6]])

toWhat=6640
i=1

patternAr = np.zeros(shape=((toWhat-30-30-1),30))
dataAr = pd.DataFrame(np.zeros(((toWhat-30-30-1),5)),
                      columns = ['Date', 'Avg(Diff)', 'E(r)5', 'E(r)6-15', 'E(r)6-20'])


curPattern=np.cumprod(TR_USD[toWhat-30:toWhat,1]+1)

while i<(toWhat-30-30-1):
    patternAr[i-1] = np.cumprod(TR_USD[i:30+i,1]+1)
    dataAr.iloc[i-1,0] = TR_USD[i:30+i,0][-1]
    dataAr.iloc[i-1,1] = np.sum(abs(TR_USD[i:30+i,1]-TR_USD[toWhat-30:toWhat,1]))/30
    dataAr.iloc[i-1,2] = np.sum(TR_USD[i+30:i+35,1])/5
    dataAr.iloc[i-1,3] = np.sum(TR_USD[i+35:i+45,1])/10
    dataAr.iloc[i-1,4] = np.sum(TR_USD[i+35:i+50,1])/15
    
    i += 1
    


arr=sparse.coo_matrix(patternAr)
dataAr['patternAr'] = arr.toarray().tolist()

dataAr.sort('Avg(Diff)').head()

plt.plot(dataAr.patternAr[3750],'r')
plt.plot(dataAr.patternAr[6478],'b')
plt.plot(dataAr.patternAr[5378],'g')
plt.plot(dataAr.patternAr[4238],'p')
plt.plot(curPattern)

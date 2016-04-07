# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 14:01:43 2016

@author: adam
"""

"""Softmax."""

scores = np.multiply([3.0, 1.0, 0.2],10)


import numpy as np

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    return np.exp(x)/np.sum(np.exp(x),axis =0)
   

print(softmax(scores*10))

# Plot softmax curves
import matplotlib.pyplot as plt
x = np.arange(-2.0, 6.0, 0.1)
scores = np.vstack([x, np.ones_like(x), 0.2 * np.ones_like(x)])

#a=scores[0][0]
#b=scores[1][0]
#c=scores[2][0]
#
#d=np.exp(a)/(np.exp(a)+np.exp(b)+np.exp(c))
#e=np.exp(b)/(np.exp(a)+np.exp(b)+np.exp(c))
#f=np.exp(c)/(np.exp(a)+np.exp(b)+np.exp(c))
#
#d+e+f

plt.plot(x, softmax(scores/10).T, linewidth=2)
plt.show()
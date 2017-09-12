# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 16:02:01 2017

@author: Frank
"""
text = "As a child, I kept thinking and dreaming how I could fly.\
        Now I am not young, but stilling dreaming about flying.\
        Some people say I should be realistic.\
        I also sometimes have to learn how to come along with the mass.\
        However, pursuit of the great doesn't stop.\
        I have been kept thinking for it.\
        I am not sure how it will end.\
        It is my destiny."

from gensim.summarization import summarize
from gensim.summarization import keywords
           
print ('Summary:')
print (summarize(text, ratio=0.5))

print ('Keywords:')
print (keywords(text, ratio=0.3))

# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 00:48:43 2017

@author: Frank

usage:
    use pretrained
    https://textblob.readthedocs.io/en/dev/quickstart.html#translation-and-language-detection
    make your own
    https://textblob.readthedocs.io/en/dev/classifiers.html#classifiers

"""

from textblob import TextBlob

#create a TextBlob
wiki = TextBlob("Python is a high-level, general-purpose programming language.")

#part of speech tagging
print(wiki.tags)

#Noun Phrase Extraction
print(wiki.noun_phrases)

#Sentiment Analysis
testimonial = TextBlob("Textblob is amazingly simple to use. What great fun!")
print(testimonial.sentiment)
print(testimonial.sentiment.polarity)

#Tokenization
zen = TextBlob("Beautiful is better than ugly. "
              "Explicit is better than implicit. "
              "Simple is better than complex.")

'''
zen = TextBlob("见到你很高兴."
               "我爱你."
               "怎得不可思议.")
'''
print(zen.words)
print(zen.sentences)
for sentence in zen.sentences:
    print(sentence.sentiment)
    
#Words Inflection and Lemmatization
sentence = TextBlob('Use 4 spaces per indentation level.')
print(sentence.words)
print(sentence.words[2].singularize())
print(sentence.words[-1].pluralize())

from textblob import Word
w = Word("octopi")
print(w.lemmatize())
w = Word("went")
print(w.lemmatize())

from textblob.wordnet import VERB

word = Word("octopus")
print(word.synsets)
print(word.definitions)

from textblob.wordnet import Synset

octopus = Synset('octopus.n.02')
shrimp = Synset('shrimp.n.03')
print(octopus.path_similarity(shrimp))

#WordLists
animals = TextBlob("cat dog octopus")
print(animals.words)
print(animals.words.pluralize())

#Spelling Correction
b = TextBlob("I havv goood speling!")
print(b.correct())
w = Word('falibility')
print(w.spellcheck())

#Get Word and Noun Phrase Frequencies
monty = TextBlob("We are no longer the Knights who say Ni. "
                 "We are now the Knights who say Ekki ekki ekki PTANG.")
print(monty.word_counts['ekki'])
print(monty.words.count('ekki', case_sensitive=True))
print(wiki.noun_phrases.count('python'))

#Translation and Language Detection
en_blob = TextBlob(u'Simple is better than complex.')
print(en_blob.translate(to='es'))
chinese_blob = TextBlob(u"美丽优于丑陋")
print(chinese_blob.translate(from_lang="zh-CN", to='en'))
chinese_blob = TextBlob(u"我爱你")
print(chinese_blob.translate(from_lang="zh-CN", to='en'))
b = TextBlob(u"بسيط هو أفضل من مجمع")
print(b.detect_language())

#Parsing
b = TextBlob("And now for something completely different.")
print(b.parse())

#TextBlobs Are Like Python Strings!
print(zen[0:19])
print(zen.upper())
print(zen.find("Simple"))
apple_blob = TextBlob('apples')
banana_blob = TextBlob('bananas')
print(apple_blob < banana_blob)
print(apple_blob == 'apples')
print(apple_blob + ' and ' + banana_blob)
print("{0} and {1}".format(apple_blob, banana_blob))

#n-grams
blob = TextBlob("Now is better than never.")
print(blob.ngrams(n=3))

#Get Start and End Indices of Sentences
for s in zen.sentences:
    print(s)
    print("---- Starts at index {}, Ends at index {}".format(s.start, s.end))

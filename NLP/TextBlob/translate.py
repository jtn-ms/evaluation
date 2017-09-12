# -*- coding: utf-8 -*-
"""

Created on Thu Sep  7 03:35:46 2017

@author: Frank

Based on Textblob

Based on google translate

Warning: you should check first if you could access to google.com.
    
"""

from textblob import TextBlob

from argparse import ArgumentParser

from gooey import Gooey


@Gooey(language='chinese')
def main():
    parser  = ArgumentParser(description='机器翻译.')
    parser.add_argument("-s", "--src", default= '我爱你。 你是我的最靠谱的朋友。', help="")
    args = parser.parse_args()
    if vars(args).get('help'):
        exit(0)  
    en_blob = TextBlob(args.src)
    print(en_blob.translate(to='en'))
       
if __name__ == '__main__':
    main()
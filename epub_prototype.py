# Author: Dylan Ruggeroli
# Date:	  5 / 9 / 2016
# Description:
#   Prototype for implementing speech recognition to track a reader's audiobook
#   progress in order to find their location within an epub version
import sys
from decimal import *



class Book:
    phrase = ''

    def __init__(self, d, num_pages):
        self.data  = d
        self.pages = num_pages
        self.book_length = len(d) 

	# Return the index of the current phrase
    def lookup(self):
        return self.data.index(self.phrase)
		
    def set_phrase(self, s):
        self.phrase = s
        self.phrase_index = self.data.index(s)

	# Get the index of the provided string and calculate progress
    def progress(self, s):
        getcontext().prec = 6
        print ("phrase index", self.phrase_index)
        print ("book length", self.book_length)
        i = Decimal(self.phrase_index)
        l = Decimal(self.book_length)
        p = Decimal(self.pages)
        return (i / l) * p

	# Log state information
    def log(self):
        print("Phrase", self.phrase)
        print("Index ", self.phrase_index) 
        print("Length", self.book_length)        

if __name__ == '__main__':
	# Instantiate book object and search for sample phrase
    p = sys.argv[1]
    s = sys.argv[2]

    ebook = Book(open('wot_sample.txt').read(), p)
    ebook.set_phrase(s)
    ebook.log()

    print ebook.progress(s)
    print ebook.pages
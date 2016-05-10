# Author: Dylan Ruggeroli
# Date:	  5 / 9 / 2016
# Description:
#   Prototype for implementing speech recognition to track a reader's audiobook
#   progress in order to find their location within an epub version


class Book:
    phrase   = ''

    def __init__(self, d):
        self.data   = d
        self.length = len(d) 

	# Return the index of the current phrase
	def lookup(self):
		return self.data.index(self.phrase)
		
	# Get the index of the provided string and calculate progress
    def progress(self, s):
        i = self.data.index(s)
        progress = i / self.length 

        return progress

	# Log state information
    def log(self):
        print("Phrase", self.phrase)
        print("Index ", self.data.index(self.phrase)) 
        print("Length", self.length)        

if __name__ == '__main__':
	# Hypothetical page count for testing purposes only
    PAGES = 1000

	# Instantiate book object and search for sample phrase
    ebook = Book(open('wot_sample.txt').read())
    ebook.phrase = 'three veiled men in tattered coats'
    ebook.log()

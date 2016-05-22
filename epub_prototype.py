# Author: Dylan Ruggeroli
# Date:	  5 / 9 / 2016
# Description:
#   Book class that uses a readers epub progress to try and predict
#   current page number within a printed version. 

import sys
import numpy as np
from decimal import *

class Book:
    # String data and mp3 metadata for the book
    __text  = ''
    __audio = []

    def __init__(self, d, num_pages):
        self.__text   = d
        self.text_len = len(d) 
        self.pages    = int(num_pages)

    def lookup(self, s):
        """
            Return the index of the given substring, if it exists
        """
        try:
            index = self.__text.index(s)
        except ValueError as e:
            print "ERROR:  ValueError {}".format(e)
            return 0

        return index

    def progress(self, s):
        """ 
            Find a string of text within the book and use it predict a potential
            page number within a physical version
        """
        try:
            index = self.__text.index(s)
        except ValueError as e:
            print "ERROR:  ValueError {}".format(e)
            return 0      

        getcontext().prec = 6
        index  = Decimal(index)
        length = Decimal(self.text_len)
        pages  = Decimal(self.pages)

        return (index / length) * pages

    # Trim the indrouctory pages 
    def WOT_trim(self):
        """
            Trim intro and outro specific to the Wheel of Time series
        """
		# Trim text before page one (prior to Prologue)
        prologue = "PROLOGUE"
        beg_index = self.__text.index(prologue)

        tmp = self.__text[beg_index+1:]
        beg_index += tmp.index(prologue)

        # Trim text after the last page (following 'About the Author')
        about_author = "Robert Jordan was born in 1948"
        end_index = self.__text.index(about_author)

        tmp = self.__text[beg_index + 1 : end_index - 1]

        self.__text   = tmp
        self.text_len = len(tmp)


    def info(self):
        """
            Print general book information
        """
        print("\n-- BOOK INFORMATION --")
        print("Length: {}".format(self.text_len))    
        print("Pages:  {}\n".format(self.pages))


def polynomial_fit(xs, ys, degree):
    """
        Use numpy to generate best fit curve for manually gathered
        book data
    """
    for i in range(len(ys)):
        tmpy = ys[i]
        tmpx = xs[i]

        ys[i] = float(tmpy)
        xs[i] = float(tmpx)

    fit = np.polyfit(xs,ys,degree)

    return np.poly1d(fit)

def least_squares_test(deviation):
    """
        Calculate least-squares figure for measuring goodness of fit
    """
    least_squares = []
    total_sum = 0

    for i in range(len(deviation)):
        square = deviation[i] ** 2
        least_squares.append(square)

    for data in least_squares:
        total_sum += data

    return total_sum


if __name__ == '__main__':
	# Instantiate book object and search for sample phrase
    p = sys.argv[1]

    ebook = Book(open('wot_sample.txt').read(), p)
    sample = open("phrases.txt", "r")
    output = open("output.txt", "w+")

    # Trim intro/outro and print book information
    ebook.WOT_trim()
    ebook.info()
    
    # Declare xs array and ys array for polynomial generation
    xs, ys = [], []

    # Iterate through sample.txt
    for line in sample:
        page_approx = Decimal(ebook.progress(line.split('\t')[0]))
        page_actual = Decimal(line.split('\t')[1])

        # Calculate disparity between approximated page and actual page
        diff = page_approx - page_actual

        # Populate xs and ys
        xs.append(page_actual)
        ys.append(diff)

        # Print to output file
        s = "{}   {}".format(page_actual, diff)
        output.write(s)
        output.write('\n')

        print(s)

    # Genereate best-fit polynomial for the data
    p = polynomial_fit(xs,ys,3)
    print(least_squares_test(ys))

    # INPUT LOOP

    done  = 0

    while not done:
        # Prompt the user until they exit
        phrase = raw_input('PHRASE: ')

        if phrase != '':
            approximate_index = ebook.lookup(phrase)
            print ("PAGE:   {}".format(ebook.progress(phrase)))
        else:
            done = 1
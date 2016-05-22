# Author: Dylan Ruggeroli
# Date:	  5 / 9 / 2016
# Description:
#   Compares two separate approaches for using phrases contained in a book
#   to calculate approximate page numbers

import sys
import numpy as np
from decimal import *

def main():
    """
        Compare progress and polynomial fit methods for predicting reader's
        location within a book. After comparing using sample input data, the
        program prompts the user for custom phrases to test. 
    """
    # Get total number of pages from command-line
    total_pages = sys.argv[1]
    # book_as_text = sys.argv
    # sample_data  = sys.argv

    ebook = Book(open('texts/wot_sample.txt').read(), total_pages)

    # Open sample data and output files
    sample = open("sample_data/phrases.txt", "r")
    output = open("output.txt", "w+")

    # Trim intro/outro, then print book information
    ebook.WOT_trim()
    ebook.info()
    
    # Actual and observed data for progress method and polynomial method
    xs, ys, poly_xs, poly_ys = [], [], [], []

    # Store the given sample data
    sample_phrases, sample_pages = [], []
    for line in sample:
        sample_phrases.append(line.split('\t')[0])
        sample_pages.append(Decimal(line.split('\t')[1]))

    # Generate best-fit for a polynomial with degree 3
    p = ebook.get_poly(sample_phrases, sample_pages)

    # Calculate approximate page numbers using the progress method as 
    # well as the polynomial method
    for i in range(len(sample_phrases)):
        cur_phrase  = sample_phrases[i]
        index = ebook.lookup(cur_phrase)

        page_approx = Decimal(ebook.progress(cur_phrase))
        page_actual = sample_pages[i]

        # Append progress method results
        xs.append(page_actual)
        ys.append(page_approx)

        # Append polynomial method results
        poly_xs.append(page_actual)
        poly_ys.append(p(index))

    # Perform least-squares tests to measure goodness of fit
    print("Lookup least-squares:     {}".format(least_squares_test(xs, ys)))
    print("Polynomial least-squares: {}".format(least_squares_test(poly_xs, poly_ys)))

    # Close the sample text
    sample.close()
    output.close()

    # Infinite loop for testing both methods using custom phrases
    done  = 0
    while not done:
        phrase = raw_input('PHRASE: ')
        if phrase != '':
            index = ebook.lookup(phrase)

            if index:
                page = p(index)
            else:
                page = 0
                
            print ("PAGE:   {}".format(ebook.progress(phrase)))
            print ("POLY:   {}".format(page))
        else:
            done = 1

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
            Calculate users progress using the index of the given phrase
        """
        index = self.lookup(s)    
        getcontext().prec = 6
        index  = Decimal(index)
        length = Decimal(self.text_len)
        pages  = Decimal(self.pages)

        return (index / length) * pages

    def get_poly(self, phrases, page_nums):
        """
            Using sample data to generate a polynomial function describing the
            relationship between index number and actual page number
        """
        xs, ys = [], []

        for i in range(len(phrases)):
            index = Decimal(self.lookup(phrases[i]))
            page_actual = Decimal(page_nums[i])

            xs.append(index)
            ys.append(page_actual)

        # Generate and return the polynomial function
        return polynomial_fit(xs, ys, 3)

    def WOT_trim(self):
        """
            Trim intro and outro for the text

            Note: This method is specific to the Wheel of Time Series
        """
		# Trim text before the prologue (page one)
        prologue = "PROLOGUE"
        beg_index = self.__text.index(prologue)

        tmp = self.__text[beg_index+1:]
        beg_index += tmp.index(prologue)

        # Trim text after 'About the Author' (last page)
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

def least_squares_test(actual, observed):
    """
        Calculate least-squares figure for measuring goodness of fit
    """
    least_squares = []
    total_sum = 0

    for i in range(len(actual)):
        diff = float(actual[i]) - float(observed[i])
        square = diff ** 2
        least_squares.append(square)

    for data in least_squares:
        total_sum += data

    return total_sum

def page_disparity(page, val):
    """
        Takes an array of page numbers and an array of approximated
        page values, returning the difference between them as an 
        array of tuples
    """
    tuples = []
    for i in range(len(page)):
        diff = float(val[i]) - float(page[i])
        tupl = (page[i], diff)
        tuples.append(tupl)

    return tuples


if __name__ == '__main__':
    main()

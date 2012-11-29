import csv
import sys
class csvReader(object):
    '''
    convert a csv (comma delimited) file with newlines separating
    rows into a list of lists of strings
    '''

    def __init__(self, csvfilename):
        '''
        input is csv file
        '''
        self.csvMatrix = []
        with open(csvfilename, 'rb') as csvfile:
            myreader = csv.reader(csvfile)
            i = 0 
            for row in myreader:
                self.csvMatrix.append(row)

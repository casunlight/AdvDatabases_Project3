'''
Accept as input the name of a file from which to extract association rules using modified 
Apriori algorithm.

Also requires as command line input, min support and min confidence levels between 0 and 1.
ie python main.py INTEGRATED-DATASET.csv 0.3 0.5
'''
import csvHelper
import logging
import sys
import AprioriTID

if __name__ == '__main__':
    
    logging.basicConfig(level=logging.ERROR)

    #create all singleton objects
    arglist = sys.argv 
    if len(arglist) < 3:
        print "Usage: <filename> <min support> <min confidence>"
        sys.exit(1) #exit interpreter   
    
    #read in csv file to a list of lists
    filename=arglist[1]
    dataMatrix=csvHelper.csvReader(filename)
    
    #test our data structure
    # for row in dataMatrix.csvMatrix:
    #     print ', '.join(row)

    # Assign unique transaction IDs for each transaction
    transactions = {}
    tid = 0
    for row in dataMatrix.csvMatrix:
        transactions[tid] = tuple([tid, row])
        tid = tid + 1


    # transactions = {}
    # transactions[100] = tuple((100, [1,3,4]))
    # transactions[200] = tuple((200, [2,3,5]))
    # transactions[300] = tuple((300, [1,2,3,5]))
    # transactions[400] = tuple((400, [2,5]))
    

    results = AprioriTID.aprioriTid(transactions, float(arglist[2]), float(arglist[3]))

    print ""
    print "RESULTS"
    print results

    


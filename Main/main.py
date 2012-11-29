'''
Accept as input the name of a file from which to extract association rules using modified 
Apriori algorithm.

Also requires as command line input, min support and min confidence levels between 0 and 1.
ie python main.py INTEGRATED-DATASET.csv 0.3 0.5
'''
import csvHelper
import logging
import sys
import itertools
import AprioriTID
from common import *

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
    

    (largesets, supportCounts) = AprioriTID.aprioriTid(transactions, float(arglist[2]), float(arglist[3]))



    
    output = "==Large itemsets (min_sup=%%%d)\n" % (float(arglist[2])*100)
    for largeset in largesets:
        itemset = largeset[0]
        if type(itemset) is not list:
            itemset = [itemset]
        
        output +="%s, %%%d\n" % (itemset, (float(largeset[1]) / len(transactions) * 100))

    output +="\n"
    output +="==High-confidence association rules (min_conf=%%%d)\n" % (float(arglist[3]) * 100)


    rules = []
    for largeset in largesets:
        itemset = largeset[0]
        if type(itemset) is not list:
            continue
        

        
        for n in map(list, itertools.permutations(itemset, len(itemset))):

            lhs = hash_set(n[0:len(n)-1])

            if len(n[0:len(n)-1]) == 1:
                lhs = n[0]

            support = float(supportCounts[hash_set(n)]) / len(transactions)
            lhs_supp = float(supportCounts[lhs]) / len(transactions) 
            rhs_supp = float(supportCounts[n[len(n)-1]]) / len(transactions)

            confidence = float(supportCounts[hash_set(n)]) / len(transactions)
            confidence /= lhs_supp


            aconf = confidence
            if aconf == 1.0:
                aconf = 0.99

            conviction = (1.0 - rhs_supp) / (1.0 - aconf)

            if conviction < 50:
                continue

            # interestingness(a->b)=sup(a,b)/(sup(a)sup(b))
            interestingness = support / (lhs_supp * rhs_supp)

            if confidence < float(arglist[3]):
                continue


            rules.append(tuple(("%s => %s" % (n[0:len(n)-1],n[len(n)-1:len(n)]), confidence*100, support*100, conviction, interestingness) ))

    rules.sort(key=lambda rule: rule[3])

    debug_output = output
    for rule in rules:   

        debug_output+="%s (Conf %%%d, Supp: %%%d, Conviction %f, Interestingness %f) \n" % \
            (rule[0], rule[1], rule[2], rule[3], rule[4])

        output+="%s (Conf %%%d, Supp: %%%d) \n" % \
            (rule[0], rule[1], rule[2])
            

    print debug_output

    f = open("output.txt", "w")
    f.write(output)
    f.close()


    

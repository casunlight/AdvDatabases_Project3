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
    
    # Assign unique transaction IDs for each transaction
    transactions = {}
    tid = 0
    for row in dataMatrix.csvMatrix:
        transactions[tid] = tuple([tid, row])
        tid = tid + 1

    # Run a-priori TID
    (largesets, supportCounts) = AprioriTID.aprioriTid(transactions, float(arglist[2]))

    
    # Generate output for large itemsets
    output = "==Large itemsets (min_sup=%%%d)\n" % (float(arglist[2])*100)
    for largeset in largesets:
        itemset = largeset[0]
        if type(itemset) is not list:
            itemset = [itemset]
        
        output +="%s, %%%d\n" % (itemset, (float(largeset[1]) / len(transactions) * 100))

    output +="\n"
    output +="==High-confidence association rules (min_conf=%%%d)\n" % (float(arglist[3]) * 100)


    # We generate association rules by generating all list permutations of 
    # each itemset and pick the last element in the set as the RHS
    rules = [] # Each element is a tuple of (rule_string, confidence, support, conviction, interestingness)
    for largeset in largesets:
        itemset = largeset[0]

        # Skipping 1-itemsets
        if type(itemset) is not list:
            continue
        

        # Permute all possible lists of this itemset
        for n in map(list, itertools.permutations(itemset, len(itemset))):

            lhs = hash_set(n[0:len(n)-1])
            rhs = n[len(n)-1]

            if len(n[0:len(n)-1]) == 1:
                lhs = n[0]

            # Calculating support for X => Y:
            # 1. support = support(X,Y)
            # 2. lhs_supp = support(X)
            # 3. rhs_supp = support(Y)
            support = float(supportCounts[hash_set(n)]) / len(transactions)
            lhs_supp = float(supportCounts[lhs]) / len(transactions) 
            rhs_supp = float(supportCounts[rhs]) / len(transactions)

            # Calculating confidence
            confidence = float(support) / lhs_supp

            # Calculating conviction
            aconf = confidence
            if aconf == 1.0:
                aconf = 0.99
            conviction = (1.0 - rhs_supp) / (1.0 - aconf)


            # Conviction cutoff (Discard less than 50)
            if conviction < 2:
                continue

            # Confidence cutoff (discard less than min_conf)
            if confidence < float(arglist[3]):
                continue

            # Calculate interestings
            interestingness = support / (lhs_supp * rhs_supp)

            # Append to our list of rules
            rules.append(tuple(("%s => %s" % (n[0:len(n)-1],n[len(n)-1:len(n)]), confidence*100, support*100, conviction, interestingness) ))

    # rules.sort(key=lambda rule: rule[3], reverse=True)


    # Generate output for rules
    debug_output = output
    for rule in rules:   

        debug_output+="%s (Conf %%%d, Supp: %%%d, Conviction %f, Interestingness %f) \n" % \
            (rule[0], rule[1], rule[2], rule[3], rule[4])

        output+="%s (Conf %%%d, Supp: %%%d) \n" % \
            (rule[0], rule[1], rule[2])
            

    print debug_output
    print ""
    print "---------------------"
    print "Large itemsets and High-confidence rules are stored in output.txt"
    print ""

    f = open("output.txt", "w")
    f.write(output)
    f.close()


    

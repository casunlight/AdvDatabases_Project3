'''
Implement AprioriTID algorithm with associated apriori-gen function to generate candidate large itemsets
from Agrawal's 'Fast Algorithms for Mining Association Rules'
'''
import itertools
import sys


#Generate all k size large itemsets, those with minimum support. 
#Return Ck where each member has two fields: i) itemset ii) support count
#assumes itemset in Lk-1 is sorted
def aprioriGen(LkminusOne, k):
    LkminusOneSets=[]
    kminus = int(k-1)
    lenCK=0
    lenCKprune=0
    Ck=[] #list{ tuple([sorted large itemset],support) } 
    if k==2: #trivial case
        for i in range(len(LkminusOne)):
            for j in range(len(LkminusOne)-i-1):
                #assume candidate set support is at most min support of each 
                tempList=[LkminusOne[i][0],LkminusOne[j+i+1][0]] #UNSORTED
                tempTuple=tuple( (tempList, min(LkminusOne[i][1],LkminusOne[j+i][1])) )
                # print tempTuple
                Ck.append(tempTuple)
    elif k>2:
        #convert LkminusOne to list of sets for easier comparisons later
        for i in range(len(LkminusOne)):
            LkminusOneSets.append(set(LkminusOne[i][0])) 
         
        
        #creates sets from the prefix of each LkminusOne itemset
        for i in range(len(LkminusOne)):
            # print i
            tempSet1=set(LkminusOne[i][0][0:k-2]) #generate prefix of LkminusOne itemset
           
            for j in range(len(LkminusOne)-i-1):
                tempSet2=set(LkminusOne[j+i+1][0][0:k-2]) #genereate another prefix
                '''
                print 'tempset1 {}'.format(tempSet1)
                print 'tempset2 {}'.format(tempSet2)
                print ''
                print 'last element from 1: {}'.format(LkminusOne[i][0][-1])
                print 'last element from 2: {}'.format(LkminusOne[j+i+1][0][-1])
                '''
                #compare prefixes of each itemset from LkminusOne
                if len(tempSet2 & tempSet1)==(k-2) and LkminusOne[i][0][-1] != LkminusOne[j+i+1][0][-1]: #if theyre equal except for last element
                    #print LkminusOne[i][0][:]
                    #print LkminusOne[j+i+1][0][:]
                    tmpList1=list(LkminusOne[i][0]) #construct by copy
                    #print 'TMPLIST1: {}'.format(tmpList1)
                    tmpList1.append(LkminusOne[j+i+1][0][-1]) #UNSORTED k size candidate itemset
                    tempList=list(tmpList1)
                    #print 'TEMPLIST: {}'.format(tempList)
                    tempTuple=tuple( (tempList, min(LkminusOne[i][1], LkminusOne[j+i+1][1])) )
                    #print 'TEMP TUPLE: {}'.format(tempTuple)
                    Ck.append(tempTuple)
        lenCK=len(Ck)
        #PRUNE STEP
        #Delete all itemsets c in Ck s.t. some (k-1) subset of c is not in Lk-1
        for i in range(len(Ck)):
            s=set(Ck[i][0])
            # print 'set: {} k: {}'.format(s,kminus)
            setList=map(set, itertools.combinations(s,kminus))  #generate all k-1 combinations of each candidate itemset
            # print 'SetList: {}'.format(setList)
            for j in range(len(setList)):
                # print j
                count = 0
                for k in range(len(LkminusOneSets)):
                    
                    if len(setList[j] & LkminusOneSets[k]) != len(LkminusOneSets[k]):
                        count = count + 1
                if count == len(LkminusOneSets): #candidate itemset subset not found in any of prior Lk-1, DISCARD entire candidate with short circuit
                    del Ck[i]
                    break      
        lenCKprune = len(Ck)     
        # print 'old length: {} pruned length: {}'.format(lenCK, lenCKprune)
    return Ck
        



#generate k=1 size large itemsets
#input a list of lists corresponding to transactions. This is the in-memory
#representation of a database table of transactions
def LargeItemsetGen(transactions,minsupp):
    #keep each unique item found during linear pass through Transactions
    #in a dictionary along with count
    transTotal=len(transactions)
    L1=[]
    dictRawItem = {}
    for tid in transactions:
        items = transactions[tid][1]
        
        for i in range(len(items)):
            if str(items[i]).lower().strip() == "unspecified" or \
               str(items[i]).lower().strip() == "n/a" or str(items[i]).strip() == "":
                continue 
            # print 'Item: {}'.format(row[i])
            if items[i] in dictRawItem:
                dictRawItem[items[i]] =  dictRawItem[items[i]] + 1
            else:
                dictRawItem[items[i]] = 1

    #extract large itemsets having minsupport and place into L1=list{ tuple([sorted large itemset],support) } 
    for key in dictRawItem:
        support = float(dictRawItem[key])/transTotal
        if support >= minsupp:
            #add item to L1
            L1.append(tuple((key, dictRawItem[key]))) #key , support count      
    return  L1
        
    
def aprioriTid(transactions, minsupp, minconf):
    L = [ [], LargeItemsetGen(transactions, minsupp) ]
    # print ""
    # print "############################"
    # print "Database"
    

    prevC_comp = transactions



    k = 2
    

    while len(L[k-1]) > 0:

        Ck = aprioriGen(L[k-1], k)
        C_comp = {}

        # print ""
        # print "############################"

        supportCounts = {}

        # print "Transactions in previous C comp:"
        for tid in prevC_comp:   
            if k == 2:
                t_set_of_items = [[x] for x in prevC_comp[tid][1]]
            else:
                t_set_of_items = prevC_comp[tid][1]

            # print "T[%d] = %s" % (tid, t_set_of_items)
            
            Ct = []
            for c in Ck:   
                c_items = c[0]
                # if k == 2:
                    # c_items_minus_ck = [[x] for x in set(c_items) - set([c_items[k-1]])]
                    # c_items_minus_ckminus1 = [[x] for x in set(c_items) - set([c_items[k-2]])]
                # else:
                c_items_minus_ck = [list(set(c_items) - set([c_items[k-1]]))]
                c_items_minus_ckminus1 = [list(set(c_items) - set([c_items[k-2]]))]

                # print ""
                # print "C: %s" % c_items
                
                
                # print ""



                ck_belongs_to_t = True
                for item in c_items_minus_ck:

                    if item not in t_set_of_items:
                        ck_belongs_to_t = False
                # print "C - c[k]: %s ? %s" % (list(c_items_minus_ck), ck_belongs_to_t)

                ckm1_belongs_to_t = True
                for item in c_items_minus_ckminus1:
                    if item not in t_set_of_items:
                        ckm1_belongs_to_t = False

                # print "C - c[k-1]: %s ? %s" % (list(c_items_minus_ckminus1), ckm1_belongs_to_t)

                if ckm1_belongs_to_t and ck_belongs_to_t:
                    # print "appending to Ct"
                    Ct.append(list(c_items))


            # print "Ct %d: %s" % (tid, Ct)

            for c in Ct:
                if str(c) not in supportCounts:
                    supportCounts[str(c)] = 0
                
                supportCounts[str(c)] += 1

            if len(Ct) > 0:
                C_comp[tid] = tuple((tid, Ct))

        # print "--------------------"
        # print "C Comp = "
        # for tid in C_comp:
            # print "%d %s" % (tid, C_comp[tid][1])

        # print "--------------------"
        
        L.append([]) # This will be L[k]


        for c in Ck:
            c_items = c[0]
            if str(c_items) not in supportCounts:
                continue
            support = float(supportCounts[str(c_items)])/len(transactions)
            if support >= minsupp:            
                L[k].append(tuple((c_items, supportCounts[str(c_items)])))

        # print "L%d = %s" % (k, L[k])

        prevC_comp = C_comp

        k = k + 1
    
    result = []
    i = 0

    for l in L:
        if i == 0 or i == k - 1:
            i += 1
            continue
        i += 1


        result = result + l

    return result


    
    

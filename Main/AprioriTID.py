'''
Implement AprioriTID algorithm with associated apriori-gen function to generate candidate large itemsets
from Agrawal's 'Fast Algorithms for Mining Association Rules'
'''




#Generate all k size large itemsets, those with minimum support. 
#Return Lk where each member has two fields: i) itemset ii) support count
def aprioriGen(LkminusOne, k):
    pass



#generate k=1 size large itemsets
#input a list of lists corresponding to transactions. This is the in-memory
#representation of a database table of transactions
def LargeItemsetGen(matrixTransactions,minsupp):
    #keep each unique item found during linear pass through Transactions
    #in a dictionary along with count
    dictRawItem = {}
    for row in matrixTransactions:
        for i in range(len(row)):
            print 'Item: {}'.format(row[i])
            if row[i] in dictRawItem:
                dictRawItem[row[i]] =  dictRawItem[row[i]] + 1
            else:
                dictRawItem[row[i]] = 1
    return dictRawItem
        
    


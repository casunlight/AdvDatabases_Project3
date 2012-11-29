
def hash_set(itemlist):
    # return str(itemlist)
    liststr = "["
    for item in sorted(itemlist):
        liststr += str(item)
        liststr += ","
    liststr += "]"
    return liststr
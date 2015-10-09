
def serialize(vector, varName):
    print "serialize [" + varName + "]",
    f = open('serialize/' + varName, 'w+')
    for item in vector:
        print>>f, item
    f.close()
    print " ... [OK]"


def unserialize(varName):
    print "unserialize [" + varName + "]",
    fname = 'serialize/' + varName
    with open(fname) as f:
        vector = f.readlines()
    ret = []
    for item in vector:
        ret.append(float(item))
    print " ... [OK]"
    return ret
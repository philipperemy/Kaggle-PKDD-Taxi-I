import os


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


def clean_serialization_folder():
    print 'cleaning serialization folder',
    folder = 'serialize/'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e
    print "... [OK]"

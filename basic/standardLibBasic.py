import os
import sys
import math
import re
#from urllib.request import urlopen


def osSysFun():
    print(os.getcwd())
    print(sys.argv)

def reMatch():
    line = "Cats are smarter than dogs"
    matchObj = re.match( r'(.*) are (.*?) .*',line, re.M|re.I)
    if matchObj:
        print ("matchObj.group() : ", matchObj.group())
        print ("matchObj.group(1) : ", matchObj.group(1))
        print ("matchObj.group(2) : ", matchObj.group(2))
    else:
        print("No match!!")

#def requestFun():
#    for line in urlopen('http://tycho.usno.navy.mil/cgi-bin/timer.pl'):
#        aLine = line.decode('utf-8')
#        if "EST" in aLine or "EDT" in aLine:
#            print(aLine)

if __name__ == '__main__':
    #requestFun()
    reMatch()
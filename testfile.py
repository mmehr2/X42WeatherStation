import os
import sys

def make_test():
    ofile = open("test.dat", "w")
    str = '''80,30.02,50
74,29.99,44
69,29.77,66
'''
    ofile.write(str)

def read_test():
    ifile = open("test.dat", "r")
    data = [ x.strip().split(',') for x in ifile ]
    return data


def main():
    make_test()
    array = read_test()
    print "Data read: ", array
    return 0

main()

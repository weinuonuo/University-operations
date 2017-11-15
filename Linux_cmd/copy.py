#!/usr/bin/env python3
import sys,getopt

def readfile(infile,outfile):
    infile = open(infile,'r').read()
    open(outfile,'w').write(infile)

def main():
    if len(sys.argv) < 2:
        print("NO action specified")
    else:
        if sys.argv[1].startswith('--'):
            if sys.argv[1][2:] == 'version':
                print("version 0.1")
            if sys.argv[1][2:] == 'help':
                print('''
                    This program prints files to standard output.
                    Any number of files can be specified.
                    Options include:
                    -- version : Prints the version number
                    -- help : Display this help
                    - i : add input file
                    - o : add output file
                ''')
            else:
                print("Unknow option.")
        else:
            opts,args = getopt.getopt(sys.argv[1:],"i:o:")
            for op,value in opts:
                if op == "-i":
                    input_file = value
                if op == "-o":
                    output_file = value
            readfile(input_file,output_file)
    
        
if __name__ == '__main__':
    main()

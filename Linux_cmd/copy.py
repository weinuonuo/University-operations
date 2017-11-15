#!/usr/bin/env python3
import sys,getopt,shutil

def copyfile(infile,outfile):
    try:
        shutil.copy(infile,outfile)
    except:
        print('''Can't open this file''')
        return

def copydir(indir,outdir):
    try:
        shutil.copytree(indir,outdir)
    except:
        print('This dir is wrong')

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
            input_file,output_file,input_dir,output_dir = '','','',''
            for op,value in opts:
                if op == "-i" :
                    if '.' in value:
                        input_file = value
                    else:
                        input_dir = value
                elif op == "-o":
                    if '.' in value:
                        output_file = value
                    else:
                        output_dir = value
            if input_file and output_file:
                copyfile(input_file,output_file)
            elif input_dir and output_dir:
                copydir(input_dir,output_dir)
            else:
                print('Input Wrong')
    
        
if __name__ == '__main__':
    main()

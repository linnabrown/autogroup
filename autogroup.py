import os
import pprint
import threading
import sys
import math
from multiprocessing import cpu_count
'''
python autogroup.py <input_directory> <output_directory> [<# of threads>]

python autorgroup.py input_dir output_dir 2
'''
'''
Function Area
'''
def chunks(l,n):
    """Yield successive n-sized chunks from l.
    """
    for i in range(0,len(l), n):
        yield l[i:i+n]

def directoryFormat(dirname, i_or_o):
    if i_or_o == "in":
        if not os.path.exists(dirname):
            print("The input directory \'%s\' does not exit!" % dirname)
            sys.exit(0)
    if i_or_o == "out":
        if os.path.exists(dirname):
            print("This output directory \%s'\' has been existed" % dirname)
            sys.exit(0)
        else:
            os.makedirs(dirname)
    if not dirname.endswith("/"):
        dirname += "/"
    return dirname

'''
I/O Area
'''
thread_number = int(cpu_count())-4

if len(sys.argv) == 1:
    print("please input <Input Dir> and <Output Dir>!")
    sys.exit(0)

if len(sys.argv) == 2:
    print("please also input <Output Dir>!")
    sys.exit(0)

if len(sys.argv) == 3 and int(cpu_count()) >= 16:
    print("Wow, your PC/Server is awesome!")

if len(sys.argv) == 4:
    thread_number = int(sys.argv[3])

print("[Attention Please] I will use %s of your %s cpu!" % (str(thread_number), cpu_count()))

'''
Start split
'''
inputDir = directoryFormat(sys.argv[1],"in")
outputDir = directoryFormat(sys.argv[2],"out")
inputDirs = os.listdir(inputDir)
block_size = math.ceil(len(inputDirs)/thread_number)
Dir_arr = list(chunks(inputDirs,block_size))
Dir_len = len(Dir_arr)

for i in range(Dir_len):
    print(i)
    os.makedirs( outputDir + str(i))
    for j in range(len(Dir_arr[i])):
        os.system("cp %s%s %s%s/" % (inputDir, Dir_arr[i][j], outputDir, str(i)))

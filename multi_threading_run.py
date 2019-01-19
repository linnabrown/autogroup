import os
import pprint
import threading
import sys
import math
from multiprocessing import cpu_count
from subprocess import Popen, call, check_output
'''
python multi_threading_run.py <input_directory> <output_directory> [<# of threads>]

python multi_threading_run.py input_dir output_dir 2

Put it into the same directory of acr_aca_finder!!!
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

def run_anti_crispr(i, inputDir, block_size, outputDir):
    inputDirs = os.listdir(inputDir)
    Dir_arr = list(chunks(inputDirs,block_size))

    for j in range(len(Dir_arr[i])):
        newFile_dir = inputDir + Dir_arr[i][j]
        if os.path.isdir(newFile_dir):
            arr = os.listdir(newFile_dir)
            file_types = [".faa", ".fna", ".gff"]
            fn = {}
            for filename in arr:
                for suffix in file_types:
                    if item.endswith(suffix):
                        fn[suffix]= newFile_dir + '/' + filename
                        break
            anti_crispr = Popen(['python', 'acr_aca_finder/acr_aca_cri_runner.py', '-f', fn[".gff"],\
            '-a', fn[".faa"], '-n', fn[".fna"], '-o', outputDir + Dir_arr[i][j] ])
            anti_crispr.wait()
            print("%s-%s [%s] OK"%( str(i), str(j), Dir_arr[i][j] ))
        else:
            if not os.path.exists( "error-log-%s.txt" % ( str(i) ) ):
                fw = open("error-log-%s.txt"%(str(i)),"w")
            print("%s-%s [%s] BAD"%( str(i), str(j), Dir_arr[i][j]))
            fw.write("%s-%s [%s] BAD"%( str(i), str(j), Dir_arr[i][j]))

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
block_size = int(math.ceil(len(inputDirs)/thread_number))
Dir_arr = list(chunks(inputDirs,block_size))
Dir_len = len(Dir_arr)

threads=[]

for i in range(Dir_len):
    threads.append(threading.Thread(target=run_anti_crispr, args=(i, inputDir, block_size, outputDir)))
for t in threads:
    t.start()

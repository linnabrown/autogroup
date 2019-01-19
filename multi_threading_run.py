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
    files_matrix = list(chunks(inputDirs,block_size))
    if not os.path.exists( "log-%s.txt" % ( str(i) ) ):
        fw = open("log-%s.txt"%(str(i)),"w")

    for j in range(len(files_matrix[i])):
        genome_full_path = inputDir + files_matrix[i][j]
        if os.path.isdir(genome_full_path):
            arr = os.listdir(genome_full_path)
            file_types = [".faa", ".fna", ".gff"]
            fn = {}
            for filename in arr:
                for suffix in file_types:
                    if filename.endswith(suffix):
                        fn[suffix]= genome_full_path + '/' + filename
                        break
            anti_crispr = Popen(['python3', 'acr_aca_finder/acr_aca_cri_runner.py', '-f', fn[".gff"],\
            '-a', fn[".faa"], '-n', fn[".fna"], '-o', outputDir + files_matrix[i][j] ])
            anti_crispr.wait()
            log_print="%s-%s\t[%s]\tOK" % ( str(i), str(j), files_matrix[i][j] )
        else:
            log_print = "%s-%s\t[%s]\tBAD" % ( str(i), str(j), files_matrix[i][j] )
        print(log_print)
        fw.write(log_print)

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
files_matrix = list(chunks(inputDirs,block_size))
Dir_len = len(files_matrix)

threads=[]

for i in range(Dir_len):
    threads.append(threading.Thread(target=run_anti_crispr, args=(i, inputDir, block_size, outputDir)))
for t in threads:
    t.start()

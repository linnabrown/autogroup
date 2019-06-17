import os
import glob

fileList = glob.glob('./complete_genome_bac/*')

for infile in fileList:
    gcfile = infile.split('/')[-1]
    gff_file = infile + '/' + gcfile + '_genomic.gff.gz'
    fna_file = infile + '/' + gcfile + '_genomic.fna.gz'
    faa_file = infile + '/' + gcfile + '_protein.faa.gz'
    if os.path.exists(gff_file):
        os.system('gzip -d {}'.format(gff_file))
    else:
        print(gff_file + ' is not existed')
    if os.path.exists(fna_file):
        os.system('gzip -d {}'.format(fna_file))
    else:
        print(fna_file + ' is not existed')
    if os.path.exists(faa_file):
        os.system('gzip -d {}'.format(faa_file))
    else:
        print(faa_file + ' is not existed')

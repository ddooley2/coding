import os, gzip

"""
Author: David Dooley
Email: ddooley2@vols.utk.edu
Description:
This code takes an input directory that contains all of the barcode subdirectories (barcode01, barcode02, etc.) within it
and performs centrifuge read mapping on all of the reads given a centrifuge index (reference). It outputs its data
to a series of tsv files in the working directory, which can be visualized using centrifuge_plot.py
"""

cent_exe = '/usr/local/bin/centrifuge'
ind_path = '/Users/ddooley/bioinformatics_packages/individual_packages/centrifuge/indices/atcc' ###Change to appropriate index path
master_dir = '/Users/ddooley/Desktop/UT_Summer_2021/sam_cohen/datasets/wimp_data/atcc_4_media_reads' ###Please change to the root directory of fastq files (code recursively goes through barcoded folders if present

for barcode_dir in sorted(os.listdir(master_dir)): ###MASTER LOOP THROUGH EVERY DIRECTORY IN SEQUENCING FOLDER
    barcode_dir = master_dir + '/' + barcode_dir
    master_fastq = barcode_dir + '/master.fastq'

    for file in os.listdir(barcode_dir): ### Go through and gunzip any gzipped files
        if ".gz" in file:
            os.system("gunzip " + str(barcode_dir + "/" + file))

    """ Concatenate all fastq files in barcode directory to a single large file """
    cat_fastq = 'cat ' + barcode_dir + '/*.fastq > ' + master_fastq
    os.system(cat_fastq)

    """  Run centrifuge """
    cline = cent_exe + ' -q -x ' + ind_path + ' ' + master_fastq +  ' > ' + os.getcwd() + '/' + barcode_dir.split('/')[-1] + '_master.tsv'
    os.system(cline)
    os.remove(master_fastq)
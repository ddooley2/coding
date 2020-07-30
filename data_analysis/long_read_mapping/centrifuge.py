import os

cent_exe = '/home/ddooley/opt/centrifuge/centrifuge'
ind_path = '/home/ddooley/opt/centrifuge/indices/3LB' ###Change to appropriate index path
master_dir = '/home/ddooley/sequencing/3LB_control' ###Please change to the root directory of fastq files (code recursively goes through barcoded folders if present

for barcode_dir in sorted(os.listdir(master_dir)): ###MASTER LOOP THROUGH EVERY DIRECTORY IN SEQUENCING FOLDER
    barcode_dir = master_dir + '/' + barcode_dir
    master_fastq = barcode_dir + '/master.fastq'
    """ Concatenate all fastq files to a single large file """
    cat_fastq = 'cat ' + barcode_dir + '/*.fastq > ' + master_fastq
    os.system(cat_fastq)

    """  Run centrifuge """
    cline = cent_exe + ' -q -x ' + ind_path + ' ' + master_fastq +  ' > ' + os.getcwd() + '/' + barcode_dir.split('/')[-1] + '_master.tsv'
    os.system(cline)
    os.remove(master_fastq)


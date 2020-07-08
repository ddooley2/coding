from Bio import SeqIO
import gzip, os, shutil
from progressBar import printProgressBar

###Assumes that all samples are in gzipped fastq format

fastq_dir = '/home/ddooley/HDD/sequencing/12_24_LB_TSB_YPD_MYD/fastq_pass'
barcode = input('\nPlease input barcode to be analyzed (e.g. barcode01) or leave empty if fastq files are in current dir: ')



if len(barcode) != 0:
    fastq_dir += "/" + barcode ###Change path to folder with fastq files for given barcode


seq_dict = {}
l = len(os.listdir(fastq_dir))
printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50) ###Initialize progress bar
for filename in os.listdir(fastq_dir): ###MASTER LOOP THROUGH EVERY FASTQ FILE
    it = 0 
    records_list = []
    seq_dict['ID: '+str(it)] = records_list
    fastq_path = fastq_dir + '/' + filename.split(".gz")[0]
    
    with gzip.open(fastq_dir + '/' + filename, 'rb') as f_in: ###Remove gzip compression
        with open(fastq_path, 'wb') as f_out: ###Create unzipped file
            shutil.copyfileobj(f_in, f_out)
    for record in SeqIO.parse(fastq_path, "fastq"): ###Read all fastq seqs into Seq.IO object
        seq_dict['ID: '+ str(it)].append(record)
    seq_dict[it] = records_list ###Assigns all reads of a fastq file to a dictionary, with arbitrary keys starting at 1
    it += 1
    printProgressBar(it+1, l, prefix = 'Progress:', suffix = 'Complete', length = 50) ###Update progress bar

#####CODE IS BROKEN, PROBABLY STORING TOO MUCH DATA IN DICT

#for key, value in seq_dict.items():
#    print(key)
#    print(value)
#    os.remove(fastq_dir + '/' + filename.split('.gz')[0]) ###Delete uncompressed file once finished with it
    
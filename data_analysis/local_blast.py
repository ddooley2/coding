import os, re, time
from Bio import SeqIO, Align
from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbiblastnCommandline

###Tool for peforming quick pairwise alignments with blastn utility

db_input = input('\nPlease input the name of your database fasta: ')
db_path = os.getcwd() + '/' + db_input
fasta_path = os.getcwd() + '/' + input('\nPlease input the name of your query fasta: ')

db_cline = "makeblastdb -in " + db_path + " -dbtype nucl -out " + db_input.split('.')[0] ###Set up argument for making blastDB for remaining genomes
os.system(db_cline) ###Make blast db

##Perform actual BLAST search
xml_path = os.getcwd() + '/' + db_input.split('.')[0] + '.xml'
cline = NcbiblastnCommandline(query=fasta_path, db=db_input.split('.')[0], evalue=1e-5, out=xml_path, outfmt=5, word_size=5)
stdout, stderr = cline()

my_list = []
with open(xml_path, 'r') as f:
    blast_records = NCBIXML.parse(f)
    for record in blast_records:
        if record.alignments:
            for aln in record.alignments:
                for hsp in aln.hsps:
                    print(hsp)
                scores = [hsp.expect for hsp in aln.hsps] ###Save all possible expect score for given BLAST search
                min_tup = [(j, score) for (j, score) in enumerate(scores) if score == min(scores)][0] ###Take the minimum expect value along with its index
                best_hsp = aln.hsps[int(min_tup[0])] ###Locate the correct hsp object by using the index of the minimum expect value
#    #        su_locs[key] = best_hsp.sbjct_start ###Assumes start of BLAST hit is start of search string
##        else:
##            su_locs[key] = 'NULL'
#        os.system('rm ' + db_path + '*')
#

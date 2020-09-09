## This script is meant to be used for determining phylogenetic distances between a reference organism and a subset of
## species. This file takes a concatenated .fasta file and creates a multiple sequence alignment between all sequences
## in file. The first organism in the .fasta file is designated as the "reference" organism, and the distances between
## this organism and the remaining species in the fasta file is exported to a .csv file of the same name as the input
## .fasta file.
##
##      INPUT = .fasta file with reference sequence first and all other sequences following
##      OUTPUT = (1) Phylogenetic tree (pop up figure)
##               (2) Distance matrix printed in terminal
##               (3) Output files: .phy, .dnd, and .csv with same name as INPUT file.

import os, csv, sys
from Bio.Align.Applications import MuscleCommandline, ClustalOmegaCommandline
from Bio import Phylo, AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio.Phylo.Consensus import *

## Pathing stuff
path = "/home/ddooley/phylo_vip"
in_file = path + "/" + input("Input filename: ")
out_file = in_file.split(".")[0] + ".phy"

####ClustalOmega#######
clustal_exe = "/home/ddooley/phylo_vip/programs/clustalo"
cline = ClustalOmegaCommandline(clustal_exe, infile=in_file, outfile=out_file, outfmt="phy", auto=True, force=True) #Set up command line arguments for multiple sequence alignment (MSA)
stdout, stderr = cline() #Execute ClustalOmega MSA
#######################

####Muscle#############
#muscle_exe = "/home/ddooley/phylo_vip/programs/muscle"
#mline = MuscleCommandline(muscle_exe, input=in_file, phyiout=out_file) #Set up command line arguments for MSA
#stdout, stderr = mline() #Execute Muscle MSA
#######################

phy_file = out_file   #Specify path for .phy file
list = []

## Calculate distance matrix to be used for phylogenetic tree and export features
phy = AlignIO.read(phy_file, 'phylip') #Prepare input for distance matrix function "get_distance"
calculator = DistanceCalculator('identity')
dm = calculator.get_distance(phy)
print(dm)

## Construct UPGMA tree from distance matrix (with and without bootstrapping for comparison)
#constructor1 = DistanceTreeConstructor() #no bootstrapping
#constructor2 = DistanceTreeConstructor(calculator) #bootstrapping
#upgma_tree = constructor1.upgma(dm)
#consensus_tree = bootstrap_consensus(phy, 100, constructor2, majority_consensus)
#
### Construct Maximum Parsimony tree
#starting_tree = upgma_tree
#scorer = Phylo.TreeConstruction.ParsimonyScorer()
#searcher = Phylo.TreeConstruction.NNITreeSearcher(scorer)
#constructor = Phylo.TreeConstruction.ParsimonyTreeConstructor(searcher, starting_tree)
#pars_tree = constructor.build_tree(phy)

## Assign indexes for species in dm
my_names = dm.names
ref_name = dm.names[0]
my_output = in_file.split(".")[0] + ".csv"

## Write contents of distance matrix to .csv output file
with open(my_output, mode='w') as output:
    my_writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    f = open(my_output, 'w+')
    for i in range(len(dm[0])):
        if dm[0][i] == 0:
            my_writer.writerow(["Reference organism:" + str(ref_name)])
            pass
        else:
            my_writer.writerow([my_names[i], dm[0][i]])

## Draw all trees
#Phylo.draw(upgma_tree)
#Phylo.draw(pars_tree)
#Phylo.draw(consensus_tree)
#
###Export trees into phyloxml format for further manipulation/use
#Phylo.write(upgma_tree, in_file.split(".")[0] + "_upgma" + ".xml", "phyloxml")
#Phylo.write(pars_tree, in_file.split(".")[0] + "_pars" + ".xml", "phyloxml")
#Phylo.write(consensus_tree, in_file.split(".")[0] + "_consensus" + ".xml", "phyloxml")

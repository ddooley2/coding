from dna_features_viewer import load_record
from translator_classes import gene_only
from color_displayer import show_colors
import matplotlib.pyplot as plt, matplotlib
import numpy as np
import pandas as pd
import os
from  time import sleep

####PSEUDO CODE####
# Input csv and make two lists: total repeats and locations
# Input genbank file and load gene features into a var
# Plot everything



###Input csv and make two lists: total repeats and locations
df = pd.read_csv(input("\nPlease input the name of the probe csv: "))
reps = df['Total Repeats'].tolist()
locs = df['Location'].tolist()

###Input genbank file (must be in cwd)
path = os.getcwd()
parameters = {"thickness": 20}
trans = gene_only(features_properties=parameters)
record = load_record(path + "/" + input("\nGive the name of a .gb file in the working folder: "))

###Make the graphicrecord object
graphic_record = trans.translate_record(record)

###Ask user if they wish to plot a specific gene
gene_bool = input("\nWould you like to map repeats to a specific gene? (y/n): ")
if gene_bool == "y":
    gene_bool = True
    ###Ask user for name or ID of gene
    gene = str(input("\nPlease enter the name of the gene of interest, as it appears in the annotation file: "))
    for i, feature in enumerate(graphic_record.features):
        if str(feature.label) == str(gene):
            continue
        else:
            del graphic_record.features[i]
            
    for feature in graphic_record.features:
        if feature.label != gene:
            graphic_record.features.remove(feature)

else:
    gene_bool = False



###Show color palettes and prompt user to select one
show_colors()
print("\nClose all figures to continue...")
plt.show()
color = input("\nPlease enter the name of your desired color palette: ").strip()
cmap = matplotlib.cm.get_cmap(color, len(graphic_record.features))
colors = []
for i, feature in enumerate(graphic_record.features):
    rgb = cmap(i)[:3]
    feature.color = matplotlib.colors.rgb2hex(rgb)
    
 
###Display sequence map
fig, (ax1, ax2) = plt.subplots(
 2, 1, sharex=True
)

if gene_bool:
    gene_feature = graphic_record.features[0]
    graphic_record.plot(ax=ax1, with_ruler=False, strand_in_label_threshold=40)
    ax1.set_xlim(left=gene_feature.start, right=gene_feature.end)
   
    ###Grab only the repeat and location pairs that fall within the gene's start and stop
    new_locs = []
    new_reps = []
    for i, loc in enumerate(locs):
        if (loc >= gene_feature.start and loc <= gene_feature.end):
            new_locs.append(loc)
            new_reps.append(reps[i])

        
    ax2.vlines(new_locs,0, new_reps, alpha=0.9, colors="black")
    ax2.set_ylabel("Repeat Count", fontsize=10)
    ax2.set(ylim=(0,(max(new_reps)+50)),xlim=(gene_feature.start, gene_feature.end))
    stepsize = 100
    start, end = ax2.get_xlim()
    ax2.xaxis.set_ticks(np.arange(start, end, stepsize))
#    ax2.tick_params(axis='x', rotation = 25) ###For changing rotation of x axis in case things get crowded

else:
    graphic_record.plot(ax=ax1, with_ruler=False, strand_in_label_threshold=40)
#    graphic_record.plot_legend(ax=ax1, loc=1, frameon=False) (for if you have multiple annotation types (peptides, CDS, etc.))
    ax2.vlines(locs,0, reps, alpha=0.9, colors="black")
    ax2.set_ylabel("Repeat Count", fontsize=10)
    ax2.set_ylim(bottom=0, top=max(reps)+50)


fig.suptitle(input("\nInput figure title: "), fontsize=16)
fig.tight_layout()
fig.savefig(input("\nPlease name your figure: "))

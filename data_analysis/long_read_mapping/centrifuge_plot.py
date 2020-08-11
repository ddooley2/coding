from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import os

###Code assumes that tsv files for different barcodes are all in the same subdirectory of the cwd

read_bool = input('\nWould you like relative abundances to be calculated base-wise? (Default is read-wise) (y/n)\n> ')
if read_bool == 'y':
    read_bool = True
else:
    read_bool = False

tsv_dir = os.getcwd() + '/' + input("\nPlease input sub directory with tsv files: ")

#Use collections.Counter on [seqID].tolist() to find out how many times each ID had a hit, after filtering out unclassified and empty hits
master_df = pd.DataFrame() ###Initialize dataframe
for it, tsv in enumerate(sorted(os.listdir(tsv_dir))):
    tsv_path = tsv_dir + '/' + tsv
    df = pd.read_table(tsv_path)
    df = df[~df.seqID.str.contains("unclassified")] ###Removes all rows with unclassified sequence hit
    df = df[~df.seqID.str.contains("no rank")] ###Removes all rows with no rank sequence hit
    df = df[~(df['numMatches'] > 1)] ###Removes all rows with non-unique hits
    seqid_list = df['seqID'].tolist()
    hit_list = df['hitLength'].tolist()
    seqid_count = Counter(seqid_list)
    """ Map num bases or num reads """
    if read_bool: ###Base-based mapping
        base_count = {}
        for i, item in enumerate(seqid_list):
            if item not in base_count.keys():
                base_count[item] = hit_list[i] 
            else:
                base_count[item] += hit_list[i]
        if it == 0:
            master_df['organism_ID'] = seqid_count.keys()
            master_df[tsv.split('_')[0]+'_mappedbases'] = master_df['organism_ID'].map(base_count)
        else:
            master_df[tsv.split('_')[0]+'_mappedbases'] = master_df['organism_ID'].map(base_count)
            
    else: ###Read-based mapping
        if it == 0:
            master_df['organism_ID'] = seqid_count.keys()
            master_df[tsv.split('_')[0]] = master_df['organism_ID'].map(seqid_count)
        else:
            master_df[tsv.split('_')[0]] = master_df['organism_ID'].map(seqid_count)


master_df.fillna(0, inplace=True) ###Replaces NaNs with 0s in case an organism got no bases mapped to it

""" Begin plotting everything """
fig, ax1 = plt.subplots()
norm_df = master_df.drop('organism_ID',axis=1).transpose().apply(lambda x: x*100/sum(x), axis =1) ###Transposes and normalizes all columns except for organism names
""" Uncomment to plot read-wise relative abundances """
barcode_names = list(norm_df.index)
a = norm_df.plot(ax=ax1,kind='bar',stacked=True, colormap = 'tab20', width=0.5, figsize=(4+len(barcode_names), 1+len(barcode_names))) ###
read_count = master_df.sum(axis=0, skipna=True, numeric_only=True).tolist() ###Sums the total number of mapped reads per barcode

""" Option to change bar names """
loop_escape = False
my_bool = input('\nWould you like to rename barcodes (y/n)? ')
while not loop_escape:
    if my_bool == "y":
        my_bool = True
        loop_escape = True
    elif my_bool == "n":
        loop_escape = True
        my_bool = False
        continue
    else:
        my_bool = input('\nPlease enter "y" or "n" ')

if my_bool:
    barcode_names = [str(input('\nEnter series name for %s: ' % name)) for name in barcode_names]
    
if read_bool:
    xlabs = [name + '\n (' + str("{:.3e}".format(read_count[i])) + ' bp)' for i, name in enumerate(barcode_names)] ###Add bases to barcode labels in scientific notation
else:
    xlabs = [name + '\n (' + str(read_count[i]) + ' reads)' for i, name in enumerate(barcode_names)] ###Add reads to barcode labels 

""" Option to change label names """
legend_names = master_df['organism_ID'].tolist()
loop_escape = False
my_bool = input('\nWould you like to rename legends (y/n)? ')
while not loop_escape:
    if my_bool == "y":
        my_bool = True
        loop_escape = True
    elif my_bool == "n":
        loop_escape = True
        my_bool = False
        continue
    else:
        my_bool = input('\nPlease enter "y" or "n" ')

if my_bool:
    legend_names = [str(input('\nEnter legend name for %s: ' % name)) for name in legend_names]

a.set_xticklabels(xlabs,rotation=0)
a.legend(labels=legend_names ,loc='center left', bbox_to_anchor=(1, 0.5)) ###Sets legend outside figure and with organism names
a.set_ylabel('Relative Abundance')
plt.show()


name = input('\nSave figure as: ')
fig.savefig(name, bbox_inches = 'tight', dpi=500)
master_df.to_csv(name.split(".")[0] +'_master.csv', index=False, header=True, sep=',')
norm_df.to_csv(name.split(".")[0] +'_norm.csv', index=False, header=True, sep=',')
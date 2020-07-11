from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import os

###Code assumes that tsv files for different barcodes are all in the same subdirectory of the cwd

tsv_dir = os.getcwd() + '/' + input("\nPlease input sub directory with tsv files: ")

#Use collections.Counter on [seqID].tolist() to find out how many times each ID had a hit, after filtering out unclassified and empty hits
master_df = pd.DataFrame() ###Initialize dataframe
for it, tsv in enumerate(sorted(os.listdir(tsv_dir))):
    tsv_path = tsv_dir + '/' + tsv
    print(tsv_path)
    df = pd.read_table(tsv_path)
    df = df[~df.seqID.str.contains("unclassified")] ###Removes all rows with unclassified sequence hit
    df = df[~df.seqID.str.contains("no rank")] ###Removes all rows with no rank sequence hit
    seqid_list = df['seqID'].tolist()
    seqid_count = Counter(seqid_list)
    if it == 0:
        master_df['organism_ID'] = seqid_count.keys()
        master_df[tsv.split('_')[0]] = master_df['organism_ID'].map(seqid_count)
    else:
        master_df[tsv.split('_')[0]] = master_df['organism_ID'].map(seqid_count)

fig, ax1 = plt.subplots()
norm_df = master_df.drop('organism_ID',axis=1).transpose().apply(lambda x: x*100/sum(x), axis =1) ###Transposes and normalizes all columns except for organism names
a = norm_df.plot(ax=ax1,kind='bar',stacked=True, colormap = 'viridis') ###Sets colormap to viridis by default
a.legend(labels = master_df['organism_ID'].tolist(),loc='center left', bbox_to_anchor=(1, 0.5)) ###Sets legend outside figure and with organism names
a.set_ylabel('Relative Abundance')
plt.show()


name = input('\nSave figure as: ')
fig.savefig(name, bbox_inches = 'tight', dpi=500)
master_df.to_csv(name.split(".")[0] +'_master.csv', index=False, header=True, sep=',')
norm_df.to_csv(name.split(".")[0] +'_norm.csv', index=False, header=True, sep=',')

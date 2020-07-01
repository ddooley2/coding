from dna_features_viewer import BlackBoxlessLabeltrans, load_record
from genome_map import Customtrans
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

#class GCIndicatingtrans(BlackBoxlessLabelTranslator):
#    def compute_feature_legend_text(self, feature):
#        if feature.qualifiers["gc%"] < 30:
#            return "GC < 30%"
#        elif feature.qualifiers["gc%"] < 60:
#            return "30-60% GC"
#        else:
#            return "GC > 60%"
#    def compute_feature_color(self, feature):
#        return {
#        "GC < 30%": "peachpuff",
#        "30-60% GC": "azure",
#        "GC > 60%": "skyblue",
#        }[self.compute_feature_legend_text(feature)]
#    def compute_feature_fontdict(self, feature):
#        return dict(size=10, weight="bold", color="#494949")
#    def compute_feature_label(self, feature):
#        if not (30 < feature.qualifiers["gc%"] < 60):
#            normal_label = super().compute_feature_label(feature)
#            return normal_label + "-%d%%" % feature.qualifiers["gc%"]
#
#def gc_content(sequence):
#    return 100.0 * len([c for c in sequence if c in "GC"]) / len(sequence)


####PSEUDO CODE####
# Input csv and make two lists: total repeats and locations
# Sort locations from low to high, keeping the appropriate number of repeats
# Plot in sub window below gene map

df = pd.read_csv(input("Please input the name of the probe csv: "))
reps = df['Total Repeats'].tolist()
locs = df['Location'].tolist()


# DISPLAY THE SEQUENCE MAP
path = os.getcwd()
fig, (ax1, ax2) = plt.subplots(
 2, 1, figsize=(50, 30.5), sharex=True, gridspec_kw={"height_ratios": [3, 1]},
)
record = load_record(path + "/" + input("\nGive the name of a .gb file in the working folder: "))

trans = CustomTranslator()
#graphic_record = trans.translate_record("plasmid.gb")
graphic_record = trans.translate_record(record)
graphic_record.plot(ax=ax1, with_ruler=False, strand_in_label_threshold=1000)
graphic_record.plot_legend(ax=ax1, loc=1, frameon=False)
# DISPLAY THE GC% PROFILE ALONG THE SEQUENCE
window_size = 50

#indices = np.arange(len(record.seq) - window_size) + 25
ax2.vlines(locs,0, reps, alpha=0.9, colors="black")
ax2.set_ylabel("Repeat #", fontsize=12)
ax2.set_ylim(bottom=0, top=max(reps)+50)
fig.tight_layout()
fig.savefig("test.svg")

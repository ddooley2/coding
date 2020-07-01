from dna_features_viewer import load_record
from translator_classes import gene_only
from color_displayer import show_colors
import matplotlib.pyplot as plt, matplotlib
import numpy as np
import pandas as pd
import os
from  time import sleep

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


###Input csv and make two lists: total repeats and locations
df = pd.read_csv(input("\nPlease input the name of the probe csv: "))
reps = df['Total Repeats'].tolist()
locs = df['Location'].tolist()

###Input genbank file (must be in cwd)
path = os.getcwd()
parameters = {"thickness": 15}
trans = gene_only(features_properties=parameters)
record = load_record(path + "/" + input("\nGive the name of a .gb file in the working folder: "))


###Make the graphicrecord object
graphic_record = trans.translate_record(record)

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
graphic_record.plot(ax=ax1, with_ruler=False, strand_in_label_threshold=40)
graphic_record.plot_legend(ax=ax1, loc=1, frameon=False)

#indices = np.arange(len(record.seq) - window_size) + 25
ax2.vlines(locs,0, reps, alpha=0.9, colors="black")
ax2.set_ylabel("Repeat Count", fontsize=10)
ax2.set_ylim(bottom=0, top=max(reps)+50)
fig.suptitle(input("\nPlease name your figure: "), fontsize=16)
fig.tight_layout()
fig.savefig("test.svg")

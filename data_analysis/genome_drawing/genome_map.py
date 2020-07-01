from Bio import Entrez, SeqIO
from dna_features_viewer import annotate_biopython_record, BiopythonTranslator
import matplotlib as plt
import numpy as np

Entrez.email = "dna_features_viewer@example.com"
handle = Entrez.efetch(
 db="nucleotide", id=1473096477, rettype="gb", retmode="text"
)
record = SeqIO.read(handle, "genbank")
annotate_biopython_record(
 record, location=(40, 1800), feature_type="backbone", label="backbone"
)
record.features = [
 f for f in record.features if f.type not in ["gene", "source"]
]
SeqIO.write(record, "plasmid.gb", "genbank")


class CustomTranslator(BiopythonTranslator):
    # Label fields indicates the order in which annotations fields are
    # considered to determine the feature's label
    label_fields = ["label", "note", "name", "gene"]
    def compute_feature_legend_text(self, feature):
        return feature.type

    def compute_feature_color(self, feature):
        return {
        "rep_origin": "yellow",
        "CDS": "#ffd383", # light orange
        "gene": "blue",
        "mRNA": "navy",
        "mat_peptide": "green",
        "stem_loop": "orange",
        "regulatory": "red",
        "misc_recomb": "#fbf3f6", # pink
        "misc_feature": "#d1e9f1", # light blue
        "misc_difference": "grey",
        "sig_peptide": "black",
        "backbone": "darkblue",
        "5'UTR": "pink",
        "3'UTR": "purple"
        }[feature.type]

    def compute_feature_box_color(self, feature):
        return "white"

    def compute_feature_box_linewidth(self, feature):
        return 0

        
translator = CustomTranslator()
graphic_record = translator.translate_record("plasmid.gb")
ax, _ = graphic_record.plot(figure_width=13, strand_in_label_threshold=7, draw_line=True)
graphic_record.plot_legend(ax=ax, loc=1, ncol=3, frameon=False)
ax.figure.savefig("test.svg", bbox_inches="tight") 
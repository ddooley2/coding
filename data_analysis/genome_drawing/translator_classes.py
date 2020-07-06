from dna_features_viewer import BiopythonTranslator
class gene_only(BiopythonTranslator):
    """Custom translator implementing the following theme:

    - Only displays gene features
    - Each gene given a random color within pallete

    """
    def compute_feature_color(self, feature):
        return "blue"
           
    def compute_filtered_features(self, features):
        """Only display genes."""
        return [feature for feature in features if (feature.type == "gene")]

        
import blosum as bl

from adagenes.tools import parse_variant_exchange


class HGVSClient:

    def __init__(self, genome_version=None):
        self.genome_version = genome_version
        self.srv_prefix = ["hgvs"]
        self.extract_keys = [ "hgvs_notation" ]
        self.key_labels = [ 'hgvs_notation' ]

    def process_data(self, variant_data):
        """
        Annotates with HGVS nomenclature identifiers

        :param variant_data:
        :return:
        """

        for var in variant_data.keys():
            variant_data[var]['hgvs'] = {}
            variant_data[var]['hgvs']['hgvs_notation'] = var

        return variant_data

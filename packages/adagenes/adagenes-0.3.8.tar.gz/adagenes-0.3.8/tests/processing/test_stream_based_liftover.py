import unittest, os
import adagenes as ag


class TestStreamBasedLiftover(unittest.TestCase):

    def test_stream_based_liftover(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        infile = __location__ + "/../test_files/somaticMutations_cclab_brca.vcf"
        outfile = __location__ + "/../test_files/somaticMutations_cclab_brca.GRCh38.vcf"

        client = ag.LiftoverClient(genome_version="hg19",target_genome="hg38")

        ag.process_file(infile, outfile, client, genome_version="hg19")

    def test_stream_based_liftover_t2t(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        infile = __location__ + "/../test_files/somaticMutations_cclab_brca.vcf"
        outfile = __location__ + "/../test_files/somaticMutations_cclab_brca.T2T.vcf"

        client = ag.LiftoverClient(genome_version="hg19",target_genome="t2t")

        ag.process_file(infile, outfile, client, genome_version="hg19")

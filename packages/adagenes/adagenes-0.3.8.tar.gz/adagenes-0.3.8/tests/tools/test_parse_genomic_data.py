import unittest
import adagenes as ag


class ParseGenomicDataTestCase(unittest.TestCase):

    def test_parse_aa_exchange(self):
        ref, pos, alt = ag.parse_variant_exchange("V600E")

        self.assertEqual(ref, "V","")
        self.assertEqual(pos, "600", "")
        self.assertEqual(alt, "E", "")

    def test_aaexchange_multi2single_letter_conversion1(self):
        aa_exchange = 'K2E'
        ref, pos, alt = ag.parse_variant_exchange(aa_exchange)
        print(ref,pos,alt)
        self.assertEqual(ref,"K","")
        self.assertEqual(pos, "2", "")
        self.assertEqual(alt, "E", "")

    def test_aaexchange_multi2single_letter_conversion1(self):
        aa_exchange = 'p.K2E'
        ref, pos, alt = ag.parse_variant_exchange(aa_exchange)
        print(ref,pos,alt)
        self.assertEqual(ref,"K","")
        self.assertEqual(pos, "2", "")
        self.assertEqual(alt, "E", "")

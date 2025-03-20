import unittest
import onkopus as op
import adagenes as ag


class TestGeneAnnotation(unittest.TestCase):

    def test_gene_annotation(self):
        data = {"TP53":{ "mutation_type": "gene" }}
        bframe = ag.BiomarkerFrame(data)
        data = op.annotate_genes(bframe.data)
        #print(data.keys())

        self.assertEqual(list(data["TP53"].keys()), ["civic", "cosmic","dgidb","gencode",  "mdesc", "mutation_type"
            , "onkopus_aggregator"
            ,
                                                     "type",
                                                     "UTA_Adapter"],"")


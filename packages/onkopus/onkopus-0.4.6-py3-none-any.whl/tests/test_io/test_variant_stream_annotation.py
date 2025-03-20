import unittest, os
import onkopus as op
import adagenes as ag

class TestStreamAnnotation(unittest.TestCase):

    def test_stream_vcf_liftover(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        infile = __location__ + '/../test_files/somaticMutations.ln50.vcf'
        outfile = __location__ + "/../test_files/somaticMutations.hg38.ln50.lo.vcf"

        client = op.LiftOverClient(genome_version="hg19", target_genome="hg38")
        ag.process_file(infile,outfile,client)

        with open(outfile, 'r') as file:
            contents = file.read()

        self.assertEqual(contents[0:200], '##reference=hg38\n'
 '##AdaGenes v0.2.7\n'
 '##reference=hg38\n'
 '##INFO=<ID=UTA-Adapter-LiftOver,Number=1,Type=String,Description="Reference '
 'Genome LiftOver">\n'
 '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n'
 'chr7\t21744592\t.', "")

    def test_stream_vcf_annotate_clinvar(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        infile = __location__ + '/../test_files/somaticMutations.hg38.ln50.vcf'
        outfile = __location__ + "/../test_files/somaticMutations.hg38.ln50.clinvar.out.vcf"

        client = op.ClinVarClient(genome_version="hg38")
        ag.process_file(infile,outfile,client,genome_version="hg38")

        with open(outfile, 'r') as file:
            contents = file.read()

        self.assertEqual(contents[0:400], '##reference=hg38\n'
 '##AdaGenes v0.2.7\n'
 '##INFO=<ID=UTA-Adapter-LiftOver,Number=1,Type=String,Description="Reference '
 'Genome LiftOver">\n'
 '##AdaGenes v0.2.7\n'
 '##reference=hg38\n'
 '##AdaGenes v0.2.7\n'
 '##INFO=<ID=UTA-Adapter-LiftOver,Number=1,Type=String,Description="Reference '
 'Genome LiftOver">\n'
 '##INFO=<ID=clinvar_CLNSIG,Number=1,Type=String,Description="Estimated '
 'pathogenicity of genomic alteration">\n'
 '##INFO=<clinvar_', "")
